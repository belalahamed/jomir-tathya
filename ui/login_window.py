import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
from core.login import view_login_area, generate_login_otp, validate_login_otp

class LoginForm:
    """Modern login form UI with username, password, captcha"""
    
    # Color scheme
    PRIMARY_COLOR = "#1e88e5"
    PRIMARY_DARK = "#1565c0"
    BG_COLOR = "#f5f5f5"
    CARD_BG = "#ffffff"
    TEXT_COLOR = "#212121"
    LABEL_COLOR = "#616161"
    BORDER_COLOR = "#e0e0e0"
    BORDER_FOCUS = "#1e88e5"
    ERROR_COLOR = "#d32f2f"
    SUCCESS_COLOR = "#388e3c"
    
    def __init__(self, root, on_login_success=None):
        self.root = root
        self.root.title("Login - Jomir Tathya")
        self.root.geometry("450x650")
        self.root.resizable(False, False)
        self.root.config(bg=self.BG_COLOR)
        self.on_login_success = on_login_success
        
        # Initialize cookies and salt variables
        self.cookies = None
        self.salt = None
        
        # Store login credentials for OTP verification
        self.username = None
        self.password = None
        
        # Generate initial captcha
        self.captcha_text = self._generate_captcha()
        
        self._setup_ui()
        
        # Call view_login_area when form is opened and assign cookies and salt
        try:
            login_data = view_login_area()
            self.cookies = login_data.get('cookies')
            self.salt = login_data.get('salt')
        except Exception as e:
            print(f"Error calling view_login_area: {e}")
    
    def _generate_captcha(self):
        """Generate a random 6-character captcha"""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    def _setup_ui(self):
        """Build the login form UI"""
        
        # Header
        header_frame = tk.Frame(self.root, bg=self.PRIMARY_COLOR, height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="🔐 LOGIN",
            font=("Segoe UI", 22, "bold"),
            bg=self.PRIMARY_COLOR,
            fg="white"
        ).pack(pady=20)
        
        # Main card
        main_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        card = tk.Frame(main_frame, bg=self.CARD_BG)
        card.pack(fill=tk.BOTH, expand=True)
        
        self.inner = tk.Frame(card, bg=self.CARD_BG, padx=25, pady=25)
        self.inner.pack(fill=tk.BOTH, expand=True)
        
        # Username
        tk.Label(
            self.inner,
            text="Username",
            font=("Segoe UI", 10, "bold"),
            bg=self.CARD_BG,
            fg=self.TEXT_COLOR
        ).pack(anchor=tk.W, pady=(0, 5))
        
        self.username_var = tk.StringVar()
        username_entry = tk.Entry(
            self.inner,
            textvariable=self.username_var,
            font=("Segoe UI", 11),
            bg=self.CARD_BG,
            fg=self.TEXT_COLOR,
            relief=tk.SOLID,
            bd=1,
            insertbackground=self.PRIMARY_COLOR,
            width=30
        )
        username_entry.pack(fill=tk.X, pady=(0, 15))
        username_entry.config(highlightthickness=1, highlightbackground=self.BORDER_COLOR, highlightcolor=self.BORDER_FOCUS)
        self._add_entry_focus(username_entry)
        
        # Password
        tk.Label(
            self.inner,
            text="Password",
            font=("Segoe UI", 10, "bold"),
            bg=self.CARD_BG,
            fg=self.TEXT_COLOR
        ).pack(anchor=tk.W, pady=(0, 5))
        
        self.password_var = tk.StringVar()
        password_entry = tk.Entry(
            self.inner,
            textvariable=self.password_var,
            font=("Segoe UI", 11),
            bg=self.CARD_BG,
            fg=self.TEXT_COLOR,
            relief=tk.SOLID,
            bd=1,
            show="•",
            insertbackground=self.PRIMARY_COLOR,
            width=30
        )
        password_entry.pack(fill=tk.X, pady=(0, 15))
        password_entry.config(highlightthickness=1, highlightbackground=self.BORDER_COLOR, highlightcolor=self.BORDER_FOCUS)
        self._add_entry_focus(password_entry)
        
        # Captcha Section
        tk.Label(
            self.inner,
            text="Security Verification",
            font=("Segoe UI", 10, "bold"),
            bg=self.CARD_BG,
            fg=self.PRIMARY_COLOR
        ).pack(anchor=tk.W, pady=(15, 10))
        
        # Captcha Display
        captcha_frame = tk.Frame(self.inner, bg=self.BORDER_COLOR, height=60)
        captcha_frame.pack(fill=tk.X, pady=(0, 10))
        captcha_frame.pack_propagate(False)
        
        captcha_inner = tk.Frame(captcha_frame, bg="white")
        captcha_inner.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        self.captcha_label = tk.Label(
            captcha_inner,
            text=self.captcha_text,
            font=("Courier New", 24, "bold"),
            bg="white",
            fg=self.PRIMARY_COLOR,
            padx=10,
            pady=10
        )
        self.captcha_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        refresh_btn = tk.Button(
            captcha_inner,
            text="🔄",
            font=("Segoe UI", 12),
            bg=self.PRIMARY_COLOR,
            fg="white",
            relief=tk.FLAT,
            bd=0,
            padx=8,
            pady=8,
            cursor="hand2",
            command=self._refresh_captcha
        )
        refresh_btn.pack(side=tk.RIGHT, padx=5)
        
        # Captcha Input
        tk.Label(
            self.inner,
            text="Enter the code above",
            font=("Segoe UI", 10, "bold"),
            bg=self.CARD_BG,
            fg=self.TEXT_COLOR
        ).pack(anchor=tk.W, pady=(0, 5))
        
        self.captcha_input_var = tk.StringVar()
        captcha_input = tk.Entry(
            self.inner,
            textvariable=self.captcha_input_var,
            font=("Segoe UI", 11),
            bg=self.CARD_BG,
            fg=self.TEXT_COLOR,
            relief=tk.SOLID,
            bd=1,
            insertbackground=self.PRIMARY_COLOR,
            width=30
        )
        captcha_input.pack(fill=tk.X, pady=(0, 20))
        captcha_input.config(highlightthickness=1, highlightbackground=self.BORDER_COLOR, highlightcolor=self.BORDER_FOCUS)
        self._add_entry_focus(captcha_input)
        
        # Login Button
        login_btn = tk.Button(
            self.inner,
            text="🔓 LOGIN",
            font=("Segoe UI", 12, "bold"),
            bg=self.PRIMARY_COLOR,
            fg="white",
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=12,
            cursor="hand2",
            command=self._login
        )
        login_btn.pack(fill=tk.X, pady=(10, 10))
        
        # Status label
        self.status_label = tk.Label(
            self.inner,
            text="",
            font=("Segoe UI", 9),
            bg=self.CARD_BG,
            fg=self.SUCCESS_COLOR
        )
        self.status_label.pack(pady=(10, 0))
    
    def _add_entry_focus(self, entry):
        """Add focus effect to entry field"""
        def on_focus_in(event):
            entry.config(highlightcolor=self.BORDER_FOCUS, highlightthickness=2)
        
        def on_focus_out(event):
            entry.config(highlightcolor=self.BORDER_COLOR, highlightthickness=1)
        
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
    
    def _refresh_captcha(self):
        """Generate and display new captcha"""
        self.captcha_text = self._generate_captcha()
        self.captcha_label.config(text=self.captcha_text)
        self.captcha_input_var.set("")
        self.status_label.config(text="Captcha refreshed", fg=self.SUCCESS_COLOR)
    
    def _login(self):
        """Handle login button click"""
        username = self.username_var.get().strip()
        password = self.password_var.get()
        captcha_input = self.captcha_input_var.get().strip().upper()
        
        # Validation
        if not username:
            self.status_label.config(text="❌ Enter username", fg=self.ERROR_COLOR)
            return
        
        if not password:
            self.status_label.config(text="❌ Enter password", fg=self.ERROR_COLOR)
            return
        
        if not captcha_input:
            self.status_label.config(text="❌ Enter captcha code", fg=self.ERROR_COLOR)
            return
        
        # if captcha_input != self.captcha_text:
        #     self.status_label.config(text="❌ Incorrect captcha", fg=self.ERROR_COLOR)
        #     self._refresh_captcha()
        #     return
        
        # Store username for OTP verification
        self.username = username
        self.password = password
        self.captcha = captcha_input
        
        # Call generate_login_otp
        try:
            self.status_label.config(text="⏳ Generating OTP...", fg=self.TEXT_COLOR)
            self.root.update()
            
            generate_login_otp(self.username, self.password, self.salt, self.captcha, self.cookies)
            # Hide login form and show OTP form
            self._show_otp_form()
        except Exception as e:
            self.status_label.config(text=f"❌ Error: {str(e)}", fg=self.ERROR_COLOR)
            print(f"Error generating OTP: {e}")
    
    def _show_otp_form(self):
        """Clear login form and show OTP form"""
        # Clear all widgets from inner frame
        for widget in self.inner.winfo_children():
            widget.destroy()
        
        # OTP title
        tk.Label(
            self.inner,
            text="OTP Verification",
            font=("Segoe UI", 10, "bold"),
            bg=self.CARD_BG,
            fg=self.PRIMARY_COLOR
        ).pack(anchor=tk.W, pady=(0, 10))
        
        # OTP instruction
        tk.Label(
            self.inner,
            text="Enter the OTP sent to your registered email/phone",
            font=("Segoe UI", 9),
            bg=self.CARD_BG,
            fg=self.LABEL_COLOR
        ).pack(anchor=tk.W, pady=(0, 15))
        
        # OTP Input
        tk.Label(
            self.inner,
            text="OTP Code",
            font=("Segoe UI", 10, "bold"),
            bg=self.CARD_BG,
            fg=self.TEXT_COLOR
        ).pack(anchor=tk.W, pady=(0, 5))
        
        self.otp_var = tk.StringVar()
        otp_entry = tk.Entry(
            self.inner,
            textvariable=self.otp_var,
            font=("Segoe UI", 11),
            bg=self.CARD_BG,
            fg=self.TEXT_COLOR,
            relief=tk.SOLID,
            bd=1,
            insertbackground=self.PRIMARY_COLOR,
            width=30
        )
        otp_entry.pack(fill=tk.X, pady=(0, 20))
        otp_entry.config(highlightthickness=1, highlightbackground=self.BORDER_COLOR, highlightcolor=self.BORDER_FOCUS)
        self._add_entry_focus(otp_entry)
        
        # Submit OTP Button
        submit_btn = tk.Button(
            self.inner,
            text="✓ VERIFY OTP",
            font=("Segoe UI", 12, "bold"),
            bg=self.SUCCESS_COLOR,
            fg="white",
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=12,
            cursor="hand2",
            command=self._verify_otp
        )
        submit_btn.pack(fill=tk.X, pady=(10, 10))
        
        # Status label
        self.status_label = tk.Label(
            self.inner,
            text="",
            font=("Segoe UI", 9),
            bg=self.CARD_BG,
            fg=self.SUCCESS_COLOR
        )
        self.status_label.pack(pady=(10, 0))
        
        # Focus on OTP entry
        otp_entry.focus()
    
    def _verify_otp(self):
        """Verify OTP"""
        otp_input = self.otp_var.get().strip()
        
        if not otp_input:
            self.status_label.config(text="❌ Enter OTP code", fg=self.ERROR_COLOR)
            return
        
        # Success message
        validate_otp_res = validate_login_otp(username=self.username_var.get().strip(), password=self.password, salt=self.salt, otp=otp_input, cookies=self.cookies)
        
        if validate_otp_res['checkmsg'] == 'error':
            print('login failed!')
            self.captcha_text = self._generate_captcha()
            self._setup_ui()
            
        self.status_label.config(text="✓ OTP verified successfully!", fg=self.SUCCESS_COLOR)
        messagebox.showinfo("Success", f"Welcome, {self.username}!\n\nLogin successful with OTP verification!")
        
        if self.on_login_success:
            self.on_login_success(self.cookies)
        
        # Reset form
        self.username = None
        self.password = None
        self.otp_var.set("")
        self.username_var.set("")
        self.password_var.set("")
        self.captcha_input_var.set("")
        self.captcha_text = self._generate_captcha()
        # self._setup_ui()


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginForm(root)
    root.mainloop()
