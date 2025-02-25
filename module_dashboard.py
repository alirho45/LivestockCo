import customtkinter as ctk  # Import customtkinter

class Dashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CustomTkinter Dashboard")
        self.geometry("800x500")

        # Set theme
        ctk.set_appearance_mode("dark")  # Options: "System" (default), "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"

        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar (Navigation Panel)
        self.sidebar = ctk.CTkFrame(self, fg_color="#2c3e50", width=200)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        # Main Content Area
        self.main_content = ctk.CTkFrame(self, fg_color="#ecf0f1")
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Sidebar buttons
        self.create_sidebar_buttons()

        # Label in main content area
        self.label = ctk.CTkLabel(self.main_content, text="Welcome to the Dashboard", font=("Arial", 20, "bold"))
        self.label.pack(pady=50)

    def create_sidebar_buttons(self):
        """ Create sidebar navigation buttons """
        buttons = [
            ("Home", self.show_home),
            ("Analytics", self.show_analytics),
            ("Settings", self.show_settings)
        ]

        for text, command in buttons:
            btn = ctk.CTkButton(self.sidebar, text=text, command=command, fg_color="#34495e", hover_color="#1abc9c", font=("Arial", 14))
            btn.pack(fill="x", pady=5, padx=10)

    def show_home(self):
        """ Update main content text for Home """
        self.label.configure(text="Home Screen")

    def show_analytics(self):
        """ Update main content text for Analytics """
        self.label.configure(text="Analytics Dashboard")

    def show_settings(self):
        """ Update main content text for Settings """
        self.label.configure(text="Settings Page")

if __name__ == "__main__":
    app = Dashboard()
    app.mainloop()
