import customtkinter
from tkinter import filedialog
import os
from datetime import date
import threading
from tkcalendar import DateEntry
import imageProcess as iP
import tkinter.messagebox as tkmb
import datetime as dt

class SettingWindow:

    def __init__(self):
        self.setting = customtkinter.CTk()
        self.setting.title("360VisualSync")
        self.setting.minsize(600, 400)  # Adjust these values as needed
        self.mp4_file_path = ""
        self.selected_mp4_file_path = ""  # Initialize with an empty string
        self.selected_output_folder_path = ""  # Initialize with an empty string

        project_directory = os.path.dirname(os.path.abspath(__file__))
        self.project_path = os.path.normpath(os.path.join(project_directory, "..", ))

        self.parsing_thread = None  # Variable to hold the parsing thread
        self.is_parsing = False  # Flag to track the parsing state
        self.selected_gnss_file_path = "None"

        # Top Rail
        top_frame = customtkinter.CTkFrame(master=self.setting)
        top_frame.pack(side="top", fill="x")

        button_width = 80

        # images_button = customtkinter.CTkButton(master=top_frame, text="Images", command=self.show_images_settings,
        #                                         width=button_width)
        # images_button.pack(side="left", padx=5)
        #
        # map_button = customtkinter.CTkButton(master=top_frame, text="Map", command=self.show_map_settings,
        #                                      width=button_width)
        # map_button.pack(side="left", padx=5)
        #
        # info_button = customtkinter.CTkButton(master=top_frame, text="Info", command=self.show_info_settings,
        #                                       width=button_width)
        # info_button.pack(side="left", padx=5)

        self.start_button = customtkinter.CTkButton(master=top_frame, text="Start", command=self.start_parse,
                                               width=button_width)
        self.start_button.pack(side="left", padx=5)

        self.cancel_button = customtkinter.CTkButton(master=top_frame, text="Cancel", command=self.cancel_parse,
                                                width=button_width, state="disabled")
        self.cancel_button.pack(side="left", padx=5)

        # You can implement code here to open a new window for your application
        # For example, you can create a new tkinter window and configure it as needed
        frame = customtkinter.CTkFrame(master=self.setting)
        frame.pack(pady=20, padx=60, fill="both", expand=True)

        label = customtkinter.CTkLabel(master=frame, text="Image Parse Settings", font=('Roboto', 24))
        label.pack(pady=12, padx=10)

        self.output_folder_button = customtkinter.CTkButton(master=frame, text="Select Output Folder", command=self.select_output_folder)
        self.output_folder_button.pack(pady=12, padx=10)

        self.mp4_button = customtkinter.CTkButton(master=frame, text="Select MP4 File", command=self.select_mp4_file)
        self.mp4_button.pack(pady=12, padx=10)

        frame_time = customtkinter.CTkFrame(master=frame)
        frame_time.pack(pady=20, padx=60, fill="both", expand=True)

        label = customtkinter.CTkLabel(master=frame_time, text="Video Start Time ", font=('Roboto', 20))
        label.pack(pady=2, padx=2)

        self.date_var = customtkinter.BooleanVar()
        self.date_checkbox = customtkinter.CTkCheckBox(master=frame_time, text="Enable Date and Time",
                                                       command=self.date_checkbox_changed, variable=self.date_var)
        self.date_checkbox.pack(pady=12, padx=10)

        today = date.today().strftime('%Y-%m-%d')
        self.date_picker = DateEntry(frame_time, background='darkblue', date_pattern='yyyy-mm-dd',date=today)
        self.date_picker.configure(state="disabled",justify='center')
        self.date_picker.pack(padx = 10, pady=12)

        # Time picker
        initial_time = "HH:MM:SS.sss"
        self.time_picker_var = customtkinter.StringVar(value=initial_time)
        self.time_picker = customtkinter.CTkEntry(frame_time, text_color="grey")
        self.time_picker.insert(0, self.time_picker_var.get())  # Set a larger width
        self.time_picker.configure(state="disabled",justify='center')
        self.time_picker.pack(padx=10, pady=12)

        frame_gnss = customtkinter.CTkFrame(master=frame_time)
        frame_gnss.pack(pady=20, padx=60, fill="both", expand=True)

        label = customtkinter.CTkLabel(master=frame_gnss, text="GNSS positions", font=('Roboto', 20))
        label.pack(pady=2, padx=2)

        self.gnss_var = customtkinter.BooleanVar()
        self.gnss_checkbox = customtkinter.CTkCheckBox(master=frame_gnss, text="Enable GNSS data",
                                                       command=self.gnss_checkbox_changed, variable=self.gnss_var, state="disabled")
        self.gnss_checkbox.pack(pady=12, padx=10)

        self.selected_gnss_file_path = customtkinter.StringVar()
        self.gnss_file_button = customtkinter.CTkButton(master=frame_gnss, text="Select GNSS File",
                                                        text_color_disabled="grey", state="disabled",
                                                        command=self.gnss_file_path)
        self.gnss_file_button.pack(pady=12, padx=10)


        self.setting.mainloop()

    def select_mp4_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])

        if file_path:
            file_name = os.path.basename(file_path)
            self.mp4_button.configure(text=file_name)
            self.selected_mp4_file_path = file_path

    def select_output_folder(self):
        # Select output folder
        output_folder_path = filedialog.askdirectory()

        if output_folder_path:
            self.output_folder_button.configure(text=output_folder_path)
            self.selected_output_folder_path = output_folder_path

    def gnss_checkbox_changed(self):
        stat = "normal" if self.gnss_var.get() else "disabled"
        self.gnss_file_button.configure(state=stat)

    def date_checkbox_changed(self):
        text_color = "grey" if not self.date_var.get() else "white"
        state = "normal" if self.date_var.get() else "disabled"
        self.time_picker.configure(state=state, text_color=text_color)

        self.date_picker.configure(state=state)
        self.gnss_checkbox.configure(state=state)
    def gnss_file_path(self):
        file_path = filedialog.askopenfilename(filetypes=[("GPX files", "*.gpx")])

        if file_path:
            file_name = os.path.basename(file_path)
            self.gnss_file_button.configure(text=file_name)
            self.selected_gnss_file_path = file_path

    def show_images_settings(self):
        # Implement logic to switch to Images settings
        print("Switching to Images Settings")

    def show_map_settings(self):
        # Implement logic to switch to Map settings
        print("Switching to Map Settings")

    def show_info_settings(self):
        # Implement logic to switch to Info settings
        print("Switching to Info Settings")

    def start_parse(self):
        self.disable_buttons_process()
        self.cancel_flag = threading.Event()

        if self.selected_mp4_file_path == "" or self.selected_output_folder_path == "":
            tkmb.showinfo(title="Missing File Paths", message="Please select both MP4 file and output folder paths.")
            self.process_buttons_ended()

        elif self.date_var.get():
            selected_date = self.parse_date()
            selected_time = self.parse_time()

            if self.parsed_time_ok and self.parsed_date_ok:
                #Input date and offset to first second up
                combined_datetime = dt.datetime.combine(selected_date, selected_time)
                rounded_datetime_sec = (combined_datetime + dt.timedelta(seconds=1)).strftime("%Y-%m-%d %H:%M:%S")
                offset_time = (1000000 - combined_datetime.microsecond) / 1000000

                #Start thread of parsing images
                image_processor = iP.ImageProcessing(
                    self.update_gui_parse,
                    self.cancel_flag,
                    offset_time,
                    self.selected_output_folder_path,
                    self.project_path,
                    self.selected_mp4_file_path,
                )

                parse_first_image = False
                self.parse_thread = threading.Thread(target=image_processor.parse_images, args=(parse_first_image,))
                self.parse_thread.start()

                self.check_process_status()

                self.parse_message = "None"
                self.exif_thread = threading.Thread(target=image_processor.add_exif, args=(rounded_datetime_sec, self.gnss_var.get(), self.selected_gnss_file_path))
                self.exif_thread.start()
            else:
                self.process_buttons_ended()
                pass

        else:
            image_processor = iP.ImageProcessing(
                self.update_gui_parse,
                self.cancel_flag,
                0,
                self.selected_output_folder_path,
                self.project_path,
                self.selected_mp4_file_path,
            )
            parse_first_image = False
            self.parse_thread = threading.Thread(target=image_processor.parse_images, args=(parse_first_image,))
            self.parse_thread.start()

            self.check_process_status()
            self.parse_message = "None"

    def check_process_status(self):
        if self.parse_thread.is_alive():
            self.setting.after(1000, self.check_process_status)
        else:
            tkmb.showinfo(title="Process Ended", message=self.parse_message)
            self.process_buttons_ended()

    def cancel_parse(self):
        self.cancel_flag.set()
        self.enable_buttons_process()
    def update_gui_parse(self, message):
        self.parse_message=message

    def parse_time(self):
        try:
            self.parsed_time_ok=True
            return dt.datetime.strptime(self.time_picker.get(), "%H:%M:%S.%f").time()
        except ValueError:
            tkmb.showinfo(title="Invalid time format", message="Invalid time format. Please use HH:MM:SS.sss")
            self.parsed_time_ok = False
    def parse_date(self):
        try:
            self.parsed_date_ok=True
            return dt.datetime.strptime(self.date_picker.get(), "%Y-%m-%d")
        except ValueError:
            tkmb.showinfo(title="Invalid date format", message="Invalid date format. Please use YYYY-MM-DD")
            self.parsed_date_ok=False

    def disable_buttons_process(self):
        #Disable buttons
        text_color = "grey"
        state = "disabled"
        self.start_button.configure(state=state)
        self.output_folder_button.configure(state=state)
        self.mp4_button.configure(state=state)
        self.date_checkbox.configure(state=state)
        self.time_picker.configure(state=state, text_color=text_color)
        self.date_picker.configure(state=state)
        self.gnss_checkbox.configure(state=state)
        self.gnss_file_button.configure(state=state)
        self.cancel_button.configure(state="normal")

    def enable_buttons_process(self):
        #enable buttons
        text_color = "white"
        state = "normal"
        self.start_button.configure(state=state)
        self.output_folder_button.configure(state=state)
        self.mp4_button.configure(state=state)
        self.date_checkbox.configure(state=state)
        date_picker_state = state if self.date_checkbox.get() == 1 else "disabled"
        time_picker_state = state if self.date_checkbox.get() == 1 else "disabled"
        time_picker_text_color = "white" if time_picker_state == "normal" else "grey"
        self.time_picker.configure(state=time_picker_state, text_color=time_picker_text_color)
        self.date_picker.configure(state=date_picker_state)
        self.gnss_checkbox.configure(state=state)
        gnss_file_state = state if self.gnss_checkbox.get() == 1 else "disabled"
        self.gnss_file_button.configure(state= gnss_file_state)
        self.cancel_button.configure(state="disabled")

    def process_buttons_ended(self):
        self.enable_buttons_process()
        self.cancel_button.configure(state="disabled")