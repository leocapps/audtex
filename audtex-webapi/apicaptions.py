from http.server import BaseHTTPRequestHandler
import json
import subprocess
import os

class handler(BaseHTTPRequestHandler):
def do_POST(self):
try:
length = int(self.headers['Content-Length'])
body = self.rfile.read(length)

```
        # Save uploaded video
        with open("input.mp4", "wb") as f:
            f.write(body)

        # Run your AI caption script
        subprocess.run(["python", "captions.py", "input.mp4", "output.mp4"])

        # Return result video
        self.send_response(200)
        self.send_header('Content-type', 'video/mp4')
        self.end_headers()

        with open("output.mp4", "rb") as f:
            self.wfile.write(f.read())

    except Exception as e:
        self.send_response(500)
        self.end_headers()
        self.wfile.write(str(e).encode())
```
