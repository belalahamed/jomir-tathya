import customtkinter as ctk
import multiprocessing

from src.ui import AppScreen, LoginScreen, PropertyScreen

class JomirTathyaApp:
    
    def __init__(self):
        
        self.app = AppScreen()
        self.app.mainloop()

    def show_login(self):
        """Initialize and display the Login Screen"""
        self.login_app = LoginScreen()
        # Define the transition callback
        self.login_app.on_login_success = self.on_login_completed
        self.login_app.mainloop()

    def on_login_completed(self):
        """Handle transition from Login to Property Lookup"""
        # Extract cookies generated during login
        cookies = self.login_app.login.get_cookies()
        
        # Destroy the login window
        self.login_app.destroy()
        
        # Initialize and start the Property Screen with authenticated cookies
        self.property_app = PropertyScreen(session_cookies=cookies)
        self.property_app.mainloop()

if __name__ == "__main__":
    multiprocessing.freeze_support()
    JomirTathyaApp()