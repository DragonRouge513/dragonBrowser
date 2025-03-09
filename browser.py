import ssl
import socket
import os
import sys
import time
import gzip
import base64
from urllib.parse import urljoin, unquote

class URL:
    def __init__(self, url) -> None:
        self.userAgent = (
            "MyCustomBrowser/1.0 (www.antoine513.com; goethuys.antoine513@outlook.com)"
        )
        self.source = False
        self.cache = {}

        if url.startswith("file://"):
            self.scheme = "file"
            self.path = url[7:]
        elif url.startswith("view-source:"):
            self.source = True
            url = url[len("view-source:") :]
            self.scheme, url = url.split("://", 1)
            assert self.scheme in ["http", "https"]
            if "/" not in url:
                url = url + "/"
            self.host, url = url.split("/", 1)
            self.path = "/" + url
            if self.scheme == "http":
                self.port = 80
            elif self.scheme == "https":
                self.port = 443
            if ":" in self.host:
                self.host, port = self.host.split(":", 1)
                self.port = int(port)
        elif url.startswith("data:"):
            self.scheme = "data"
            self.data = url[len("data:"):]
        else:
            self.scheme, url = url.split("://", 1)
            assert self.scheme in ["http", "https"]
            if "/" not in url:
                url = url + "/"
            self.host, url = url.split("/", 1)
            self.path = "/" + url
            if self.scheme == "http":
                self.port = 80
            elif self.scheme == "https":
                self.port = 443
            if ":" in self.host:
                self.host, port = self.host.split(":", 1)
                self.port = int(port)

    def request(self):
        if self.scheme == "file":
            # view contents of the current Directory
            if os.path.isdir(self.path):
                try:
                    # List all files and directories in the specified path
                    contents = os.listdir(self.path)
                    detailed_contents = []
                    detailed_contents.append(
                        f"This is a Directory({self.path}) with this contents:"
                    )
                    for item in contents:
                        item_path = os.path.join(self.path, item)
                        if os.path.isdir(item_path):
                            detailed_contents.append(f"Directory: {item}")
                        elif os.path.isfile(item_path):
                            detailed_contents.append(f"File: {item}")
                    detailed_contents += "\r\n"
                    return "\n".join(detailed_contents)
                except Exception as e:
                    return f"An error occurred: {e}"
            # view contents of the current file
            else:
                try:
                    with open(self.path, "r", encoding="utf-8") as file:
                        return file.read()
                except FileNotFoundError:
                    return f"File not found: {self.path}"
        elif self.scheme == "data":
            # Handle data scheme
            if "," in self.data:
                metadata, data = self.data.split(",", 1)
                if ";base64" in metadata:
                    data = base64.b64decode(data).decode("utf-8")
                else:
                    data = unquote(data)
                return data
            else:
                return unquote(self.data)
        elif self.scheme == "http" or self.scheme == "https":
            # Check cache
            cache_key = f"{self.scheme}://{self.host}{self.path}"
            if cache_key in self.cache:
                cached_response, expires = self.cache[cache_key]
                if expires is None or time.time() < expires:
                    print(f"Cache hit for: {cache_key}")
                    return cached_response

            try:
                s = socket.socket(
                    family=socket.AF_INET,
                    type=socket.SOCK_STREAM,
                    proto=socket.IPPROTO_TCP,
                )
                s.connect((self.host, self.port))
                if self.scheme == "https":
                    ctx = ssl.create_default_context()
                    s = ctx.wrap_socket(s, server_hostname=self.host)
                # header
                request = f"GET {self.path} HTTP/1.1\r\n"
                request += f"HOST: {self.host}\r\n"
                request += f"User-Agent: {self.userAgent}\r\n"
                request += "Accept-Encoding: gzip\r\n"
                request += "\r\n"
                # end header
                s.send(request.encode("utf8"))
                response = s.makefile("rb", newline="\r\n")
                statusline = response.readline().decode("utf-8")
                version, status, explanation = statusline.split(" ", 2)
                print(f"Status: {status} {explanation.strip()}")  # Debugging line
                response_headers = {}
                while True:
                    line = response.readline().decode("utf-8")
                    if line == "\r\n":
                        break
                    if ":" in line:
                        header, value = line.split(":", 1)
                        response_headers[header.casefold()] = value.strip()
                print(f"Headers: {response_headers}")  # Debugging line

                # Handle 301 Moved Permanently
                if status == "301":
                    new_url = response_headers.get("location")
                    if new_url:
                        # Handle relative URLs
                        new_url = urljoin(f"{self.scheme}://{self.host}{self.path}", new_url)
                        print(f"Redirecting to: {new_url}")
                        s.close()
                        return URL(new_url).request()

                content_encoding = response_headers.get("content-encoding", "").lower()
                transfer_encoding = response_headers.get("transfer-encoding", "").lower()

                if transfer_encoding == "chunked":
                    content = b""
                    while True:
                        chunk_size_line = response.readline().strip()
                        if not chunk_size_line:
                            break
                        chunk_size = int(chunk_size_line, 16)
                        if chunk_size == 0:
                            break
                        content += response.read(chunk_size)
                        response.readline()  # Read the CRLF after the chunk
                else:
                    content_length = int(response_headers.get("content-length", 0))
                    content = response.read(content_length)

                s.close()

                if content_encoding == "gzip":
                    content = gzip.decompress(content)

                content = content.decode("utf-8")

                # Cache the response if appropriate
                cache_control = response_headers.get("cache-control", "")
                if status == "200" and "no-store" not in cache_control:
                    max_age = None
                    for directive in cache_control.split(","):
                        if directive.strip().startswith("max-age="):
                            max_age = int(directive.strip().split("=")[1])
                            break
                    expires = time.time() + max_age if max_age is not None else None
                    self.cache[cache_key] = (content, expires)
                    print(f"Cached response for: {cache_key}")

                if self.source:
                    return f"<pre> / {content} /</pre>"
                return content
            except Exception as e:
                return f"An error occurred: {e}"
