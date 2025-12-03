# 🐍 Python Sticky Notes GUI App

A modern, terminal-style desktop sticky notes application built using Python's built-in **Tkinter** library.

The application features a dark, high-contrast **black and green theme** and fully **dynamic resizing** for both the main window and individual notes.

---

## ✨ Current Features

* **Terminal Theme:** Uses a sharp black background (`#111111`) and bright green text (`#00FF00`) for a modern, high-contrast look.
* **Dynamic Resizing:** Both the note container and individual notes expand and contract **proportionally** with the main window width and height.
* **Dynamic Heading:** The heading, **"TODAY'S MISSION - <current date>"**, adjusts its font size dynamically to fit the window width, preventing overflow and remaining visible.
* **Stable Deletion:** Notes can be deleted via a **right-click context menu** or a "Delete Last Note" menu option without crashing the application (using `after_idle()` for stable event handling).
* **Menu System:** Simple menu for adding notes, deleting the last note, and exiting.

---

## 🛠️ Requirements

* **Python 3.x**
* **Tkinter** (Usually included with standard Python installations)

No external libraries are required.

---

## 🚀 How to Run

1.  **Save the Code:** Save the Python script (containing the `StickyNotesApp` class) as a file named `sticky_notes_app.py`.
2.  **Open Terminal:** Navigate to the directory where you saved the file.
3.  **Execute:** Run the application using the Python interpreter:

    ```bash
    python sticky_notes_app.py
    ```

---

## 💡 How to Use

| Feature | Action | Description |
| :--- | :--- | :--- |
| **Add New Note** | `Options` -> `➕ Add Note` | Adds a new, editable note frame to the bottom of the window. |
| **Delete Specific Note** | **Right-click** on any note text area | A context menu appears with the option to delete that specific note. |
| **Delete Last Note** | `Options` -> `🗑️ Delete Last Note` | Removes the most recently added note. |
| **Edit Content** | Click directly on the note's text area | All notes are persistent, editable `Text` widgets. |
| **Exit App** | `Options` -> `🚪 Exit` | Closes the application window. |

---

## 🏗️ Code Structure Highlights

The application is built on stable Tkinter architecture:

* **`StickyNotesApp`:** Manages the main window, global settings, menu bar, and the overall note management logic.
* **`NoteFrame`:** Represents a single sticky note instance, containing the themed `tk.Text` widget and the right-click binding.
* **Grid Management:** Intensive use of `grid_columnconfigure(weight=1)` and `grid_rowconfigure(weight=1)` ensures fully proportional resizing across all components.

---

## 🔮 Future Enhancements

The current app provides a stable foundation, but its future evolution could focus on persistence, user experience, and expanded functionality:

### 💾 Data Persistence

* **Saving Notes to File:** Implement functionality to save all notes and their content to a **JSON** file. Load this data automatically when the app starts.
* **Automatic Saving:** Use `self.master.after()` to schedule a function that saves the notes every few minutes, preventing data loss.

### 🎨 User Interface and Experience (UX)

* **Individual Note Windows:** Convert notes from stacked frames into **separate, always-on-top `Toplevel` windows** for true desktop stickiness.
* **Custom Note Colors:** Implement a submenu that allows users to change the primary text and border color scheme of individual notes (e.g., green, yellow, blue) for visual organization.
* **Transparency:** Add an option to set the **transparency** (alpha channel) of the notes' windows.

### ⚙️ Enhanced Functionality

* **Search/Filtering:** Implement a search bar at the top of the main window to quickly **filter** the displayed notes based on keywords.
* **Task List Integration:** Add simple task tracking features like **checkboxes** or bullet points functionality.
* **Modularization:** Refactor the classes into separate Python files (e.g., `note_widget.py`, `app.py`) for better organization and maintainability.