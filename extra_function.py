def show(body) -> None:
    in_tag = False
    i = 0
    while i < len(body):
        if body[i] == "<":
            in_tag = True
            # print("<", end="")
        elif body[i] == ">":
            in_tag = False
            # print(">", end="")
        elif body[i : i + 4] == "&lt;":
            if not in_tag:
                print("<", end="")
            i += 3
        elif body[i : i + 4] == "&gt;":
            if not in_tag:
                print(">", end="")
            i += 3
        elif not in_tag:
            print(body[i], end="")
        i += 1

def load(url) -> None:
    body = url.request()
    show(body)
