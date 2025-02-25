import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import customtkinter as ctk
import mysql.connector
import bcrypt
import threading
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Secure database credentials
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "lco_auth")

# Get script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
theme_path = os.path.join(script_dir, "custom_theme.json")

# Apply custom theme if available
if os.path.isfile(theme_path):
    try:
        ctk.set_default_color_theme(theme_path)
    except Exception as e:
        print(f"Error loading theme: {e}. Falling back to default.")
else:
    print("Warning: Theme file not found. Using default theme.")

# Function to hash passwords
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Function to check passwords securely
def check_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))

# Database authentication with improved error handling
def authenticate_user(username, password, callback):
    def db_thread():
        try:
            connection = mysql.connector.connect(
                host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
            )
            cursor = connection.cursor()
            cursor.execute("SELECT password FROM user WHERE username = %s", (username,))
            result = cursor.fetchone()
            cursor.close()
            connection.close()

            if result and check_password(result[0], password):
                callback(True, None)
            else:
                callback(False, "Invalid username or password")

        except mysql.connector.Error as err:
            print(f"Database error: {err}")  # Log for debugging
            callback(False, "Database connection error. Please try again later.")

    threading.Thread(target=db_thread, daemon=True).start()

# Function to handle login with improved error display
def login():
    username = username_entry.get()
    password = password_entry.get()
    login_button.configure(state="disabled")
    error_label.configure(text="Authenticating...", text_color="blue")

    def on_auth_result(success, message):
        if success:
            open_homescreen()
        else:
            error_label.configure(text=message, text_color="red")
        login_button.configure(state="normal")

    authenticate_user(username, password, on_auth_result)

# Function to open the homescreen
def open_homescreen():
    window.withdraw()
    homescreen = Homescreen()
    homescreen.mainloop()

# Get the script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Get the script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Get the script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Main login window
window = ctk.CTk()
window.title("Livestock & Co")
window.geometry("440x680")

frame = ctk.CTkFrame(window)
frame.pack(expand=True, fill="both", padx=20, pady=20)

# Load logo
logo_path = os.path.join(script_dir, "logo.png")
logo_image = None

try:
    # Open the image and resize it
    original_logo = Image.open(logo_path)
    resized_logo = original_logo.resize((300, 300), Image.LANCZOS)
    
    # Print the resized image size to confirm it is resized correctly
    print(f"Resized image size: {resized_logo.size}")
    
    # Convert resized image using ImageTk.PhotoImage
    logo_image = ImageTk.PhotoImage(resized_logo)
except FileNotFoundError:
    print(f"Warning: Logo not found at {logo_path}")
except Exception as e:
    print(f"Error loading logo: {e}")

if logo_image:
    # Use the resized image in the label
    logo_label = ctk.CTkLabel(frame, image=logo_image, text="")
    logo_label.pack(pady=10)
else:
    print("Logo image could not be loaded.")

# UI Elements
header_label = ctk.CTkLabel(frame, text="Welcome to LCMS!", font=("Arial", 20, "bold"))
header_label.pack(pady=10)

login_label = ctk.CTkLabel(frame, text="Login", font=("Arial", 16, "bold"))
login_label.pack(pady=5)

username_entry = ctk.CTkEntry(frame, width=220, placeholder_text="Username")
username_entry.pack(pady=5)

password_entry = ctk.CTkEntry(frame, width=220, show="*", placeholder_text="Password")
password_entry.pack(pady=5)

# Password visibility toggle
def toggle_password():
    if password_entry.cget("show") == "*":
        password_entry.configure(show="")
    else:
        password_entry.configure(show="*")

toggle_password_button = ctk.CTkButton(frame, text="👁️", command=toggle_password, width=30)
toggle_password_button.pack(pady=5)

login_button = ctk.CTkButton(frame, text="Login", command=login)
login_button.pack(pady=20)

# Reset/Forgot password button
reset_button = ctk.CTkButton(frame, text="Forgot Username or Password?",
                             fg_color="red", hover_color="dark red", text_color="white")
reset_button.pack()

error_label = ctk.CTkLabel(frame, text="", font=("Arial", 12))
error_label.pack(pady=5)

# Registration window
def open_registration():
    register_window = ctk.CTkToplevel(window)
    register_window.title("User Registration")
    register_window.geometry("360x300")

    def register_user():
        username = reg_username_entry.get()
        password = reg_password_entry.get()
        confirm_password = reg_confirm_password_entry.get()

        if password != confirm_password:
            reg_error_label.configure(text="Passwords do not match", text_color="red")
        else:
            hashed_password = hash_password(password)
            try:
                connection = mysql.connector.connect(
                    host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
                )
                cursor = connection.cursor()
                cursor.execute("INSERT INTO user (username, password) VALUES (%s, %s)", (username, hashed_password))
                connection.commit()
                cursor.close()
                connection.close()
                reg_error_label.configure(text="Registration successful! Please login.", text_color="green")
            except mysql.connector.Error as err:
                reg_error_label.configure(text=f"Error: {err}", text_color="red")

    reg_frame = ctk.CTkFrame(register_window)
    reg_frame.pack(expand=True, fill="both", padx=20, pady=20)

    reg_username_entry = ctk.CTkEntry(reg_frame, width=220, placeholder_text="Username")
    reg_username_entry.pack(pady=5)

    reg_password_entry = ctk.CTkEntry(reg_frame, width=220, show="*", placeholder_text="Password")
    reg_password_entry.pack(pady=5)

    reg_confirm_password_entry = ctk.CTkEntry(reg_frame, width=220, show="*", placeholder_text="Confirm Password")
    reg_confirm_password_entry.pack(pady=5)

    reg_button = ctk.CTkButton(reg_frame, text="Register", command=register_user)
    reg_button.pack(pady=20)

    reg_error_label = ctk.CTkLabel(reg_frame, text="", font=("Arial", 12))
    reg_error_label.pack(pady=5)

# Button to open registration window
register_button = ctk.CTkButton(frame, text="Register", command=open_registration)
register_button.pack(pady=5)

# Dashboard class
class Homescreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Livestock Management Dashboard")
        self.geometry("800x500")
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.sidebar = tk.Frame(self, bg="#2c3e50", width=200, height=500)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.main_content = tk.Frame(self, bg="#ecf0f1")
        self.main_content.grid(row=0, column=1, sticky="nsew")
        self.create_sidebar_buttons()
        self.label = tk.Label(self.main_content, text="Welcome to your Operation", font=("Arial", 16), bg="#ecf0f1")
        self.label.grid(row=0, column=0, padx=10, pady=10)

    def create_sidebar_buttons(self):
        buttons = [("Home", self.show_home), ("My Operation", self.show_operations),
                   ("Resources", self.show_resources), ("Contact Us", self.show_contact)]
        for text, command in buttons:
            btn = tk.Button(self.sidebar, text=text, command=command, font=("Arial", 12),
                            bg="#34495e", fg="white", bd=0, padx=10, pady=5)
            btn.pack(fill="x", pady=5)

    def show_home(self):
        self.label.config(text="Home Screen")

    def show_operations(self):
        self.label.config(text="Analytics Dashboard")

    def show_resources(self):
        self.label.config(text="Resources Page")

    def show_contact(self):
        self.label.config(text="Contact Page")

# Run application
if __name__ == "__main__":
    window.mainloop()
