from url import URL

# from extra_function import load, show
from browser import Browser
import sys
import tkinter


def main():
    if len(sys.argv) == 1:
        # Default file to open if no URL is provided
        # default_file = "file:///home/antoine/Documents/obsidian/projects/browser/browser.py"
        default_file = "file:///"
        url = URL(default_file)
        browser = Browser()
        browser.load(url)
        # url = "This is a test &lt;body&gt; with &lt; and &gt; symbols."
    elif len(sys.argv) == 2:
        url = URL(sys.argv[1])
        browser = Browser()
        browser.load(url)
    elif len(sys.argv) == 3:
        url = URL(sys.argv[1])
        browser = Browser()
        browser.load(url) 
    else:
        print("Usage: python3 browser.py <url>")
        sys.exit(1)
    tkinter.mainloop()


if __name__ == "__main__":
    main()
