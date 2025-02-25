import tkinter as tk
from tkinker import ttk
import customtkinter as ctk  # Import customtkinter
from PIL import Image

# Create the main window
ctk.set_appearance_mode("light")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("green")  # Themes: "blue", "green", "dark-blue"

window = ctk.CTk()  # Create a custom Tkinter window
window.title("Livestock & Co")
window.geometry("340x440")  # Set window size

# Create a frame inside the window
frame = ctk.CTkFrame(window)
frame.pack(expand=True, fill="both", padx=20, pady=20)

# Header label
header_label = ctk.CTkLabel(frame, text="Welcome to LCMS!", font=("Arial", 20, "bold"))
header_label.pack(pady=10)

# Login label
login_label = ctk.CTkLabel(frame, text="Login", font=("Arial", 16, "bold"))
login_label.pack(pady=5)

# Username input
username_label = ctk.CTkLabel(frame, text="Username:", font=("Arial", 12))
username_label.pack()
username_entry = ctk.CTkEntry(frame, width=220)
username_entry.pack(pady=5)

# Password input
password_label = ctk.CTkLabel(frame, text="Password:", font=("Arial", 12))
password_label.pack()
password_entry = ctk.CTkEntry(frame, width=220, show="*")  # Hide password characters
password_entry.pack(pady=5)

# Login button
login_button = ctk.CTkButton(frame, text="Login", corner_radius=32, fg_color="transparent", hover_color="#A2E1DB", border_color="#14525D", border_width=1)
login_button.pack(pady=20)

# Reset/Forgot password button
reset_button = ctk.CTkButton(frame, text="Forgot Username or Password?", fg_color="red", hover_color="dark red", text_color="white")
reset_button.pack()

# Run the app
window.mainloop()
