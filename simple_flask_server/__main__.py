from werkzeug.exceptions import NotFound
from werkzeug.utils import safe_join
from flask import Flask, request, make_response, send_file, redirect
import sys, os, html, urllib.request, urllib.parse, urllib.error, posixpath, argparse
from io import StringIO
import re

app = Flask(__name__, static_folder=None)


def show_directory(path):
    """Helper to produce a directory listing (absent index.html).

    Return value is either a file object, or None (indicating an
    error).  In either case, the headers are sent, making the
    interface the same as for send_head().

    https://stackoverflow.com/questions/46951468/make-python-simplehttpserver-list-subdirectories-on-top
    """
    try:
        list = os.listdir(path)
    except os.error:
        raise NotFound()

    list.sort(key=lambda a: a.lower())
    f = StringIO()
    displaypath = html.escape(path)
    f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
    f.write("<html>\n<title>Directory listing for %s</title>\n" % displaypath)
    encoding = sys.getfilesystemencoding()
    f.write('<meta http-equiv="Content-Type" content="text/html; charset=%s">' % encoding)
    f.write("<body>\n<h2>Directory listing for %s</h2>\n" % displaypath)
    f.write("<hr>\n<ul>\n")
    for name in list:
        fullname = os.path.join(path, name)
        displayname = linkname = name
        # Append / for directories or @ for symbolic links
        if os.path.isdir(fullname):
            displayname = name + "/"
            linkname = name + "/"
        if os.path.islink(fullname):
            displayname = name + "@"
            # Note: a link to a directory displays with @ and links with /
        f.write('<li><a href="%s">%s</a>\n'
                % (urllib.parse.quote(linkname), html.escape(displayname)))
    f.write("</ul>\n<hr>\n</body>\n</html>\n")
    length = f.tell()

    encoded = f.getvalue().encode(encoding, 'surrogateescape')
    resp = make_response(encoded)
    resp.headers["Content-type"] = "text/html; charset=%s" % encoding
    resp.headers["Content-Length"] = len(encoded)
    return resp

@app.route('/<path:filename>')
@app.route('/')
def show_file(filename=""):
    filepath = safe_join(ROOT_DIR, filename)
    if os.path.isdir(filepath):
        if filename and not filename.endswith("/"):
            return redirect(f"/{filename}/", 301)

        for index in ("index.html", "index.htm"):
            index = safe_join(filepath, index)
            if os.path.isfile(index):
                return send_file(index)

        return show_directory(filepath)

    if not os.path.isfile(filepath):
        raise NotFound()
    return send_file(filepath)

DEFAULT_ADDR = "127.0.0.1"
DEFAULT_PORT = "8001"

parser = argparse.ArgumentParser(description='Simple HTTP server in Flask.')
parser.add_argument('path', default="", nargs="?")
parser.add_argument('--bind', '-b', help="bind address and port", default=f"{DEFAULT_ADDR}:{DEFAULT_PORT}")


def main():
    global ROOT_DIR
    args = parser.parse_args()
    ROOT_DIR = os.path.abspath(args.path or os.getcwd())

    addr, port = re.match(r"([^:]*):?(.*)", args.bind).groups()
    app.run(debug=True, host=addr or DEFAULT_ADDR, port=port or DEFAULT_PORT)

if __name__ == '__main__':
    main()
