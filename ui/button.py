import tkinter as tk

def create_rounded_button(parent, text, command, x, y, width=90, height=24, radius=2, bg="#1e293b", fg="white", font=("Helvetica", 12)):
    """Creates a rounded button on a canvas."""
    canvas = tk.Canvas(parent, width=width, height=height, highlightthickness=0, bg=parent["bg"])
    canvas.place(x=x, y=y)

    # Draw the rounded rectangle
    canvas.create_oval((0, 0, radius * 2, height), fill=bg, outline=bg)
    canvas.create_oval((width - radius * 2, 0, width, height), fill=bg, outline=bg)
    canvas.create_rectangle((radius, 0, width - radius, height), fill=bg, outline=bg)

    # Add the text
    canvas.create_text(width // 2, height // 2, text=text, fill=fg, font=font)

    # Add the click functionality
    def on_click(event):
        command()

    canvas.bind("<Button-1>", on_click)
    return canvas