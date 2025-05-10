import json
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import os

class JobApplicationManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Job Application Manager")
        self.root.geometry("1200x700") # Increased window size for better layout
        self.root.configure(bg="#1e1e1e")

        self.data_file = "applications.json"
        self.applications = []
        self.selected_item_id = None # To store the IID of the selected item in Treeview

        self.setup_style()
        self.load_data()
        self.create_widgets()
        self.sort_applications() # Initial sort
        self.update_treeview()

    def setup_style(self):
        style = ttk.Style(self.root)
        style.theme_use("default") #clam, alt, default, classic
        style.configure(".", background="#1e1e1e", foreground="white", fieldbackground="#2e2e2e")
        style.configure("TEntry", padding=5, fieldbackground="#2e2e2e", foreground="white")
        style.map("TEntry", fieldbackground=[("!disabled", "#2e2e2e")])
        style.configure("TLabel", padding=5)
        style.configure("TButton", background="#2e2e2e", foreground="white", padding=5)
        style.configure("TCombobox", fieldbackground="#2e2e2e", background="#2e2e2e", foreground="white", selectbackground="#2e2e2e", selectforeground="white", padding=5)
        style.map("TCombobox", fieldbackground=[("readonly", "#2e2e2e")], background=[("readonly", "#2e2e2e")])
        style.configure("Treeview", background="#2e2e2e", foreground="white", fieldbackground="#2e2e2e", rowheight=25) # Adjusted row height
        style.configure("Treeview.Heading", background="#1e1e1e", foreground="white", anchor="w", font=('Calibri', 10,'bold'))
        style.map("TButton", background=[("active", "#3e3e3e")])
        # Custom style for description button in Treeview
        style.configure("Desc.TButton", background="#4CAF50", foreground="white", padding=2)
        style.map("Desc.TButton", background=[("active", "#45a049")])


    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.applications = json.load(f)
            except json.JSONDecodeError:
                messagebox.showerror("Load Error", f"Error decoding JSON from {self.data_file}. Starting with an empty list.")
                self.applications = []
        # Ensure all applications have a unique ID, if not present (for backward compatibility)
        for i, app in enumerate(self.applications):
            if "id" not in app:
                app["id"] = i # Simple sequential ID for older data, can be improved
            if "timestamp" not in app: # Add timestamp if missing for sorting
                try:
                    # Attempt to parse date, default to now if invalid
                    dt_obj = datetime.strptime(app["date"], "%d/%m/%Y")
                except ValueError:
                    dt_obj = datetime.now()
                app["timestamp"] = dt_obj.timestamp()


    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.applications, f, indent=2)

    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Form frame (left side)
        form_frame_container = ttk.Frame(main_frame)
        form_frame_container.pack(side=tk.LEFT, fill=tk.Y, padx=(0,10))

        form_frame = ttk.LabelFrame(form_frame_container, text="Application Details", padding=10)
        form_frame.pack(expand=True, fill=tk.BOTH)

        entry_width = 40 # Increased width for input fields

        ttk.Label(form_frame, text="Application Date:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.date_entry = ttk.Entry(form_frame, width=entry_width)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.set_today_date()

        ttk.Label(form_frame, text="Company Name:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.company_entry = ttk.Entry(form_frame, width=entry_width)
        self.company_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Job Title:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.job_entry = ttk.Entry(form_frame, width=entry_width)
        self.job_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Job Description:").grid(row=3, column=0, padx=5, pady=5, sticky="nw")
        self.description_entry = tk.Text(form_frame, width=entry_width, height=28, wrap="word", bg="#2e2e2e", fg="white", insertbackground="white", borderwidth=1, relief="solid", font=('Calibri', 10))
        self.description_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        # Make description text widget expand with form_frame
        form_frame.grid_columnconfigure(1, weight=1)


        ttk.Label(form_frame, text="Application Status:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.status_var = tk.StringVar(value="pending")
        self.status_combo = ttk.Combobox(form_frame, textvariable=self.status_var,
                                         values=["pending", "submitted", "assessment", "interview", "offer", "rejected", "accepted", "withdrawn"], width=entry_width -2, state="readonly")
        self.status_combo.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        self.submit_btn = ttk.Button(form_frame, text="Add Application", command=self.add_or_edit_application)
        self.submit_btn.grid(row=5, column=0, columnspan=2, pady=15)

        # Treeview and controls frame (right side)
        tree_controls_frame = ttk.Frame(main_frame)
        tree_controls_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)


        controls_frame = ttk.Frame(tree_controls_frame)
        controls_frame.pack(pady=5, fill=tk.X)

        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(controls_frame, textvariable=self.search_var, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=(0,5))
        self.search_entry.bind("<KeyRelease>", self.filter_applications_event)

        search_btn = ttk.Button(controls_frame, text="Search", command=self.filter_applications_event)
        search_btn.pack(side=tk.LEFT, padx=5)

        delete_btn = ttk.Button(controls_frame, text="Remove Selected", command=self.remove_selected)
        delete_btn.pack(side=tk.LEFT, padx=5)

        ttk.Label(controls_frame, text="Sort by:").pack(side=tk.LEFT, padx=(10,5))
        self.sort_var = tk.StringVar(value="New to Old")
        self.sort_combo = ttk.Combobox(controls_frame, textvariable=self.sort_var,
                                       values=["New to Old", "Old to New", "Company A-Z", "Job Title A-Z", "Status A-Z"],
                                       width=15, state="readonly")
        self.sort_combo.pack(side=tk.LEFT, padx=5)
        self.sort_combo.bind("<<ComboboxSelected>>", self.sort_and_refresh_treeview)


        self.tree = ttk.Treeview(tree_controls_frame, columns=("index", "date", "company", "job", "desc_action", "status"), show="headings")
        self.tree.heading("index", text="ID")
        self.tree.heading("date", text="Date")
        self.tree.heading("company", text="Company")
        self.tree.heading("job", text="Job Title")
        self.tree.heading("desc_action", text="Description")
        self.tree.heading("status", text="Status")

        self.tree.column("index", width=30, anchor="center", stretch=tk.NO)
        self.tree.column("date", width=80, anchor="w")
        self.tree.column("company", width=150, anchor="w")
        self.tree.column("job", width=150, anchor="w")
        self.tree.column("desc_action", width=100, anchor="center") # For "View" button
        self.tree.column("status", width=100, anchor="w")

        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        self.tree.bind("<<TreeviewSelect>>", self.load_selected_to_form)
        self.tree.bind("<Double-1>", self.handle_tree_double_click)


    def handle_tree_double_click(self, event):
        item_id = self.tree.identify_row(event.y)
        column_id = self.tree.identify_column(event.x)

        if not item_id:
            return

        # Check if the click was on the "Description" column (now "desc_action")
        # The column index is #<col_num>, e.g., #5 for the 5th column (1-based)
        if column_id == "#5": # Column for description action
            item_values = self.tree.item(item_id, "values")
            # The actual description is not directly in values, retrieve from self.applications
            app_id = item_values[0] # Assuming index is the app_id shown in tree
            
            # Find the application by the ID displayed in the tree.
            # The 'app_id' in tree is the visual index + 1.
            # We need to find the original application based on a unique identifier if possible.
            # For now, let's assume the app_id from the tree helps find it if the list is static
            # Or better, store the original app's unique_id in the tree item itself.

            # Let's retrieve the original application by its unique ID
            # When inserting into treeview, we should store the app['id']
            original_app = None
            for app in self.applications:
                # Assuming the visual index in the tree can map back if we store the app['id']
                # For simplicity, if tree shows '1', it means index 0 of *currently displayed* items
                # This is tricky if the tree is filtered/sorted differently than self.applications
                # The best way is to store the unique app['id'] when inserting items.
                # We get the app_id from the tree's 'values'
                if self.tree.item(item_id, 'tags') and len(self.tree.item(item_id, 'tags')) > 0:
                    unique_app_id = self.tree.item(item_id, 'tags')[0]
                    if str(app.get("id")) == str(unique_app_id):
                        original_app = app
                        break
            
            if original_app:
                self.show_description_popup(original_app["description"])
            else:
                # Fallback if direct ID mapping fails (e.g. if tags not used properly)
                # This is less reliable if the tree order doesn't match self.applications order
                try:
                    # If 'app_id' is the visual index (1-based)
                    actual_index_in_current_view = int(app_id) -1
                    # Get the IID of the item at that visual index
                    all_items_in_tree = self.tree.get_children('')
                    if 0 <= actual_index_in_current_view < len(all_items_in_tree):
                        target_iid = all_items_in_tree[actual_index_in_current_view]
                        if self.tree.item(target_iid, 'tags') and len(self.tree.item(target_iid, 'tags')) > 0:
                             unique_app_id_fallback = self.tree.item(target_iid, 'tags')[0]
                             for app_fallback in self.applications:
                                 if str(app_fallback.get("id")) == str(unique_app_id_fallback):
                                     self.show_description_popup(app_fallback["description"])
                                     return
                except (ValueError, IndexError):
                    messagebox.showinfo("Info", "Could not retrieve description for this item using visual index.")


    def show_description_popup(self, description_text):
        popup = tk.Toplevel(self.root)
        popup.title("Job Description")
        popup.geometry("500x400")
        popup.configure(bg="#1e1e1e")

        # Add a frame for padding
        content_frame = ttk.Frame(popup, padding=10)
        content_frame.pack(expand=True, fill=tk.BOTH)

        desc_text_widget = tk.Text(content_frame, wrap="word", bg="#2e2e2e", fg="white", insertbackground="white", height=15, width=60, font=('Calibri', 10))
        desc_text_widget.insert(tk.END, description_text)
        desc_text_widget.config(state="disabled") # Read-only
        desc_text_widget.pack(expand=True, fill=tk.BOTH, pady=(0,10))

        close_btn = ttk.Button(content_frame, text="Close", command=popup.destroy)
        close_btn.pack()
        popup.transient(self.root) # Keep popup on top of the main window
        popup.grab_set() # Modal behavior
        self.root.wait_window(popup) # Wait for popup to close

    def set_today_date(self):
        if self.selected_item_id is None: # Only set today if not editing
            today = datetime.now().strftime("%d/%m/%Y")
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, today)

    def get_next_id(self):
        if not self.applications:
            return 1
        return max(app.get("id", 0) for app in self.applications) + 1

    def add_or_edit_application(self):
        date_str = self.date_entry.get()
        company = self.company_entry.get()
        job = self.job_entry.get()
        description = self.description_entry.get("1.0", tk.END).strip()
        status = self.status_var.get()

        if not all([date_str, company, job, description, status]): # status also required
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            dt_obj = datetime.strptime(date_str, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Error", "Date format must be DD/MM/YYYY.")
            return

        timestamp = dt_obj.timestamp()

        app_data = {
            "date": date_str,
            "company": company,
            "job": job,
            "description": description,
            "status": status,
            "timestamp": timestamp # Store timestamp for reliable sorting
        }

        if self.selected_item_id: # Editing existing
            # Find the application in self.applications using the stored unique ID
            unique_id_of_selected = self.tree.item(self.selected_item_id, 'tags')[0]
            found = False
            for i, app in enumerate(self.applications):
                if str(app.get("id")) == str(unique_id_of_selected):
                    app_data["id"] = app.get("id") # Preserve original ID
                    self.applications[i] = app_data
                    found = True
                    break
            if not found:
                messagebox.showerror("Error", "Could not find the application to update.")
                return
            
        else: # Adding new
            app_data["id"] = self.get_next_id() # Assign a new unique ID
            self.applications.append(app_data)

        self.save_data()
        self.sort_applications() # Sort after add/edit
        self.update_treeview(self.search_var.get()) # Preserve search filter
        self.clear_form()


    def load_selected_to_form(self, event=None):
        selected_items = self.tree.selection()
        if not selected_items:
            self.selected_item_id = None # Clear selection if nothing is selected
            self.submit_btn.config(text="Add Application")
            self.set_today_date() # Reset date to today if form is for new entry
            return

        self.selected_item_id = selected_items[0] # Store IID of the selected item
        
        # Retrieve the unique ID from the tag
        unique_app_id_tags = self.tree.item(self.selected_item_id, 'tags')
        if not unique_app_id_tags:
            messagebox.showerror("Error", "Selected item has no ID tag. Cannot load.")
            return
        unique_app_id = unique_app_id_tags[0]


        selected_app = None
        for app in self.applications:
            if str(app.get("id")) == str(unique_app_id):
                selected_app = app
                break
        
        if not selected_app:
            messagebox.showerror("Error", f"Could not find application with ID {unique_app_id} to load.")
            self.clear_form() # Clear form if app not found
            return

        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, selected_app["date"])
        self.company_entry.delete(0, tk.END)
        self.company_entry.insert(0, selected_app["company"])
        self.job_entry.delete(0, tk.END)
        self.job_entry.insert(0, selected_app["job"])
        self.description_entry.delete("1.0", tk.END)
        self.description_entry.insert("1.0", selected_app["description"])
        self.status_var.set(selected_app["status"])
        self.submit_btn.config(text="Edit Application")


    def clear_form(self):
        self.selected_item_id = None
        # self.date_entry.delete(0, tk.END) # Keep date as today or last entry
        self.set_today_date()
        self.company_entry.delete(0, tk.END)
        self.job_entry.delete(0, tk.END)
        self.description_entry.delete("1.0", tk.END)
        self.status_var.set("pending")
        self.submit_btn.config(text="Add Application")
        self.search_entry.focus() # Set focus back to search or a relevant field

    def remove_selected(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "No application selected to remove.")
            return

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to remove the selected application(s)?"):
            ids_to_remove = []
            for item_id in selected_items:
                unique_app_id_tags = self.tree.item(item_id, 'tags')
                if unique_app_id_tags:
                    ids_to_remove.append(unique_app_id_tags[0])
            
            self.applications = [app for app in self.applications if str(app.get("id")) not in ids_to_remove]
            
            self.save_data()
            self.update_treeview(self.search_var.get()) # Update tree with current filter
            self.clear_form()


    def sort_applications(self):
        sort_key = self.sort_var.get()
        reverse_order = False
        key_func = None

        if sort_key == "New to Old":
            reverse_order = True
            key_func = lambda app: app.get("timestamp", 0)
        elif sort_key == "Old to New":
            key_func = lambda app: app.get("timestamp", 0)
        elif sort_key == "Company A-Z":
            key_func = lambda app: app.get("company", "").lower()
        elif sort_key == "Job Title A-Z":
            key_func = lambda app: app.get("job", "").lower()
        elif sort_key == "Status A-Z":
            key_func = lambda app: app.get("status", "").lower()
        
        if key_func:
            self.applications.sort(key=key_func, reverse=reverse_order)


    def sort_and_refresh_treeview(self, event=None):
        self.sort_applications()
        self.update_treeview(self.search_var.get())


    def update_treeview(self, filter_text=""):
        self.tree.delete(*self.tree.get_children())
        
        # Filter applications first
        filtered_apps = self.applications
        if filter_text:
            filter_text = filter_text.lower()
            filtered_apps = [
                app for app in filtered_apps if
                filter_text in app.get("company", "").lower() or
                filter_text in app.get("job", "").lower() or
                filter_text in app.get("description", "").lower() or
                filter_text in app.get("status", "").lower()
            ]
        
        # Then display
        for i, app in enumerate(filtered_apps):
            # Use the app's unique ID as a tag for later retrieval
            app_unique_id = app.get("id", f"fallback_{i}") # Fallback if ID somehow missing
            # The first value in `values` will be the visual index for the "ID" column
            self.tree.insert("", tk.END, iid=f"item_{app_unique_id}", values=(
                i + 1, # Visual 1-based index
                app["date"],
                app["company"],
                app["job"],
                "View Details", # Placeholder text for the button/action column
                app["status"]
            ), tags=(str(app_unique_id),)) # Store unique app ID in tag


    def filter_applications_event(self, event=None): # Renamed to avoid conflict
        self.sort_applications() # Ensure sorting is applied before filtering/displaying
        self.update_treeview(self.search_var.get())


if __name__ == "__main__":
    root = tk.Tk()
    app = JobApplicationManager(root)
    root.mainloop()