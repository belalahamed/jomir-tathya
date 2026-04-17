import customtkinter as ctk
import threading
from PIL import Image

from ..auth import LoginService
from ..store import AppState
from assets import app_logo as APP_LOGO, back_icon as BACK_ICON


class LoginScreen(ctk.CTkFrame):

    def __init__(self, parent_frame, root_app):
        super().__init__(parent_frame, fg_color="white", corner_radius=0)

        self.parent_frame = parent_frame
        self.root_app = root_app

        # # Callback for application control
        # self.on_login_success = None

        """Login Instance"""
        self.login = LoginService()

        """Extraction Login Data from login instance"""
        self.cookies = self.login.cookies
        self.salt = self.login.salt
        self.captcha = self.login.captcha
        self.login_response = self.login.response

        self.view_login_ui()

    def view_login_ui(self):
        """Build Login Form UI"""

        # Sync local attributes with the current state of the login service
        self.cookies = self.login.cookies
        self.salt = self.login.salt
        self.captcha = self.login.captcha
        self.login_response = self.login.response
        
        # Header Frame
        self.header_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=0, width=400)
        self.header_frame.pack(side="top")
        
        #* Back Button
        self.back_btn_img = ctk.CTkImage(light_image=Image.open(BACK_ICON))
        self.back_btn = ctk.CTkButton(self.header_frame, text="", image=self.back_btn_img, width=50, height=50, command=self._open_app_screen)
        self.back_btn.pack(side="left", padx=20)

        # Header logo outside the frame
        self.logo = ctk.CTkImage(light_image=Image.open(APP_LOGO), size=(50, 50))
        
        self.logo_label = ctk.CTkLabel(
            self.header_frame,
            image=self.logo,
            text=" BANGLARBHUMI",
            text_color="#007AFF",
            font=("Calibri", 35, "bold")
        )
        self.logo_label.pack(side="right",pady=(10, 10))

        # Create a container frame for the login form
        self.login_frame = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            width=400,
            height=600,
            corner_radius=16,
            border_width=2,
            border_color="#E5E5E7",
        )
        self.login_frame.pack(pady=(10, 20), padx=20)
        self.login_frame.pack_propagate(False)

        # Form header label - Login
        self.header_label = ctk.CTkLabel(
            self.login_frame,
            text="SIGN IN",
            font=("Calibri", 20, "bold"),
            text_color="white",
            fg_color="#007AFF"
        )
        self.header_label.pack(fill="both", pady=(15, 20), ipady=10, padx=1)

        # Username input field
        self.username_entry = ctk.CTkEntry(
            self.login_frame,
            placeholder_text="Username",
            width=320,
            height=45,
            fg_color="white",
            text_color="#1D1D1F",
            font=("Calibri", 16),
            corner_radius=8,
            border_color="#D1D1D6",
        )
        self.username_entry.pack(pady=10)
        self.username_entry.bind("<KeyRelease>", self.handle_send_otp_btn_state)
        self.username_entry.bind("<Return>", self.handle_send_otp)

        # Password input field with show/hide button
        self.password_frame = ctk.CTkFrame(self.login_frame, fg_color="transparent")
        self.password_frame.pack(pady=10)

        self.password_entry = ctk.CTkEntry(
            self.password_frame,
            placeholder_text="Password",
            show="*",
            width=320,
            height=45,
            fg_color="white",
            text_color="#1D1D1F",
            font=("Calibri", 16),
            corner_radius=8,
            border_color="#D1D1D6",
        )
        self.password_entry.pack()
        self.password_entry.bind("<KeyRelease>", self.handle_send_otp_btn_state)
        self.password_entry.bind("<Return>", self.handle_send_otp)

        self.show_pass_btn = ctk.CTkButton(
            self.password_frame,
            text="👁",
            width=35,
            height=35,
            fg_color="#E5E5E7",
            text_color="#1D1D1F",
            hover_color="#D1D1D6",
            corner_radius=8,
            command=self.toggle_password,
        )
        self.show_pass_btn.place(relx=0.88, y=5)

        # Captcha image display and refresh button
        self.captcha_frame = ctk.CTkFrame(
            self.login_frame, fg_color="transparent", border_color="#D1D1D6"
        )
        self.captcha_frame.pack(pady=10)

        self.captcha_label = ctk.CTkLabel(self.captcha_frame, text="")
        self.captcha_label.pack(side="left")
        self.captcha_label.bind(
            "<Button-1>", self.refresh_captcha
        )  # Click image to refresh
        self.refresh_btn = ctk.CTkButton(
            self.captcha_frame,
            text="🔄",
            width=45,
            height=45,
            fg_color="#E5E5E7",
            text_color="#1D1D1F",
            hover_color="#D1D1D6",
            corner_radius=8,
            command=self.refresh_captcha,
        )
        self.refresh_btn.pack(side="left", padx=(10, 0))

        self.update_captcha_display()

        # Captcha input field
        self.captcha_entry = ctk.CTkEntry(
            self.login_frame,
            placeholder_text="Enter Captcha",
            width=320,
            height=45,
            fg_color="white",
            text_color="#1D1D1F",
            font=("Calibri", 16),
            corner_radius=8,
            border_color="#D1D1D6",
        )
        self.captcha_entry.pack(pady=10)
        self.captcha_entry.bind("<KeyRelease>", self.handle_send_otp_btn_state)
        self.captcha_entry.bind("<Return>", self.handle_send_otp)

        # Send OTP button
        self.send_otp_btn = ctk.CTkButton(
            self.login_frame,
            text="Send OTP",
            width=320,
            height=50,
            font=("Calibri", 16, "bold"),
            state="disabled",
            fg_color="#007AFF",  # Apple System Blue
            hover_color="#005FB8",
            corner_radius=10,
            command=self.handle_send_otp,
        )
        self.send_otp_btn.pack(pady=(20, 0))

        # OTP field
        self.otp_entry = ctk.CTkEntry(
            self.login_frame,
            placeholder_text="Enter OTP",
            width=320,
            height=45,
            fg_color="white",
            text_color="#1D1D1F",
            font=("Calibri", 16),
            corner_radius=8,
            border_color="#D1D1D6",
        )
        self.otp_entry.bind("<KeyRelease>", self.handle_login_btn_state)
        self.otp_entry.bind("<Return>", self.handle_login)

        # Login button
        self.login_btn = ctk.CTkButton(
            self.login_frame,
            text="Login",
            width=320,
            height=50,
            font=("Calibri", 16, "bold"),
            state="disabled",
            fg_color="#007AFF",
            hover_color="#005FB8",
            corner_radius=10,
            command=self.handle_login,
        )

        # Status Message
        self.status_message_label = ctk.CTkLabel(
            self.login_frame, text="", font=("Calibri", 13), fg_color="white"
        )
        self.status_message_label.pack(pady=(20, 20))

    def _open_app_screen(self):
        self.pack_forget()
        self.root_app.show_frame(self.root_app.app_screen_frame)

    def handle_login_btn_state(self, event=None):
        """Handle Login Button State"""

        otp = self.otp_entry.get()

        if otp:
            self.login_btn.configure(state="normal")
        else:
            self.login_btn.configure(state="disabled")

    def handle_send_otp_btn_state(self, event=None):
        username = self.username_entry.get()
        password = self.password_entry.get()
        captcha = self.captcha_entry.get()

        if username and password and captcha:
            self.send_otp_btn.configure(state="normal")
        else:
            self.send_otp_btn.configure(state="disabled")

    def toggle_password(self):
        """Toggle visibility of the password entry"""

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
        """Fetch and update a new captcha image"""

        try:
            self.captcha = self.login.generate_captcha()

        except Exception as err:
            print(f"Error: {err}")

        self.update_captcha_display()

    def update_captcha_display(self):
        """Update the captcha label with the current PIL image"""

        try:
            if self.captcha:
                ctk_img = ctk.CTkImage(
                    light_image=self.captcha, dark_image=self.captcha, size=(250, 55)
                )
                self.captcha_label.configure(image=ctk_img)

        except Exception as err:
            print(f"Error: {err}")

    def handle_send_otp(self, event=None):
        """Handle Send OTP button click with threading for UX"""
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
                text="Requesting OTP...", text_color="#1D1D1F"
            )

            # Run network call in a separate thread
            threading.Thread(
                target=self._send_otp_thread,
                args=(username, password, captcha),
                daemon=True,
            ).start()

    def _send_otp_thread(self, username, password, captcha):
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
        self.send_otp_btn.pack_forget()
        self.otp_entry.pack(pady=10)
        self.login_btn.pack(pady=(20, 0))
        self.otp_entry.focus()
        self.status_message_label.configure(
            text="OTP generated successfully!", text_color="green"
        )

    def _on_otp_fail(self, message):
        self.status_message_label.configure(text=message, text_color="red")
        self.send_otp_btn.configure(state="normal", text="Send OTP")
        self.captcha_entry.delete(0, "end")
        self.refresh_captcha()

    def handle_login(self, event=None):
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
        try:
            validate_otp_response = self.login.validate_otp(username, password, otp)
            if validate_otp_response.get("checkmsg") == "success":
                self.after(
                    0,
                    lambda: self.status_message_label.configure(
                        text="Login successful!", text_color="green"
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
                    text="Login Error: Connection lost.", text_color="red"
                ),
            )
            self.after(
                0, lambda: self.login_btn.configure(state="normal", text="Login")
            )
            print(e)

    def _on_login_fail(self):
        """Handle login failure without full UI rebuild"""
        self.status_message_label.configure(
            text="Login failed! Invalid OTP.", text_color="red"
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
        """Handle login success"""

        AppState.set_login_state(True, self.cookies)
        self.pack_forget()
        self.after(0, self._open_app_screen)
