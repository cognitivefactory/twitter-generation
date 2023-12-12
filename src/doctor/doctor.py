import os

from typing import NoReturn
import logging

from alive_progress import alive_bar

from ..core import find_possible_topics_file_paths


__all__ = ["Doctor"]


class Doctor:
    def __init__(self, colored_output: bool = False) -> None:
        self.logger = logging.getLogger("doctor")
        self.__colored_output = colored_output

    def doctor(self) -> int:
        """Run the doctor and returns the number of warnings"""
        self.logger.info("Running doctor")

        return self.__check_modules() + self.__check_files()

    def __check_files(self) -> int:
        # check if all files are present
        # animate progress bar for each file

        __total_items = 3
        warnings = 0
        with alive_bar(__total_items, title="Checking files  ") as bar:
            # checking topics file
            bar.text("topics file")
            if len(find_possible_topics_file_paths()) == 0:
                self.logger.warning("No topics file candidate found - you would have to specify it manually")
                warnings += 1
            bar()

            # checking for cache directory
            bar.text("cache directory")
            if not os.path.isdir("cache"):
                self.logger.warning("Cache directory not found")
                try:
                    os.mkdir("cache")
                    with open(os.path.join("cache", ".gitignore"), "w") as f:
                        f.write("*\n!.git*\n")
                except OSError as e:
                    self.logger.error("Failed to create cache directory: %s", str(e))
                warnings += 1
            bar()

            # checking for resume file
            bar.text("resume file")
            if os.path.isfile(os.path.join("cache", "resume.json")):
                self.logger.warning(
                    "The resume file is present\nPlease delete it to start from scratch or use the --resume flag"
                )
                warnings += 1
            bar()

        return warnings

    def __critical(self, module_name: str) -> NoReturn:
        self.logger.critical(
            "Module %s is not installed %s\nPlease run `pip install --upgrade -r requirements.txt`",
            module_name,
            "❌" if self.__colored_output else "",
        )

    def __check_modules(self) -> int:
        # check if all modules are installed and working
        # animate progress bar for each module

        __total_items = 6
        warnings = 0
        with alive_bar(__total_items, title="Checking modules") as bar:
            # checking pandas
            bar.text("Checking pandas")
            try:
                import pandas  # noqa

                bar()
            except ImportError:
                self.__critical("pandas")

            # checking numpy
            bar.text("Checking numpy")
            try:
                import numpy  # noqa

                bar()
            except ImportError:
                self.__critical("numpy")

            # checking sentencepiece
            bar.text("Checking sentencepiece")
            try:
                import sentencepiece  # noqa

                bar()
            except ImportError:
                self.__critical("sentencepiece")

            # checking transformers
            bar.text("Checking transformers")
            try:
                import transformers  # noqa

                bar()
            except ImportError:
                self.__critical("transformers")

            # checking torch
            bar.text("Checking torch")
            try:
                import torch  # noqa

                bar()
            except ImportError:
                self.__critical("torch")

            # checking cuda and GPU
            bar.text("Checking cuda and GPU")
            try:
                import torch.cuda as cuda  # noqa

                if not cuda.is_available():
                    self.logger.warning("torch is installed w/ cuda support but GPU is not available")
                    warnings += 1

            except ImportError:
                self.logger.warning("torch is installed without cuda GPU support")
                warnings += 1
            bar()

            return warnings
