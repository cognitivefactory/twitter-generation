# ⌨️ the CLI

```yml
usage: xs-gen.py [-h] [-v] {run,do} ...

Xs (former tweets) Generator

positional arguments:
  {run,do}       command to run
    run          run the main program
    do           secondary action to perform

options:
  -h, --help     show this help message and exit
  -v, --version  show program's version number and exit

https://github.com/cognitivefactory/twitter-generation
```

## Run

::: details run command man

```yml
usage: xs-gen.py run [-h] [-i INPUT_TOPICS] [-o OUTPUT] [-s SENTIMENTS] [-l LOCAL] [-g GPU] [-t TEMPERATURE] [-d]

options:
  -h, --help            show this help message and exit
  -i INPUT_TOPICS, --input-topics INPUT_TOPICS
                        topic file path (file used to retrieve the list of topics) (default: auto)
  -o OUTPUT, --output OUTPUT
                        output file path (file used to store generated tweets) (default: tweets.txt)
  -s SENTIMENTS, --sentiments SENTIMENTS
                        sentiments file path (file used to retrieve the list of sentiments) (default: auto)
  -l LOCAL, --local LOCAL
                        local (fr, en, ...) (default: en)
  -g GPU, --gpu GPU     gpu id (default: 0)
  -t TEMPERATURE, --temperature TEMPERATURE
                        temperature (default: 0.7)
  -d, --debug           activate debug mode (default: release mode)
```

:::

| Option | Description                                                                                  | Default    |
| ------ | -------------------------------------------------------------------------------------------- | ---------- |
| `-i`   | topic file path (file used to retrieve the list of topics) [one topic per line]              | ~auto      |
| `-o`   | output file path (`r"topic\tsentiment\ttweet\n"`)                                            | tweets.txt |
| `-s`   | sentiments file path (file used to retrieve the list of sentiments) [one sentiment per line] | ~auto      |
| `-l`   | local language to use for generated tweets (fr, en, ...)                                     | en         |
| `-g`   | gpu id to use (will issue a warning at runtime if gpu is not available)                      | 0          |
| `-t`   | temperature to use for generation (higher = more random) [in range 0..=1]                    | 0.7        |
| `-d`   | activate debug mode (will be very noisy)                                                     | False      |

At the time of writing, only single-gpu mode is supported. Multi-gpu support is planned for a future release. For now, if you have multiple gpus, you can use the app multiple times with different gpu ids.

::: warning

```yml
min required vram per device: 28GB
min required ram: 40GB
```

:::

## Do

::: details do commands man

```yml
usage: xs-gen.py do [-h] {warmup,doctor} ...

positional arguments:
  {warmup,doctor}  subcommand to run
    warmup         do a warmup (load model and wait for next command)
    doctor         do a doctor and exit (check for hadware and if all dependencies are installed)

options:
  -h, --help       show this help message and exit
```

:::

- **Doctor** subcommand will check for hadware and if all dependencies are installed. It will then exit.
- **Warmup** subcommand will load the model and wait for the next command in the background.

At the time of writing, warmup is not available.
