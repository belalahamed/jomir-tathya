"""
App Screen Module
"""

import customtkinter as ctk
from PIL import Image

from assets import IMAGES
from ..store import AppState
from .login_screen import LoginScreen
from .property_screen import PropertyScreen

class AppScreen(ctk.CTk):
    """App Screen UI"""
    
    def __init__(self):
        """App Screen UI Initialization"""
        
        super().__init__()
        
        
        # State Variables
        self.login_screen = None # login screen exist or not
        self.property_screen = None # Property screen exist or not
        
        # Subscribe to AppState changes
        AppState.add_listener(self._change_header_btn)
        
        self.title("Jomir Tathya")
        self.configure(fg_color="#F5F5F7")  # Configure App Screen background color
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight}")
        
        # Header Frame
        self.header_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=0, border_width=2, border_color="#E5E5E7")
        self.header_frame.pack(side="top", fill="both", padx=0, pady=0, ipady=20)
        
        # Services Frame
        self.services_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=10, border_width=2, border_color="#E5E5E7")
        self.services_frame.pack(after=self.header_frame, fill="both", padx=50, pady=30, ipady=20, ipadx=20)
        
        # Services Label - Pack this first to keep it at the top of the services_frame
        self.services_label = ctk.CTkLabel(self.services_frame, text="Services", text_color="white", font=("Calibri", 28), fg_color="#007AFF")
        self.services_label.pack(side="top", fill="both", pady=10, padx=1, ipady=10)

        # Find Information Frame
        self.find_info_frame = ctk.CTkFrame(self.services_frame, fg_color="#FFFFFF")
        self.find_info_frame.pack(side="top", fill="both", padx=5, pady=5)
        
        # Check Status Frame
        self.check_status_frame = ctk.CTkFrame(self.services_frame, fg_color="#FFFFFF")
        self.check_status_frame.pack(side="top", fill="both", padx=5, pady=5)
        
        # Header Logo
        self.logo = ctk.CTkImage(light_image=Image.open(IMAGES.get("logo")), size=(40, 40))
        
        self.logo_label = ctk.CTkLabel(self.header_frame, image=self.logo, text="JOMIR TATHYA", text_color="#007AFF", font=("Calibri", 28, "bold"), compound="left")
        self.logo_label.pack(side="left", padx=50)
        
        # Header Login Button
        self.login_btn = ctk.CTkButton(self.header_frame, width=80, height=40, text="Login", text_color="white", fg_color="#007AFF", font=("Calibri", 18), command=self._open_login_screen)
        self.login_btn.pack(side="right", padx=50)
        
        # Header Logout Button
        self.logout_btn = ctk.CTkButton(self.header_frame, width=80, height=40, text="Logout", text_color="white", fg_color="#007AFF", font=("Calibri", 18), command=self._handle_logout_btn)
        
        # Find Information Label
        self.find_info_label = ctk.CTkLabel(self.find_info_frame, text="Find Information", text_color="black", font=("Calibri", 25))
        self.find_info_label.pack(side="top", anchor="w", padx=20)
        
        # Know Your Property Card
        self.know_your_property_card = ctk.CTkButton(self.find_info_frame, text="🏠 Know Your Property", fg_color="green", font=("Calibri", 20, "bold"), hover_color="#044a04", command=self._handle_know_your_property_card)
        self.know_your_property_card.pack(side="left", padx=40, pady=30, ipadx=20, ipady=30)
        
        # RS-LR Info Card
        self.rs_lr_info_card = ctk.CTkButton(self.find_info_frame, text="🏠 RS-LR Information", fg_color="green", font=("Calibri", 20, "bold"), hover_color="#044a04")
        self.rs_lr_info_card.pack(side="left", padx=40, pady=30, ipadx=20, ipady=30)
        
        # Check Status Label
        self.check_status_label = ctk.CTkLabel(self.check_status_frame, text="Check Status", text_color="black", font=("Calibri", 25))
        self.check_status_label.pack(side="top", anchor="w", padx=20)
        
        # Mutation Plot Khatian Status Card
        self.mutation_plot_khatian_card = ctk.CTkButton(self.check_status_frame, text="🏠 Mutation Plot Khatian Status", fg_color="green", font=("Calibri", 20, "bold"), hover_color="#044a04")
        self.mutation_plot_khatian_card.pack(side="left", padx=40, pady=30, ipadx=20, ipady=30)
        
        
        
    def _open_login_screen(self):
        """Handling Login Screen Opening"""
                
        if self.login_screen is None or not self.login_screen.winfo_exists():
            self.login_screen = LoginScreen()  # create window if its None or destroyed
                
        else:
            self.login_screen.focus()  # if window exists focus it
    
            
    def _handle_know_your_property_card(self):
        """Handles Know Your Property Button (Card) Click"""
        
        if AppState.is_logged_in:
            if self.property_screen is None or not self.property_screen.winfo_exists():
                self.property_screen = PropertyScreen(session_cookies=AppState.cookies)
            
            else:
                self.property_screen.focus()
            
        
        else:
            self._open_login_screen()
            
    
    def _change_header_btn(self):
        """Handles the login and logout button visibility"""
        
        if AppState.is_logged_in:
            self.login_btn.pack_forget()
            self.logout_btn.pack(side="right", padx=50)
        else:
            self.logout_btn.pack_forget()
            self.login_btn.pack(side="right", padx=50)
        
    def _handle_logout_btn(self):
        """Handling Logout Button Click"""
        
        AppState.set_login_state(False, None)