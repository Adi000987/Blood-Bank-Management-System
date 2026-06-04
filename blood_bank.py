import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import hashlib

# --- Database Connection ---
def connect_db():
    return mysql.connector.connect(
        host='YOUR HOST NAME HERE',
        user='YOUR USERNAME HERE',
        password='YOUR PASSWORD HERE',
        database='YOUR DATABASE NAME HERE'
    )

def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

is_admin_logged_in = False

# --- Core Functions ---
def admin_login(username, password, status_label, admin_tab, notebook):
    global is_admin_logged_in
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tbladmin WHERE UserName = %s", (username,))
    admin = cursor.fetchone()
    conn.close()
    if admin and admin["Password"] == hash_password(password):
        is_admin_logged_in = True
        status_label.config(text="Login successful!", foreground="lightgreen")
        load_admin_panel(admin_tab)
        notebook.tab(0, text="Admin Panel (Logged In)")
    else:
        status_label.config(text="Invalid credentials", foreground="red")

def register_donor(data, status_label, entries):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tblblooddonars 
        (FullName, MobileNumber, EmailId, Gender, Age, BloodGroup, Address, Message, status, Password) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 1, %s)
    """, data)
    conn.commit()
    conn.close()
    status_label.config(text="Donor registered successfully!", foreground="lightgreen")
    for e in entries:
        e.delete(0, tk.END)

def request_blood(data, status_label, entries):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tblbloodrequirer 
        (name, EmailId, ContactNumber, BloodRequirefor, Message) 
        VALUES (%s, %s, %s, %s, %s)
    """, data)
    conn.commit()
    conn.close()
    status_label.config(text="Blood request submitted!", foreground="lightgreen")
    for e in entries:
        e.delete(0, tk.END)

def view_donors(tree):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT FullName, MobileNumber, BloodGroup, Address FROM tblblooddonars WHERE status=1")
    rows = cursor.fetchall()
    conn.close()
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert("", tk.END, values=row)

def view_requests(tree):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name, EmailId, ContactNumber, BloodRequirefor, Message FROM tblbloodrequirer")
    rows = cursor.fetchall()
    conn.close()
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert("", tk.END, values=row)

def delete_donor(name, status_label, donors_tree):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tblblooddonars WHERE FullName = %s", (name,))
    conn.commit()
    conn.close()
    status_label.config(text=f"Donor '{name}' removed.", foreground="lightgreen")
    view_donors(donors_tree)

def delete_request(name, status_label, requests_tree):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tblbloodrequirer WHERE name = %s", (name,))
    conn.commit()
    conn.close()
    status_label.config(text=f"Request from '{name}' removed.", foreground="lightgreen")
    view_requests(requests_tree)

def search_donor(bg, tree, status_label):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT FullName, MobileNumber, Address FROM tblblooddonars WHERE BloodGroup=%s AND status=1", (bg,))
    results = cursor.fetchall()
    conn.close()
    tree.delete(*tree.get_children())
    if results:
        for row in results:
            tree.insert("", tk.END, values=row)
        status_label.config(text="")
    else:
        status_label.config(text="No donors found for this blood group.", foreground="orange")

# --- GUI Setup ---
root = tk.Tk()
root.title("Blood Bank Management System")
root.geometry("900x600")
root.configure(bg="#181c24")

style = ttk.Style()
style.theme_use('clam')
style.configure("TNotebook", background="#23272f", borderwidth=0)
style.configure("TNotebook.Tab", background="#2e3440", foreground="#fff", padding=[10, 5], font=('Arial', 12, 'bold'))
style.map("TNotebook.Tab", background=[("selected", "#4c566a")])
style.configure("TFrame", background="#23272f")
style.configure("TLabel", background="#23272f", foreground="#eceff4", font=('Arial', 11))
style.configure("TButton", background="#4c566a", foreground="#eceff4", font=('Arial', 11), padding=6, relief="flat")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both', padx=10, pady=10)

# --- Tabs ---
admin_tab = ttk.Frame(notebook)
register_tab = ttk.Frame(notebook)
request_tab = ttk.Frame(notebook)
search_tab = ttk.Frame(notebook)
exit_tab = ttk.Frame(notebook)

notebook.add(admin_tab, text="Admin Panel")
notebook.add(register_tab, text="Register Donor")
notebook.add(request_tab, text="Request Blood")
notebook.add(search_tab, text="Search Donor")
notebook.add(exit_tab, text="Exit")

# --- Admin Panel Tab ---
def load_admin_panel(tab):
    for widget in tab.winfo_children():
        widget.destroy()
    # Donors Table
    donors_frame = ttk.LabelFrame(tab, text="Donors")
    donors_frame.pack(fill='both', expand=True, padx=10, pady=5)
    donors_tree = ttk.Treeview(donors_frame, columns=("Name", "Mobile", "Group", "Address"), show="headings")
    for col in ("Name", "Mobile", "Group", "Address"):
        donors_tree.heading(col, text=col)
        donors_tree.column(col, width=120)
    donors_tree.pack(fill='both', expand=True)
    view_donors(donors_tree)

    # Delete Donor
    del_donor_frame = ttk.Frame(tab)
    del_donor_frame.pack(pady=5)
    ttk.Label(del_donor_frame, text="Delete Donor by Name:").pack(side='left')
    del_donor_entry = tk.Entry(del_donor_frame, fg="black", bg="white", font=('Arial', 11))
    del_donor_entry.pack(side='left', padx=5)
    del_donor_status = ttk.Label(del_donor_frame, text="")
    del_donor_status.pack(side='left', padx=5)
    ttk.Button(del_donor_frame, text="Delete", command=lambda: delete_donor(del_donor_entry.get(), del_donor_status, donors_tree)).pack(side='left')

    # Requests Table
    requests_frame = ttk.LabelFrame(tab, text="Blood Requests")
    requests_frame.pack(fill='both', expand=True, padx=10, pady=5)
    requests_tree = ttk.Treeview(requests_frame, columns=("Name", "Email", "Contact", "Group", "Message"), show="headings")
    for col in ("Name", "Email", "Contact", "Group", "Message"):
        requests_tree.heading(col, text=col)
        requests_tree.column(col, width=120)
    requests_tree.pack(fill='both', expand=True)
    view_requests(requests_tree)

    # Delete Request
    del_req_frame = ttk.Frame(tab)
    del_req_frame.pack(pady=5)
    ttk.Label(del_req_frame, text="Delete Request by Name:").pack(side='left')
    del_req_entry = tk.Entry(del_req_frame, fg="black", bg="white", font=('Arial', 11))
    del_req_entry.pack(side='left', padx=5)
    del_req_status = ttk.Label(del_req_frame, text="")
    del_req_status.pack(side='left', padx=5)
    ttk.Button(del_req_frame, text="Delete", command=lambda: delete_request(del_req_entry.get(), del_req_status, requests_tree)).pack(side='left')

    # Logout
    ttk.Button(tab, text="Logout", command=lambda: admin_logout(tab)).pack(pady=10)

def admin_logout(tab):
    global is_admin_logged_in
    is_admin_logged_in = False
    for widget in tab.winfo_children():
        widget.destroy()
    load_admin_login(tab)

def load_admin_login(tab):
    for widget in tab.winfo_children():
        widget.destroy()
    login_frame = ttk.Frame(tab)
    login_frame.pack(pady=60)
    ttk.Label(login_frame, text="Admin Login", font=('Arial', 16, 'bold')).pack(pady=10)
    # Admin login hint
    ttk.Label(login_frame, text="Username: admin", font=('Arial', 11, 'italic'), foreground="#a3be8c").pack()
    ttk.Label(login_frame, text="Password: Admin@1", font=('Arial', 11, 'italic'), foreground="#a3be8c").pack()
    ttk.Label(login_frame, text="").pack()
    ttk.Label(login_frame, text="Username:").pack()
    username_entry = tk.Entry(login_frame, fg="black", bg="white", font=('Arial', 11))
    username_entry.pack()
    ttk.Label(login_frame, text="Password:").pack()
    password_entry = tk.Entry(login_frame, show="*", fg="black", bg="white", font=('Arial', 11))
    password_entry.pack()
    status_label = ttk.Label(login_frame, text="")
    status_label.pack()
    ttk.Button(login_frame, text="Login", command=lambda: admin_login(username_entry.get(), password_entry.get(), status_label, tab, notebook)).pack(pady=10)

load_admin_login(admin_tab)

# --- Register Donor Tab ---
labels = ["Full Name", "Mobile", "Email", "Gender", "Age", "Blood Group", "Address", "Message", "Password"]
entries = []
reg_frame = ttk.Frame(register_tab)
reg_frame.pack(pady=30)
for label in labels:
    ttk.Label(reg_frame, text=label).pack(anchor='w')
    entry = tk.Entry(reg_frame, fg="black", bg="white", font=('Arial', 11))
    entry.pack(fill='x', padx=5, pady=2)
    entries.append(entry)
reg_status = ttk.Label(reg_frame, text="")
reg_status.pack()
ttk.Button(reg_frame, text="Register",
           command=lambda: register_donor(
               tuple(e.get() if i != 8 else hash_password(e.get()) for i, e in enumerate(entries)),
               reg_status, entries
           )).pack(pady=10)

# --- Request Blood Tab ---
req_labels = ["Name", "Email", "Contact", "Required Blood Group", "Message"]
req_entries = []
req_frame = ttk.Frame(request_tab)
req_frame.pack(pady=30)
for label in req_labels:
    ttk.Label(req_frame, text=label).pack(anchor='w')
    entry = tk.Entry(req_frame, fg="black", bg="white", font=('Arial', 11))
    entry.pack(fill='x', padx=5, pady=2)
    req_entries.append(entry)
req_status = ttk.Label(req_frame, text="")
req_status.pack()
ttk.Button(req_frame, text="Request",
           command=lambda: request_blood(tuple(e.get() for e in req_entries), req_status, req_entries)
          ).pack(pady=10)

# --- Search Donor Tab ---
search_frame = ttk.Frame(search_tab)
search_frame.pack(pady=20)
ttk.Label(search_frame, text="Enter Blood Group:").pack(side='left')
search_entry = tk.Entry(search_frame, fg="black", bg="white", font=('Arial', 11))
search_entry.pack(side='left', padx=5)
search_status = ttk.Label(search_frame, text="")
search_status.pack(side='left', padx=10)
search_tree = ttk.Treeview(search_tab, columns=("Name", "Mobile", "Address"), show="headings")
for col in ("Name", "Mobile", "Address"):
    search_tree.heading(col, text=col)
    search_tree.column(col, width=150)
search_tree.pack(fill='both', expand=True, padx=10, pady=10)
ttk.Button(search_frame, text="Search", command=lambda: search_donor(search_entry.get(), search_tree, search_status)).pack(side='left', padx=5)

# --- Exit Tab ---
exit_frame = ttk.Frame(exit_tab)
exit_frame.pack(expand=True)
ttk.Label(exit_frame, text="Click below to exit the application.", font=('Arial', 14)).pack(pady=20)
ttk.Button(exit_frame, text="Exit Application", command=root.destroy).pack(pady=10)

root.mainloop()
