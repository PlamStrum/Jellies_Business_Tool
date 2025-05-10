import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Import database connection utility
def get_connection():
    from db_config import get_connection as _gc
    return _gc()

class JelliesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Jellies Business Tool")
        self.root.geometry("640x700")

        # --- Section 1: Customer Data ---
        cust_frame = ttk.LabelFrame(root, text="Customer Data")
        cust_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(cust_frame, text="Client Name:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.client_name_var = tk.StringVar()
        ttk.Entry(cust_frame, textvariable=self.client_name_var).grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(cust_frame, text="Client Address:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.client_address_var = tk.StringVar()
        ttk.Entry(cust_frame, textvariable=self.client_address_var).grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(cust_frame, text="City:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.city_var = tk.StringVar()
        ttk.Entry(cust_frame, textvariable=self.city_var).grid(row=2, column=1, padx=5, pady=2)

        # --- Section 2: Inventory ---
        inv_frame = ttk.LabelFrame(root, text="Inventory")
        inv_frame.pack(fill="x", padx=10, pady=5)

        # Inventory header labels
        header = ttk.Frame(inv_frame)
        header.pack(fill="x", pady=2)
        ttk.Label(header, text="Product Name", width=20).pack(side="left", padx=2)
        ttk.Label(header, text="Price", width=10).pack(side="left", padx=2)
        ttk.Label(header, text="Shop", width=15).pack(side="left", padx=2)
        ttk.Label(header, text="Purchase Date (DD/MM/YYYY)", width=30).pack(side="left", padx=2)

        # Container for dynamic product rows
        self.inventory_rows = []
        self.inv_container = ttk.Frame(inv_frame)
        self.inv_container.pack(fill="x")

        add_btn = ttk.Button(inv_frame, text="+ Add Product", command=self.add_inventory_row)
        add_btn.pack(pady=5)

        # Add an initial inventory row
        self.add_inventory_row()

        # --- Section 3: Business Index ---
        biz_frame = ttk.LabelFrame(root, text="Business Index")
        biz_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(biz_frame, text="Transport Method:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.transport_var = tk.StringVar()
        ttk.Entry(biz_frame, textvariable=self.transport_var).grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(biz_frame, text="Employee Name:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.employee_var = tk.StringVar()
        ttk.Entry(biz_frame, textvariable=self.employee_var).grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(biz_frame, text="Geographical Data:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.geo_var = tk.StringVar()
        ttk.Entry(biz_frame, textvariable=self.geo_var).grid(row=2, column=1, padx=5, pady=2)

        ttk.Label(biz_frame, text="Additional Notes:").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.notes_var = tk.StringVar()
        ttk.Entry(biz_frame, textvariable=self.notes_var).grid(row=3, column=1, padx=5, pady=2)

        # --- Submit Button ---
        submit_btn = ttk.Button(root, text="Submit", command=self.submit_data)
        submit_btn.pack(pady=15)

    def add_inventory_row(self):
        """Adds a new row of entry widgets for Product Name, Price, Shop, and Purchase Date."""
        row_frame = ttk.Frame(self.inv_container)
        row_frame.pack(fill="x", pady=2)

        # Product Name
        name_var = tk.StringVar()
        ttk.Entry(row_frame, textvariable=name_var, width=20).pack(side="left", padx=2)
        # Product Price
        price_var = tk.StringVar()
        ttk.Entry(row_frame, textvariable=price_var, width=10).pack(side="left", padx=2)
        # Shop Name
        shop_var = tk.StringVar()
        ttk.Entry(row_frame, textvariable=shop_var, width=15).pack(side="left", padx=2)
        # Purchase Date
        date_var = tk.StringVar()
        ttk.Entry(row_frame, textvariable=date_var, width=12).pack(side="left", padx=2)

        self.inventory_rows.append((name_var, price_var, shop_var, date_var))

    def submit_data(self):
        """Reads form fields, inserts into DB, and resets the form on success."""
        # Gather customer data
        client = self.client_name_var.get().strip()
        address = self.client_address_var.get().strip()
        city = self.city_var.get().strip()

        if not (client and address and city):
            messagebox.showerror("Validation Error", "Please fill in all customer fields.")
            return

        cnx = None
        try:
            cnx = get_connection()
            cursor = cnx.cursor()

            # 1) Insert CustomerData
            insert_cust = (
                "INSERT INTO CustomerData (client_name, client_address, city) VALUES (%s, %s, %s)"
            )
            cursor.execute(insert_cust, (client, address, city))
            job_id = cursor.lastrowid

            # 2) Insert Inventory rows
            insert_inv = (
                "INSERT INTO Inventory (job_id, product_name, product_price, shop_name, purchase_date)"
                " VALUES (%s, %s, %s, %s, %s)"
            )
            for name_var, price_var, shop_var, date_var in self.inventory_rows:
                name = name_var.get().strip()
                price = price_var.get().strip()
                shop = shop_var.get().strip()
                date_str = date_var.get().strip()
                if name and price and shop and date_str:
                    # Validate and convert date format
                    try:
                        date_obj = datetime.strptime(date_str, "%d/%m/%Y").date()
                    except ValueError:
                        messagebox.showerror("Date Error", f"Invalid date format for '{date_str}'. Use DD/MM/YYYY.")
                        return
                    cursor.execute(insert_inv, (job_id, name, price, shop, date_obj))

            # 3) Insert BusinessIndex
            transport = self.transport_var.get().strip()
            employee = self.employee_var.get().strip()
            geo = self.geo_var.get().strip()
            notes = self.notes_var.get().strip()
            insert_biz = (
                "INSERT INTO BusinessIndex (job_id, transport_method, employee_name, geo_data, additional_notes)"
                " VALUES (%s, %s, %s, %s, %s)"
            )
            cursor.execute(insert_biz, (job_id, transport, employee, geo, notes))

            # Commit transaction
            cnx.commit()
            messagebox.showinfo("Success", "Data submitted successfully!")

            # Reset form
            self.client_name_var.set("")
            self.client_address_var.set("")
            self.city_var.set("")
            self.transport_var.set("")
            self.employee_var.set("")
            self.geo_var.set("")
            self.notes_var.set("")

            # Clear and re-add one inventory row
            for widget in self.inv_container.winfo_children():
                widget.destroy()
            self.inventory_rows.clear()
            self.add_inventory_row()

        except Exception as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            if cnx and cnx.is_connected():
                cnx.close()

if __name__ == '__main__':
    root = tk.Tk()
    app = JelliesApp(root)
    root.mainloop()
