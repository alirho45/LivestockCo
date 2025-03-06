"""
Author: Tesha Alisha Rhodes
Final Project
Livestock Management System
"""
# Import necessary modules
import os
import csv
import pandas as pd
import customtkinter as ctk
import bcrypt
import webbrowser
from PIL import Image
from tkinter import simpledialog

# Initialize customtkinter appearance and theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Custom color scheme
CUSTOM_THEME = {
    "fg_color": "#4F7486",
    "bg_color": "#FEE6C4",
    "button_color": "#4F7486",
    "button_hover_color": "#3A5460",
    "entry_color": "#4F7486",
    "entry_hover_color": "#3A5460",
    "frame_color": "#FDDAC0",
    "text_color": "#4F7486"
}

# Get script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
users_csv_path = os.path.join(script_dir, "users.csv")
logo_path = os.path.join(script_dir, "logo.png")
chicken_breeds_path = os.path.join(script_dir, "chicken_breeds.xlsx")

def load_image(path, size):
    try:
        return ctk.CTkImage(light_image=Image.open(path), dark_image=Image.open(path), size=size)
    except Exception as e:
        print(f"Error loading image {path}: {e}")
        return None

# Function to check passwords
def check_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))

# Authenticate user
def authenticate_user(username, password, callback):
    try:
        with open(users_csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row["username"] == username and check_password(row["password_hash"], password):
                    callback(True, row["farm_id"])
                    return
        callback(False, "Invalid username or password")
    except FileNotFoundError:
        callback(False, "User database not found.")
    except Exception as e:
        callback(False, f"Error: {e}")

class LoginScreen(ctk.CTk):
    def __init__(self, on_success):
        super().__init__()
        self.on_success = on_success
        self.title("Login - LCMS")
        self.geometry("400x400")
        self.configure(fg_color=CUSTOM_THEME["bg_color"])
        self.create_widgets()
    
    def create_widgets(self):
        frame = ctk.CTkFrame(self, fg_color=CUSTOM_THEME["frame_color"])
        frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        logo = load_image(logo_path, (100, 100))
        if logo:
            logo_label = ctk.CTkLabel(frame, image=logo, text="")
            logo_label.pack(pady=10)
        
        header_label = ctk.CTkLabel(frame, text="Welcome to LCMS!", font=("Arial", 20, "bold"))
        header_label.pack(pady=10)
        
        self.username_entry = ctk.CTkEntry(frame, width=220, placeholder_text="Username")
        self.username_entry.pack(pady=5)
        
        self.password_entry = ctk.CTkEntry(frame, width=220, show="*", placeholder_text="Password")
        self.password_entry.pack(pady=5)
        
        self.show_password_button = ctk.CTkButton(frame, text="Show", command=self.toggle_password)
        self.show_password_button.pack(pady=5)
        
        self.login_button = ctk.CTkButton(frame, text="Login", command=self.authenticate)
        self.login_button.pack(pady=20)
    
    def toggle_password(self):
        if self.password_entry.cget("show") == "*":
            self.password_entry.configure(show="")
            self.show_password_button.configure(text="Hide")
        else:
            self.password_entry.configure(show="*")
            self.show_password_button.configure(text="Show")
    
    def authenticate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        print(f"Attempting login for user: {username}")  # Debugging
        authenticate_user(username, password, self.login_result)
    
    def login_result(self, success, farm_id):
        print(f"Login Success: {success}, Farm ID: {farm_id}")  # Debugging output
        if success:
            print("Closing login screen...")
            self.withdraw()  # Close login window
            self.on_success(farm_id)
            print("Starting main application...")
            app = App(farm_id)
            app.mainloop()
        else:
            print(f"Login failed: {farm_id}")  # Print error message for debugging

class App(ctk.CTk):
    def __init__(self, farm_id):
        super().__init__()
        self.title("Livestock & Co Management System")
        self.geometry("800x500")
        self.configure(fg_color=CUSTOM_THEME["bg_color"])
        self.farm_id = farm_id
        self.create_sidebar()

    def load_chicken_breeds(self):
        try:
            chicken_df = pd.read_excel(chicken_breeds_path)
            return chicken_df
        except Exception as e:
            print(f"Error loading chicken breeds: {e}")
            return pd.DataFrame()  # Return empty DataFrame if error occurs        

    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, fg_color=CUSTOM_THEME["frame_color"])
        self.sidebar.pack(side="left", fill="y")

        ctk.CTkButton(self.sidebar, text="Home", command=self.show_poultry).pack(pady=5)
        ctk.CTkButton(self.sidebar, text="Poultry", command=self.show_poultry).pack(pady=5)
        ctk.CTkButton(self.sidebar, text="Contact Us", command=lambda: webbrowser.open("mailto:trhodes45@ivytech.edu")).pack(pady=5)
        ctk.CTkButton(self.sidebar, text="Logout", command=self.logout).pack(pady=5)
        ctk.CTkButton(self.sidebar, text="Exit", command=self.quit).pack(pady=5)

    def logout(self):
        self.withdraw()
        login_screen = LoginScreen(lambda farm_id: self.deiconify() or App(farm_id))
        login_screen.mainloop()
        
    def show_poultry(self):
        for widget in self.winfo_children():
            if widget != self.sidebar:
                widget.destroy()
        self.create_poultry_tab()

    def create_poultry_tab(self):
        self.poultry_frame = ctk.CTkFrame(self, fg_color=CUSTOM_THEME["frame_color"])
        self.poultry_frame.pack(expand=True, fill="both", padx=20, pady=20)

        ctk.CTkLabel(self.poultry_frame, text="Poultry Management", font=("Arial", 16, "bold")).pack(pady=10)

        table_frame = ctk.CTkFrame(self.poultry_frame, fg_color=CUSTOM_THEME["frame_color"])
        table_frame.pack(fill="both", padx=10, pady=10)

        self.load_poultry_data(table_frame)

        add_button = ctk.CTkButton(self.poultry_frame, text="Add Chicken", command=self.add_chicken)
        add_button.pack(pady=10)

        update_button = ctk.CTkButton(self.poultry_frame, text="Update Chicken", command=self.update_chicken)
        update_button.pack(pady=10)

    def load_poultry_data(self, table_frame):
        farm_excel_path = os.path.join(script_dir, f"{self.farm_id}.xlsx")
        if os.path.exists(farm_excel_path):
            poultry_data = pd.read_excel(farm_excel_path, sheet_name="Poultry")
            for _, row in poultry_data.iterrows():
                row_frame = ctk.CTkFrame(table_frame, fg_color=CUSTOM_THEME["frame_color"])
                row_frame.pack(fill="x", pady=2)
                for col in poultry_data.columns:
                    ctk.CTkLabel(row_frame, text=str(row[col]), font=("Arial", 10), width=20).pack(side="left", padx=5)
        else:
            ctk.CTkLabel(table_frame, text="No poultry data found.", font=("Arial", 12)).pack(pady=10)

    def populate_chicken_details(self, chicken_data):
        breed = chicken_data.loc[0, "Breed"]  # Get breed from first row of Excel data
        self.breed_entry.insert(0, breed)  # Insert breed into the UI entry field
       # Similarly, map other fields like age, size, etc.

        
        # Ask for breed selection
        breed_choices = chicken_df['Breed'].tolist()
        breed = simpledialog.askstring("Select Chicken Breed", "Available Breeds: " + ", ".join(breed_choices))
        
        if breed and breed in breed_choices:
            # Ask for the number of chickens to add
            number_of_chickens = simpledialog.askinteger("Enter Number", f"How many chickens of breed {breed} would you like to add?")
            if number_of_chickens:
                new_chicken = {
                    "Breed": breed,
                    "Number": number_of_chickens,
                    "Added On": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                # Check if the farm's poultry sheet exists, if not, create one
                farm_excel_path = os.path.join(script_dir, f"{self.farm_id}.xlsx")
                if os.path.exists(farm_excel_path):
                    poultry_data = pd.read_excel(farm_excel_path, sheet_name="Poultry") if "Poultry" in pd.ExcelFile(farm_excel_path).sheet_names else pd.DataFrame(columns=["Breed", "Number", "Added On"])
                    
                    # Use pd.concat instead of append
                    poultry_data = pd.concat([poultry_data, pd.DataFrame([new_chicken])], ignore_index=True)
                    
                    # Write updated data back to the sheet
                    with pd.ExcelWriter(farm_excel_path, mode="a", if_sheet_exists="replace", engine="openpyxl") as writer:
                        poultry_data.to_excel(writer, sheet_name="Poultry", index=False)
                    
                    self.load_poultry_data(self.poultry_frame)  # Refresh the data display
                    print(f"Added new chicken: {new_chicken}")
                else:
                    print("Farm Excel file does not exist.")
            else:
                print("Invalid number of chickens.")
        else:
            print("Invalid breed selected or no breed selected.")

    def update_chicken(self):
        farm_excel_path = os.path.join(script_dir, f"{self.farm_id}.xlsx")
        if os.path.exists(farm_excel_path):
            poultry_data = pd.read_excel(farm_excel_path, sheet_name="Poultry")
            if poultry_data.empty:
                print("No poultry data available to update.")
                return
            
            chicken_index = simpledialog.askinteger("Update Chicken", f"Enter the index (0 to {len(poultry_data)-1}) of the chicken record to update:")
            if chicken_index is not None and 0 <= chicken_index < len(poultry_data):
                chicken_to_update = poultry_data.iloc[chicken_index]
                print(f"Updating chicken: {chicken_to_update['Breed']}")
                
                field = simpledialog.askstring("Update Field", f"Which field to update: {', '.join(poultry_data.columns)}?")
                if field and field in poultry_data.columns:
                    new_value = simpledialog.askstring(f"New Value for {field}", f"Enter the new value for {field}:")
                    poultry_data.at[chicken_index, field] = new_value
                    poultry_data.to_excel(farm_excel_path, sheet_name="Poultry", index=False)
                    self.load_poultry_data(self.poultry_frame)
                    print(f"Updated {field} of chicken at index {chicken_index}.")
                else:
                    print(f"Invalid field: {field}")
            else:
                print(f"Invalid index: {chicken_index}")
        else:
            print("No poultry data found.")

if __name__ == "__main__":
    LoginScreen(lambda farm_id: App(farm_id)).mainloop()
