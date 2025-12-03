import tkinter as tk
from tkinter import messagebox, Menu, Text
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

class NoteFrame(tk.Frame):
    """A custom Frame containing a Text widget and handling right-click deletion."""
    def __init__(self, master, app_instance):
        super().__init__(master, bg=THEME_BG_MAIN, padx=NOTE_PADDING, pady=NOTE_PADDING)
        self.app = app_instance

        # Configure for Horizontal and Vertical Expansion
        self.grid_columnconfigure(0, weight=1) 
        self.grid_rowconfigure(0, weight=1)    

        # Text Widget for the Note Content
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

        # Right-Click Context Menu (for deletion)
        self.context_menu = Menu(self, tearoff=0, bg=THEME_BG_MAIN, fg=THEME_FG_GREEN)
        self.context_menu.add_command(
            label="Delete Note", 
            command=self.delete_note, # Now calls a simple wrapper
            activebackground='#008000',
            activeforeground='white'
        )

        # Bind the right-click event to the text widget
        self.text_widget.bind("<Button-3>", self._show_context_menu)

    def _show_context_menu(self, event):
        """Displays the context menu at the cursor position."""
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def delete_note(self):
        """Schedules the deletion to prevent crashing during event processing."""
        # --- CRITICAL FIX: Schedule deletion using after_idle ---
        self.app.schedule_safe_deletion(self)


# ------------------------------------------------------------------
# Main Application Class
# ------------------------------------------------------------------

class StickyNotesApp:
    """The main application class for the Sticky Notes GUI."""
    def __init__(self, master):
        self.master = master
        master.title("Sticky Notes Terminal - Safe Deletion")
        master.geometry("600x400")
        master.config(bg=THEME_BG_MAIN)
        
        # Root Window Configuration for Resizing
        master.grid_columnconfigure(0, weight=1) 
        master.grid_rowconfigure(1, weight=1) 

        self.notes = [] 

        self._setup_heading()
        self._setup_note_container()
        self._setup_menu_bar()

        self.add_note()

    # --- Setup Methods (Unchanged) ---
    def _setup_heading(self):
        current_date = datetime.now().strftime("%Y-%m-%d")
        heading_text = f"TODAY'S MISSION - {current_date}"
        self.heading_label = tk.Label(
            self.master,
            text=heading_text,
            bg=THEME_BG_MAIN,
            fg=THEME_FG_GREEN,
            font=THEME_FONT_HEADING
        )
        self.heading_label.grid(row=0, column=0, sticky='new', padx=10, pady=10)

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


    # --- Note Management Methods ---

    def add_note(self):
        """Creates a new NoteFrame, adds it to the container, and sets its row weight."""
        new_note = NoteFrame(self.note_container, self)
        
        row_index = len(self.notes)
        new_note.grid(row=row_index, column=0, sticky='ew')
        
        self.note_container.grid_rowconfigure(row_index, weight=1) 
        
        self.notes.append(new_note)

    def delete_last_note(self):
        """Deletes the last NoteFrame added to the list and performs cleanup."""
        if not self.notes:
            messagebox.showinfo("Attention", "No notes to delete.")
            return

        note_to_delete = self.notes[-1] 
        self.schedule_safe_deletion(note_to_delete, is_specific_delete=False)
        
    def schedule_safe_deletion(self, note_frame, is_specific_delete=True):
        """
        Schedules the deletion of a note using after_idle to avoid crashes.
        This is the new robust entry point for deletion.
        """
        # We pass the function reference and its arguments to after_idle
        self.master.after_idle(self._execute_safe_deletion, note_frame)

    def _execute_safe_deletion(self, note_frame):
        """
        Performs the destruction and cleanup when Tkinter is idle.
        """
        # 1. Check Existence before operation (Requirement)
        if note_frame not in self.notes:
            return

        # 2. Get the row index safely before destruction
        try:
            row_index = note_frame.grid_info()['row']
        except Exception:
            row_index = None

        # 3. Remove from the tracking list
        self.notes.remove(note_frame)
        
        # 4. Destroy the widget
        note_frame.destroy()
        
        # 5. Reorganize the remaining notes
        self._reorganize_notes(deleted_row_index=row_index)

    def _reorganize_notes(self, deleted_row_index=None):
        """
        Re-grids all existing notes after a specific one is deleted and updates weights.
        """
        num_notes = len(self.notes)
        
        # Clear the row weight for the deleted note's row if known
        if deleted_row_index is not None:
             self.note_container.grid_rowconfigure(deleted_row_index, weight=0)
        
        # Re-grid and apply weight to the new configuration
        for i, note in enumerate(self.notes):
            # Ensure the note object still exists (Safety Check)
            if not note.winfo_exists():
                continue

            # Re-grid to the new sequential row index
            note.grid(row=i, column=0, sticky='ew')
            
            # Re-apply vertical expansion weight (proportional resizing)
            self.note_container.grid_rowconfigure(i, weight=1)
            
        # Ensure no higher-indexed rows retain weight
        for i in range(num_notes, self.note_container.grid_size()[1]):
             self.note_container.grid_rowconfigure(i, weight=0)


# --- Main Execution Block ---
if __name__ == "__main__":
    root = tk.Tk()
    app = StickyNotesApp(root)
    root.mainloop()