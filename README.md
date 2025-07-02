# simple_flask_server

[![PyPI version](https://badge.fury.io/py/simple_flask_server.svg)](https://badge.fury.io/py/simple_flask_server)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Flask equivalent of `python -m http.server`.

This package provides a simple HTTP server that serves files from the current directory or a specified directory, just like Python's built-in `http.server` module, but implemented with Flask.

## Features

-   Serves files from a specified directory.
-   Lists directory contents if `index.html` or `index.htm` is not found.
-   Redirects to add a trailing slash for directories.
-   Extends server functionality by loading external Python files.
-   Dynamically adds routes from a command-line string.

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

-   `-h, --help`: Show this help message and exit.
-   `--bind BIND`, `-b BIND`: Specify the address and port to bind to (e.g., `0.0.0.0:8080`).
-   `--ext EXT`, `-e EXT`: Execute a Python file in the context of the Flask app. This allows for adding custom routes. Can be specified multiple times.
-   `--cmd CMD [CMD ...]`, `-c CMD [CMD ...]`: Execute a program passed in as a string.
-   `--open`, `-o`: Open the default web browser to the server's address.

### Examples

To serve files from the current directory on the default address and port:

```bash
simple-flask-server
```

To serve files from a specific directory (e.g., `/var/www`):

```bash
simple-flask-server /var/w
```

To run the server on a different address and port (e.g., all interfaces on port 8080):

```bash
simple-flask-server -b 0.0.0.0:8080
```

To open the browser automatically:
```bash
simple-flask-server -o
```

### Extending the Server

You can extend the server with custom Python code or external commands.

#### Using `--ext`

Specify a Python file to execute. The file is executed in the context of the Flask application, allowing you to define new routes. This option can be used multiple times.

**Example:**

The `samples/json-entry.py` file provides a simple example of a custom endpoint:

```python
@app.route('/sample-api', methods=["POST"])
def post1():
    print(dict(request.json))
    return {"hello":"world"}
```

To run the server and load this extension:

```bash
simple-flask-server -e samples/json-entry.py
```

You can then send requests to the new endpoint:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"key":"value"}' http://127.0.0.1:8001/sample-api
```

The server will respond with:

```json
{
  "hello": "world"
}
```

#### Using `--cmd`

Execute a Python script string. This is useful for defining simple, dynamic routes on the fly.

**Example:**

```bash
simple-flask-server \
-c "@app.route('/api', methods=['POST'])
def api():
  print(dict(request.json))
  return {'hello':'world'}
"
```

More concisely:

```
simple-flask-server -c "app.route('/api', methods=['POST'])(lambda : {'hello':'world'})"
```

You can then call this new endpoint:

```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"key":"value"}' http://127.0.0.1:8001/api
```

The server will respond with:

```json
{
  "hello": "world"
}
```

## License


This project is licensed under the MIT License. See the LICENSE file for details.

## Author

Atsuo Ishimoto
