import tkinter as tk
from tkinter import messagebox, Menu, Text, font 
from datetime import datetime

# --- Configuration Constants ---
THEME_BG_MAIN = 'black'
THEME_BG_NOTE = '#111111'  
THEME_FG_GREEN = '#00FF00' 
THEME_FONT = ('Consolas', 12)
THEME_FONT_HEADING = ('Consolas', 18, 'bold')
NOTE_PADDING = 5
NOTE_BORDER_WIDTH = 2
DEFAULT_NOTE_HEIGHT = 8

# --- NoteFrame Class (Unchanged) ---
class NoteFrame(tk.Frame):
    def __init__(self, master, app_instance):
        super().__init__(master, bg=THEME_BG_MAIN, padx=NOTE_PADDING, pady=NOTE_PADDING)
        self.app = app_instance
        self.grid_columnconfigure(0, weight=1) 
        self.grid_rowconfigure(0, weight=1)    

        self.text_widget = Text(
            self,
            bg=THEME_BG_NOTE,
            fg=THEME_FG_GREEN,
            insertbackground=THEME_FG_GREEN, 
            font=THEME_FONT,
            height=DEFAULT_NOTE_HEIGHT, 
            relief='ridge', 
            borderwidth=NOTE_BORDER_WIDTH,
            insertwidth=2,
            selectbackground='#008000', 
            selectforeground='white'
        )
        self.text_widget.grid(row=0, column=0, sticky='nsew')
        self.text_widget.insert('1.0', "New mission objective...\n\n(Right-click to delete this note)\n\nThis note is now safely deleted via after_idle().")

        self.context_menu = Menu(self, tearoff=0, bg=THEME_BG_MAIN, fg=THEME_FG_GREEN)
        self.context_menu.add_command(label="Delete Note", command=self.delete_note, activebackground='#008000', activeforeground='white')
        self.text_widget.bind("<Button-3>", self._show_context_menu)

    def _show_context_menu(self, event):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def delete_note(self):
        self.app.schedule_safe_deletion(self)


# --- StickyNotesApp Class (Fixes applied) ---
class StickyNotesApp:
    def __init__(self, master):
        self.master = master
        master.title("Sticky Notes Terminal - Always On Top")
        master.geometry("600x400")
        master.config(bg=THEME_BG_MAIN)
        
        # --- FIX: Set the window to always stay on top ---
        master.wm_attributes('-topmost', 1) 
        
        master.grid_columnconfigure(0, weight=1) 
        master.grid_rowconfigure(1, weight=1) 

        self.notes = [] 

        self._setup_heading()
        self._setup_note_container()
        self._setup_menu_bar()
        
        self.master.bind('<Configure>', self._resize_heading_font)
        self.master.after(100, self._initial_heading_resize)

        self.add_note()

    def _setup_heading(self):
        """Creates and places the dynamic heading label."""
        current_date = datetime.now().strftime("%Y-%m-%d")
        heading_text = f"TODAY'S MISSION - {current_date}"
        
        self.heading_font = font.Font(family='Consolas', size=18, weight='bold')

        self.heading_label = tk.Label(
            self.master,
            text=heading_text,
            bg=THEME_BG_MAIN,
            fg=THEME_FG_GREEN,
            font=self.heading_font 
        )
        self.heading_label.grid(row=0, column=0, sticky='new', padx=10, pady=10)
        
    def _initial_heading_resize(self):
        """Calculates the initial font size only when the window's geometry is valid."""
        self.master.update_idletasks() 
        
        if self.master.winfo_width() > 100:
            current_width = self.master.winfo_width()
            self._calculate_and_set_font_size(current_width)

    def _resize_heading_font(self, event):
        """Dynamically adjusts the heading font size based on the window width during resizing."""
        self._calculate_and_set_font_size(event.width)

    def _calculate_and_set_font_size(self, width):
        """Common logic to calculate and set the new font size."""
        new_size = max(10, int(width / 30))
        
        if new_size != self.heading_font['size']:
            self.heading_font.config(size=new_size)

    def _setup_note_container(self):
        self.note_container = tk.Frame(self.master, bg=THEME_BG_MAIN)
        self.note_container.grid(row=1, column=0, sticky='nsew')
        self.note_container.grid_columnconfigure(0, weight=1) 

    def _setup_menu_bar(self):
        menubar = Menu(self.master, bg=THEME_BG_MAIN, fg=THEME_FG_GREEN)
        self.master.config(menu=menubar)
        options_menu = Menu(menubar, tearoff=0, bg=THEME_BG_MAIN, fg=THEME_FG_GREEN, 
                            activebackground='#008000', activeforeground='white')
        options_menu.add_command(label="➕ Add Note", command=self.add_note)
        options_menu.add_command(label="🗑️ Delete Last Note", command=self.delete_last_note)
        options_menu.add_separator()
        options_menu.add_command(label="🚪 Exit", command=self.master.quit)
        menubar.add_cascade(label="Options", menu=options_menu)

    def add_note(self):
        new_note = NoteFrame(self.note_container, self)
        row_index = len(self.notes)
        new_note.grid(row=row_index, column=0, sticky='ew')
        self.note_container.grid_rowconfigure(row_index, weight=1) 
        self.notes.append(new_note)

    def delete_last_note(self):
        if not self.notes:
            messagebox.showinfo("Attention", "No notes to delete.")
            return
        note_to_delete = self.notes[-1] 
        self.schedule_safe_deletion(note_to_delete, is_specific_delete=False)
        
    def schedule_safe_deletion(self, note_frame, is_specific_delete=True):
        self.master.after_idle(self._execute_safe_deletion, note_frame)

    def _execute_safe_deletion(self, note_frame):
        if note_frame not in self.notes:
            return

        try:
            row_index = note_frame.grid_info()['row']
        except Exception:
            row_index = None

        self.notes.remove(note_frame)
        note_frame.destroy()
        self._reorganize_notes(deleted_row_index=row_index)

    def _reorganize_notes(self, deleted_row_index=None):
        num_notes = len(self.notes)
        
        if deleted_row_index is not None:
             self.note_container.grid_rowconfigure(deleted_row_index, weight=0)
        
        for i, note in enumerate(self.notes):
            if not note.winfo_exists():
                continue

            note.grid(row=i, column=0, sticky='ew')
            self.note_container.grid_rowconfigure(i, weight=1)
            
        for i in range(num_notes, self.note_container.grid_size()[1]):
             self.note_container.grid_rowconfigure(i, weight=0)


# --- Main Execution Block ---
if __name__ == "__main__":
    root = tk.Tk()
    app = StickyNotesApp(root)
    root.mainloop()