# simple_flask_server

[![PyPI version](https://badge.fury.io/py/simple_flask_server.svg)](https://badge.fury.io/py/simple_flask_server)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Flask equivalent of `python -m http.server`.

This package provides a simple HTTP server that serves files from the current directory or a specified directory, just like Python's built-in `http.server` module, but implemented with Flask.

## Installation

It is recommended to use `uv` for installation.

```bash
uv tool install simple_flask_server
```

Alternatively, you can use `pip`:

```bash
pip install simple_flask_server
```

## Usage

Run the server from the command line:

```bash
simple-flask-server [path] [options]
```

You can also run it as a Python module:

```bash
python -m simple_flask_server [path] [options]
```

### Arguments

-   `path` (optional): The directory to serve files from. If not specified, it defaults to the current working directory.

### Options

-   `--bind` / `-b`: Specify the address and port to bind to.
    -   Format: `[address][:port]`
    -   Default: `127.0.0.1:8001`

### Examples

To serve files from the current directory on the default address and port:

```bash
simple-flask-server
```

To serve files from a specific directory (e.g., `/var/www`):

```bash
simple-flask-server /var/www
```

To run the server on a different address and port (e.g., all interfaces on port 8080):

```bash
simple-flask-server -b 0.0.0.0:8080
```

## Features

-   Serves files from a specified directory.
-   Lists directory contents if `index.html` or `index.htm` is not found.
-   Redirects to add a trailing slash for directories.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

Atsuo Ishimoto
