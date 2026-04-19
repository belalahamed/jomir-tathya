# * ====================================================================== * #
# *                      Location Entry Form Module                        * #
# * ====================================================================== * #

import customtkinter as ctk
import threading
import logging

from ..api import fetch_districts, fetch_blocks, fetch_mouzas


class LocationEntryForm(ctk.CTkFrame):
    """
    * Location Entry Form
    """

    def __init__(self, parent_frame):
        """
        * Initializtion of Location Entry Form
        """

        # * Create Location Entry Form Frame using ctk.CTkFrame (parent class)
        super().__init__(parent_frame, fg_color="transparent")

        # * =============== Grid Configuration =============== * #

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=0)

        # * =============== State Variables =============== * #

        self.district_list = []
        self.block_list = []
        self.mouza_list = []
        self.selected_district_code = None
        self.selected_block_code = None
        self.selected_mouza_code = None

        # * =============== UI Elements =============== * #

        # * Location Details Label
        self.location_details_label = ctk.CTkLabel(
            self,
            text="🌐 Location Details",
            font=("Calibri", 16, "bold"),
            text_color="#0066CC",
            fg_color="#F8F9FA",
            corner_radius=8,
        )
        self.location_details_label.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="nsew",
            padx=15,
            pady=(15, 10),
            ipady=10,
        )

        # * District Label
        self.district_label = ctk.CTkLabel(
            self,
            text="District:",
            font=("Calibri", 14, "bold"),
            text_color="#1D1D1F",
        )
        self.district_label.grid(row=1, column=0, sticky="w", padx=15, pady=(10, 5))

        # * District Option Menu
        self.district_option_menu = ctk.CTkOptionMenu(
            self,
            values=["Loading..."],
            height=40,
            text_color="#1D1D1F",
            dropdown_text_color="#1D1D1F",
            fg_color="#F8F9FA",
            button_color="#0066CC",
            button_hover_color="#0052A3",
            dropdown_fg_color="#FFFFFF",
            dropdown_hover_color="#0066CC",
            corner_radius=8,
            dynamic_resizing=False,
            state="disabled",
            command=self.on_district_selected,
        )
        self.district_option_menu.grid(
            row=1, column=1, sticky="nsew", padx=(0, 15), pady=(10, 5)
        )

        # * Block Label
        self.block_label = ctk.CTkLabel(
            self,
            text="Block:",
            font=("Calibri", 14, "bold"),
            text_color="#1D1D1F",
        )
        self.block_label.grid(row=2, column=0, sticky="w", padx=15, pady=(10, 5))

        # * Block Option Menu
        self.block_option_menu = ctk.CTkOptionMenu(
            self,
            values=["Select Block"],
            height=40,
            text_color="#1D1D1F",
            dropdown_text_color="#1D1D1F",
            fg_color="#F8F9FA",
            button_color="#0066CC",
            button_hover_color="#0052A3",
            dropdown_fg_color="#FFFFFF",
            dropdown_hover_color="#0066CC",
            corner_radius=8,
            dynamic_resizing=False,
            state="disabled",
            command=self.on_block_selected,
        )
        self.block_option_menu.grid(
            row=2, column=1, sticky="nsew", padx=(0, 15), pady=(10, 5)
        )

        # * Mouza Label
        self.mouza_label = ctk.CTkLabel(
            self,
            text="Mouza:",
            font=("Calibri", 14, "bold"),
            text_color="#1D1D1F",
        )
        self.mouza_label.grid(row=3, column=0, sticky="w", padx=15, pady=(10, 5))

        # * Mouza Option Menu
        self.mouza_option_menu = ctk.CTkOptionMenu(
            self,
            values=["Select Mouza"],
            height=40,
            text_color="#1D1D1F",
            dropdown_text_color="#1D1D1F",
            fg_color="#F8F9FA",
            button_color="#0066CC",
            button_hover_color="#0052A3",
            dropdown_fg_color="#FFFFFF",
            dropdown_hover_color="#0066CC",
            corner_radius=8,
            dynamic_resizing=False,
            state="disabled",
            command=self.on_mouza_selected,
        )
        self.mouza_option_menu.grid(
            row=3, column=1, sticky="nsew", padx=(0, 15), pady=(10, 5)
        )

        # * Load Districts on Location Entry Form Initialization
        self.load_districts()

    def load_districts(self):
        """
        * Load Districts
        """
        self.after(0, self.fetch_and_update_districts)

    def fetch_and_update_districts(self):
        """
        * Fetch and Update Districts
        """

        try:
            district_list = fetch_districts()
            self.after(0, self.update_district_option_menu, district_list)
        except Exception as e:
            logging.exception("An error occurred: ", e)
            raise

    def update_district_option_menu(self, district_list):
        """
        * Update District Option Menu
        """

        self.district_list = district_list

        if self.district_list:
            district_names = [
                district.get("eng_dname")
                for district in self.district_list
                if district.get("eng_dname")
            ]
            district_options = ["Select District"] + district_names
            self.district_option_menu.configure(values=district_options, state="normal")
            self.district_option_menu.set("Select District")

        else:
            self.district_option_menu.configure(values=["Select district"])
            self.district_option_menu.set("Select District")

    def on_district_selected(self, selected_district_name):
        """
        * On District Selected
        """

        if selected_district_name == "Select District":
            self.selected_district_code = None
            self.block_option_menu.configure(values=["Select Block"], state="disabled")
            self.block_option_menu.set("Select Block")
            self.mouza_option_menu.configure(values=["Select Mouza"], state="disabled")
            self.mouza_option_menu.set("Select Mouza")

        else:
            selected_district = next(
                (
                    district
                    for district in self.district_list
                    if district.get("eng_dname") == selected_district_name
                ),
                None,
            )
            self.selected_district_code = selected_district.get("dcode")
            self.district_option_menu.set(selected_district_name)
            self.load_blocks()

    def load_blocks(self):
        """
        * Load Blocks
        """

        self.block_option_menu.configure(values=["Loading..."], state="disabled")
        self.after(0, self.fetch_and_update_blocks)

    def fetch_and_update_blocks(self):
        """
        * Fetch and Update Blocks
        """

        try:
            block_list = fetch_blocks(self.selected_district_code)
            self.after(0, self.update_block_option_menu, block_list)
        except Exception as e:
            logging.exception("An error occurred: ", e)
            raise

    def update_block_option_menu(self, block_list):
        """
        * Update Block Option Menu
        """

        self.block_list = block_list
        if self.block_list:
            block_names = [
                b.get("eng_bname") for b in self.block_list if b.get("eng_bname")
            ]
            block_options = ["Select Block"] + block_names
            self.block_option_menu.configure(values=block_options, state="normal")
            self.block_option_menu.set("Select Block")

        else:
            self.block_option_menu.configure(values=["Select Block"], state="disabled")
            self.block_option_menu.set("Select Block")

    def on_block_selected(self, selected_block_name):
        """
        * On Block Selected
        """

        if selected_block_name == "Select Block":
            self.selected_block_code = None
            self.mouza_option_menu.configure(values=["Select Mouza"], state="disabled")
            self.mouza_option_menu.set("Select Mouza")

        else:
            selected_block = next(
                (
                    block
                    for block in self.block_list
                    if block.get("eng_bname") == selected_block_name
                ),
                None,
            )
            block_key = selected_block.get("blockKey")
            self.selected_block_code = block_key.get("bcode")
            self.block_option_menu.set(selected_block_name)
            self.load_mouzas()

    def load_mouzas(self):
        """
        * Load Mouzas
        """

        self.mouza_option_menu.configure(values=["Loading..."], state="disabled")
        # threading.Thread(target=self.fetch_and_update_mouzas, daemon=True).start()
        self.after(0, self.fetch_and_update_mouzas)

    def fetch_and_update_mouzas(self):
        """
        * Fetch and Update Mouzas
        """

        try:
            mouza_list = fetch_mouzas(
                self.selected_district_code, self.selected_block_code
            )
            self.after(0, self.update_mouza_option_menu, mouza_list)

        except Exception as e:
            logging.exception("An error occurred: ", e)
            raise

    def update_mouza_option_menu(self, mouza_list):
        """
        * Update Mouza Option Menu
        """

        self.mouza_list = mouza_list

        if self.mouza_list:
            mouza_names = [
                mouza.get("mouName")
                for mouza in self.mouza_list
                if mouza.get("mouName")
            ]
            mouza_options = ["Select Mouza"] + mouza_names
            self.mouza_option_menu.configure(values=mouza_options, state="normal")
            self.mouza_option_menu.set("Select Mouza")
        else:
            self.mouza_option_menu.configure(
                values=["No Mouzas Found"], state="disabled"
            )

    def on_mouza_selected(self, selected_mouza_name):
        """
        * On Mouza Selected
        """

        if selected_mouza_name == "Select Mouza":
            self.selected_mouza_code = None

        else:
            selected_mouza = next(
                (
                    mouza
                    for mouza in self.mouza_list
                    if mouza.get("mouName") == selected_mouza_name
                ),
                None,
            )
            self.selected_mouza_code = selected_mouza.get("moucode")
            self.mouza_option_menu.set(selected_mouza_name)
