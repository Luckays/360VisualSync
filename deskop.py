import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime
from PIL import Image, ImageTk

class TkinterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("360VizualSync")
        self.root.minsize(600, 400)  # Adjust these values as needed



        # Left column
        self.left_frame = ttk.Frame(root)
        self.left_frame.grid(row=0, column=0, padx=10, sticky='n')  # 'n' makes the left column sticky to the north (top)

        # Frame for buttons and checkboxes
        button_frame = ttk.Frame(self.left_frame, padding=(10, 10, 10, 10))
        button_frame.grid(row=0, column=0, sticky='nsew')

        # MP4 button
        mp4_button = ttk.Button(button_frame, text="Select MP4 File", command=self.select_mp4_file)
        mp4_button.grid(row=0, column=0, pady=5)

        # Checkbox for GNSS file
        self.gnss_var = tk.BooleanVar()
        gnss_checkbox = ttk.Checkbutton(button_frame, text="Include GNSS File", variable=self.gnss_var, command=self.gnss_checkbox_changed)
        gnss_checkbox.grid(row=1, column=0, pady=5)

        # File selection for GNSS
        self.gnss_file_path = tk.StringVar()
        gnss_file_button = ttk.Button(button_frame, text="Select GNSS File", command=self.select_gnss_file, state=tk.DISABLED)
        gnss_file_button.grid(row=2, column=0, pady=5)

        # Checkbox for date
        self.date_var = tk.BooleanVar()
        date_checkbox = ttk.Checkbutton(button_frame, text="Select Date", variable=self.date_var, command=self.date_checkbox_changed)
        date_checkbox.grid(row=3, column=0, pady=5)

        # Date picker
        self.date_picker = DateEntry(button_frame, state=tk.DISABLED)
        self.date_picker.grid(row=4, column=0, pady=5)

        # Time picker
        initial_time = "YYYY-MM-DD hh:mm:ss.sss"
        self.time_picker_var = tk.StringVar(value=initial_time)
        self.time_picker = ttk.Entry(button_frame, textvariable=self.time_picker_var, state=tk.DISABLED, width=20)  # Set a larger width
        self.time_picker.grid(row=5, column=0, pady=5)

        # Separators
        separator_top = ttk.Separator(self.left_frame, orient="horizontal")
        separator_top.grid(row=1, column=0, sticky="ew", pady=10)

        separator_bottom = ttk.Separator(self.left_frame, orient="horizontal")
        separator_bottom.grid(row=2, column=0, sticky="ew", pady=10)

        # Image display
        self.image_label = ttk.Label(root)
        self.image_label.grid(row=0, column=1, rowspan=6, padx=10,
                              sticky='nsew')  # 'nsew' makes the image label sticky to the north, south, east, and west

        # Log display
        self.log_text = tk.Text(root, height=10, width=40)
        self.log_text.grid(row=6, column=1, pady=10, padx=10,
                           sticky='nsew')  # 'nsew' makes the log text sticky to the north, south, east, and west

        # Configure column weights
        root.columnconfigure(0, weight=0)  # Left column
        root.columnconfigure(1, weight=2)  # Right column (image and log box)

        # Configure row weights if needed
        root.rowconfigure(0, weight=1)  # Top row (if you have additional rows)

        # Update the image and log every second
        self.update_display()

    def select_mp4_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
        self.mp4_file_path.set(file_path)
        print("Selected MP4 File:", file_path)

    def gnss_checkbox_changed(self):
        state = tk.NORMAL if self.gnss_var.get() else tk.DISABLED
        self.gnss_file_path.set("")
        self.gnss_file_button.config(state=state)

    def select_gnss_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("GPX files", "*.gpx")])
        self.gnss_file_path.set(file_path)
        print("Selected GNSS File:", file_path)

    def date_checkbox_changed(self):
        state = tk.NORMAL if self.date_var.get() else tk.DISABLED
        self.date_picker.config(state=state)
        self.time_picker.config(state=state)


    def update_display(self):
        # Update image
        # Replace 'path_to_your_image_file' with the path to your extracted image file
        image_path = 'D:\CVUT\PhD\SMICHOVSKENADRAZI_RAW\out\VID_20240110_121842_00_025_00001.png'
        self.display_image(image_path)

        # Update log (replace this with the actual log information)
        log_info = "Log information goes here\n"
        self.log_text.insert(tk.END, log_info)
        self.log_text.see(tk.END)  # Scroll to the end of the log

        # Schedule the next update after 1000 milliseconds (1 second)
        self.root.after(1000, self.update_display)

    def display_image(self, image_path):
        # Load the image
        img = Image.open(image_path)

        # Resize the image to fit the label while maintaining its aspect ratio
        img.thumbnail((400, 400))

        # Convert the image to PhotoImage format for Tkinter
        img = ImageTk.PhotoImage(img)

        # Update the label with the new image
        self.image_label.configure(image=img)
        self.image_label.image = img

if __name__ == "__main__":
    root = tk.Tk()
    app = TkinterApp(root)
    root.mainloop()