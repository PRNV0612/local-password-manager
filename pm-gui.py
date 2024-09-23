'''The GUI is still under development'''


import tkinter as tk
from tkinter import messagebox
import utils.add
import utils.retrieve
import utils.generate
from utils.dbconfig import dbconfig
from getpass import getpass

# Global root Tkinter instance
root = tk.Tk()
root.title("Password Manager")
root.geometry("400x500")

# Utility function to validate the master password
def inputAndValidateMasterPassword(mp):
    hashed_mp = hashlib.sha256(mp.encode()).hexdigest()

    db = dbconfig()
    cursor = db.cursor()
    query = "SELECT * FROM pm.secrets"
    cursor.execute(query)
    result = cursor.fetchall()
    
    if not result:
        messagebox.showerror("Error", "Configuration not found. Please configure first.")
        return None

    if hashed_mp != result[0][0]:
        messagebox.showerror("Error", "Invalid Master Password")
        return None

    return [mp, result[0][1]]

# Dashboard with all options
def show_dashboard():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Password Manager", font=("Arial", 20)).pack(pady=20)

    tk.Button(root, text="Add Password", command=add_password).pack(pady=10)
    tk.Button(root, text="Retrieve Password", command=retrieve_password).pack(pady=10)
    tk.Button(root, text="Generate Password", command=generate_password).pack(pady=10)
    tk.Button(root, text="Configure Master Key", command=configure_master_key).pack(pady=10)

# Add Password Screen
def add_password():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Add New Password").pack(pady=5)

    tk.Label(root, text="Site Name").pack(pady=5)
    name_entry = tk.Entry(root)
    name_entry.pack(pady=5)

    tk.Label(root, text="Site URL").pack(pady=5)
    url_entry = tk.Entry(root)
    url_entry.pack(pady=5)

    tk.Label(root, text="Email (Optional)").pack(pady=5)
    email_entry = tk.Entry(root)
    email_entry.pack(pady=5)

    tk.Label(root, text="Username").pack(pady=5)
    username_entry = tk.Entry(root)
    username_entry.pack(pady=5)

    tk.Label(root, text="Master Password").pack(pady=5)
    master_password_entry = tk.Entry(root, show="*")
    master_password_entry.pack(pady=5)

    def add():
        name = name_entry.get()
        url = url_entry.get()
        email = email_entry.get() or ""
        username = username_entry.get()
        master_password = master_password_entry.get()

        if not (name and url and username and master_password):
            messagebox.showerror("Error", "All fields except Email are required.")
            return

        res = inputAndValidateMasterPassword(master_password)
        if res is not None:
            device_secret = res[1]
            utils.add.addEntry(master_password, device_secret, name, url, email, username)
            messagebox.showinfo("Success", "Password added successfully.")

    tk.Button(root, text="Add Password", command=add).pack(pady=10)
    tk.Button(root, text="Back", command=show_dashboard).pack(pady=10)

# Retrieve Password Screen
def retrieve_password():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Retrieve Password").pack(pady=5)

    tk.Label(root, text="Site Name (Optional)").pack(pady=5)
    name_entry = tk.Entry(root)
    name_entry.pack(pady=5)

    tk.Label(root, text="Site URL (Optional)").pack(pady=5)
    url_entry = tk.Entry(root)
    url_entry.pack(pady=5)

    tk.Label(root, text="Email (Optional)").pack(pady=5)
    email_entry = tk.Entry(root)
    email_entry.pack(pady=5)

    tk.Label(root, text="Username (Optional)").pack(pady=5)
    username_entry = tk.Entry(root)
    username_entry.pack(pady=5)

    tk.Label(root, text="Master Password").pack(pady=5)
    master_password_entry = tk.Entry(root, show="*")
    master_password_entry.pack(pady=5)

    def retrieve():
        search_criteria = {
            "sitename": name_entry.get(),
            "siteurl": url_entry.get(),
            "email": email_entry.get(),
            "username": username_entry.get()
        }
        search_criteria = {k: v for k, v in search_criteria.items() if v}

        if not search_criteria:
            messagebox.showerror("Error", "Provide at least one search criteria.")
            return

        master_password = master_password_entry.get()
        res = inputAndValidateMasterPassword(master_password)
        if res is not None:
            device_secret = res[1]
            utils.retrieve.retrieveEntries(master_password, device_secret, search_criteria, decryptPassword=True)

    tk.Button(root, text="Retrieve Password", command=retrieve).pack(pady=10)
    tk.Button(root, text="Back", command=show_dashboard).pack(pady=10)

# Generate Password Screen
def generate_password():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Generate Password").pack(pady=5)

    tk.Label(root, text="Password Length").pack(pady=5)
    length_entry = tk.Entry(root)
    length_entry.pack(pady=5)

    def generate():
        try:
            length = int(length_entry.get())
            password = utils.generate.generatePassword(length)
            messagebox.showinfo("Generated Password", f"Password: {password}")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for password length.")

    tk.Button(root, text="Generate", command=generate).pack(pady=10)
    tk.Button(root, text="Back", command=show_dashboard).pack(pady=10)

# Configure Master Key Screen
def configure_master_key():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Configure Master Key").pack(pady=5)

    tk.Label(root, text="Enter New Master Key").pack(pady=5)
    master_password_entry = tk.Entry(root, show="*")
    master_password_entry.pack(pady=5)

    def configure():
        mp = master_password_entry.get()
        if mp:
            # Logic to configure master key
            res = utils.dbconfig.configureMasterKey(mp)  # Placeholder for master key configuration
            if res:
                messagebox.showinfo("Success", "Master Key Configured.")
            else:
                messagebox.showerror("Error", "Failed to configure Master Key.")
        else:
            messagebox.showerror("Error", "Master Key is required.")

    tk.Button(root, text="Configure", command=configure).pack(pady=10)
    tk.Button(root, text="Back", command=show_dashboard).pack(pady=10)

# Start with the dashboard view
show_dashboard()

# Start the GUI event loop
root.mainloop()
