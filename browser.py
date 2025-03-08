import ssl
import socket
import os
import sys

class URL:
    def __init__(self, url) -> None:
        self.userAgent = "MyCustomBrowser/1.0 (www.antoine513.com; goethuys.antoine513@outlook.com)"

        if url.startswith("file://"):
            self.scheme = "file"
            self.path = url[7:]
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
                    detailed_contents.append(f"This is a Directory({self.path}) with this contents:")
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
        else:
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
            request += "\r\n"
            # end header

            s.send(request.encode("utf8"))
            response = s.makefile("r", encoding="utf8", newline="\r\n")
            statusline = response.readline()
            version, status, explanation = statusline.split(" ", 2)
            response_headers = {}
            while True:
                line = response.readline()
                if line == "\r\n": break
                if ":" in line:
                    header, value = line.split(":", 1)
                    response_headers[header.casefold()] = value.strip()
            assert "transfer-encoding" not in response_headers
            assert "content-encoding" not in response_headers
            content = response.read()
            s.close()
            return content

def show(body) -> None:
    in_tag = False
    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            print(c, end="")

def load(url) -> None:
    body = url.request()
    show(body)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # Default file to open if no URL is provided
        #default_file = "file:///home/antoine/Documents/obsidian/projects/browser/browser.py"
        default_file = "file:///"
        url = URL(default_file)
    elif len(sys.argv) == 2:
        url = URL(sys.argv[1])
    else:
        print("Usage: python3 browser.py <url>")
        sys.exit(1)

    load(url)
