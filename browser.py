import tkinter
from url import URL
from extra_function import lex, layout
import os

HSTEP, VSTEP = 10, 20
SCROLL_STEP = 100
SCROLLBAR_WIDTH = 10


class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.window)
        self.canvas.pack(fill=tkinter.BOTH, expand=True)
        self.scroll_x = 0
        self.scroll_y = 0
        self.is_rtl = False
        self.body = ""  # Initialize body attribute
        self.display_list = []  # Initialize display list
        self.window.bind("<Button-4>", self.scrollup)  # Linux
        self.window.bind("<Button-5>", self.scrolldown)  # Linux
        self.window.bind("<MouseWheel>", self.on_mouse_wheel)  # Windows and macOS
        self.window.bind("<Configure>", self.on_resize)  # Handle window resizing

    def draw(self):
        self.canvas.delete("all")
        max_y = max(y for _, y, _ in self.display_list) if self.display_list else 0
        max_x = max(x for x, _, _ in self.display_list) if self.display_list else 0
        max_scroll_y = max(0, max_y - self.window.winfo_height() + VSTEP)
        max_scroll_x = max(0, max_x - self.window.winfo_width() + HSTEP)

        if self.scroll_y > max_scroll_y:
            self.scroll_y = max_scroll_y
        elif self.scroll_y < 0:
            self.scroll_y = 0

        if self.scroll_x > max_scroll_x:
            self.scroll_x = max_scroll_x
        elif self.scroll_x < 0:
            self.scroll_x = 0

        for x, y, c in self.display_list:
            if y > self.scroll_y + self.window.winfo_height() or x > self.scroll_x + self.window.winfo_width():
                continue
            if y + VSTEP < self.scroll_y or x + HSTEP < self.scroll_x:
                continue
            else:
                self.canvas.create_text(x - self.scroll_x, y - self.scroll_y, text=c)

        # Draw vertical scrollbar
        if max_y > self.window.winfo_height():
            scrollbar_height = self.window.winfo_height() * self.window.winfo_height() / (max_y + VSTEP)
            scrollbar_y = self.scroll_y * self.window.winfo_height() / (max_y + VSTEP)
            self.canvas.create_rectangle(
                self.window.winfo_width() - SCROLLBAR_WIDTH,
                scrollbar_y,
                self.window.winfo_width(),
                scrollbar_y + scrollbar_height,
                fill="blue"
            )

        # Draw horizontal scrollbar
        if max_x > self.window.winfo_width():
            scrollbar_width = self.window.winfo_width() * self.window.winfo_width() / (max_x + HSTEP)
            scrollbar_x = self.scroll_x * self.window.winfo_width() / (max_x + HSTEP)
            self.canvas.create_rectangle(
                scrollbar_x,
                self.window.winfo_height() - SCROLLBAR_WIDTH,
                scrollbar_x + scrollbar_width,
                self.window.winfo_height(),
                fill="blue"
            )

    def load(self, url) -> None:
        self.body = url.request()  # Store body content
        text = lex(self.body)
        self.display_list = layout(text, HSTEP, VSTEP, self.window.winfo_width(), self.window.winfo_height(), is_rtl=self.is_rtl)
        self.draw()

    def scrolldown(self, e):
        self.scroll_y += SCROLL_STEP
        self.draw()

    def scrollup(self, e):
        self.scroll_y -= SCROLL_STEP
        self.draw()

    def scrollright(self, e):
        self.scroll_x += SCROLL_STEP
        self.draw()

    def scrollleft(self, e):
        self.scroll_x -= SCROLL_STEP
        self.draw()

    def on_mouse_wheel(self, e):
        if e.state & 0x0001:  # Shift key is pressed
            if e.delta > 0:
                self.scrollleft(e)
            else:
                self.scrollright(e)
        else:
            if e.delta > 0:
                self.scrollup(e)
            else:
                self.scrolldown(e)

    def on_resize(self, event):
        text = lex(self.body)
        self.display_list = layout(text, HSTEP, VSTEP, event.width, event.height, is_rtl=self.is_rtl)
        self.draw()


if __name__ == "__main__":
    import sys

    browser = Browser()
    browser.load(URL(sys.argv[1]))
    tkinter.mainloop()
# https://browser.engineering/examples/xiyouji.html
