from dateutil.relativedelta import relativedelta
from datetime import datetime
import subprocess, os
import tkinter as tk

WIDTH = 52
HEIGHT = 7

SIZE = 25

class Squares(tk.Canvas):
    def __init__(self, master, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._squares = squares = {}

        self.actual = set()

        for x in range(WIDTH):
            for y in range(HEIGHT):
                squares[(x, y)] = self.create_rectangle(x * SIZE, y * SIZE, (x + 1) * SIZE, (y + 1) * SIZE, fill="white")

        self.bind("<Button-1>", self.click)

    def click(self, event):
        post = event.x // SIZE, event.y // SIZE
        square = self._squares[post]

        if post in self.actual:
            self.itemconfig(square, fill="white")
            self.actual.remove(post)
        else:
            self.itemconfig(square, fill="green")
            self.actual.add(post)

    def get_squares(self):
        return self.actual


class SquareConverter:
    @staticmethod
    def squares_to_dates(squares):
        first = datetime.now() - relativedelta(years=1)

        for square in squares:
            days_since = square[0] * HEIGHT + square[1]
            days_since = relativedelta(days=days_since)

            day = first + days_since

            yield day

EMAIL = "emilyb3333@gmail.com"
NAME = "Emily Bennett"

def commit_date(date):
    with open("repo/dates.txt", "w+") as f:
        f.write(str(date))

    subprocess.call(["git", "add", "dates.txt"], cwd="repo")
    subprocess.call(["git", "commit", f"--date={str(date)}", "-m", "h8u"], cwd="repo",
                    env=dict(os.environ, 
                        GIT_COMMITTER_EMAIL=EMAIL,
                        GIT_COMMITTER_NAME=NAME,
                        GIT_AUTHOR_EMAIL=EMAIL,
                        GIT_AUTHOR_NAME=NAME
                        ))

def main():
    root = tk.Tk()
    root.geometry("{0}x{1}+0+0".format(
            root.winfo_screenwidth(), root.winfo_screenheight()))
    squares = Squares(root)
    squares.pack(expand=True, fill=tk.BOTH)

    def print_dates():
        for day in SquareConverter.squares_to_dates(squares.get_squares()):
            print(day)

    print_squares = tk.Button(root, text="PRINT", command=print_dates)
    print_squares.pack(side=tk.TOP)

    def generate_commits():
        for day in SquareConverter.squares_to_dates(squares.get_squares()):
            commit_date(day)

    generate = tk.Button(root, text="Generate", command=generate_commits)
    generate.pack(side=tk.TOP)
        

    root.mainloop()


if __name__ == "__main__":
    main()
