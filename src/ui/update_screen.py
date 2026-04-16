"""
Update Screen Module provides Update Screen UI.
"""

import customtkinter as ctk

from ..config import APP_CONFIG


class UpdateScreen(ctk.CTk):
    """Update Screen UI"""

    def __init__(self):
        """Update Screen UI Initialization"""

        super().__init__()

        self.app_version = APP_CONFIG.get("version")

        self.title("Update - Jomir Tathya")
        self.geometry("450x500")
        self.configure(fg_color="#F5F5F7")
        self.resizable(False, False)

        # Updater Frame
        self.updater_frame = ctk.CTkFrame(self, fg_color="white")
        self.updater_frame.pack(fill="both", padx=10, pady=10, expand=True)

        # App Version Label
        self.app_version_label = ctk.CTkLabel(
            self.updater_frame,
            text=f"App Version: {self.app_version}",
            text_color="black",
        )
        self.app_version_label.pack(padx=5, pady=10)

        self.new_app_version_label = ctk.CTkLabel(
            self.updater_frame,
            text=f"New update available: {self.app_version}",
            text_color="black",
        )
        self.app_version_label.pack(padx=5, pady=10)


update_screen = UpdateScreen()
update_screen.mainloop()

