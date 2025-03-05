import tkinter
import customtkinter
import tkinter.messagebox as tkmb
import desktop.appwindow as aw

class LoginWindow:
    def __init__(self):
        customtkinter.set_appearance_mode("system")
        customtkinter.set_default_color_theme("dark-blue")

        self.root = customtkinter.CTk()
        self.root.title("360VisualApp")
        self.root.geometry("500x350")
        self.root.minsize(500, 350)

        aw.SettingWindow()

        self.create_widgets()

    def create_widgets(self):
        frame = customtkinter.CTkFrame(master=self.root)
        frame.pack(pady=20, padx=60, fill="both", expand=True)

        label = customtkinter.CTkLabel(master=frame, text="Login System", font=('Roboto', 24))
        label.pack(pady=12, padx=10)

        self.entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="Username")
        self.entry1.pack(pady=12, padx=10)

        self.entry2 = customtkinter.CTkEntry(master=frame, placeholder_text="Password")
        self.entry2.pack(pady=12, padx=10)

        button = customtkinter.CTkButton(master=frame, text="Login", command=self.login)
        button.pack(pady=12, padx=10)

        checkbox = customtkinter.CTkCheckBox(master=frame, text="Remember Me")
        checkbox.pack(pady=12, padx=10)

        creator = customtkinter.CTkLabel(
            master=self.root, fg_color=("white", "#000066"), text="Creator: Lukáš Běloch, CTU Prague",
            corner_radius=8, anchor="e"
        )
        creator.pack(fill="both")
        self.root.mainloop()



    def login(self):
        # Get the entered username and password
        entered_username = self.entry1.get()
        entered_password = self.entry2.get()

        valid_username = "visualsync"
        valid_password = "360"

        # Check the entered credentials
        if entered_username == valid_username and entered_password == valid_password:
            tkmb.showinfo(title="Login Successful", message="You have logged in successfully")
            self.root.destroy()  # Close the login window
            aw.SettingWindow()
        elif entered_username == valid_username and entered_password != valid_password:
            tkmb.showwarning(title='Wrong password', message='Please check your password')
        elif entered_username != valid_username and entered_password == valid_password:
            tkmb.showwarning(title='Wrong username', message='Please check your username')
        else:
            tkmb.showerror(title="Login Failed", message="Invalid Username and password")

