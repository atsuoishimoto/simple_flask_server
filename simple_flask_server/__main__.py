from werkzeug.exceptions import NotFound
from flask import Flask, request, make_response, send_file, safe_join, redirect
import sys, os, cgi, urllib.request, urllib.parse, urllib.error, posixpath, argparse
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


app = Flask(__name__, static_folder=None)


def show_directory(path):
    """Helper to produce a directory listing (absent index.html).

    Return value is either a file object, or None (indicating an
    error).  In either case, the headers are sent, making the
    interface the same as for send_head().

    """
    try:
        list = os.listdir(path)
    except os.error:
        self.send_error(404, "No permission to list directory")
        return None
    list.sort(key=lambda a: a.lower())
    f = StringIO()
    displaypath = cgi.escape(path)
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
                % (urllib.parse.quote(linkname), cgi.escape(displayname)))
    f.write("</ul>\n<hr>\n</body>\n</html>\n")
    length = f.tell()
    f.seek(0)

    resp = make_response(f.read())
    return resp

@app.route('/<path:filename>')
@app.route('/')
def show_file(filename=''):
    filename = safe_join(ROOT_DIR, filename)
    if os.path.isdir(filename):
        return show_directory(filename)

    if not os.path.isfile(filename):
        raise NotFound()
    return send_file(filename)

parser = argparse.ArgumentParser(description='Simple HTTP server in Flask.')
parser.add_argument('--path')

def main():
    global ROOT_DIR
    ROOT_DIR = os.path.abspath(parser.parse_args().path or os.getcwd())
    app.run(debug=True)

if __name__ == '__main__':
    main()
