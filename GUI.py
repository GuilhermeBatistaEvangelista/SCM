import tkinter as tk

class Window(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title("SCM")
		self.configure(background="blue")
		self.geometry("800x400")

		self.button = tk.Button(text="Exit", command=quit)
		self.button.pack(fill="both", expand=True)
		tk.Label(self, text="Nothing will work unless you do.").pack()