#!/usr/bin/env python3
"""Local preview server that behaves like GitHub Pages: /ev-chargers serves ev-chargers.html.
Usage: python3 tools/serve.py [port]   (default 8771). Ctrl-C to stop."""
import http.server, os, sys, functools
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
class H(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        p = super().translate_path(path.split("?")[0])
        if not os.path.exists(p) and os.path.exists(p + ".html"):
            return p + ".html"
        return p
    def log_message(self, *a): pass
port = int(sys.argv[1]) if len(sys.argv) > 1 else 8771
http.server.ThreadingHTTPServer(("127.0.0.1", port), functools.partial(H, directory=ROOT)).serve_forever()
