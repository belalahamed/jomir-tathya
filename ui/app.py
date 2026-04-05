import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import tempfile
import webbrowser
import os
from bs4 import BeautifulSoup
from core.fetch_request import fetch_districts, fetch_blocks, fetch_mouzas, fetch_khatian, fetch_plot


class TableParser:
    """Parse HTML tables using BeautifulSoup - tolerates malformed HTML"""
    def __init__(self):
        self.tables = []
    
    def feed(self, html):
        """Parse HTML and extract all tables"""
        try:
            soup = BeautifulSoup(html, 'lxml')
            html_tables = soup.find_all('table')
            
            for table in html_tables:
                rows_list = []
                rows = table.find_all('tr')
                
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    if cells:
                        row_data = []
                        for cell in cells:
                            cell_text = cell.get_text(strip=True)
                            colspan = int(cell.get('colspan', 1))
                            row_data.append(cell_text)
                            for _ in range(colspan - 1):
                                row_data.append('')
                        
                        rows_list.append(row_data)
                
                if rows_list:
                    self.tables.append(rows_list)
        except Exception as e:
            print(f"Error parsing HTML with BeautifulSoup: {e}")
            self.tables = []


class BhumiApp:
    # Modern color scheme
    PRIMARY_COLOR = "#1e88e5"
    PRIMARY_DARK = "#1565c0"
    ACCENT_COLOR = "#00bcd4"
    SUCCESS_COLOR = "#4caf50"
    WARNING_COLOR = "#ff9800"
    BG_COLOR = "#f5f5f5"
    CARD_BG = "#ffffff"
    TEXT_COLOR = "#212121"
    LABEL_COLOR = "#616161"
    BORDER_COLOR = "#e0e0e0"
    BORDER_FOCUS = "#1e88e5"
    PLACEHOLDER_COLOR = "#b0bec5"
    
    def __init__(self, root):
        self.root = root
        self.root.title("Jomir Tathya")
        self.root.geometry("500x700")
        self.root.resizable(False, False)
        self.root.config(bg=self.BG_COLOR)
        
        self._setup_style()
        
        self.districts = []
        self.blocks = []
        self.mouzas = []
        self.district_codes = {}
        self.block_codes = {}
        self.mouza_codes = {}
        
        # Header
        header_frame = tk.Frame(self.root, bg=self.PRIMARY_COLOR)
        header_frame.pack(fill=tk.X)
        
        title_frame = tk.Frame(header_frame, bg=self.PRIMARY_COLOR)
        title_frame.pack(fill=tk.X, padx=15, pady=(15, 5))
        
        tk.Label(
            title_frame, text="🏞️ JOMIR TATHYA",
            font=("Segoe UI", 18, "bold"),
            bg=self.PRIMARY_COLOR, fg="white"
        ).pack(side=tk.LEFT)
        
        credit_frame = tk.Frame(header_frame, bg=self.PRIMARY_COLOR)
        credit_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        tk.Label(
            credit_frame, text="Made with ❤️ by Belal Ahamed",
            font=("Segoe UI", 10),
            bg=self.PRIMARY_COLOR, fg="#b3e5fc"
        ).pack(side=tk.LEFT)
        
        # Content
        content_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        card_frame = tk.Frame(content_frame, bg=self.CARD_BG)
        card_frame.pack(fill=tk.BOTH, expand=True)
        
        inner_frame = tk.Frame(card_frame, bg=self.CARD_BG, padx=20, pady=20)
        inner_frame.pack(fill=tk.BOTH, expand=True)
        
        self._create_section_label(inner_frame, "📍 Location Details", 0)
        self._create_field(inner_frame, "District:", 1, self._create_district_combo)
        self._create_field(inner_frame, "Block:", 2, self._create_block_combo)
        self._create_field(inner_frame, "Mouza:", 3, self._create_mouza_combo)
        
        type_label = tk.Label(inner_frame, text="Property Type:", font=("Segoe UI", 10, "bold"),
                            bg=self.CARD_BG, fg=self.TEXT_COLOR)
        type_label.grid(row=4, column=0, sticky=tk.W, pady=(20, 8))
        
        radio_frame = tk.Frame(inner_frame, bg=self.CARD_BG)
        radio_frame.grid(row=4, column=1, sticky=tk.W, pady=(20, 8))
        
        self.property_type = tk.StringVar(value="khatina")
        tk.Radiobutton(radio_frame, text="🏠 Khatina", variable=self.property_type,
                      value="khatina", command=self.on_property_type_changed,
                      font=("Segoe UI", 10), bg=self.CARD_BG, fg=self.TEXT_COLOR).pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(radio_frame, text="📦 Plot", variable=self.property_type,
                      value="plot", command=self.on_property_type_changed,
                      font=("Segoe UI", 10), bg=self.CARD_BG, fg=self.TEXT_COLOR).pack(side=tk.LEFT, padx=10)
        
        self._create_section_label(inner_frame, "📋 Property Details", 5)
        
        self.khatian_label = tk.Label(inner_frame, text="🏠 Khatian Number:", font=("Segoe UI", 10, "bold"),
                                     bg=self.CARD_BG, fg=self.PRIMARY_COLOR)
        self.khatian_label.grid(row=6, column=0, sticky=tk.W, pady=(12, 4), padx=(0, 10))
        
        self.khatian_var = tk.StringVar()
        self.khatian_entry = tk.Entry(inner_frame, textvariable=self.khatian_var,
                                     font=("Segoe UI", 10), width=35, bg=self.CARD_BG, fg=self.TEXT_COLOR, 
                                     relief=tk.SOLID, bd=1, insertwidth=2, insertbackground=self.PRIMARY_COLOR)
        self.khatian_entry.grid(row=6, column=1, sticky=(tk.W, tk.E), pady=(12, 4), padx=5)
        self.khatian_entry.config(highlightthickness=1, highlightbackground=self.BORDER_COLOR, highlightcolor=self.BORDER_FOCUS)
        self._add_entry_border(self.khatian_entry)
        
        self.bata_label = tk.Label(inner_frame, text="📍 Bata Number:", font=("Segoe UI", 10, "bold"),
                                  bg=self.CARD_BG, fg=self.PRIMARY_COLOR)
        self.bata_label.grid(row=7, column=0, sticky=tk.W, pady=(8, 4), padx=(0, 10))
        
        self.bata_var = tk.StringVar()
        self.bata_entry = tk.Entry(inner_frame, textvariable=self.bata_var,
                                  font=("Segoe UI", 10), width=35, bg=self.CARD_BG, fg=self.TEXT_COLOR, 
                                  relief=tk.SOLID, bd=1, insertwidth=2, insertbackground=self.PRIMARY_COLOR)
        self.bata_entry.grid(row=7, column=1, sticky=(tk.W, tk.E), pady=(8, 4), padx=5)
        self.bata_entry.config(highlightthickness=1, highlightbackground=self.BORDER_COLOR, highlightcolor=self.BORDER_FOCUS)
        self._add_entry_border(self.bata_entry)
        
        self.plot_label = tk.Label(inner_frame, text="📦 Plot Number:", font=("Segoe UI", 10, "bold"),
                                  bg=self.CARD_BG, fg=self.PRIMARY_COLOR)
        self.plot_label.grid(row=6, column=0, sticky=tk.W, pady=(12, 4), padx=(0, 10))
        self.plot_label.grid_remove()
        
        self.plot_var = tk.StringVar()
        self.plot_entry = tk.Entry(inner_frame, textvariable=self.plot_var,
                                  font=("Segoe UI", 10), width=35, bg=self.CARD_BG, fg=self.TEXT_COLOR, 
                                  relief=tk.SOLID, bd=1, insertwidth=2, insertbackground=self.PRIMARY_COLOR)
        self.plot_entry.grid(row=6, column=1, sticky=(tk.W, tk.E), pady=(12, 4), padx=5)
        self.plot_entry.config(highlightthickness=1, highlightbackground=self.BORDER_COLOR, highlightcolor=self.BORDER_FOCUS)
        self.plot_entry.grid_remove()
        self._add_entry_border(self.plot_entry)
        
        self.bata_plot_label = tk.Label(inner_frame, text="🔖 Bata Number:", font=("Segoe UI", 10, "bold"),
                                       bg=self.CARD_BG, fg=self.PRIMARY_COLOR)
        self.bata_plot_label.grid(row=7, column=0, sticky=tk.W, pady=(8, 4), padx=(0, 10))
        self.bata_plot_label.grid_remove()
        
        self.bata_plot_var = tk.StringVar()
        self.bata_plot_entry = tk.Entry(inner_frame, textvariable=self.bata_plot_var,
                                       font=("Segoe UI", 10), width=35, bg=self.CARD_BG, fg=self.TEXT_COLOR, 
                                       relief=tk.SOLID, bd=1, insertwidth=2, insertbackground=self.PRIMARY_COLOR)
        self.bata_plot_entry.grid(row=7, column=1, sticky=(tk.W, tk.E), pady=(8, 4), padx=5)
        self.bata_plot_entry.config(highlightthickness=1, highlightbackground=self.BORDER_COLOR, highlightcolor=self.BORDER_FOCUS)
        self.bata_plot_entry.grid_remove()
        self._add_entry_border(self.bata_plot_entry)
        
        button_frame = tk.Frame(inner_frame, bg=self.CARD_BG)
        button_frame.grid(row=8, column=0, columnspan=2, pady=25, sticky=(tk.W, tk.E))
        
        self.search_button = tk.Button(button_frame, text="🔍 Search", command=self.search_property,
                                      font=("Segoe UI", 11, "bold"), bg=self.PRIMARY_COLOR, fg="white",
                                      relief=tk.FLAT, bd=0, padx=25, pady=10, cursor="hand2")
        self.search_button.pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="🔄 Clear", command=self.clear_form,
                 font=("Segoe UI", 11, "bold"), bg=self.LABEL_COLOR, fg="white",
                 relief=tk.FLAT, bd=0, padx=25, pady=10, cursor="hand2").pack(side=tk.LEFT, padx=5)
        
        self.status_label = tk.Label(inner_frame, text="✓ Ready", font=("Segoe UI", 9),
                                    bg=self.CARD_BG, fg=self.SUCCESS_COLOR)
        self.status_label.grid(row=9, column=0, columnspan=2, pady=10)
        
        inner_frame.columnconfigure(1, weight=1)
        
        self.load_districts()
    
    def _setup_style(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TCombobox', font=('Segoe UI', 10), padding=8, relief=tk.FLAT, borderwidth=1)
    
    def _create_section_label(self, parent, text, row):
        label = tk.Label(parent, text=text, font=("Segoe UI", 11, "bold"),
                        bg=self.CARD_BG, fg=self.PRIMARY_COLOR, pady=10)
        label.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(15, 5))
    
    def _create_field(self, parent, label_text, row, create_widget_func):
        label = tk.Label(parent, text=label_text, font=("Segoe UI", 10, "bold"),
                        bg=self.CARD_BG, fg=self.TEXT_COLOR)
        label.grid(row=row, column=0, sticky=tk.W, pady=8)
        widget = create_widget_func(parent, row)
        widget.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=8)
        return widget
    
    def _create_district_combo(self, parent, row):
        self.district_var = tk.StringVar()
        combo = ttk.Combobox(parent, textvariable=self.district_var, state="readonly", width=35, font=("Segoe UI", 10))
        combo.bind("<<ComboboxSelected>>", self.on_district_selected)
        self.district_combo = combo
        return combo
    
    def _create_block_combo(self, parent, row):
        self.block_var = tk.StringVar()
        combo = ttk.Combobox(parent, textvariable=self.block_var, state="disabled", width=35, font=("Segoe UI", 10))
        combo.bind("<<ComboboxSelected>>", self.on_block_selected)
        self.block_combo = combo
        return combo
    
    def _create_mouza_combo(self, parent, row):
        self.mouza_var = tk.StringVar()
        combo = ttk.Combobox(parent, textvariable=self.mouza_var, state="disabled", width=35, font=("Segoe UI", 10))
        self.mouza_combo = combo
        return combo
    
    def _add_entry_border(self, entry):
        """Enhanced entry field styling with focus effects and visual feedback"""
        def on_focus_in(event):
            entry.config(bg=self.CARD_BG, highlightcolor=self.BORDER_FOCUS, highlightthickness=2)
            entry.config(relief=tk.SOLID, bd=1)
        
        def on_focus_out(event):
            entry.config(bg=self.CARD_BG, highlightcolor=self.BORDER_COLOR, highlightthickness=1)
            entry.config(relief=tk.SOLID, bd=1)
        
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
    
    def load_districts(self):
        self.status_label.config(text="Loading districts...", fg=self.WARNING_COLOR)
        self.district_combo.config(state="disabled")
        thread = threading.Thread(target=self._load_districts_thread)
        thread.daemon = True
        thread.start()
    
    def _load_districts_thread(self):
        try:
            self.districts = fetch_districts()
            self.district_codes = {d['eng_dname']: d['dcode'] for d in self.districts}
            district_names = [d['eng_dname'] for d in self.districts]
            self.root.after(0, lambda: self._update_district_combo(district_names))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to load districts: {str(e)}"))
    
    def _update_district_combo(self, district_names):
        self.district_combo['values'] = district_names
        self.district_combo.config(state="readonly")
        self.status_label.config(text="✓ Ready", fg=self.SUCCESS_COLOR)
    
    def on_district_selected(self, event=None):
        district_name = self.district_var.get()
        if not district_name:
            return
        self.status_label.config(text="Loading blocks...", fg=self.WARNING_COLOR)
        self.block_combo.config(state="disabled")
        self.mouza_combo.config(state="disabled")
        self.mouza_var.set("")
        self.block_var.set("")
        dist_code = self.district_codes[district_name]
        thread = threading.Thread(target=self._load_blocks_thread, args=(dist_code,))
        thread.daemon = True
        thread.start()
    
    def _load_blocks_thread(self, dist_code):
        try:
            self.blocks = fetch_blocks(dist_code)
            self.block_codes = {b['eng_bname']: b['blockKey']['bcode'] for b in self.blocks}
            block_names = [b['eng_bname'] for b in self.blocks]
            self.root.after(0, lambda: self._update_block_combo(block_names))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to load blocks: {str(e)}"))
    
    def _update_block_combo(self, block_names):
        self.block_combo['values'] = block_names
        self.block_combo.config(state="readonly")
        self.status_label.config(text="✓ Ready", fg=self.SUCCESS_COLOR)
    
    def on_block_selected(self, event=None):
        district_name = self.district_var.get()
        block_name = self.block_var.get()
        if not district_name or not block_name:
            return
        self.status_label.config(text="Loading mouzas...", fg=self.WARNING_COLOR)
        self.mouza_combo.config(state="disabled")
        self.mouza_var.set("")
        dist_code = self.district_codes[district_name]
        block_code = self.block_codes[block_name]
        thread = threading.Thread(target=self._load_mouzas_thread, args=(dist_code, block_code))
        thread.daemon = True
        thread.start()
    
    def _load_mouzas_thread(self, dist_code, block_code):
        try:
            self.mouzas = fetch_mouzas(dist_code, block_code)
            self.mouza_codes = {m['mouName']: m['moucode'] for m in self.mouzas}
            mouza_names = [m['mouName'] for m in self.mouzas]
            self.root.after(0, lambda: self._update_mouza_combo(mouza_names))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to load mouzas: {str(e)}"))
    
    def _update_mouza_combo(self, mouza_names):
        self.mouza_combo['values'] = mouza_names
        self.mouza_combo.config(state="readonly")
        self.status_label.config(text="✓ Ready", fg=self.SUCCESS_COLOR)
    
    def on_property_type_changed(self):
        show_khatian = self.property_type.get() == "khatina"
        self.khatian_label.grid() if show_khatian else self.khatian_label.grid_remove()
        self.khatian_entry.grid() if show_khatian else self.khatian_entry.grid_remove()
        self.bata_label.grid() if show_khatian else self.bata_label.grid_remove()
        self.bata_entry.grid() if show_khatian else self.bata_entry.grid_remove()
        self.plot_label.grid() if not show_khatian else self.plot_label.grid_remove()
        self.plot_entry.grid() if not show_khatian else self.plot_entry.grid_remove()
        self.bata_plot_label.grid() if not show_khatian else self.bata_plot_label.grid_remove()
        self.bata_plot_entry.grid() if not show_khatian else self.bata_plot_entry.grid_remove()
    
    def search_property(self):
        district_name = self.district_var.get()
        block_name = self.block_var.get()
        mouza_name = self.mouza_var.get()
        
        if not all([district_name, block_name, mouza_name]):
            messagebox.showwarning("Missing Data", "Please select District, Block, and Mouza")
            return
        
        property_type = self.property_type.get()
        if property_type == "khatina":
            khatian_no = self.khatian_var.get().strip()
            if not khatian_no:
                messagebox.showwarning("Missing Data", "Please enter Khatian Number")
                return
            bata_no = self.bata_var.get().strip()
        else:
            plot_no = self.plot_var.get().strip()
            if not plot_no:
                messagebox.showwarning("Missing Data", "Please enter Plot Number")
                return
            khatian_no = plot_no
            bata_no = self.bata_plot_var.get().strip()
        
        self.status_label.config(text="🔍 Searching...", fg=self.WARNING_COLOR)
        self.search_button.config(state="disabled")
        
        dist_code = self.district_codes[district_name]
        block_code = self.block_codes[block_name]
        mouza_code = self.mouza_codes[mouza_name]
        
        thread = threading.Thread(target=self._search_property_thread, args=(dist_code, block_code, mouza_code, khatian_no, bata_no, property_type))
        thread.daemon = True
        thread.start()
    
    def _search_property_thread(self, dist_code, block_code, mouza_code, number_no, bata_no, property_type):
        try:
            if property_type == "khatina":
                result = fetch_khatian(dist_code, block_code, mouza_code, number_no, bata_no)
            else:
                result = fetch_plot(dist_code, block_code, mouza_code, number_no, bata_no)
            self.root.after(0, lambda: self._show_search_result(result))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Search failed: {str(e)}"))
        finally:
            self.root.after(0, lambda: self.search_button.config(state="normal"))
    
    def _get_column_mapping(self, rows):
        if not rows:
            return []
        header_row = rows[0]
        num_cols = max(len(row) for row in rows)
        columns_with_data = set()
        for row in rows:
            for col_idx in range(num_cols):
                if col_idx < len(row) and row[col_idx].strip():
                    columns_with_data.add(col_idx)
        columns = []
        for col_idx in range(num_cols):
            if col_idx in columns_with_data or col_idx < len(header_row):
                header = header_row[col_idx].strip() if col_idx < len(header_row) else f"Col {col_idx}"
                if header:
                    columns.append((header, col_idx))
        return columns
    
    def _show_search_result(self, result):
        try:
            if not result or "Please Select" in result or "No data" in result.lower():
                messagebox.showwarning("No Data", "No property data found. Please verify your selection.")
                self.status_label.config(text="✓ Ready", fg=self.SUCCESS_COLOR)
                return
            parser = TableParser()
            parser.feed(result)
            tables = parser.tables
            if not tables:
                messagebox.showwarning("No Data", "No table data found in response.")
                self.status_label.config(text="✓ Ready", fg=self.SUCCESS_COLOR)
                return
            valid_tables = [t for t in tables if len(t) > 1]
            if not valid_tables:
                messagebox.showwarning("No Data", "No table with data rows found.")
                self.status_label.config(text="✓ Ready", fg=self.SUCCESS_COLOR)
                return
            rows = max(valid_tables, key=lambda t: len(t) * (len(t[0]) if t else 0))
            if not rows or len(rows) < 2:
                messagebox.showwarning("No Data", "Table is empty or contains only headers.")
                self.status_label.config(text="✓ Ready", fg=self.SUCCESS_COLOR)
                return
            columns = self._get_column_mapping(rows)
            if not columns:
                messagebox.showwarning("No Data", "No valid data columns found in table.")
                self.status_label.config(text="✓ Ready", fg=self.SUCCESS_COLOR)
                return
            
            result_window = tk.Toplevel(self.root)
            result_window.title("Property Details")
            result_window.geometry("1400x750")
            result_window.config(bg=self.BG_COLOR)
            
            header = tk.Frame(result_window, bg=self.PRIMARY_COLOR, height=50)
            header.pack(fill=tk.X)
            header.pack_propagate(False)
            tk.Label(header, text="📊 Property Details", font=("Segoe UI", 14, "bold"),
                    bg=self.PRIMARY_COLOR, fg="white", pady=10).pack()
            
            tree_frame = ttk.Frame(result_window)
            tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            vsb = ttk.Scrollbar(tree_frame, orient="vertical")
            hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
            
            col_headers = [col[0] for col in columns]
            tree = ttk.Treeview(tree_frame, columns=col_headers, show='tree headings',
                               yscrollcommand=vsb.set, xscrollcommand=hsb.set, height=25)
            vsb.config(command=tree.yview)
            hsb.config(command=tree.xview)
            
            for col_idx, (header, orig_idx) in enumerate(columns):
                max_width = len(header)
                for row in rows[1:]:
                    if orig_idx < len(row):
                        max_width = max(max_width, len(str(row[orig_idx]).strip()))
                col_width = min(max(max_width * 7 + 20, 80), 400)
                tree.heading(header, text=header)
                tree.column(header, width=col_width, anchor='w')
            
            data_row_count = 0
            for row in rows[1:]:
                values = []
                has_data = False
                for _, orig_idx in columns:
                    val = str(row[orig_idx]).strip() if orig_idx < len(row) else ''
                    values.append(val)
                    has_data = has_data or bool(val)
                if has_data:
                    data_row_count += 1
                    tag = 'oddrow' if data_row_count % 2 == 1 else 'evenrow'
                    tree.insert('', 'end', values=values, tags=(tag,))
            
            tree.tag_configure('oddrow', background='#f5f5f5')
            tree.tag_configure('evenrow', background='#ffffff')
            
            tree.grid(row=0, column=0, sticky='nsew')
            vsb.grid(row=0, column=1, sticky='ns')
            hsb.grid(row=1, column=0, sticky='ew')
            tree_frame.columnconfigure(0, weight=1)
            tree_frame.rowconfigure(0, weight=1)
            
            button_frame = tk.Frame(result_window, bg=self.BG_COLOR)
            button_frame.pack(fill="x", padx=10, pady=10)
            
            buttons = [
                ("📋 Copy HTML", lambda: self._copy_html(result)),
                ("💾 Save HTML", lambda: self._save_html(result)),
                ("📊 Copy Table", lambda: self._copy_table(rows, columns)),
                ("🌐 Browser", lambda: self._open_in_browser(result)),
                ("❌ Close", result_window.destroy)
            ]
            
            for text, cmd in buttons:
                btn = tk.Button(button_frame, text=text, command=cmd,
                              font=("Segoe UI", 9, "bold"),
                              bg=self.PRIMARY_COLOR if text != "❌ Close" else self.LABEL_COLOR,
                              fg="white", relief=tk.FLAT, bd=0, padx=12, pady=8, cursor="hand2")
                btn.pack(side=tk.LEFT, padx=3)
            
            info_text = f"📈 Records: {data_row_count} | Columns: {len(columns)} | Tables: {len(tables)}"
            tk.Label(result_window, text=info_text, font=("Segoe UI", 9),
                    bg=self.BG_COLOR, fg=self.LABEL_COLOR).pack(side=tk.BOTTOM, padx=10, pady=5)
            
            self.status_label.config(text="✓ Property loaded!", fg=self.SUCCESS_COLOR)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to display results: {str(e)}")
            self.status_label.config(text="✓ Ready", fg=self.SUCCESS_COLOR)
    
    def _save_html(self, html_content):
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".html",
                filetypes=[("HTML files", "*.html"), ("All files", "*.*")],
                initialfile="property_details.html"
            )
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                messagebox.showinfo("Success", f"HTML saved to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save HTML: {str(e)}")
    
    def _open_in_browser(self, html_content):
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
                full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Property Details</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        table {{ border-collapse: collapse; width: 100%; background-color: white; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        td, th {{ border: 1px solid #e0e0e0; padding: 12px; text-align: left; }}
        th {{ background-color: #1e88e5; color: white; font-weight: bold; }}
        tr:nth-child(even) {{ background-color: #f9f9f9; }}
        tr:hover {{ background-color: #f0f0f0; }}
    </style>
</head>
<body>
    {html_content}
</body>
</html>"""
                f.write(full_html)
                temp_file = f.name
            webbrowser.open('file://' + os.path.realpath(temp_file))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open in browser: {str(e)}")
    
    def _copy_html(self, html_content):
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(html_content)
            messagebox.showinfo("Success", "HTML copied to clipboard!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy: {str(e)}")
    
    def _copy_table(self, rows, columns):
        try:
            lines = ['\t'.join(col[0] for col in columns)]
            for row in rows[1:]:
                values = []
                for _, orig_idx in columns:
                    val = str(row[orig_idx]).strip() if orig_idx < len(row) else ''
                    values.append(val)
                if any(values):
                    lines.append('\t'.join(values))
            table_text = '\n'.join(lines)
            self.root.clipboard_clear()
            self.root.clipboard_append(table_text)
            data_count = len(lines) - 1
            messagebox.showinfo("Success", f"Table copied!\n({data_count} rows)")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy table: {str(e)}")
    
    def clear_form(self):
        self.district_var.set("")
        self.block_var.set("")
        self.mouza_var.set("")
        self.khatian_var.set("")
        self.bata_var.set("")
        self.plot_var.set("")
        self.property_type.set("khatina")
        self.block_combo.config(state="disabled")
        self.mouza_combo.config(state="disabled")
        self.status_label.config(text="✓ Form cleared", fg=self.SUCCESS_COLOR)

