import browser, extra_function
import sys

def main():
    if len(sys.argv) == 1:
        # Default file to open if no URL is provided
        # default_file = "file:///home/antoine/Documents/obsidian/projects/browser/browser.py"
        default_file = "file:///"
        url = URL(default_file)
        # url = "This is a test &lt;body&gt; with &lt; and &gt; symbols."
    elif len(sys.argv) == 2:
        url = URL(sys.argv[1])
    else:
        print("Usage: python3 browser.py <url>")
        sys.exit(1)

    load(url)


if __name__ == "__main__":
    main()
