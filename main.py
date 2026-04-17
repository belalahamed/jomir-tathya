import customtkinter as ctk
from pathlib import Path

from src.ui import AppScreen
from assets import app_icon as APP_ICON


class RootApp(ctk.CTk):
    """Root App"""

    def __init__(self):
        """Initialize Root App"""

        super().__init__()

        self.iconbitmap(APP_ICON)  # * APP ICON
        self.title("Banglarbhumi")  # * ROOT APP TITLE
        self.after(0, self.maximize)

        # * Screens Container Frame (parent_frame)
        self.container_frame = ctk.CTkFrame(self)
        self.container_frame.pack(fill="both", expand=True)

        """
        *Create the app screen frame and 
        *store it in 'self.app_screen_frame' as property of RootApp(self),
        *so that it can be accessible through all over the application through the RootApp(self)
        """
        self.app_screen_frame = AppScreen(self.container_frame, self)
        self.show_frame(self.app_screen_frame)  # * Display app screen frame

    def show_frame(self, frame):
        """Render different screen frames by passing its instance reference"""
        
        frame.pack(fill="both", expand=True)
        frame.tkraise()

    def maximize(self):
        """Show screen in full window view"""

        self.state("zoomed")


if __name__ == "__main__":
    root = RootApp()
    root.mainloop()
