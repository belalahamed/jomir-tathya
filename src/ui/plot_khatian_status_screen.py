import customtkinter as ctk
import threading
import multiprocessing
import webview
from tkinterweb import HtmlFrame
from PIL import Image

from ..api import fetch_khatian_mutation_status, fetch_plot_mutation_status
from assets import back_icon as BACK_ICON
from .location_entry_form import LocationEntryForm


def _run_webview_viewer(html_content, should_print=False):
    """Helper function to launch pywebview in its own process/main thread."""
    window = webview.create_window(
        "Mutation Status Details", html=html_content, width=1000, height=800
    )

    if should_print:
        webview.start(lambda: window.evaluate_js("window.print()"))
    else:
        webview.start()


class PlotKhatianStatusScreen(ctk.CTkFrame):
    """
    * Mutation Status Screen Frame UI
    """

    def __init__(self, parent_frame, root_app, session_cookies=None):
        super().__init__(parent_frame, fg_color="#F8F9FA", corner_radius=0)

        # * State Variables
        self.session_cookies = session_cookies
        self.property_type_var = ctk.StringVar(value="Plot")
        self.current_html = ""
        self.parent_frame = parent_frame
        self.root_app = root_app

        # * Grid Layout Configuration
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # * ============== Form Container frame =========== * #
        self.form_frame = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            width=420,
            corner_radius=15,
            border_width=1,
            border_color="#E8E8E8",
        )
        self.form_frame.grid(column=0, row=0, sticky="nsew", padx=15, pady=15)
        self.form_frame.grid_columnconfigure((0, 1), weight=1)
        self.form_frame.grid_rowconfigure(10, weight=1)

        # * ============== Header Frame =========== * #
        self.header_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.header_frame.grid(
            row=0, column=0, columnspan=2, sticky="nsew", padx=15, pady=(15, 10)
        )
        self.header_frame.grid_columnconfigure(0, weight=1)

        # Header Elements
        self.back_btn_img = ctk.CTkImage(
            light_image=Image.open(BACK_ICON), size=(24, 24)
        )
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

        self.header_label = ctk.CTkLabel(
            self.header_frame,
            text="⏱️ Mutation Status",
            font=("Calibri", 24, "bold"),
            text_color="#0066CC",
        )
        self.header_label.grid(row=0, column=0, sticky="w")

        # * ============== Location Form =========== * #
        self.location_entry_form = LocationEntryForm(self.form_frame, self)
        self.location_entry_form.grid(
            row=1, column=0, columnspan=2, sticky="nsew", padx=15, pady=(15, 10)
        )

        # * ============== Property Type Selection =========== * #
        self.details_label = ctk.CTkLabel(
            self.form_frame,
            text="📝 Search Criteria",
            font=("Calibri", 16, "bold"),
            text_color="#0066CC",
            fg_color="#F8F9FA",
            corner_radius=8,
        )
        self.details_label.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="nsew",
            padx=15,
            pady=(15, 10),
            ipady=10,
        )

        self.type_label = ctk.CTkLabel(
            self.form_frame, text="Search By:", font=("Calibri", 14, "bold")
        )
        self.type_label.grid(row=3, column=0, sticky="w", padx=15, pady=(10, 5))

        self.radio_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.radio_frame.grid(row=3, column=1, sticky="ew", padx=15, pady=(10, 5))
        self.radio_frame.grid_columnconfigure((0, 1), weight=1)

        self.plot_radio = ctk.CTkRadioButton(
            self.radio_frame,
            text="Plot",
            variable=self.property_type_var,
            value="Plot",
            command=self._on_type_change,
        )
        self.plot_radio.grid(row=0, column=0, sticky="w")

        self.khatian_radio = ctk.CTkRadioButton(
            self.radio_frame,
            text="Khatian",
            variable=self.property_type_var,
            value="Khatian",
            command=self._on_type_change,
        )
        self.khatian_radio.grid(row=0, column=1, sticky="w")

        # * ============== Input Fields =========== * #
        self.input_label = ctk.CTkLabel(
            self.form_frame, text="Plot No:", font=("Calibri", 14, "bold")
        )
        self.input_label.grid(row=4, column=0, sticky="w", padx=15, pady=(10, 5))

        self.entries_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.entries_frame.grid(row=4, column=1, sticky="nsew", padx=15, pady=(10, 5))
        self.entries_frame.grid_columnconfigure((0, 1), weight=1)

        self.first_entry = ctk.CTkEntry(
            self.entries_frame, placeholder_text="Plot No", height=40
        )
        self.first_entry.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        self.second_entry = ctk.CTkEntry(
            self.entries_frame, placeholder_text="Bata No", height=40
        )
        self.second_entry.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

        # * ============== Buttons =========== * #
        self.buttons_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.buttons_frame.grid(
            row=5, column=0, columnspan=2, sticky="nsew", padx=15, pady=(15, 10)
        )
        self.buttons_frame.grid_columnconfigure((0, 1), weight=1)

        self.clear_btn = ctk.CTkButton(
            self.buttons_frame,
            text="🧹 Clear",
            height=45,
            fg_color="#6C757D",
            command=self._clear_form,
        )
        self.clear_btn.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        self.search_btn = ctk.CTkButton(
            self.buttons_frame,
            text="🔎 Search",
            height=45,
            fg_color="#28A745",
            command=self._on_search,
        )
        self.search_btn.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

        # Status Label
        self.status_message_label = ctk.CTkLabel(
            self.form_frame,
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

        # * ============== Results Panel =========== * #
        self.results_frame = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=15,
            border_width=1,
            border_color="#E8E8E8",
        )
        self.results_frame.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
        self.results_frame.grid_columnconfigure(0, weight=1)
        self.results_frame.grid_rowconfigure(1, weight=1)

        self.results_label = ctk.CTkLabel(
            self.results_frame,
            text="🔍 Mutation Status Results",
            font=("Calibri", 18, "bold"),
            text_color="#0066CC",
        )
        self.results_label.grid(row=0, column=0, sticky="nsew", padx=15, pady=(15, 10))

        self.results_browser = HtmlFrame(self.results_frame)
        self.results_browser.grid(row=1, column=0, sticky="nsew", padx=15, pady=10)

        self.res_buttons_frame = ctk.CTkFrame(
            self.results_frame, fg_color="transparent"
        )
        self.res_buttons_frame.grid(
            row=2, column=0, sticky="nsew", padx=15, pady=(10, 15)
        )
        self.res_buttons_frame.grid_columnconfigure((0, 1), weight=1)

        self.open_browser_btn = ctk.CTkButton(
            self.res_buttons_frame,
            text="🌐 Open in Browser",
            height=40,
            fg_color="#17A2B8",
            command=self._on_open_in_browser,
        )
        self.open_browser_btn.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        self.save_pdf_btn = ctk.CTkButton(
            self.res_buttons_frame,
            text="💾 Save as PDF",
            height=40,
            fg_color="#0066CC",
            command=self._on_save_as_pdf,
        )
        self.save_pdf_btn.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

    def _on_type_change(self):
        p_type = self.property_type_var.get()
        self.input_label.configure(text=f"{p_type} No:")
        self.first_entry.configure(placeholder_text=f"{p_type} No")
        self.first_entry.delete(0, "end")
        self.second_entry.delete(0, "end")

    def _clear_form(self):
        self.first_entry.delete(0, "end")
        self.second_entry.delete(0, "end")
        self.results_browser.load_html("")
        self.current_html = ""
        self.status_message_label.configure(text="Ready", text_color="#28A745")

    def _display_results(self, html_content):
        styled_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
            <style>
                body {{ font-family: 'Segoe UI', sans-serif; padding: 20px; font-size: 16px; }}
                .table {{ margin-top: 20px; }}
                th {{ background-color: #f8f9fa; }}
            </style>
        </head>
        <body>{html_content}</body>
        </html>
        """
        self.current_html = styled_html
        self.results_browser.load_html(styled_html)

    def _on_open_in_browser(self):
        self._launch_webview(should_print=False)

    def _on_save_as_pdf(self):
        self._launch_webview(should_print=True)

    def _launch_webview(self, should_print=False):
        if not self.current_html or len(self.current_html.strip()) < 100:
            return
        p = multiprocessing.Process(
            target=_run_webview_viewer,
            args=(self.current_html, should_print),
            daemon=True,
        )
        p.start()

    def _on_search(self):
        if not all(
            [
                self.location_entry_form.selected_district_code,
                self.location_entry_form.selected_block_code,
                self.location_entry_form.selected_mouza_code,
            ]
        ):
            self.status_message_label.configure(
                text="❌ Select Location Details", text_color="red"
            )
            return

        main_no = self.first_entry.get().strip()
        if not main_no:
            self.status_message_label.configure(
                text=f"❌ Enter {self.property_type_var.get()} No", text_color="red"
            )
            return

        bata_no = self.second_entry.get().strip()
        self.status_message_label.configure(text="Searching...", text_color="#0066CC")
        self.search_btn.configure(state="disabled")

        threading.Thread(
            target=self.__search_thread, args=(main_no, bata_no), daemon=True
        ).start()

    def __search_thread(self, main_no, bata_no):
        try:
            cookies_str = self.session_cookies if self.session_cookies else ""

            if self.property_type_var.get() == "Plot":
                html_result = fetch_plot_mutation_status(
                    cookies_str,
                    self.location_entry_form.selected_district_code,
                    self.location_entry_form.selected_block_code,
                    self.location_entry_form.selected_mouza_code,
                    main_no,
                    bata_no,
                )
            else:
                html_result = fetch_khatian_mutation_status(
                    cookies_str,
                    self.location_entry_form.selected_district_code,
                    self.location_entry_form.selected_block_code,
                    self.location_entry_form.selected_mouza_code,
                    main_no,
                    bata_no,
                )

            self.after(0, lambda: self._display_results(html_result))
            self.after(
                0,
                lambda: self.status_message_label.configure(
                    text="✅ Search Completed", text_color="#28A745"
                ),
            )

        except Exception as e:
            self.after(
                0,
                lambda: self.status_message_label.configure(
                    text="❌ Search Failed", text_color="red"
                ),
            )
        finally:
            self.after(0, lambda: self.search_btn.configure(state="normal"))

    def _open_app_screen(self):
        self.pack_forget()
        self.root_app.show_frame(self.root_app.app_screen_frame)
