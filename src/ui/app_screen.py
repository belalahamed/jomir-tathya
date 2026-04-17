"""
* App Screen Frame Module
"""

import customtkinter as ctk
from PIL import Image

from assets import app_logo as APP_LOGO
from ..store import AppState
from .login_screen import LoginScreen
from .property_search_screen import PropertySearchScreen


class AppScreen(ctk.CTkFrame):
    """App Screen Frame UI"""

    def __init__(self, parent_frame, root_app):
        """App Frame UI Initialization"""

        """
        * parent_frame -> it receives the reference of 'self.container_frame'(parent_frame) property of 'RootApp' instance
        * root_app -> it receives the reference of 'RootApp'(self) instance
        """

        super().__init__(parent_frame, fg_color="white", corner_radius=0)

        self.parent_frame = parent_frame  # * This is reference of 'self.container_frame'(parent_frame) of 'RootApp'
        self.root_app = root_app  # * This is the reference of 'RootApp' instance

        # * Subscribe to AppState changes
        AppState.add_listener(self.change_header_btn)

        # * Header Frame
        self.header_frame = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=0,
            border_width=2,
            border_color="#E5E5E7",
        )
        self.header_frame.pack(side="top", fill="both", padx=0, pady=0, ipady=15)

        # * Services Frame
        self.services_frame = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=10,
            border_width=2,
            border_color="#E5E5E7",
        )
        self.services_frame.pack(
            after=self.header_frame, fill="both", padx=150, pady=30, ipady=20, ipadx=20
        )

        # * Services Label
        self.services_label = ctk.CTkLabel(
            self.services_frame,
            text="Services",
            text_color="white",
            font=("Calibri", 28),
            fg_color="#007AFF",
        )
        self.services_label.pack(side="top", fill="both", pady=10, padx=1, ipady=10)

        # * Find Information Frame
        self.find_info_frame = ctk.CTkFrame(self.services_frame, fg_color="#FFFFFF")
        self.find_info_frame.pack(side="top", fill="both", padx=5, pady=5)

        # * Check Status Frame
        self.check_status_frame = ctk.CTkFrame(self.services_frame, fg_color="#FFFFFF")
        self.check_status_frame.pack(side="top", fill="both", padx=5, pady=5)

        # * Header Logo
        self.logo = ctk.CTkImage(light_image=Image.open(APP_LOGO), size=(50, 50))

        self.logo_label = ctk.CTkLabel(
            self.header_frame,
            image=self.logo,
            text=" BANGLARBHUMI",
            text_color="#007AFF",
            font=("Calibri", 35, "bold"),
            compound="left",
        )
        self.logo_label.pack(side="left", padx=50)

        # * Header Login Button
        self.login_btn = ctk.CTkButton(
            self.header_frame,
            width=80,
            height=40,
            text="Login",
            text_color="white",
            fg_color="#007AFF",
            font=("Calibri", 18),
            command=self.open_login_screen,
        )
        self.login_btn.pack(side="right", padx=50)

        # * Header Logout Button
        self.logout_btn = ctk.CTkButton(
            self.header_frame,
            width=80,
            height=40,
            text="Logout",
            text_color="white",
            fg_color="#007AFF",
            font=("Calibri", 18),
            command=self.handle_logout_btn,
        )

        # * Find Information Label
        self.find_info_label = ctk.CTkLabel(
            self.find_info_frame,
            text="Find Information",
            text_color="black",
            font=("Calibri", 25),
        )
        self.find_info_label.pack(side="top", anchor="w", padx=20)

        # * Know Your Property Card
        self.know_your_property_card = ctk.CTkButton(
            self.find_info_frame,
            text="Know Your Property",
            fg_color="green",
            font=("Calibri", 20, "bold"),
            hover_color="#044a04",
            command=self.open_property_search_screen,
        )
        self.know_your_property_card.pack(
            side="left", padx=40, pady=30, ipadx=20, ipady=30
        )

        # * RS-LR Info Card
        self.rs_lr_info_card = ctk.CTkButton(
            self.find_info_frame,
            text="RS-LR Information",
            fg_color="green",
            font=("Calibri", 20, "bold"),
            hover_color="#044a04",
        )
        self.rs_lr_info_card.pack(side="left", padx=40, pady=30, ipadx=20, ipady=30)

        # * Check Status Label
        self.check_status_label = ctk.CTkLabel(
            self.check_status_frame,
            text="Check Status",
            text_color="black",
            font=("Calibri", 25),
        )
        self.check_status_label.pack(side="top", anchor="w", padx=20)

        # * Mutation Plot Khatian Status Card
        self.mutation_plot_khatian_card = ctk.CTkButton(
            self.check_status_frame,
            text="Mutation Plot Khatian Status",
            fg_color="green",
            font=("Calibri", 20, "bold"),
            hover_color="#044a04",
        )
        self.mutation_plot_khatian_card.pack(
            side="left", padx=40, pady=30, ipadx=20, ipady=30
        )

    def open_login_screen(self):
        """Handling Login Screen Opening"""

        # * Remove the app screen frame
        self.pack_forget()

        # * Create the login screen frame
        self.login_screen_frame = LoginScreen(self.parent_frame, self.root_app)

        # * Display login screen frame
        self.root_app.show_frame(self.login_screen_frame)

    def change_header_btn(self):
        """Handles the login and logout button visibility"""

        if AppState.is_logged_in:
            self.login_btn.pack_forget()
            self.logout_btn.pack(side="right", padx=50)
        else:
            self.logout_btn.pack_forget()
            self.login_btn.pack(side="right", padx=50)

    def handle_logout_btn(self):
        """Handling Logout Button Click"""

        AppState.set_login_state(False, None)

    def open_property_search_screen(self):
        """Open Property Search Screen"""

        if not AppState.is_logged_in:
            # * Remove App Screen Frame
            self.pack_forget()

            # * Create Property Search Screen Instance
            self.property_search_screen_frame = PropertySearchScreen(
                self.parent_frame, self.root_app, session_cookies=AppState.cookies
            )
            # * Display Property Search Screen in Parent Frame in Root App
            self.root_app.show_frame(self.property_search_screen_frame)

        else:
            self.open_login_screen()
