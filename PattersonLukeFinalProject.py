# Luke Patterson 12/13/23

import tkinter as tk
from tkinter import messagebox, simpledialog, colorchooser

class MusicManifestApp:
    def __init__(self, master, user_type):
        # Initializes the application
        self.master = master
        self.master.title("Music Manifest")
        self.master.geometry("800x600")

        self.user_type = user_type
        self.current_user = None  # To store the current user's name
        self.customer_lists = {}
        self.record_stores = {}

        if self.user_type == "customer":
            self.current_user = simpledialog.askstring("Enter Your Name", "Enter Your Name:")

        self.image1 = tk.PhotoImage(file="American_Football.png")
        self.image2 = tk.PhotoImage(file="leaving_Meaning.png")

        self.create_dashboard()

    def create_dashboard(self):
    # Creates the main dashboard frame
    # Destroy the current dashboard frame if it exists
        if hasattr(self, 'dashboard_frame') and self.dashboard_frame:
            self.dashboard_frame.destroy()

        self.dashboard_frame = tk.Frame(self.master, bg="white")
        self.dashboard_frame.pack(expand=True, fill="both")

        tk.Label(self.dashboard_frame, text="Music Manifest", font=("Arial", 16, "bold"), bg="white").pack(pady=(20, 10))

        buttons = [
        ("Create List", self.show_create_list),
        ("View Lists", self.view_lists),
        ("Browse Inventory", self.browse_inventory),
        ("Showcase", self.showcase_images),
        ("Settings", self.show_settings),
        ("About", self.show_about),
        ("Exit", self.master.destroy)
    ]

        if self.user_type == "store":
            buttons = [
            ("Add to Inventory", self.show_add_to_inventory),
            ("View Inventory", self.view_inventory),
            ("Showcase", self.showcase_images),
            ("Settings", self.show_settings),
            ("About", self.show_about),
            ("Exit", self.master.destroy) 
        ]

        for text, command in buttons:
            button = tk.Button(self.dashboard_frame, text=text, command=command, font=("Arial", 12), padx=10, pady=5)
            button.pack(fill=tk.BOTH, expand=True)

        for i in range(2):
            self.dashboard_frame.columnconfigure(i, weight=1)
            self.dashboard_frame.rowconfigure(i + 1, weight=1)

    def show_create_list(self):
        # Shows the create list windows for customers
        if self.user_type == "customer":
            list_name = simpledialog.askstring("Create List", "Enter List Name:")
            if list_name:
                self.customer_lists[list_name] = []
                messagebox.showinfo("Success", f"List '{list_name}' created successfully.")
        else:
            messagebox.showinfo("Info", "Record stores cannot edit lists.")

    def view_lists(self):
        # Creates the view lists window for customers.

        view_lists_window = tk.Toplevel(self.master)
        view_lists_window.title("View Lists")

        tk.Label(view_lists_window, text=f"{self.current_user}'s Lists", font=("Arial", 16, "bold")).pack(pady=(20, 10))

        if self.user_type == "customer":
            for list_name in self.customer_lists:
                tk.Button(view_lists_window, text=list_name, command=lambda name=list_name: self.view_list_entries(name), font=("Arial", 12), padx=10, pady=5).pack()
        else:
            messagebox.showinfo("Info", "Record stores do not have customer lists.")

    def view_list_entries(self, list_name):
        # Allows users to view entries for specific lists
        view_entries_window = tk.Toplevel(self.master)
        view_entries_window.title(f"{list_name} - Entries")

        tk.Label(view_entries_window, text=f"Entries for {list_name}", font=("Arial", 14, "bold")).pack()

        for entry in self.customer_lists[list_name]:
            tk.Label(view_entries_window, text=f"  - {entry}", font=("Arial", 12)).pack()

        if self.user_type == "customer":
            tk.Button(view_entries_window, text="Add Item", command=lambda name=list_name: self.add_to_list(name), font=("Arial", 12)).pack()
            tk.Button(view_entries_window, text="Remove Item", command=lambda name=list_name: self.remove_from_list(name), font=("Arial", 12)).pack()

    def add_to_list(self, list_name):
        # Allows customers to add items to lists
        item = simpledialog.askstring("Add Item", "Enter Item:")
        if item:
            self.customer_lists[list_name].append(item)
            messagebox.showinfo("Success", f"Item '{item}' added to the list '{list_name}'.")

    def remove_from_list(self, list_name):
        # Allows customers to remove items from lists
        item = simpledialog.askstring("Remove Item", "Enter Item:")
        if item in self.customer_lists[list_name]:
            self.customer_lists[list_name].remove(item)
            messagebox.showinfo("Success", f"Item '{item}' removed from the list '{list_name}'.")
        else:
            messagebox.showerror("Error", f"Item '{item}' not found in the list '{list_name}'.")

    def show_settings(self):
        # Creates the settings window
        settings_window = tk.Toplevel(self.master)
        settings_window.title("Settings")

        tk.Label(settings_window, text="Background Color:", font=("Arial", 12)).pack()
        tk.Button(settings_window, text="Choose Color", command=self.choose_bg_color, font=("Arial", 12)).pack()

        tk.Label(settings_window, text="Font Style:", font=("Arial", 12)).pack()
        tk.Button(settings_window, text="Choose Font", command=self.choose_font_style, font=("Arial", 12)).pack()

        tk.Button(settings_window, text="Switch View", command=self.switch_view, font=("Arial", 12)).pack()

    def choose_bg_color(self):
        # Allows user to choose background color through colorchooser
        color = colorchooser.askcolor(title="Choose Background Color")[1]
        if color:
            self.master.configure(bg=color)
            self.dashboard_frame.configure(bg=color)
            messagebox.showinfo("Success", "Background color changed successfully.")

    def choose_font_style(self):
        # Allows user to choose font style through simpledialog
        font = simpledialog.askstring("Choose Font Style", "Enter font family and size (e.g., Arial 12):")
        if font:
            font_family, font_size = font.split()
            self.master.option_add("*Font", (font_family, int(font_size)))
            self.dashboard_frame.option_add("*Font", (font_family, int(font_size)))
            messagebox.showinfo("Success", "Font style changed successfully.")

    def switch_view(self):
        # Allows user to switch between customer and store view
        if self.user_type == "customer":
            new_type = "store"
        else:
            new_type = "customer"

        result = messagebox.askquestion("Switch View", f"Do you want to switch to {new_type} view?")
        if result == "yes":
            self.user_type = new_type
            self.create_dashboard()

    def show_add_to_inventory(self):
        # Shows the add to inventory window for stores
        if self.user_type == "store":
            store_name = simpledialog.askstring("Record Store", "Enter Store Name:")
            if store_name not in self.record_stores:
                self.record_stores[store_name] = []

            inventory_window = tk.Toplevel(self.master)
            inventory_window.title(f"{store_name} - Inventory Management")

            tk.Label(inventory_window, text=f"Inventory Management for {store_name}", font=("Arial", 16, "bold")).pack(pady=(20, 10))

            tk.Label(inventory_window, text="Title:", font=("Arial", 12)).pack()
            title_entry = tk.Entry(inventory_window, font=("Arial", 12))
            title_entry.pack()

            tk.Label(inventory_window, text="Artist:", font=("Arial", 12)).pack()
            artist_entry = tk.Entry(inventory_window, font=("Arial", 12))
            artist_entry.pack()

            tk.Label(inventory_window, text="Quantity:", font=("Arial", 12)).pack()
            quantity_entry = tk.Entry(inventory_window, font=("Arial", 12))
            quantity_entry.pack()

            tk.Button(inventory_window, text="Add to Inventory", command=lambda: self.add_to_inventory(store_name, title_entry.get(), artist_entry.get(), quantity_entry.get()), font=("Arial", 12)).pack()

            tk.Label(inventory_window, text="Current Inventory", font=("Arial", 14, "bold")).pack()

            for item in self.record_stores[store_name]:
                tk.Label(inventory_window, text=f"Title: {item['title']}, Artist: {item['artist']}, Quantity: {item['quantity']}", font=("Arial", 12)).pack()
        else:
            messagebox.showinfo("Info", "Customers cannot add to inventory.")

    def add_to_inventory(self, store_name, title, artist, quantity):
        # Allows stores to add items to inventory
        if title and artist and quantity.isdigit():
            item = {"title": title, "artist": artist, "quantity": int(quantity)}
            self.record_stores[store_name].append(item)
            messagebox.showinfo("Success", "Item added to inventory successfully.")
            self.show_add_to_inventory()
        else:
            messagebox.showerror("Error", "Invalid input. Please provide valid details.")

    def view_inventory(self):
        # Allows stores to view inventory
        view_inventory_window = tk.Toplevel(self.master)
        view_inventory_window.title("View Record Store Inventory")

        tk.Label(view_inventory_window, text="Record Store Inventory", font=("Arial", 16, "bold")).pack(pady=(20, 10))

        for store_name, inventory in self.record_stores.items():
            tk.Button(view_inventory_window, text=f"{store_name} Inventory", command=lambda name=store_name: self.show_store_inventory(name), font=("Arial", 12), padx=10, pady=5).pack()

    def show_store_inventory(self, store_name):
        # Shows the inventory for specific stores
        store_inventory_window = tk.Toplevel(self.master)
        store_inventory_window.title(f"{store_name} Inventory")

        tk.Label(store_inventory_window, text=f"Inventory for {store_name}", font=("Arial", 14, "bold")).pack()

        for item in self.record_stores[store_name]:
            tk.Label(store_inventory_window, text=f"Title: {item['title']}, Artist: {item['artist']}, Quantity: {item['quantity']}", font=("Arial", 12)).pack()

            if self.user_type == "customer":
                tk.Button(store_inventory_window, text="Add to My List", command=lambda item=item, store=store_name: self.add_to_customer_list(item, store), font=("Arial", 12)).pack()

    def add_to_customer_list(self, item, store_name):
        # Allows user to add item from store inventory to list
        list_name = simpledialog.askstring("Add to List", "Enter List Name:")
        if list_name in self.customer_lists:
            self.customer_lists[list_name].append(f"{item['title']} by {item['artist']} from {store_name}")
            messagebox.showinfo("Success", "Item added to your list successfully.")
        else:
            messagebox.showerror("Error", "List not found. Please enter a valid list name.")

    def browse_inventory(self):
        # Shows the browse inventory button for customers
        browse_window = tk.Toplevel(self.master)
        browse_window.title("Browse Record Store Inventory")

        tk.Label(browse_window, text="Browse Record Store Inventory", font=("Arial", 16, "bold")).pack(pady=(20, 10))

        for store_name, inventory in self.record_stores.items():
            tk.Button(browse_window, text=f"{store_name} Inventory", command=lambda name=store_name: self.show_store_inventory(name), font=("Arial", 12), padx=10, pady=5).pack()

    def create_showcase_button_frame(self):
        # Creates the Showcase button frame.
        
        showcase_button_frame = tk.Frame(self.dashboard_frame, bg="white")
        showcase_button_frame.pack(expand=True, fill="both")

        showcase_button = tk.Button(showcase_button_frame, text="Showcase", command=self.showcase_images, font=("Arial", 12), padx=10, pady=5)
        showcase_button.pack(fill=tk.BOTH, expand=True)

        return showcase_button_frame

    def showcase_images(self):
        # Opens a window to showcase images.
        showcase_window = tk.Toplevel(self.master)
        showcase_window.title("Showcase")

        # Display images in labels with alt text
        label1 = tk.Label(showcase_window, image=self.image1)
        label1.pack(pady=10)
        label1.text = "The album American Football by American Football"
        label1.config(compound=tk.BOTTOM)

        label2 = tk.Label(showcase_window, image=self.image2)
        label2.pack(pady=10)
        label2.text = "The album Leaving Meaning by Swans"
        label2.config(compound=tk.BOTTOM)

    def show_about(self):
        # Information in the "About" section
        about_window = tk.Toplevel(self.master)
        about_window.title("About Music Manifest")

        about_text = (
            "Music Manifest\n\n"
            "A simple application for managing music lists and record store inventory.\n\n"
            "Developed by Luke Patterson"
        )

        tk.Label(about_window, text=about_text, font=("Arial", 14)).pack(pady=(20, 10))

def start_program():
    # Entry point to start program
    choice = simpledialog.askstring("Music Manifest", "Are you a Customer or a Record Store?\nEnter 'customer' or 'store':").lower()
    if choice == "customer" or choice == "store":
        root = tk.Tk()
        app = MusicManifestApp(root, choice)
        root.mainloop()
    else:
        messagebox.showerror("Error", "Invalid choice. Please enter 'customer' or 'store'.")

if __name__ == "__main__":
    start_program()