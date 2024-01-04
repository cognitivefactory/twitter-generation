import os

from dataclasses import dataclass
from argparse import ArgumentParser, Namespace

from ..doctor import Doctor
from ..core import App, find_possible_sentiments_file_paths, find_possible_topics_file_paths

from ..version import __version__
from ..helper.auto_numbered import AutoNumberedEnum

__all__ = ["gp_parser", "CliApp"]


def gp_parser() -> ArgumentParser:
    """
    Create a general parser.

    xs-gen [run|do] [warmup|doctor] [-v | --version] [-h | --help]\\
    `-v | --version` : print version and exit\\
    `-h | --help` : print help and exit

    run : run the main program
        - `-i | --input-topics` <topic file path>
        - `-o | --output` <output file path>
        - `-s | --sentiments` <sentiments file path>
        - `-l | --local` <local (fr, en, ...)> (default: en)
        - `-g | --gpu` <gpu id> (default: 0)
        - `-t | --temperature` <temperature> (default: 0.7)
        - `-d | --debug` : activate debug mode (default: release mode)

    do [warmup|doctor] : secondary action to perform

    warmup : do a warmup (load model and wait for next command)
        - `-d | --delay` <max delay to wait after in seconds> (default: 0 to wait indefinitely)
        - `-n | --nice` <nice level> (default: 0)

    doctor : do a doctor and exit (check if all dependencies are installed)

    ## Returns
    `ArgumentParser` - New general parser.
    """
    parser = ArgumentParser(
        description="Xs (former tweets) Generator",
        epilog="https://github.com/cognitivefactory/twitter-generation",
    )
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")

    subparsers = parser.add_subparsers(dest="command", help="command to run")

    run_parser = subparsers.add_parser("run", help="run the main program")
    run_parser.add_argument(
        "-i",
        "--input-topics",
        help="topic file path (file used to retrieve the list of topics) (default: auto)",
        default=None,
    )
    run_parser.add_argument(
        "-o",
        "--output",
        help="output file path (file used to store generated tweets) (default: tweets.txt)",
        default=None,
    )
    run_parser.add_argument(
        "-s",
        "--sentiments",
        help="sentiments file path (file used to retrieve the list of sentiments) (default: auto)",
        default=None,
    )
    run_parser.add_argument(
        "-l",
        "--local",
        help="local (fr, en, ...) (default: en)",
        default=None,
    )
    run_parser.add_argument(
        "-g",
        "--gpu",
        help="gpu id (default: 0)",
        default=0,
        type=int,
    )
    run_parser.add_argument(
        "-t",
        "--temperature",
        help="temperature (default: 0.7)",
        default=0.7,
        type=float,
    )
    run_parser.add_argument(
        "-d",
        "--debug",
        help="activate debug mode (default: release mode)",
        action="store_true",
    )

    do_parser = subparsers.add_parser("do", help="secondary action to perform")
    do_subparsers = do_parser.add_subparsers(dest="subcommand", help="subcommand to run")

    warmup_parser = do_subparsers.add_parser(
        "warmup",
        help="do a warmup (load model and wait for next command)",
    )
    warmup_parser.add_argument(
        "-d",
        "--delay",
        help="max delay to wait after in seconds (default: 0 to wait indefinitely)",
        default=None,
        type=int,
    )
    warmup_parser.add_argument(
        "-n",
        "--nice",
        help="nice level (default: 0), lower values mean higher priority",
        default=None,
        type=int,
    )

    doctor_parser = do_subparsers.add_parser(  # noqa: F841
        "doctor",
        help="do a doctor and exit (check for hadware and if all dependencies are installed)",
    )

    return parser


class Command(AutoNumberedEnum):
    RUN = ()
    WARMUP = ()
    DOCTOR = ()


@dataclass
class Args:
    command: Command = Command.RUN

    # run subcommand
    topics_file_path: str = None
    sentiments_file_path: str = None
    output_file_path: str = "tweets.txt"  # this is the default value in case gpu is not specified
    local_lang: str = "en"
    gpu_id: int = 0
    temperature: float = 0.7
    debug: bool = False

    # do warmup subcommand
    max_delay: int = 0
    nice_level: int = 0


class CliApp:
    def __init__(self) -> None:
        self.__args = Args()

    def check_args(self, nsp: Namespace) -> "App":
        """
        Check cli arguments and stores them in `self.__args`.\\
        Returns `self` for fluent style chaining.

        ## Parameters
        - `nsp` - Namespace\\
        command line parsed arguments (see `gp_parser().parse_args()`)

        ## Returns
        `App` - `self`
        """
        if nsp.command == "run":
            if nsp.input_topics:
                if not os.path.isfile(nsp.input_topics):
                    raise FileNotFoundError(f"File {nsp.input_topics} does not exist")
                self.__args.topics_file_path = nsp.input_topics

            if nsp.output:
                # will check for file existence and cache later
                self.__args.output_file_path = nsp.output

            if nsp.sentiments:
                if not os.path.isfile(nsp.sentiments):
                    raise FileNotFoundError(f"File {nsp.sentiments} does not exist")
                self.__args.sentiments_file_path = nsp.sentiments

            if nsp.local:
                # check if local is valid
                if nsp.local not in {"fr", "en"}:
                    raise ValueError(f"Unknown local {nsp.local}")
                self.__args.local_lang = nsp.local

            if nsp.gpu is not None:
                # check if gpu is valid (positive)
                if nsp.gpu < 0:
                    raise ValueError("GPU id must be positive")
                self.__args.gpu_id = nsp.gpu
                if not nsp.output:
                    # if output is not specified, we set it to "tweets_<gpu_id>.txt"
                    self.__args.output_file_path = f"tweets_{nsp.gpu}.txt"

            if nsp.temperature is not None:
                # check if temperature is valid (between 0 and 1)
                if not (0 <= nsp.temperature <= 1):
                    raise ValueError("Temperature must be between 0 and 1")
                self.__args.temperature = nsp.temperature

            if nsp.debug:
                self.__args.debug = True

        elif nsp.command == "do":
            if nsp.subcommand == "warmup":
                self.__args.command = Command.WARMUP

                if nsp.delay is not None:
                    # check if delay is valid (positive)
                    if nsp.delay <= 0:
                        raise ValueError(
                            "Delay must be positive - please leave it empty to wait indefinitely"
                        )
                    self.__args.max_delay = nsp.delay

                if nsp.nice:
                    # check if nice is valid (between -20 and 19)
                    if not (-20 <= nsp.nice <= 19):
                        raise ValueError("Nice level must be between -20 and 19")
                    self.__args.nice_level = nsp.nice

            elif nsp.subcommand == "doctor":
                self.__args.command = Command.DOCTOR

            else:
                raise ValueError(f'Unknown "do" subcommand {nsp.subcommand}')

        else:
            raise ValueError(f"Unknown command {nsp.command}")
        return self

    def run(self):
        import logging
        from ..helper.logger import init_logger

        colored_output = init_logger(logging.DEBUG if self.__args.debug else logging.INFO)
        logger = logging.getLogger("cli")

        match self.__args.command:
            case Command.RUN:
                logger.debug('Got "run" command (on %d at %f)', self.__args.gpu_id, self.__args.temperature)
                if self.__args.topics_file_path is None:
                    try:
                        self.__args.topics_file_path = find_possible_topics_file_paths()[0]
                    except IndexError:
                        logger.critical("No topics file found - please specify it manually")
                if self.__args.sentiments_file_path is None:
                    try:
                        self.__args.sentiments_file_path = find_possible_sentiments_file_paths()[0]
                    except IndexError:
                        logger.critical("No sentiments file found - please specify it manually")
                App(self.__args.gpu_id, self.__args.temperature).run(
                    self.__args.topics_file_path,
                    self.__args.sentiments_file_path,
                    self.__args.output_file_path,
                    self.__args.local_lang,
                )

            case Command.WARMUP:
                logger.debug('Got "warmup" command')

            case Command.DOCTOR:
                logger.debug('Got "doctor" command')
                if (n := Doctor(colored_output).doctor()) == 0:
                    logger.info("Doctor found no problems %s", "✅" if colored_output else "")
                else:
                    logger.warning(
                        "Doctor found %d problem%s %s",
                        n,
                        "s" if n > 1 else "",
                        "🚧" if colored_output else "",
                    )
