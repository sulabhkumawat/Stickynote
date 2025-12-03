import tkinter as tk
from tkinter import font, messagebox
from datetime import date

class StickyNoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sticky Notes")
        self.root.geometry("600x600")
        self.root.configure(bg="black")
        self.root.attributes('-topmost', True)

        # Fonts
        self.heading_font = font.Font(family="Helvetica", size=24, weight="bold")  # Extra bold
        self.note_font = font.Font(family="Helvetica", size=12, weight="bold")  # Bold notes

        # Heading text
        today = date.today().strftime("%B %d, %Y")
        self.heading_text = f"Today's Mission - {today}"

        # Heading Label with wraplength to auto-fit
        self.heading = tk.Label(root, text=self.heading_text, 
                                bg="black", fg="green", font=self.heading_font,
                                wraplength=self.root.winfo_width(), justify="center")
        self.heading.pack(pady=10, fill=tk.X)

        # Bind resize to adjust heading wraplength and font size
        self.root.bind("<Configure>", self.resize_heading)

        # Menu
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Options", menu=file_menu)
        file_menu.add_command(label="Add Note", command=self.add_note)
        file_menu.add_command(label="Delete Note", command=self.delete_note)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Frame to hold notes
        self.notes_frame = tk.Frame(self.root, bg="black")
        self.notes_frame.pack(fill=tk.BOTH, expand=True)

        self.notes = []

    def resize_heading(self, event):
        # Dynamically adjust heading font size based on window width
        new_size = max(16, int(event.width / 25))  # Prevent too small
        self.heading_font.configure(size=new_size)
        # Adjust wraplength to fit inside window
        self.heading.config(wraplength=event.width - 20)

    def add_note(self):
        note = tk.Text(self.notes_frame, height=5, width=40, 
                       bg="black", fg="green", insertbackground="green",
                       font=self.note_font)
        note.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)
        note.bind("<Button-3>", lambda e, n=note: self.show_delete_menu(e, n))
        self.notes.append(note)
        note.focus_set()

    def delete_note(self):
        if not self.notes:
            messagebox.showinfo("Info", "No notes to delete!")
            return
        note_to_delete = self.notes.pop()
        note_to_delete.destroy()

    def show_delete_menu(self, event, note):
        menu = tk.Menu(self.root, tearoff=0, bg="black", fg="green")
        menu.add_command(label="Delete", command=lambda: self.delete_specific_note(note))
        menu.tk_popup(event.x_root, event.y_root)

    def delete_specific_note(self, note):
        if note in self.notes:
            self.notes.remove(note)
            note.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = StickyNoteApp(root)
    root.mainloop()
