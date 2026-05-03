# * ====================================================================== * #
# *                             App Screen Module                          * #
# * ====================================================================== * #

import customtkinter as ctk
from PIL import Image

from assets import app_logo as APP_LOGO
from ..store import AppState
from .login_screen import LoginScreen
from .property_search_screen import PropertySearchScreen
from .plot_khatian_status_screen import PlotKhatianStatusScreen


class AppScreen(ctk.CTkFrame):
    """
    * App Screen Frame UI
    """

    def __init__(self, parent_frame, root_app):
        """
        * App Screen Frame UI Initialization
        """

        # * ================================================================================================================ * #
        # * parent_frame -> it receives the reference of 'self.container_frame'(parent_frame) property of 'RootApp' instance * #
        # * root_app -> it receives the reference of 'RootApp'(self) instance                                                * #
        # * ================================================================================================================ * #

        # * Create App Screen Frame
        super().__init__(parent_frame, fg_color="#F8F9FA", corner_radius=0)

        # * Subscribe to AppState changes
        AppState.add_listener(self.change_header_btn)

        # * ====================================================================== * #
        # *                             Root App References                        * #
        # * ====================================================================== * #

        # * Reference of 'self.container_frame'(parent_frame) of 'RootApp'
        self.parent_frame = parent_frame

        # * Reference of 'RootApp' instance
        self.root_app = root_app

        # * ====================================================================== * #
        # *              Grid Layout Configuration (App Screen Frame)              * #
        # * ====================================================================== * #

        self.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
        self.grid_rowconfigure(0, weight=0)

        # * ====================================================================== * #
        # *                     Child Frames of App Screen Frame                   * #
        # * ====================================================================== * #

        # * ============== Header Frame =========== * #

        # * Create Header Frame
        self.header_frame = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=0,
            border_width=0,
            border_color="#E5E5E7",
        )
        self.header_frame.grid(
            column=0, row=0, columnspan=7, sticky="nsew", pady=(0, 20)
        )

        # * Header Frame Grid Layout Configuration
        self.header_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
        self.header_frame.grid_rowconfigure(0, weight=0)

        # * ============== Services Frame =========== * #

        # * Create Services Frame
        self.services_frame = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=20,
            border_width=0,
            border_color="#E0E0E0",
        )
        self.services_frame.grid(
            column=1, row=1, columnspan=5, rowspan=5, sticky="nsew", padx=15, pady=15
        )

        # * Services Frame Grid Layout Configuration
        self.services_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.services_frame.grid_rowconfigure(0, weight=2)
        self.services_frame.grid_rowconfigure((1, 3), weight=1)
        self.services_frame.grid_rowconfigure((2, 4), weight=3)

        # * ============== Find Information Frame =========== * #

        # * Create Find Information Frame
        self.find_info_frame = ctk.CTkFrame(
            self.services_frame,
            fg_color="#FFFFFF",
            corner_radius=15,
            border_width=1,
            border_color="#E8E8E8",
        )
        self.find_info_frame.grid(
            column=0, row=2, columnspan=4, sticky="nsew", padx=20, pady=(10, 15)
        )

        # * Find Information Frame Grid Layout Configuration
        self.find_info_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.find_info_frame.grid_rowconfigure(0, weight=1)

        # * ============== Check Status Frame =========== * #

        # * Create Check Status Frame
        self.check_status_frame = ctk.CTkFrame(
            self.services_frame,
            fg_color="#FFFFFF",
            corner_radius=15,
            border_width=1,
            border_color="#E8E8E8",
        )
        self.check_status_frame.grid(
            column=0, row=4, columnspan=4, sticky="nsew", padx=20, pady=(10, 20)
        )

        # * Check Status Frame Grid Layout Configuration
        self.check_status_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.check_status_frame.grid_rowconfigure(0, weight=1)

        # * ====================================================================== * #
        # *                             Elements of Frames                         * #
        # * ====================================================================== * #

        # * ============== Logo =========== * #

        # * Create Logo Image
        self.logo = ctk.CTkImage(light_image=Image.open(APP_LOGO), size=(50, 50))

        # * Create Logo Label
        self.logo_label = ctk.CTkLabel(
            self.header_frame,
            image=self.logo,
            text=" BANGLARBHUMI",
            text_color="#0066CC",
            font=("Calibri", 32, "bold"),
            compound="left",
        )
        self.logo_label.grid(
            column=0, row=0, columnspan=4, sticky="w", padx=25, pady=10
        )

        # * ============== Login Button =========== * #

        # * Create Login Button
        self.login_btn = ctk.CTkButton(
            self.header_frame,
            width=90,
            height=38,
            text="Login",
            text_color="white",
            fg_color="#0066CC",
            hover_color="#0052A3",
            font=("Calibri", 16, "bold"),
            corner_radius=8,
            command=self.open_login_screen,
        )
        self.login_btn.grid(column=6, row=0, sticky="e", padx=25, pady=10)

        # * ============== Logout Button =========== * #

        # * Create Logout Button
        self.logout_btn = ctk.CTkButton(
            self.header_frame,
            width=90,
            height=38,
            text="Logout",
            text_color="white",
            fg_color="#DC3545",
            hover_color="#bb2d3b",
            font=("Calibri", 16, "bold"),
            corner_radius=8,
            command=self.handle_logout_btn,
        )

        # * ============== Services Label =========== * #

        # * Create Services Label
        self.services_label = ctk.CTkLabel(
            self.services_frame,
            text="🎯 Our Services",
            text_color="white",
            font=("Calibri", 34, "bold"),
            fg_color="#0066CC",
        )
        self.services_label.grid(
            column=0, row=0, columnspan=4, sticky="nsew", padx=25, pady=25
        )

        # * ============== Find Information Label =========== * #

        # * Create Find Information Label
        self.find_info_label = ctk.CTkLabel(
            self.services_frame,
            text="📋 Find Information",
            text_color="#0066CC",
            font=("Calibri", 22, "bold"),
        )
        self.find_info_label.grid(
            column=0, row=1, columnspan=4, sticky="w", padx=20, pady=(15, 10)
        )

        # * ============== Know Your Property Button =========== * #

        # * Create Know Your Property Button
        self.know_your_property_card = ctk.CTkButton(
            self.find_info_frame,
            text="🏠 Know Your Property",
            fg_color="#28A745",
            hover_color="#1e7e34",
            text_color="white",
            font=("Calibri", 17, "bold"),
            corner_radius=12,
            command=self.open_property_search_screen,
        )
        self.know_your_property_card.grid(
            column=0, row=0, sticky="nsew", padx=10, pady=12
        )

        # * ============== RS-LR Info Button =========== * #

        # * Create RS-LR Info Button
        self.rs_lr_info_card = ctk.CTkButton(
            self.find_info_frame,
            text="📑 RS-LR Information",
            fg_color="#17A2B8",
            hover_color="#0f6674",
            text_color="white",
            font=("Calibri", 17, "bold"),
            corner_radius=12,
        )
        self.rs_lr_info_card.grid(column=1, row=0, sticky="nsew", padx=10, pady=12)

        # * ============== Check Status Label =========== * #

        # * Create Check Status Label
        self.check_status_label = ctk.CTkLabel(
            self.services_frame,
            text="✅ Check Status",
            text_color="#0066CC",
            font=("Calibri", 22, "bold"),
        )
        self.check_status_label.grid(
            column=0, row=3, columnspan=4, sticky="w", padx=20, pady=(15, 10)
        )

        # * ============== Mutation Plot Khatian Status Button =========== * #

        # * Create Mutation Plot Khatian Status Button
        self.mutation_plot_khatian_card = ctk.CTkButton(
            self.check_status_frame,
            text="⏱️ Mutation Plot Khatian Status",
            fg_color="#FFC107",
            hover_color="#d39e00",
            text_color="#333333",
            font=("Calibri", 17, "bold"),
            corner_radius=12,
            command=self.open_mutation_status_screen,
        )
        self.mutation_plot_khatian_card.grid(
            column=0, row=0, sticky="nsew", padx=10, pady=12
        )

        # * ============== Mutation Status Button =========== * #

        # * Create Mutation Status Button
        self.mutation_status_card = ctk.CTkButton(
            self.check_status_frame,
            text="📊 Mutation Status",
            fg_color="#6F42C1",
            hover_color="#5a32a3",
            text_color="white",
            font=("Calibri", 17, "bold"),
            corner_radius=12,
        )
        self.mutation_status_card.grid(column=1, row=0, sticky="nsew", padx=10, pady=12)

    def open_login_screen(self):
        """
        * Handling Login Screen Opening
        """

        # * Remove the app screen frame
        self.pack_forget()

        # * Create the login screen frame
        self.login_screen_frame = LoginScreen(self.parent_frame, self.root_app)

        # * Display login screen frame
        self.root_app.show_frame(self.login_screen_frame)

    def change_header_btn(self):
        """
        * Handles the login and logout button visibility
        """

        if AppState.is_logged_in:
            self.login_btn.grid_remove()
            self.logout_btn.grid(column=6, row=0, sticky="e", padx=25, pady=10)
        else:
            self.logout_btn.grid_remove()
            self.login_btn.grid(column=6, row=0, sticky="e", padx=25, pady=10)

    def handle_logout_btn(self):
        """
        * Handling Logout Button Click
        """

        AppState.set_login_state(False, None)

    def open_property_search_screen(self):
        """
        * Open Property Search Screen
        """

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

    def open_mutation_status_screen(self):
        """
        * Open Plot Khatian Mutation Status Screen
        """

        if AppState.is_logged_in:
            # * Remove App Screen Frame
            self.pack_forget()

            # * Create Mutation Status Screen Instance
            self.mutation_status_screen_frame = PlotKhatianStatusScreen(
                self.parent_frame, self.root_app, session_cookies=AppState.cookies
            )
            # * Display Screen
            self.root_app.show_frame(self.mutation_status_screen_frame)
        else:
            self.open_login_screen()
