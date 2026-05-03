# * ====================================================================== * #
# *                       Property Search Screen Module                    * #
# * ====================================================================== * #

import customtkinter as ctk
import threading
import multiprocessing
import webview
from tkinterweb import HtmlFrame
from PIL import Image

from ..api import fetch_khatian, fetch_plot
from assets import app_logo as APP_LOGO, back_icon as BACK_ICON
from .location_entry_form import LocationEntryForm


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
    """
    * Property Screen Frame UI
    """

    def __init__(self, parent_frame, root_app, session_cookies=None):
        """
        * Initialization of Property Search Screen Frame Instance
        """

        super().__init__(parent_frame, fg_color="#F8F9FA", corner_radius=0)

        # * ====================================================================== * #
        # *                              State Variables                           * #
        # * ====================================================================== * #

        self.session_cookies = session_cookies
        self.property_type_var = ctk.StringVar(value="Khatian")
        self.current_html = ""

        # * ====================================================================== * #
        # *                             Root App References                        * #
        # * ====================================================================== * #

        # * Reference of 'self.container_frame'(parent_frame) of 'RootApp'
        self.parent_frame = parent_frame

        # * Reference of 'RootApp' instance
        self.root_app = root_app

        # * ====================================================================== * #
        # *        Grid Layout Configuration (Property Search Screen Frame)        * #
        # * ====================================================================== * #

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # * ====================================================================== * #
        # *                     Child Frames of App Screen Frame                   * #
        # * ====================================================================== * #

        # * ============== Property Lookup Form Container frame =========== * #

        # * Create container frame for property lookup form
        self.property_form_frame = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            width=420,
            corner_radius=15,
            border_width=1,
            border_color="#E8E8E8",
        )
        self.property_form_frame.grid(column=0, row=0, sticky="nsew", padx=15, pady=15)

        # * Grid Layout configuration for property form container frame
        self.property_form_frame.grid_columnconfigure(0, weight=1)
        self.property_form_frame.grid_columnconfigure(1, weight=1)
        self.property_form_frame.grid_rowconfigure(
            (0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=0
        )
        self.property_form_frame.grid_rowconfigure(10, weight=1)

        # * ============== Header Frame of Property Form Frame =========== * #

        # * Create Header Frame
        self.header_frame = ctk.CTkFrame(
            self.property_form_frame, fg_color="transparent"
        )
        self.header_frame.grid(
            row=0, column=0, columnspan=2, sticky="nsew", padx=15, pady=(15, 10)
        )

        # * Grid Layout Configuration of Header Frame
        self.header_frame.grid_columnconfigure(0, weight=1)
        self.header_frame.grid_columnconfigure(1, weight=0)
        self.header_frame.grid_rowconfigure(0, weight=1)

        # * ============== Location Entries Container Frame =========== * #

        # * Create Location Entries Container Frame
        self.location_entry_form = LocationEntryForm(self.property_form_frame, self)
        self.location_entry_form.grid(
            row=1, column=0, columnspan=2, sticky="nsew", padx=15, pady=(15, 10)
        )

        # * ============== Radio Buttons Frame =========== * #

        # * Create Radio buttons frame
        self.radio_frame = ctk.CTkFrame(
            self.property_form_frame, fg_color="transparent"
        )
        self.radio_frame.grid(row=3, column=1, sticky="ew", padx=15, pady=(10, 5))

        # * Grid Layout Configuration of Radion Buttons Frame
        self.radio_frame.grid_columnconfigure((0, 1), weight=1)

        # * ============== Property Entries Container Frame =========== * #

        # * Create Property entries container frame
        self.property_entries_frame = ctk.CTkFrame(
            self.property_form_frame, fg_color="transparent"
        )
        self.property_entries_frame.grid(
            row=4, column=1, sticky="nsew", padx=15, pady=(10, 5)
        )

        # * Grid Layout Configuration of Property Entries Frame
        self.property_entries_frame.grid_columnconfigure((0, 1), weight=1)

        # * ============== Form Control Buttons Container Frame =========== * #

        # * Create Form Control Buttons Container Frame
        self.buttons_frame = ctk.CTkFrame(
            self.property_form_frame, fg_color="transparent"
        )
        self.buttons_frame.grid(
            row=5, column=0, columnspan=2, sticky="nsew", padx=15, pady=(15, 10)
        )

        # * Grid Layout Configuration of Form Control Buttons Container Frame
        self.buttons_frame.grid_columnconfigure((0, 1), weight=1)

        # * ============== Results Panel Container Frame =========== * #

        # * Create Results Panel Container Frame
        self.results_frame = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=15,
            border_width=1,
            border_color="#E8E8E8",
        )
        self.results_frame.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)

        # * Grid Layout Configuration of Results Panel Container Frame
        self.results_frame.grid_columnconfigure(0, weight=1)
        self.results_frame.grid_rowconfigure(1, weight=1)

        # * ====================================================================== * #
        # *                             Elements of Frames                         * #
        # * ====================================================================== * #

        # * ============== Back Button =========== * #

        # * Create Back Button Image
        self.back_btn_img = ctk.CTkImage(
            light_image=Image.open(BACK_ICON), size=(24, 24)
        )

        # * Create Back Button
        self.back_btn = ctk.CTkButton(
            self.header_frame,
            text="",
            image=self.back_btn_img,
            width=40,
            height=40,
            fg_color="#0066CC",
            hover_color="#0052A3",
            corner_radius=6,
            command=self._open_app_screen,
        )
        self.back_btn.grid(row=0, column=1, sticky="e", padx=(10, 0))

        # * ============== Header Label =========== * #

        # * Create Header Label
        self.header_label = ctk.CTkLabel(
            self.header_frame,
            text="🏠 Know Your Property",
            font=("Calibri", 24, "bold"),
            text_color="#0066CC",
        )
        self.header_label.grid(row=0, column=0, sticky="w")

        # * ============== Property Details Label =========== * #

        # * Create Property Details Label
        self.property_details_label = ctk.CTkLabel(
            self.property_form_frame,
            text="📝 Property Details",
            font=("Calibri", 16, "bold"),
            text_color="#0066CC",
            fg_color="#F8F9FA",
            corner_radius=8,
        )
        self.property_details_label.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="nsew",
            padx=15,
            pady=(15, 10),
            ipady=10,
        )

        # * ============== Property Type Label =========== * #

        # * Create Property Type Label
        self.property_type_label = ctk.CTkLabel(
            self.property_form_frame,
            text="Property Type:",
            font=("Calibri", 14, "bold"),
            text_color="#1D1D1F",
        )
        self.property_type_label.grid(
            row=3, column=0, sticky="w", padx=15, pady=(10, 5)
        )

        # * ============== Khatian Radio Button =========== * #

        # * Create Khatian Radio Button
        self.khatian_radio_btn = ctk.CTkRadioButton(
            self.radio_frame,
            text="Khatian",
            variable=self.property_type_var,
            value="Khatian",
            text_color="#1D1D1F",
            fg_color="#0066CC",
            hover_color="#0052A3",
            command=self._on_property_type_change,
        )
        self.khatian_radio_btn.grid(row=0, column=0, sticky="w")

        # * ============== Plot Radio Button =========== * #

        # * Create Plot Radio Button
        self.plot_radio_btn = ctk.CTkRadioButton(
            self.radio_frame,
            text="Plot",
            variable=self.property_type_var,
            value="Plot",
            text_color="#1D1D1F",
            fg_color="#0066CC",
            hover_color="#0052A3",
            command=self._on_property_type_change,
        )
        self.plot_radio_btn.grid(row=0, column=1, sticky="w")

        # * ============== Property Label (Khatian or Plot) =========== * #

        # * Create Property Label (Khatian or Plot)
        self.property_label = ctk.CTkLabel(
            self.property_form_frame,
            text="Khatian No:",
            font=("Calibri", 14, "bold"),
            text_color="#1D1D1F",
        )
        self.property_label.grid(row=4, column=0, sticky="w", padx=15, pady=(10, 5))

        # * ============== Property Entry (Khatian or Plot) =========== * #

        # * Create Property first Entry (Khatian or Plot)
        self.property_first_entry = ctk.CTkEntry(
            self.property_entries_frame,
            placeholder_text="Khatian No",
            height=40,
            fg_color="#F8F9FA",
            text_color="#1D1D1F",
            font=("Calibri", 14),
            corner_radius=8,
            border_color="#D1D1D6",
            border_width=1,
        )
        self.property_first_entry.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        # * Create Property second Entry (Khatian or Plot)
        self.property_second_entry = ctk.CTkEntry(
            self.property_entries_frame,
            placeholder_text="Bata No",
            height=40,
            fg_color="#F8F9FA",
            text_color="#1D1D1F",
            font=("Calibri", 14),
            corner_radius=8,
            border_color="#D1D1D6",
            border_width=1,
        )
        self.property_second_entry.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

        # * ============== Search Button =========== * #

        # * Create Search Button
        self.search_btn = ctk.CTkButton(
            self.buttons_frame,
            text="🔎 Search",
            height=45,
            font=("Calibri", 16, "bold"),
            fg_color="#28A745",
            hover_color="#1e7e34",
            text_color="white",
            corner_radius=12,
            command=self._on_search,
        )
        self.search_btn.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

        # * ============== Clear Button =========== * #

        # * Create Clear Button
        self.clear_btn = ctk.CTkButton(
            self.buttons_frame,
            text="🧹 Clear",
            height=45,
            font=("Calibri", 16, "bold"),
            fg_color="#6C757D",
            hover_color="#5a6268",
            text_color="white",
            corner_radius=12,
            command=self._clear_form,
        )
        self.clear_btn.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        # * ============== Status Message Label =========== * #

        # * Create Status Message Label
        self.status_message_label = ctk.CTkLabel(
            self.property_form_frame,
            text="Ready",
            font=("Calibri", 14, "bold"),
            text_color="#28A745",
            fg_color="#F8F9FA",
            corner_radius=8,
        )
        self.status_message_label.grid(
            row=9,
            column=0,
            columnspan=2,
            sticky="nsew",
            padx=15,
            pady=(10, 15),
            ipady=10,
        )

        # * ============== Results Label =========== * #

        # * Create Results Label
        self.results_label = ctk.CTkLabel(
            self.results_frame,
            text="🔍 Search Results",
            font=("Calibri", 18, "bold"),
            text_color="#0066CC",
        )
        self.results_label.grid(row=0, column=0, sticky="nsew", padx=15, pady=(15, 10))

        # Replace Textbox with HtmlFrame for rich rendering
        self.results_browser = HtmlFrame(self.results_frame)
        self.results_browser.grid(row=1, column=0, sticky="nsew", padx=15, pady=10)

        # * Buttons frame for results actions
        self.results_buttons_frame = ctk.CTkFrame(
            self.results_frame, fg_color="transparent"
        )
        self.results_buttons_frame.grid(
            row=2, column=0, sticky="nsew", padx=15, pady=(10, 15)
        )
        self.results_buttons_frame.grid_columnconfigure((0, 1), weight=1)

        # Open in Browser Button
        self.open_browser_btn = ctk.CTkButton(
            self.results_buttons_frame,
            text="🌐 Open in Browser",
            height=40,
            font=("Calibri", 14, "bold"),
            fg_color="#17A2B8",
            hover_color="#0f6674",
            text_color="white",
            corner_radius=12,
            command=self._on_open_in_browser,
        )
        self.open_browser_btn.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        # Save as PDF Button using pywebview
        self.save_pdf_btn = ctk.CTkButton(
            self.results_buttons_frame,
            text="💾 Save as PDF",
            height=40,
            font=("Calibri", 14, "bold"),
            fg_color="#0066CC",
            hover_color="#0052A3",
            text_color="white",
            corner_radius=12,
            command=self._on_save_as_pdf,
        )
        self.save_pdf_btn.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

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

        # # Reset Location Selection drop-downs and internal state codes
        # self.district_option_menu.set("Select District")
        # self._on_district_selected("Select District")
        # self.selected_block_code = None
        # self.selected_mouza_code = None

        # Clear Property Number entry fields
        self.property_first_entry.delete(0, "end")
        self.property_second_entry.delete(0, "end")

        # Clear the results textbox and reset UI state
        self.results_browser.load_html("")
        self.current_html = ""
        self.search_btn.configure(state="normal")
        # self.status_label.configure(text="Ready", text_color="green")

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
            # self.status_label.configure(text=status_text, text_color="blue")
            html_content = self.current_html

            if not html_content or len(html_content.strip()) < 100:
                err_text = (
                    "No results found to save!"
                    if should_print
                    else "No results found to open!"
                )
                # self.status_label.configure(text=err_text, text_color="orange")
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
            # self.status_label.configure(text=success_text, text_color="green")

        except Exception as e:
            err_type = "PDF Error" if should_print else "Viewer Error"
            # self.status_label.configure(text=f"{err_type}: {str(e)}", text_color="red")

    def _on_search(self):
        """Validate inputs and initiate the search process."""
        print("on searh")
        print(self.location_entry_form.selected_district_code)
        # if not all(
        #     [
        #         self.selected_district_code,
        #         self.selected_block_code,
        #         self.selected_mouza_code,
        #     ]
        # ):
        #     # self.status_label.configure(
        #     #     text="Error: Select District, Block, and Mouza", text_color="red"
        #     # )
        #     return

        main_no = self.property_first_entry.get().strip()
        # if not main_no:
        #     # self.status_label.configure(
        #     #     text=f"Error: Enter {self.property_type_var.get()} Number",
        #     #     text_color="red",
        #     # )
        #     return

        bata_no = self.property_second_entry.get().strip()

        # self.status_label.configure(text="Searching...", text_color="blue")
        self.search_btn.configure(state="disabled")

        # Run search in a thread to keep UI responsive
        threading.Thread(
            target=self.__search_thread, args=(main_no, bata_no), daemon=True
        ).start()

    def __search_thread(self, main_no, bata_no):
        """Threaded worker to call the portal APIs."""
        print("thread started")

        try:
            if self.session_cookies:
                cookies_str = self.session_cookies

            html_result = ""
            if self.property_type_var.get() == "Khatian":
                html_result = fetch_khatian(
                    cookies_str,
                    self.location_entry_form.selected_district_code,
                    self.location_entry_form.selected_block_code,
                    self.location_entry_form.selected_mouza_code,
                    main_no,
                    bata_no,
                )
                print(html_result)
            else:
                html_result = fetch_plot(
                    cookies_str,
                    self.location_entry_form.selected_district_code,
                    self.location_entry_form.selected_block_code,
                    self.location_entry_form.selected_mouza_code,
                    main_no,
                    bata_no,
                )

            # self.after(
            #     0,
            #     lambda: self.status_label.configure(
            #         text="Search completed.", text_color="green"
            #     ),
            # )

            # Pass the raw HTML result directly to the browser view
            self.after(0, lambda: self._display_results(html_result))

        except Exception:
            # self.after(
            #     0,
            #     lambda: self.status_label.configure(
            #         text=f"Search failed", text_color="red"
            #     ),
            # )
            pass
        finally:
            self.after(0, lambda: self.search_btn.configure(state="normal"))

    def _open_app_screen(self):
        """Open App Screen"""

        # * Remove Property Search Screen
        self.pack_forget()

        # * Display App Screen Frame in Parent Frame(Container Frame) in Root App
        self.root_app.show_frame(self.root_app.app_screen_frame)
