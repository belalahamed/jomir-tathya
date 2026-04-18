# * ====================================================================== * #
# *                            Login Screen Module                         * #
# * ====================================================================== * #

import customtkinter as ctk
import threading
from PIL import Image

from ..auth import LoginService
from ..store import AppState
from assets import app_logo as APP_LOGO, back_icon as BACK_ICON


class LoginScreen(ctk.CTkFrame):
    """
    * Login Screen Frame UI
    """

    def __init__(self, parent_frame, root_app):
        """
        * Login Screen Frame UI Initialization
        """

        # * ================================================================================================================ * #
        # * parent_frame -> it receives the reference of 'self.container_frame'(parent_frame) property of 'RootApp' instance * #
        # * root_app -> it receives the reference of 'RootApp'(self) instance                                                * #
        # * ================================================================================================================ * #

        super().__init__(parent_frame, fg_color="#F8F9FA", corner_radius=0)

        # * ====================================================================== * #
        # *                             Root App References                        * #
        # * ====================================================================== * #

        # * Reference of 'self.container_frame'(parent_frame) of 'RootApp'
        self.parent_frame = parent_frame

        # * Reference of 'RootApp' instance
        self.root_app = root_app

        # * ====================================================================== * #
        # *                             Login Service Instance                     * #
        # * ====================================================================== * #

        # * Initialize Login Service
        self.login = LoginService()

        # * Get Cookies from Login Service Instance
        self.cookies = self.login.cookies

        # * Get Salt Text from Login Service Instance
        self.salt = self.login.salt

        # * Get Captcha from Login Service Instance
        self.captcha = self.login.captcha

        # * ====================================================================== * #
        # *              Grid Layout Configuration of Login Screen Frame           * #
        # * ====================================================================== * #

        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)

        # * ====================================================================== * #
        # *                     Child Frames of Login Screen Frame                 * #
        # * ====================================================================== * #

        # * =============== Login Form Frame ============== * #

        # * Container Frame for Login Form
        self.login_frame = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            width=440,
            height=640,
            corner_radius=20,
            border_width=0,
            border_color="#E5E5E7",
        )
        self.login_frame.grid(column=1, row=1, rowspan=6, sticky="n", padx=20, pady=20)
        self.login_frame.pack_propagate(False)

        # * Grid configuration of login form frame
        self.login_frame.grid_columnconfigure(0, weight=1)
        self.login_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=0)
        self.login_frame.grid_rowconfigure(8, weight=1)

        # * =============== Login Form Header Frame ============== * #

        # * Create Header frame to hold both title and back button
        self.header_frame = ctk.CTkFrame(
            self.login_frame, fg_color="#0066CC", corner_radius=8
        )
        self.header_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=(15, 10))

        # * Grid configuration of login form header frame
        self.header_frame.grid_columnconfigure(0, weight=0)
        self.header_frame.grid_columnconfigure(1, weight=1)
        self.header_frame.grid_rowconfigure(0, weight=0)

        # * =============== Password Entry Container Frame ============== * #

        # * Create Password Entry Container Frame
        self.password_frame = ctk.CTkFrame(self.login_frame, fg_color="transparent")
        self.password_frame.grid(row=2, column=0, sticky="nsew", padx=25, pady=12)

        # * Grid Configuration of Password Entry Container Frame
        self.password_frame.grid_columnconfigure(0, weight=1)
        self.password_frame.grid_rowconfigure(0, weight=1)

        # * =============== Captcha Container Frame ============== * #

        # * Create Captcha Container Frame
        self.captcha_frame = ctk.CTkFrame(
            self.login_frame, fg_color="transparent", border_color="#D1D1D6"
        )
        self.captcha_frame.grid(row=3, column=0, sticky="nsew", padx=25, pady=12)

        # * Grid Configuration of Captcha Container Frame
        self.captcha_frame.grid_columnconfigure((0, 1), weight=1)
        self.captcha_frame.grid_rowconfigure(0, weight=1)

        # * ====================================================================== * #
        # *                             Elements of Frames                         * #
        # * ====================================================================== * #

        # * =================== Logo ================= * #

        # * Create Logo Image
        self.logo = ctk.CTkImage(light_image=Image.open(APP_LOGO), size=(55, 55))

        # * Create Logo Label
        self.logo_label = ctk.CTkLabel(
            self,
            image=self.logo,
            text="BANGLARBHUMI",
            text_color="#0066CC",
            font=("Calibri", 36, "bold"),
            compound="top",
        )
        self.logo_label.grid(row=0, column=1, sticky="nsew", pady=(10, 20))

        # * =================== Back Button ================= * #

        # * Create Back Button Image
        self.back_btn_img = ctk.CTkImage(light_image=Image.open(BACK_ICON))

        # * Create Back Button
        self.back_btn = ctk.CTkButton(
            self.header_frame,
            text="",
            hover_color="#D1D1D6",
            image=self.back_btn_img,
            width=45,
            height=45,
            command=self.open_app_screen,
        )
        self.back_btn.grid(row=0, column=0, sticky="nsw", padx=(10, 0))

        # * =================== Login Form Header Label ================= * #

        # * Create Form header label - Sign In
        self.header_label = ctk.CTkLabel(
            self.header_frame,
            text="🔐 SIGN IN",
            font=("Calibri", 24, "bold"),
            text_color="white",
        )
        self.header_label.grid(row=0, column=1, sticky="nsew", ipady=15)

        # * =================== Username Entry Field ================= * #

        # * Create Username input entry field
        self.username_entry = ctk.CTkEntry(
            self.login_frame,
            placeholder_text="Username",
            width=360,
            height=48,
            fg_color="#F8F9FA",
            text_color="#1D1D1F",
            font=("Calibri", 16),
            corner_radius=10,
            border_color="#D1D1D6",
            border_width=1,
        )
        self.username_entry.grid(row=1, column=0, sticky="nsew", padx=25, pady=(20, 12))
        self.username_entry.bind("<KeyRelease>", self.handle_send_otp_btn_state)
        self.username_entry.bind("<Return>", self.handle_send_otp)

        # * =================== Username Entry Field ================= * #

        # * Create Password input entry field
        self.password_entry = ctk.CTkEntry(
            self.password_frame,
            placeholder_text="Password",
            show="*",
            width=330,
            height=48,
            fg_color="#F8F9FA",
            text_color="#1D1D1F",
            font=("Calibri", 16),
            corner_radius=10,
            border_color="#D1D1D6",
            border_width=1,
        )
        self.password_entry.grid(row=0, column=0, sticky="nsew")
        self.password_entry.bind("<KeyRelease>", self.handle_send_otp_btn_state)
        self.password_entry.bind("<Return>", self.handle_send_otp)

        # * =================== Show Password Button ================= * #

        # * Create Show Password Button
        self.show_pass_btn = ctk.CTkButton(
            self.password_frame,
            text="👁",
            width=40,
            height=40,
            fg_color="#E5E5E7",
            text_color="#1D1D1F",
            hover_color="#D1D1D6",
            corner_radius=8,
            command=self.toggle_password,
        )
        self.show_pass_btn.grid(row=0, column=1, sticky="e", padx=(8, 0))

        # * =================== Captcha Label ================= * #

        # * Create Captcha Label
        self.captcha_label = ctk.CTkLabel(self.captcha_frame, text="")
        self.captcha_label.grid(row=0, column=0, sticky="w")
        self.captcha_label.bind("<Button-1>", self.refresh_captcha)

        # * =================== Captcha Refresh Button ================= * #

        # * Create captcha refresh button
        self.refresh_btn = ctk.CTkButton(
            self.captcha_frame,
            text="🔄",
            width=50,
            height=50,
            fg_color="#E5E5E7",
            text_color="#1D1D1F",
            hover_color="#D1D1D6",
            corner_radius=8,
            command=self.refresh_captcha,
        )
        self.refresh_btn.grid(row=0, column=1, sticky="e", padx=(10, 0))

        self.update_captcha_display()

        # * =================== Captcha Entry Field ================= * #

        # * Create Captcha entry input field
        self.captcha_entry = ctk.CTkEntry(
            self.login_frame,
            placeholder_text="Enter Captcha",
            width=360,
            height=48,
            fg_color="#F8F9FA",
            text_color="#1D1D1F",
            font=("Calibri", 16),
            corner_radius=10,
            border_color="#D1D1D6",
            border_width=1,
        )
        self.captcha_entry.grid(row=4, column=0, sticky="nsew", padx=25, pady=12)
        self.captcha_entry.bind("<KeyRelease>", self.handle_send_otp_btn_state)
        self.captcha_entry.bind("<Return>", self.handle_send_otp)

        # * =================== Send OTP Button ================= * #

        # * Create Send OTP button
        self.send_otp_btn = ctk.CTkButton(
            self.login_frame,
            text="Send OTP",
            width=360,
            height=50,
            font=("Calibri", 16, "bold"),
            state="disabled",
            fg_color="#0066CC",
            hover_color="#0052A3",
            corner_radius=10,
            command=self.handle_send_otp,
        )
        self.send_otp_btn.grid(row=5, column=0, sticky="nsew", padx=25, pady=(20, 0))

        # * =================== OTP Entry Field ================= * #

        # * Create OTP input entry field
        self.otp_entry = ctk.CTkEntry(
            self.login_frame,
            placeholder_text="Enter OTP",
            width=360,
            height=48,
            fg_color="#F8F9FA",
            text_color="#1D1D1F",
            font=("Calibri", 16),
            corner_radius=10,
            border_color="#D1D1D6",
            border_width=1,
        )
        self.otp_entry.grid(row=6, column=0, sticky="nsew", padx=25, pady=12)
        self.otp_entry.grid_remove()  # Initially hidden
        self.otp_entry.bind("<KeyRelease>", self.handle_login_btn_state)
        self.otp_entry.bind("<Return>", self.handle_login)

        # * =================== Login Button ================= * #

        # * Create Login button
        self.login_btn = ctk.CTkButton(
            self.login_frame,
            text="Login",
            width=360,
            height=50,
            font=("Calibri", 16, "bold"),
            state="disabled",
            fg_color="#28A745",
            hover_color="#1e7e34",
            corner_radius=10,
            command=self.handle_login,
        )
        self.login_btn.grid(row=7, column=0, sticky="nsew", padx=25, pady=12)
        self.login_btn.grid_remove()  # Initially hidden

        # * =================== Status Message Label ================= * #

        # * Create Status Message Label
        self.status_message_label = ctk.CTkLabel(
            self.login_frame, text="", font=("Calibri", 14), fg_color="white"
        )
        self.status_message_label.grid(
            row=8, column=0, sticky="nsew", padx=25, pady=(20, 20)
        )

    def open_app_screen(self):
        """
        * Display App Screen Frame
        """

        # * Remove Current Frame (Login Screen Frame) from Root App
        self.pack_forget()

        # * Display App Screen Frame in Root App
        self.root_app.show_frame(self.root_app.app_screen_frame)

    def handle_login_btn_state(self, event=None):
        """
        * Handle Login Button State
        """

        otp = self.otp_entry.get()

        if otp:
            self.login_btn.configure(state="normal")
        else:
            self.login_btn.configure(state="disabled")

    def handle_send_otp_btn_state(self, event=None):
        """
        * Handle Send OTP Button
        """

        username = self.username_entry.get()
        password = self.password_entry.get()
        captcha = self.captcha_entry.get()

        if username and password and captcha:
            self.send_otp_btn.configure(state="normal")
        else:
            self.send_otp_btn.configure(state="disabled")

    def toggle_password(self):
        """
        * Toggle visibility of the password entry
        """

        if (
            self.password_entry.cget("show") == "*"
            and self.show_pass_btn.cget("text") == "👁"
        ):
            self.password_entry.configure(show="")
            self.show_pass_btn.configure(text="︶")
        else:
            self.password_entry.configure(show="*")
            self.show_pass_btn.configure(text="👁")

    def refresh_captcha(self):
        """
        * Fetch and update a new captcha image
        """

        try:
            self.captcha = self.login.generate_captcha()

        except Exception as err:
            print(f"Error: {err}")

        self.update_captcha_display()

    def update_captcha_display(self):
        """
        * Update the captcha label with the current PIL image
        """

        try:
            if self.captcha:
                ctk_img = ctk.CTkImage(
                    light_image=self.captcha, dark_image=self.captcha, size=(250, 55)
                )
                self.captcha_label.configure(image=ctk_img)

        except Exception as err:
            print(f"Error: {err}")

    def handle_send_otp(self, event=None):
        """
        * Handle Send OTP button click with threading for UX
        """

        username = self.username_entry.get()
        password = self.password_entry.get()
        captcha = self.captcha_entry.get()

        if (
            username
            and password
            and captcha
            and self.send_otp_btn.cget("state") == "normal"
        ):
            self.send_otp_btn.configure(state="disabled", text="Sending...")
            self.status_message_label.configure(
                text="⏳ Requesting OTP...", text_color="#0066CC"
            )

            # Run network call in a separate thread
            threading.Thread(
                target=self._send_otp_thread,
                args=(username, password, captcha),
                daemon=True,
            ).start()

    def _send_otp_thread(self, username, password, captcha):
        """
        * OTP Sending Thread
        """

        try:
            send_otp_response = self.login.generate_otp(username, password, captcha)

            if send_otp_response.get("message") == "OK":
                self.after(0, self._on_otp_success)
            else:
                self.after(
                    0,
                    lambda: self._on_otp_fail(
                        "OTP generation failed! Check credentials."
                    ),
                )
        except Exception as e:
            self.after(0, lambda: self._on_otp_fail(f"Error: Connection issue."))

    def _on_otp_success(self):
        """
        * Handling OTP generation success
        """

        self.send_otp_btn.grid_remove()
        self.otp_entry.grid(row=6, column=0, sticky="nsew", padx=25, pady=12)
        self.login_btn.grid(row=7, column=0, sticky="nsew", padx=25, pady=12)
        self.otp_entry.focus()
        self.status_message_label.configure(
            text="✅ OTP generated successfully!", text_color="#28A745"
        )

    def _on_otp_fail(self, message):
        """
        * Handling OTP failure
        """

        self.status_message_label.configure(text="❌ " + message, text_color="#DC3545")
        self.send_otp_btn.configure(state="normal", text="Send OTP")
        self.captcha_entry.delete(0, "end")
        self.refresh_captcha()

    def handle_login(self, event=None):
        """
        * Handling Login
        """

        """Handle Login button click with threading for UX"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        otp = self.otp_entry.get()

        if otp and self.login_btn.cget("state") == "normal":
            self.login_btn.configure(state="disabled", text="Logging in...")
            threading.Thread(
                target=self._login_thread, args=(username, password, otp), daemon=True
            ).start()

    def _login_thread(self, username, password, otp):
        """
        * Login Thread
        """

        try:
            validate_otp_response = self.login.validate_otp(username, password, otp)
            if validate_otp_response.get("checkmsg") == "success":
                self.after(
                    0,
                    lambda: self.status_message_label.configure(
                        text="✅ Login successful!", text_color="#28A745"
                    ),
                )
                # Trigger the transition callback after a short delay
                self.after(0, self._on_login_success)
            else:
                self.after(0, self._on_login_fail)
        except Exception as e:
            self.after(
                0,
                lambda: self.status_message_label.configure(
                    text="❌ Connection lost. Please try again.", text_color="#DC3545"
                ),
            )
            self.after(
                0, lambda: self.login_btn.configure(state="normal", text="Login")
            )
            print(e)

    def _on_login_fail(self):
        """
        * Handling Login Failure
        """

        """Handle login failure without full UI rebuild"""
        self.status_message_label.configure(
            text="❌ Login failed! Invalid OTP.", text_color="#DC3545"
        )
        self.login_btn.configure(state="disabled", text="Login")
        self.otp_entry.delete(0, "end")

        # Refresh session data but keep the entries filled (except OTP/Captcha)
        try:
            self.login.view_login_area()
            self.refresh_captcha()
        except Exception as e:
            print(e)

    def _on_login_success(self):
        """
        * Handling Login Success
        """

        # * Update cookies in AppState
        AppState.set_login_state(True, self.cookies)

        # * Remove the current frame (login screen frame) from root app
        self.pack_forget()

        # * Display App Screen Frame in Root App
        self.after(0, self.open_app_screen)
