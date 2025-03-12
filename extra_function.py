# for terminal
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


# for terminal
def load(url) -> None:
    body = url.request()
    show(body)


# for gui
def layout(text, HSTEP, VSTEP, WIDTH, HEIGHT, is_rtl=False):
    display_list = []
    cursor_x, cursor_y = HSTEP, VSTEP if not is_rtl else WIDTH - HSTEP

    for c in text:
        if c == "\n":
            cursor_y += VSTEP
            cursor_x = HSTEP if not is_rtl else WIDTH - HSTEP
        else:
            display_list.append((cursor_x, cursor_y, c))
            if is_rtl:
                cursor_x -= HSTEP
                if cursor_x <= HSTEP:
                    cursor_y += VSTEP
                    cursor_x = WIDTH - HSTEP
            else:
                cursor_x += HSTEP
                if cursor_x >= WIDTH - HSTEP:
                    cursor_y += VSTEP
                    cursor_x = HSTEP

    return display_list


# for gui
def lex(body) -> str:
    text = ""
    in_tag = False
    i = 0
    if body == "about:blank":
        return ""
    while i < len(body):
        if body[i] == "<":
            in_tag = True
        elif body[i] == ">":
            in_tag = False
        elif body[i : i + 4] == "&lt;":
            if not in_tag:
                text += "<"
            i += 3
        elif body[i : i + 4] == "&gt;":
            if not in_tag:
                text += ">"
            i += 3
        elif not in_tag:
            text += body[i]
        i += 1
    return text
