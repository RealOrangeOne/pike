# pike 🐟

![Tests Status](https://github.com/RealOrangeOne/pike/workflows/CI/badge.svg)
![PyPI](https://img.shields.io/pypi/v/pike-tasks.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pike-tasks.svg)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/pike-tasks.svg)
![PyPI - Status](https://img.shields.io/pypi/status/pike-tasks.svg)
![PyPI - License](https://img.shields.io/pypi/l/pike-tasks.svg)

It's `make`, but Python.

## Example

See [`examples/pikefile.py`](examples/pikefile.py) for an example file.

```
$ pike -f ./examples/pikefile.py --help
usage: pike [-h] [--file FILE] [--list] [--validate] {do-thing,wrapped-task} ...

An example pikefile

optional arguments:
  -h, --help            show this help message and exit
  --file FILE, -f FILE  pikefile.py to use. If not provided, look in the current working directory and all its parents
  --list                List tasks
  --validate            Validate tasks

Tasks:
  Things to run

  {do-thing,wrapped-task}
```

Each task also has a `--help`:

```
$ pike -f ./examples/pikefile.py do-thing --help
usage: pike do-thing [-h] thing

Do a thing, and do it perfectly

positional arguments:
  thing       The thing to do

optional arguments:
  -h, --help  show this help message and exit
```

If a default value is provided, it's also shown:

```
$ pike -f ./examples/pikefile.py wrapped-task --help
usage: pike wrapped-task [-h] [--thing THING]

optional arguments:
  -h, --help     show this help message and exit
  --thing THING  (default: Rap)
```

If a type is provided, it should be cast automatically.
