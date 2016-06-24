"""
A http server to server MarkDown files to slide
"""

from http import server
from http import HTTPStatus
import logging
import sys
import os
import inspect
import urllib
import html
import posixpath
import io

md_slide_dir = ''
remarkjs = ''
controljs = ''
controlcss = ''
slidecss = ''
README = ''


class MDSlideHandler(server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """Serve a GET request."""

        if self.path.endswith('/slide'):
            file_name = self.path.replace('/slide', '.md')
            f = self.slide_content(file_name[1:])
        elif self.path == '/remark.js':
            f = self.static_content(remarkjs, 'application/javascript')
        elif self.path == '/control.js':
            f = self.static_content(controljs, 'application/javascript')
        elif self.path == '/control.css':
            f = self.static_content(controlcss, 'text/css')
        elif self.path == '/slide.css':
            f = self.static_content(slidecss, 'text/css')
        elif self.path == '/README.md':
            f = self.static_content(README, 'text/plain')
        elif self.path.startswith('/help'):
            f = self.slide_content('README.md#1')
        else:
            f = self.send_head()
        if f:
            try:
                self.copyfile(f, self.wfile)
            finally:
                f.close()

    def static_content(self, content, mime_type):
        r = [content]
        enc = sys.getfilesystemencoding()
        encoded = '\n'.join(r).encode(enc, 'surrogateescape')
        f = io.BytesIO()
        f.write(encoded)
        f.seek(0)
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", mime_type + "; charset=%s" % enc)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        return f

    def slide_content(self, file_name):
        r = []
        enc = sys.getfilesystemencoding()
        r.append('<!DOCTYPE html>')
        r.append('<html>\n<head>')
        r.append('<title>%s</title>' % file_name)
        r.append('<meta http-equiv="Content-Type" '
                 'content="text/html; charset=%s">' % enc)        
        r.append('<link rel="stylesheet" type="text/css" href="/slide.css" />')
        r.append('</head>')
        r.append('<body>')
        r.append('<script src="/remark.js"></script>')
        r.append("<script>var slideshow = remark.create({sourceUrl: '/" + file_name + "'});</script>")
        r.append('</body>\n</html>\n')
        encoded = '\n'.join(r).encode(enc, 'surrogateescape')
        f = io.BytesIO()
        f.write(encoded)
        f.seek(0)
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "text/html; charset=%s" % enc)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        return f

    def list_directory(self, path):
        """Helper to produce a directory listing md files.
        """
        try:
            list = os.listdir(path)
        except OSError:
            self.send_error(
                HTTPStatus.NOT_FOUND,
                "No permission to list directory")
            return None
        list.sort(key=lambda a: a.lower())
        enc = sys.getfilesystemencoding()
        r = []
        r.append('<!DOCTYPE html>')
        r.append('<html>\n<head>')
        r.append('<meta http-equiv="Content-Type" '
                 'content="text/html; charset=%s">' % enc)
        r.append('<link rel="stylesheet" type="text/css" href="/control.css" />')

        r.append('<title>MD2Slide</title>\n</head>')
        r.append('<body  onFocus="controlState(true)" onBlur="controlState(false)">\n<div id="header"><h1 id="title">Slide list</h1></div>')
        r.append('<div id="nav">')
        for name in list:
            file_name, extension = os.path.splitext(name)
            if extension.lower() != '.md':
                continue
            linkname = name.replace('.md', '/slide')
            r.append('<button class="slide_btn" data-slide="%s">%s</button>' %
                     (urllib.parse.quote(linkname, errors='surrogatepass'), html.escape(file_name)))
        r.append('</div>')
        r.append('<iframe id="preview" src="/help#1"></iframe>')
        r.append('<div id="info">Control the preview window only</div>')
        r.append('<script src="/control.js"></script>')
        r.append('</body>\n</html>\n')
        encoded = '\n'.join(r).encode(enc, 'surrogateescape')
        f = io.BytesIO()
        f.write(encoded)
        f.seek(0)
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "text/html; charset=%s" % enc)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        return f

    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax with md_slide_dir  md_slide_dir prefix
        """
        # abandon query parameters
        path = path.split('?', 1)[0]
        path = path.split('#', 1)[0]
        # Don't forget explicit trailing slash when normalizing. Issue17324
        trailing_slash = path.rstrip().endswith('/')
        try:
            path = urllib.parse.unquote(path, errors='surrogatepass')
        except UnicodeDecodeError:
            path = urllib.parse.unquote(path)
        path = posixpath.normpath(path)
        words = path.split('/')
        if words == ['', 'README.md']:
            return os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), 'README.md')
        words = filter(None, words)
        path = md_slide_dir
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir): continue
            path = os.path.join(path, word)
        if trailing_slash:
            path += '/'
        return path


def run(folder=None, bind='', port=8000, HandlerClass=MDSlideHandler, ServerClass=server.HTTPServer):

    set_up(folder)

    server_address = (bind, port)

    HandlerClass.protocol_version = 'HTTP/1/1'

    httpd = ServerClass(server_address, HandlerClass)

    sa = httpd.socket.getsockname()
    logging.debug("Serving HTTP on {}:{} ...".format(sa[0], sa[1]))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logging.debug("\nKeyboard interrupt received, exiting.")
        httpd.server_close()
        sys.exit(0)


def set_up(folder=None):
    set_dir(folder)
    update_statics()

def update_statics():
    global remarkjs
    global controljs
    global controlcss
    global slidecss

    if not os.path.isfile(os.path.join(md_slide_dir, 'remark.js')):
        logging.debug('loading remarkjs fall back')
        with open(os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), 'remark-20160618.min.js'), 'r') as f:
            remarkjs = f.read()

    if not os.path.isfile(os.path.join(md_slide_dir, 'control.js')):
        logging.debug('loading control.js fall back')
        with open(os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), 'control.js'), 'r') as f:
            controljs= f.read()

    if not os.path.isfile(os.path.join(md_slide_dir, 'control.css')):
        logging.debug('loading control.css fall back')
        with open(os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), 'control.css'), 'r') as f:
            controlcss = f.read()

    if not os.path.isfile(os.path.join(md_slide_dir, 'slide.css')):
        logging.debug('loading slide.css fall back')
        with open(os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), 'slide.css'), 'r') as f:
            slidecss = f.read()

    global README
    with open(os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), 'README.md'), 'r') as f:
        README = f.read()


def set_dir(dir_path=None):
    global md_slide_dir
    if dir_path:
        md_slide_dir = dir_path
    else:
        md_slide_dir = os.getcwd()

if __name__ == '__main__':
    global md_slide_dir
    if not md_slide_dir:
        md_slide_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    logging.basicConfig(level=logging.DEBUG, format='LINE %(lineno)-4d  %(levelname)-8s %(message)s', datefmt='%m-%d %H:%M')
    run()
