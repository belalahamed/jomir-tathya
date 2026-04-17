"""
Property Search Screen Module is UI module to load the Propery Lookup UI
"""

import customtkinter as ctk
import threading
import multiprocessing
import webview
from tkinterweb import HtmlFrame
from PIL import Image

from ..api import fetch_districts, fetch_blocks, fetch_mouzas, fetch_khatian, fetch_plot
from ..services import session
from assets import app_logo as APP_LOGO, back_icon as BACK_ICON


def _run_webview_viewer(html_content, should_print=False):
    """Helper function to launch pywebview in its own process/main thread."""
    window = webview.create_window(
        "Property Details", html=html_content, width=1000, height=800
    )

    if should_print:
        # Execute JavaScript to trigger the browser's native print dialog
        webview.start(lambda: window.evaluate_js("window.print()"))
    else:
        webview.start()


class PropertySearchScreen(ctk.CTkFrame):
    """Property Screen UI"""

    def __init__(self, parent_frame, root_app, session_cookies=None):
        """Initialization Property Screen Instance"""

        super().__init__(parent_frame, fg_color="white", corner_radius=0)

        self.session_cookies = session_cookies
        self.parent_frame = parent_frame  # * This is reference of 'self.container_frame'(parent_frame) of 'RootApp'
        self.root_app = root_app  # * This is the reference of 'RootApp' instance

        # State variables
        self.districts_list = []
        self.blocks_list = []
        self.mouzas_list = []
        self.selected_district_code = None
        self.selected_block_code = None
        self.selected_mouza_code = None
        self.property_type_var = ctk.StringVar(value="Khatian")
        self.current_html = ""

        # Container frame for Propery Lookup Form
        self.property_form_frame = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            width=400,
            border_width=1,
            border_color="#E5E5E7",
        )
        self.property_form_frame.pack(side="left", fill="y", padx=0, pady=0)
        self.property_form_frame.pack_propagate(False)

        # * Back Button
        self.back_btn_img = ctk.CTkImage(light_image=Image.open(BACK_ICON))
        self.back_btn = ctk.CTkButton(
            self.property_form_frame,
            text="",
            image=self.back_btn_img,
            width=50,
            height=50,
            command=self._open_app_screen,
        )
        self.back_btn.place(relx=0, y=30)

        # Header Label
        self.header_label = ctk.CTkLabel(
            self.property_form_frame,
            text="Know Your Property",
            font=("Calibri", 26, "bold"),
            text_color="#007AFF",
        )
        self.header_label.place(relx=0.5, y=30, anchor="center")

        # Location Details Label
        self.location_label = ctk.CTkLabel(
            self.property_form_frame,
            text="🌐 Location Details",
            font=("Calibri", 18, "bold"),
            text_color="#007AFF",
        )
        self.location_label.place(x=30, y=80)

        # District Option Menu Label
        self.district_label = ctk.CTkLabel(
            self.property_form_frame,
            text="District:",
            font=("Calibri", 16, "bold"),
            text_color="#1D1D1F",
        )
        self.district_label.place(x=30, y=130)

        # District Option Menu
        self.district_option_menu = ctk.CTkOptionMenu(
            self.property_form_frame,
            values=["Loading..."],  # Initial value
            width=240,
            height=40,
            text_color="black",
            dropdown_text_color="black",
            fg_color="#E5E5E7",
            button_color="#007AFF",
            button_hover_color="#005FB8",
            dropdown_fg_color="white",
            dropdown_hover_color="#007AFF",  # Changed to match button_hover_color for consistency
            command=self._on_district_selected,
            state="disabled",  # Disable until districts are loaded
        )
        self.district_option_menu.place(x=130, y=125)

        # Block Option Menu Label
        self.block_label = ctk.CTkLabel(
            self.property_form_frame,
            text="Block:",
            font=("Calibri", 16, "bold"),
            text_color="#1D1D1F",
        )
        self.block_label.place(x=30, y=185)

        # Block Option Menu
        self.block_option_menu = ctk.CTkOptionMenu(
            self.property_form_frame,
            values=["Select Block"],  # Initial value
            width=240,
            height=40,
            text_color="black",
            dropdown_text_color="black",
            fg_color="#E5E5E7",
            button_color="#007AFF",
            button_hover_color="#005FB8",
            dropdown_fg_color="white",
            dropdown_hover_color="#007AFF",  # Changed to match button_hover_color for consistency
            command=self._on_block_selected,
            state="disabled",  # Disable until a district is selected
        )
        self.block_option_menu.place(x=130, y=180)

        # Mouza Option Menu Label
        self.mouza_label = ctk.CTkLabel(
            self.property_form_frame,
            text="Mouza:",
            font=("Calibri", 16, "bold"),
            text_color="#1D1D1F",
        )
        self.mouza_label.place(x=30, y=240)

        # Mouza Option Menu
        self.mouza_option_menu = ctk.CTkOptionMenu(
            self.property_form_frame,
            values=["Select Mouza"],  # Initial value
            width=240,
            height=40,
            text_color="black",
            dropdown_text_color="black",
            fg_color="#E5E5E7",
            button_color="#007AFF",
            button_hover_color="#005FB8",
            dropdown_fg_color="white",
            dropdown_hover_color="#007AFF",  # Changed to match button_hover_color for consistency
            command=self._on_mouza_selected,
            dynamic_resizing=True,
            state="disabled",  # Disable until a block is selected
        )
        self.mouza_option_menu.place(x=130, y=235)

        # Property Details Label
        self.property_details_label = ctk.CTkLabel(
            self.property_form_frame,
            text="📝 Property Details",
            font=("Calibri", 18, "bold"),
            text_color="#007AFF",
        )
        self.property_details_label.place(x=30, y=310)

        # Property Type Label
        self.property_type_label = ctk.CTkLabel(
            self.property_form_frame,
            text="Property Type:",
            font=("Calibri", 16, "bold"),
            text_color="black",
        )
        self.property_type_label.place(x=35, y=360)

        # Khatian Radio Button
        self.khatian_radio_btn = ctk.CTkRadioButton(
            self.property_form_frame,
            text="Khatian",
            variable=self.property_type_var,
            value="Khatian",
            text_color="black",
            fg_color="#007AFF",
            hover_color="#005FB8",
            command=self._on_property_type_change,
        )
        self.khatian_radio_btn.place(x=150, y=365)

        # Plot Radio Button
        self.plot_radio_btn = ctk.CTkRadioButton(
            self.property_form_frame,
            text="Plot",
            variable=self.property_type_var,
            value="Plot",
            text_color="black",
            fg_color="#007AFF",
            hover_color="#005FB8",
            command=self._on_property_type_change,
        )
        self.plot_radio_btn.place(x=270, y=365)

        # Property Label (Khatian or Plot)
        self.property_label = ctk.CTkLabel(
            self.property_form_frame,
            text="Khatian No:",
            font=("Calibri", 16, "bold"),
            text_color="black",
        )
        self.property_label.place(x=35, y=420)

        # Property Entry (Khatian or Plot)
        self.property_first_entry = ctk.CTkEntry(
            self.property_form_frame,
            placeholder_text="Khatian No",
            width=120,
            height=40,
            fg_color="white",
            text_color="#1D1D1F",
            font=("Calibri", 16),
            corner_radius=8,
            border_color="#D1D1D6",
        )
        self.property_first_entry.place(x=130, y=415)

        self.property_second_entry = ctk.CTkEntry(
            self.property_form_frame,
            placeholder_text="Bata No",
            width=110,
            height=40,
            fg_color="white",
            text_color="#1D1D1F",
            font=("Calibri", 16),
            corner_radius=8,
            border_color="#D1D1D6",
        )
        self.property_second_entry.place(x=260, y=415)

        # Search Button
        self.search_btn = ctk.CTkButton(
            self.property_form_frame,
            text="🔎 Search",
            width=150,
            height=45,
            font=("Calibri", 16, "bold"),
            fg_color="#007AFF",
            hover_color="#005FB8",
            corner_radius=10,
            command=self._on_search,
        )
        self.search_btn.place(x=200, y=500)

        # Clear Button
        self.clear_btn = ctk.CTkButton(
            self.property_form_frame,
            text="🧹 Clear",
            width=150,
            height=45,
            font=("Calibri", 16, "bold"),
            fg_color="#007AFF",
            hover_color="#005FB8",
            corner_radius=10,
            command=self._clear_form,
        )
        self.clear_btn.place(x=40, y=500)

        # Status Message Label
        self.status_label = ctk.CTkLabel(
            self.property_form_frame,
            text="Ready",
            font=("Calibri", 16, "bold"),
            text_color="green",
        )
        self.status_label.place(relx=0.5, y=580, anchor="center")

        # Results Panel
        self.results_frame = ctk.CTkFrame(
            self, fg_color="transparent", corner_radius=10
        )
        self.results_frame.pack(
            side="right", expand=True, fill="both", padx=20, pady=20
        )

        self.results_label = ctk.CTkLabel(
            self.results_frame,
            text="Search Results",
            font=("Calibri", 18, "bold"),
            text_color="black",
        )
        self.results_label.pack(pady=(0, 10))

        # Replace Textbox with HtmlFrame for rich rendering
        self.results_browser = HtmlFrame(self.results_frame)
        self.results_browser.pack(expand=True, fill="both")

        # Open in Browser Button
        self.open_browser_btn = ctk.CTkButton(
            self.results_frame,
            text="🌐 Open in Browser",
            width=200,
            height=40,
            font=("Calibri", 16, "bold"),
            fg_color="#34C759",  # iOS/macOS Green for success actions
            hover_color="#28A745",
            corner_radius=10,
            command=self._on_open_in_browser,
        )
        self.open_browser_btn.pack(pady=10)

        # Save as PDF Button using pywebview
        self.save_pdf_btn = ctk.CTkButton(
            self.results_frame,
            text="💾 Save as PDF",
            width=200,
            height=40,
            font=("Calibri", 16, "bold"),
            fg_color="#007AFF",
            hover_color="#005FB8",
            corner_radius=10,
            command=self._on_save_as_pdf,
        )
        self.save_pdf_btn.pack(pady=10)

        # Load districts on startup
        self._load_districts()

    def _load_districts(self):
        """Initiate loading of districts in a separate thread."""

        self.status_label.configure(text="Loading districts...", text_color="blue")
        threading.Thread(target=self.__fetch_and_update_districts, daemon=True).start()

    def __fetch_and_update_districts(self):
        """Fetch districts from the API and update the UI."""

        try:
            districts_list = fetch_districts()  # Fetching Districts List from API
            self.after(0, self._update_district_options_ui, districts_list)

        except Exception:
            self.after(
                0,
                lambda: self.status_label.configure(
                    text="Failed to load districts!", text_color="red"
                ),
            )

    def _update_district_options_ui(self, districts_list):
        """Update the district option menu with fetched data."""

        self.districts_list = districts_list

        if self.districts_list:
            # Using List Comprehension to create district names list from districts_list
            district_names = [
                district.get("eng_dname")
                for district in self.districts_list
                if district.get("eng_dname")
            ]
            district_options = ["Select District"] + district_names
            self.district_option_menu.configure(values=district_options, state="normal")
            self.district_option_menu.set("Select District")
            self.status_label.configure(
                text="Districts loaded successfully!", text_color="green"
            )

        else:
            self.district_option_menu.configure(values=["Select district"])
            self.district_option_menu.set("Select District")
            self.status_label.configure(text="No districts found.", text_color="orange")

    def _on_district_selected(self, selected_district_name):
        """Handle district selection from the option menu."""

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
                    for district in self.districts_list
                    if district.get("eng_dname") == selected_district_name
                ),
                None,
            )
            self.selected_district_code = selected_district.get("dcode")
            self.district_option_menu.set(selected_district_name)
            self._load_blocks()

    def _load_blocks(self):
        """Initiate loading of blocks for the selected district."""

        self.status_label.configure(text="Loading blocks...", text_color="blue")
        self.block_option_menu.configure(values=["Loading..."], state="disabled")
        threading.Thread(target=self.__fetch_and_update_blocks, daemon=True).start()

    def __fetch_and_update_blocks(self):
        """Fetch blocks from the API and update the UI."""

        try:
            blocks_list = fetch_blocks(self.selected_district_code)
            self.after(0, self._update_block_options_ui, blocks_list)

        except Exception:
            self.after(
                0,
                lambda: self.status_label.configure(
                    text="Failed to load blocks!", text_color="red"
                ),
            )

    def _update_block_options_ui(self, blocks_list):
        """Update the block option menu with fetched data."""

        self.blocks_list = blocks_list

        if self.blocks_list:
            block_names = [
                b.get("eng_bname") for b in self.blocks_list if b.get("eng_bname")
            ]
            block_options = ["Select Block"] + block_names
            self.block_option_menu.configure(values=block_options, state="normal")
            self.block_option_menu.set("Select Block")
            self.status_label.configure(
                text="Blocks loaded successfully.", text_color="green"
            )

        else:
            self.block_option_menu.configure(values=["Select Block"], state="disabled")
            self.block_option_menu.set("Select Block")
            self.status_label.configure(text="No blocks found.", text_color="orange")

    def _on_block_selected(self, selected_block_name):
        """Handle block selection from the option menu."""

        if selected_block_name == "Select Block":
            self.selected_block_code = None
            self.mouza_option_menu.configure(values=["Select Mouza"], state="disabled")
            self.mouza_option_menu.set("Select Mouza")

        else:
            selected_block = next(
                (
                    block
                    for block in self.blocks_list
                    if block.get("eng_bname") == selected_block_name
                ),
                None,
            )
            block_key = selected_block.get("blockKey")
            self.selected_block_code = block_key.get("bcode")
            self.block_option_menu.set(selected_block_name)
            self._load_mouzas()

    def _load_mouzas(self):
        """Initiate loading of mouzas for the selected district and block."""

        self.status_label.configure(text="Loading mouzas...", text_color="blue")
        self.mouza_option_menu.configure(values=["Loading..."], state="disabled")
        threading.Thread(target=self.__fetch_and_update_mouzas, daemon=True).start()

    def __fetch_and_update_mouzas(self):
        """Fetch mouzas from the API and update the UI."""

        try:
            mouzas = fetch_mouzas(self.selected_district_code, self.selected_block_code)
            self.after(0, self._update_mouza_options_ui, mouzas)

        except Exception:
            self.after(
                0,
                lambda: self.status_label.configure(
                    text="Failed to load mouzas!", text_color="red"
                ),
            )

    def _update_mouza_options_ui(self, mouzas_list):
        """Update the mouza option menu with fetched data."""

        self.mouzas_list = mouzas_list

        if self.mouzas_list:
            mouza_names = [
                mouza.get("mouName")
                for mouza in self.mouzas_list
                if mouza.get("mouName")
            ]
            mouza_options = ["Select Mouza"] + mouza_names
            self.mouza_option_menu.configure(values=mouza_options, state="normal")
            self.mouza_option_menu.set("Select Mouza")
            self.status_label.configure(
                text="Mouzas loaded successfully.", text_color="green"
            )

        else:
            self.mouza_option_menu.configure(
                values=["No Mouzas Found"], state="disabled"
            )

    def _on_mouza_selected(self, selected_mouza_name):
        """Handle mouza selection from the option menu."""

        if selected_mouza_name == "Select Mouza":
            self.selected_mouza_code = None

        else:
            selected_mouza = next(
                (
                    mouza
                    for mouza in self.mouzas_list
                    if mouza.get("mouName") == selected_mouza_name
                ),
                None,
            )
            self.selected_mouza_code = selected_mouza.get("moucode")
            self.mouza_option_menu.set(selected_mouza_name)
            self.status_label.configure(text="Ready", text_color="green")

    def _display_results(self, html_content):
        """Update the browser widget with styled HTML content."""
        # Wrap the snippet with Bootstrap and custom styles to match the portal
        styled_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
            <style>
                body {{ 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    background-color: #ffffff; 
                    padding: 20px;
                    font-size: 18px; /* Increased font size for zoom effect */
                    line-height: 1.6;
                }}
                .table {{ margin-top: 20px; border: 1px solid #dee2e6; width: 100%; }}
                th {{ background-color: #f8f9fa; color: #333; font-weight: bold; }}
                td, th {{ padding: 12px !important; }}
                b {{ color: #007AFF; }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        self.current_html = styled_html
        self.results_browser.load_html(styled_html)

    def _on_property_type_change(self):
        """Update labels and placeholders when property type changes."""

        p_type = self.property_type_var.get()
        self.property_label.configure(text=f"{p_type} No:")
        self.property_first_entry.configure(placeholder_text=f"{p_type} No")
        self.property_first_entry.delete(0, "end")
        self.property_second_entry.delete(0, "end")

    def _clear_form(self):
        """Clear inputs and reset status."""

        # Reset Location Selection drop-downs and internal state codes
        self.district_option_menu.set("Select District")
        self._on_district_selected("Select District")
        self.selected_block_code = None
        self.selected_mouza_code = None

        # Clear Property Number entry fields
        self.property_first_entry.delete(0, "end")
        self.property_second_entry.delete(0, "end")

        # Clear the results textbox and reset UI state
        self.results_browser.load_html("")
        self.current_html = ""
        self.search_btn.configure(state="normal")
        self.status_label.configure(text="Ready", text_color="green")

    def _on_open_in_browser(self):
        """Open the search results content in a pywebview window."""
        self._launch_webview(should_print=False)

    def _on_save_as_pdf(self):
        """Open results in pywebview and automatically trigger the print/PDF dialog."""
        self._launch_webview(should_print=True)

    def _launch_webview(self, should_print=False):
        """Internal helper to launch the pywebview process."""
        try:
            status_text = (
                "Opening PDF viewer..." if should_print else "Opening viewer..."
            )
            self.status_label.configure(text=status_text, text_color="blue")
            html_content = self.current_html

            if not html_content or len(html_content.strip()) < 100:
                err_text = (
                    "No results found to save!"
                    if should_print
                    else "No results found to open!"
                )
                self.status_label.configure(text=err_text, text_color="orange")
                return

            # pywebview requires being on the main thread of its process.
            # Since CustomTkinter's loop is already on this process's main thread,
            # we use multiprocessing to create a new process where pywebview can own the main thread.
            p = multiprocessing.Process(
                target=_run_webview_viewer,
                args=(html_content, should_print),
                daemon=True,
            )
            p.start()

            success_text = (
                "Print dialog opened."
                if should_print
                else "Opened in pywebview viewer."
            )
            self.status_label.configure(text=success_text, text_color="green")

        except Exception as e:
            err_type = "PDF Error" if should_print else "Viewer Error"
            self.status_label.configure(text=f"{err_type}: {str(e)}", text_color="red")

    def _on_search(self):
        """Validate inputs and initiate the search process."""

        if not all(
            [
                self.selected_district_code,
                self.selected_block_code,
                self.selected_mouza_code,
            ]
        ):
            self.status_label.configure(
                text="Error: Select District, Block, and Mouza", text_color="red"
            )
            return

        main_no = self.property_first_entry.get().strip()
        if not main_no:
            self.status_label.configure(
                text=f"Error: Enter {self.property_type_var.get()} Number",
                text_color="red",
            )
            return

        bata_no = self.property_second_entry.get().strip()

        self.status_label.configure(text="Searching...", text_color="blue")
        self.search_btn.configure(state="disabled")

        # Run search in a thread to keep UI responsive
        threading.Thread(
            target=self.__search_thread, args=(main_no, bata_no), daemon=True
        ).start()

    def __search_thread(self, main_no, bata_no):
        """Threaded worker to call the portal APIs."""

        try:
            if self.session_cookies:
                cookies_str = self.session_cookies

            html_result = ""
            if self.property_type_var.get() == "Khatian":
                html_result = fetch_khatian(
                    cookies_str,
                    self.selected_district_code,
                    self.selected_block_code,
                    self.selected_mouza_code,
                    main_no,
                    bata_no,
                )
            else:
                html_result = fetch_plot(
                    cookies_str,
                    self.selected_district_code,
                    self.selected_block_code,
                    self.selected_mouza_code,
                    main_no,
                    bata_no,
                )
            self.after(
                0,
                lambda: self.status_label.configure(
                    text="Search completed.", text_color="green"
                ),
            )

            # Pass the raw HTML result directly to the browser view
            self.after(0, lambda: self._display_results(html_result))

        except Exception:
            self.after(
                0,
                lambda: self.status_label.configure(
                    text=f"Search failed", text_color="red"
                ),
            )
        finally:
            self.after(0, lambda: self.search_btn.configure(state="normal"))

    def _open_app_screen(self):
        """Open App Screen"""

        # * Remove Property Search Screen
        self.pack_forget()

        # * Display App Screen Frame in Parent Frame(Container Frame) in Root App
        self.root_app.show_frame(self.root_app.app_screen_frame)
