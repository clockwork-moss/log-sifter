# log-sifter

Sift service logs one line at a time. JSON arrays and CSV are emitted incrementally, so export memory usage does not grow with the file.

## Install

Requires Python 3.11 or newer. From this directory:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e .
```

## Use

```sh
log-sifter samples/service.log --stats
log-sifter samples/service.log --severity ERROR --keyword connection --format json
log-sifter samples/service.log --format csv
```

Statistics count all valid input severities before filters, plus unparsed lines; they go to stderr. Repeat `--severity` to include multiple levels. UTF-8 decoding replaces malformed bytes. See [parser notes](docs/parser-notes.md) for the accepted format. Sample logs model a queue capacity warning and retry.

## Development

```sh
python -m unittest discover -s tests -v
```

Licensed under MIT.
