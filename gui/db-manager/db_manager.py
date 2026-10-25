"""
DB Manager - A lightweight SQL Server Management Studio-style GUI for SQLite.

Features:
  - Create / open a database file
  - Browse tables in a sidebar
  - View, add, edit, and delete rows in any table (spreadsheet-style grid)
  - Create and drop tables through a dialog (column name / type / PK / NOT NULL)
  - Run arbitrary SQL in a query editor and see results or rows-affected

Built entirely on Python's standard library (tkinter + sqlite3), so it runs
anywhere Python runs, no extra installs needed.

To point this at a different DBMS (PostgreSQL, MySQL, SQL Server, etc.)
instead of SQLite, swap out the `sqlite3.connect(...)` call and the
PRAGMA-based helpers (`get_tables`, `get_columns`) for the equivalent
driver (psycopg2, mysql-connector-python, pyodbc, ...) and information-
schema queries. The UI layer does not need to change.

"""

import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog


COLUMN_TYPES = ["INTEGER", "TEXT", "REAL", "NUMERIC", "BLOB"]


class ColumnRow:
    """One row of widgets in the Create Table dialog representing a column."""

    def __init__(self, parent, row_index, remove_callback):
        self.frame = parent
        self.name_var = tk.StringVar()
        self.type_var = tk.StringVar(value="TEXT")
        self.pk_var = tk.BooleanVar()
        self.notnull_var = tk.BooleanVar()

        self.name_entry = ttk.Entry(parent, textvariable=self.name_var, width=18)
        self.name_entry.grid(row=row_index, column=0, padx=4, pady=3)

        self.type_combo = ttk.Combobox(
            parent, textvariable=self.type_var, values=COLUMN_TYPES,
            width=10, state="readonly"
        )
        self.type_combo.grid(row=row_index, column=1, padx=4, pady=3)

        self.pk_check = ttk.Checkbutton(parent, text="PK", variable=self.pk_var)
        self.pk_check.grid(row=row_index, column=2, padx=4, pady=3)

        self.notnull_check = ttk.Checkbutton(
            parent, text="NOT NULL", variable=self.notnull_var
        )
        self.notnull_check.grid(row=row_index, column=3, padx=4, pady=3)

        self.remove_btn = ttk.Button(
            parent, text="✕", width=3,
            command=lambda: remove_callback(self)
        )
        self.remove_btn.grid(row=row_index, column=4, padx=4, pady=3)

    def destroy(self):
        for w in (self.name_entry, self.type_combo, self.pk_check,
                   self.notnull_check, self.remove_btn):
            w.destroy()

    def to_sql(self):
        name = self.name_var.get().strip()
        if not name:
            return None
        col_type = self.type_var.get()
        parts = [f'"{name}"', col_type]
        if self.pk_var.get():
            parts.append("PRIMARY KEY")
        if self.notnull_var.get() and not self.pk_var.get():
            parts.append("NOT NULL")
        return " ".join(parts)


class CreateTableDialog(tk.Toplevel):
    def __init__(self, master, on_created):
        super().__init__(master)
        self.title("Create Table")
        self.resizable(False, False)
        self.on_created = on_created
        self.rows = []

        top = ttk.Frame(self, padding=10)
        top.pack(fill="both", expand=True)

        name_frame = ttk.Frame(top)
        name_frame.pack(fill="x", pady=(0, 10))
        ttk.Label(name_frame, text="Table name:").pack(side="left")
        self.table_name_var = tk.StringVar()
        ttk.Entry(name_frame, textvariable=self.table_name_var, width=30).pack(
            side="left", padx=6
        )

        self.cols_frame = ttk.Frame(top)
        self.cols_frame.pack(fill="both", expand=True)

        header = ttk.Frame(top)
        header.pack(fill="x")

        btns = ttk.Frame(top)
        btns.pack(fill="x", pady=(10, 0))
        ttk.Button(btns, text="+ Add Column", command=self.add_row).pack(side="left")
        ttk.Button(btns, text="Create Table", command=self.create_table).pack(
            side="right"
        )
        ttk.Button(btns, text="Cancel", command=self.destroy).pack(
            side="right", padx=6
        )

        # header labels for the column grid
        for i, text in enumerate(["Column", "Type", "PK", "Not Null", ""]):
            ttk.Label(self.cols_frame, text=text, font=("", 9, "bold")).grid(
                row=0, column=i, padx=4
            )

        self._next_row = 1
        self.add_row()
        self.add_row()

    def add_row(self):
        row = ColumnRow(self.cols_frame, self._next_row, self.remove_row)
        self._next_row += 1
        self.rows.append(row)

    def remove_row(self, row):
        if len(self.rows) <= 1:
            return
        row.destroy()
        self.rows.remove(row)

    def create_table(self):
        table_name = self.table_name_var.get().strip()
        if not table_name:
            messagebox.showerror("Error", "Please enter a table name.")
            return
        col_defs = [r.to_sql() for r in self.rows]
        col_defs = [c for c in col_defs if c]
        if not col_defs:
            messagebox.showerror("Error", "Please define at least one column.")
            return
        sql = f'CREATE TABLE "{table_name}" ({", ".join(col_defs)})'
        try:
            self.on_created(sql)
            self.destroy()
        except Exception as exc:
            messagebox.showerror("SQL Error", str(exc))


class RowEditDialog(tk.Toplevel):
    """Dialog used for both inserting a new row and editing an existing one."""

    def __init__(self, master, columns, initial_values, on_submit, title):
        super().__init__(master)
        self.title(title)
        self.resizable(False, False)
        self.on_submit = on_submit
        self.entries = {}

        frame = ttk.Frame(self, padding=10)
        frame.pack(fill="both", expand=True)

        for i, col in enumerate(columns):
            ttk.Label(frame, text=col).grid(row=i, column=0, sticky="w", padx=4, pady=3)
            var = tk.StringVar(value="" if initial_values is None else str(
                initial_values[i] if initial_values[i] is not None else ""
            ))
            entry = ttk.Entry(frame, textvariable=var, width=30)
            entry.grid(row=i, column=1, padx=4, pady=3)
            self.entries[col] = var

        btns = ttk.Frame(frame)
        btns.grid(row=len(columns), column=0, columnspan=2, pady=(10, 0))
        ttk.Button(btns, text="Save", command=self.submit).pack(side="left", padx=4)
        ttk.Button(btns, text="Cancel", command=self.destroy).pack(side="left", padx=4)

    def submit(self):
        values = [v.get() for v in self.entries.values()]
        try:
            self.on_submit(values)
            self.destroy()
        except Exception as exc:
            messagebox.showerror("SQL Error", str(exc))


class DBManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DB Manager")
        self.geometry("1000x650")

        self.conn: sqlite3.Connection | None = None
        self.db_path = None
        self.current_table = None

        self._build_menu()
        self._build_layout()
        self._set_status("Not connected. Use File > New Database or Open Database.")

    # ---------------------------------------------------------------- menu
    def _build_menu(self):
        menubar = tk.Menu(self)

        file_menu = tk.Menu(menubar, tearoff=False)
        file_menu.add_command(label="New Database...", command=self.new_database)
        file_menu.add_command(label="Open Database...", command=self.open_database)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.destroy)
        menubar.add_cascade(label="File", menu=file_menu)

        table_menu = tk.Menu(menubar, tearoff=False)
        table_menu.add_command(label="Create Table...", command=self.create_table_dialog)
        table_menu.add_command(label="Drop Table", command=self.drop_table)
        table_menu.add_command(label="Refresh Tables", command=self.refresh_tables)
        menubar.add_cascade(label="Table", menu=table_menu)

        self.config(menu=menubar)

    # -------------------------------------------------------------- layout
    def _build_layout(self):
        main = ttk.Frame(self)
        main.pack(fill="both", expand=True)

        # --- sidebar: table list ---
        sidebar = ttk.Frame(main, width=220)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        ttk.Label(sidebar, text="Tables", font=("", 10, "bold")).pack(
            anchor="w", padx=8, pady=(8, 2)
        )
        self.table_list = tk.Listbox(sidebar)
        self.table_list.pack(fill="both", expand=True, padx=8, pady=4)
        self.table_list.bind("<<ListboxSelect>>", self.on_table_selected)

        # --- main area: notebook with Data tab and Query tab ---
        right = ttk.Frame(main)
        right.pack(side="left", fill="both", expand=True)

        self.notebook = ttk.Notebook(right)
        self.notebook.pack(fill="both", expand=True, padx=6, pady=6)

        self._build_data_tab()
        self._build_query_tab()

        # --- status bar ---
        self.status_var = tk.StringVar()
        status_bar = ttk.Label(
            self, textvariable=self.status_var, relief="sunken", anchor="w"
        )
        status_bar.pack(side="bottom", fill="x")

    def _build_data_tab(self):
        self.data_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.data_tab, text="Table Data")

        toolbar = ttk.Frame(self.data_tab)
        toolbar.pack(fill="x", pady=4)
        ttk.Button(toolbar, text="Add Row", command=self.add_row).pack(side="left", padx=4)
        ttk.Button(toolbar, text="Edit Row", command=self.edit_row).pack(side="left", padx=4)
        ttk.Button(toolbar, text="Delete Row", command=self.delete_row).pack(side="left", padx=4)
        ttk.Button(toolbar, text="Refresh", command=self.load_table_data).pack(side="left", padx=4)

        tree_frame = ttk.Frame(self.data_tab)
        tree_frame.pack(fill="both", expand=True)

        self.data_tree = ttk.Treeview(tree_frame, show="headings")
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.data_tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.data_tree.xview)
        self.data_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.data_tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

    def _build_query_tab(self):
        self.query_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.query_tab, text="SQL Query")

        editor_frame = ttk.Frame(self.query_tab)
        editor_frame.pack(fill="x", pady=4)

        self.query_text = tk.Text(editor_frame, height=8, wrap="none")
        self.query_text.pack(fill="x", padx=4)
        self.query_text.insert("1.0", "SELECT name FROM sqlite_master WHERE type='table';")

        btn_frame = ttk.Frame(self.query_tab)
        btn_frame.pack(fill="x", pady=4)
        ttk.Button(btn_frame, text="Execute (F5)", command=self.execute_query).pack(
            side="left", padx=4
        )
        self.bind("<F5>", lambda e: self.execute_query())

        result_frame = ttk.Frame(self.query_tab)
        result_frame.pack(fill="both", expand=True)

        self.query_tree = ttk.Treeview(result_frame, show="headings")
        vsb = ttk.Scrollbar(result_frame, orient="vertical", command=self.query_tree.yview)
        hsb = ttk.Scrollbar(result_frame, orient="horizontal", command=self.query_tree.xview)
        self.query_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.query_tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        result_frame.rowconfigure(0, weight=1)
        result_frame.columnconfigure(0, weight=1)

    # ------------------------------------------------------------- status
    def _set_status(self, text):
        self.status_var.set(text)

    # --------------------------------------------------------- connection
    def new_database(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".db",
            filetypes=[("SQLite Database", "*.db"), ("All Files", "*.*")],
        )
        if not path:
            return
        self._connect(path)

    def open_database(self):
        path = filedialog.askopenfilename(
            filetypes=[("SQLite Database", "*.db *.sqlite *.sqlite3"), ("All Files", "*.*")]
        )
        if not path:
            return
        self._connect(path)

    def _connect(self, path):
        try:
            if self.conn:
                self.conn.close()
            self.conn = sqlite3.connect(path)
            self.conn.execute("PRAGMA foreign_keys = ON")
            self.db_path = path
            self._set_status(f"Connected: {path}")
            self.refresh_tables()
        except Exception as exc:
            messagebox.showerror("Connection Error", str(exc))

    def _require_connection(self):
        if not self.conn:
            messagebox.showwarning("No Database", "Open or create a database first.")
            return False
        return True

    # -------------------------------------------------------------- tables
    def refresh_tables(self):
        if not self._require_connection():
            return
        self.table_list.delete(0, "end")
        cur = self.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' "
            "AND name NOT LIKE 'sqlite_%' ORDER BY name"
        )
        for (name,) in cur.fetchall():
            self.table_list.insert("end", name)
        self._set_status(f"Connected: {self.db_path} | {self.table_list.size()} table(s)")

    def on_table_selected(self, event=None):
        selection = self.table_list.curselection()
        if not selection:
            return
        self.current_table = self.table_list.get(selection[0])
        self.notebook.select(self.data_tab)
        self.load_table_data()

    def get_columns(self, table):
        cur = self.conn.execute(f'PRAGMA table_info("{table}")')
        return [row[1] for row in cur.fetchall()]

    def create_table_dialog(self):
        if not self._require_connection():
            return

        def on_created(sql):
            self.conn.execute(sql)
            self.conn.commit()
            self.refresh_tables()

        CreateTableDialog(self, on_created)

    def drop_table(self):
        if not self._require_connection():
            return
        selection = self.table_list.curselection()
        if not selection:
            messagebox.showwarning("No Table", "Select a table to drop.")
            return
        table = self.table_list.get(selection[0])
        if not messagebox.askyesno("Confirm", f'Drop table "{table}"? This cannot be undone.'):
            return
        try:
            self.conn.execute(f'DROP TABLE "{table}"')
            self.conn.commit()
            self.current_table = None
            self.refresh_tables()
            self.data_tree.delete(*self.data_tree.get_children())
        except Exception as exc:
            messagebox.showerror("SQL Error", str(exc))

    # ---------------------------------------------------------- row data
    def load_table_data(self):
        if not self.current_table or not self.conn:
            return
        table = self.current_table
        self.data_tree.delete(*self.data_tree.get_children())

        cur = self.conn.execute(f'SELECT rowid, * FROM "{table}"')
        col_names = [d[0] for d in cur.description][1:]  # drop rowid

        self.data_tree["columns"] = col_names
        for col in col_names:
            self.data_tree.heading(col, text=col)
            self.data_tree.column(col, width=120, anchor="w")

        for row in cur.fetchall():
            rowid = row[0]
            values = row[1:]
            self.data_tree.insert("", "end", iid=str(rowid), values=values)

        self._set_status(f"Table '{table}': {len(self.data_tree.get_children())} row(s)")

    def add_row(self):
        if not self.current_table:
            messagebox.showwarning("No Table", "Select a table first.")
            return
        columns = self.get_columns(self.current_table)

        def on_submit(values):
            placeholders = ", ".join(["?"] * len(columns))
            col_list = ", ".join(f'"{c}"' for c in columns)
            cleaned = [v if v != "" else None for v in values]
            self.conn.execute(
                f'INSERT INTO "{self.current_table}" ({col_list}) VALUES ({placeholders})',
                cleaned,
            )
            self.conn.commit()
            self.load_table_data()

        RowEditDialog(self, columns, None, on_submit, "Add Row")

    def _selected_rowid(self):
        selection = self.data_tree.selection()
        if not selection:
            messagebox.showwarning("No Row Selected", "Select a row first.")
            return None
        return selection[0]  # iid == rowid

    def edit_row(self):
        if not self.current_table:
            return
        rowid = self._selected_rowid()
        if rowid is None:
            return
        columns = self.get_columns(self.current_table)
        current_values = self.data_tree.item(rowid, "values")

        def on_submit(values):
            set_clause = ", ".join(f'"{c}" = ?' for c in columns)
            cleaned = [v if v != "" else None for v in values]
            self.conn.execute(
                f'UPDATE "{self.current_table}" SET {set_clause} WHERE rowid = ?',
                cleaned + [rowid],
            )
            self.conn.commit()
            self.load_table_data()

        RowEditDialog(self, columns, current_values, on_submit, "Edit Row")

    def delete_row(self):
        if not self.current_table:
            return
        rowid = self._selected_rowid()
        if rowid is None:
            return
        if not messagebox.askyesno("Confirm", "Delete the selected row?"):
            return
        try:
            self.conn.execute(f'DELETE FROM "{self.current_table}" WHERE rowid = ?', (rowid,))
            self.conn.commit()
            self.load_table_data()
        except Exception as exc:
            messagebox.showerror("SQL Error", str(exc))

    # --------------------------------------------------------------- query
    def execute_query(self):
        if not self._require_connection():
            return
        sql = self.query_text.get("1.0", "end").strip()
        if not sql:
            return
        try:
            cur = self.conn.execute(sql)
            if cur.description:  # SELECT-like statement with results
                col_names = [d[0] for d in cur.description]
                self.query_tree["columns"] = col_names
                self.query_tree.delete(*self.query_tree.get_children())
                for col in col_names:
                    self.query_tree.heading(col, text=col)
                    self.query_tree.column(col, width=120, anchor="w")
                rows = cur.fetchall()
                for i, row in enumerate(rows):
                    self.query_tree.insert("", "end", iid=str(i), values=row)
                self._set_status(f"Query OK, {len(rows)} row(s) returned")
            else:  # DML/DDL statement
                self.conn.commit()
                self.query_tree.delete(*self.query_tree.get_children())
                self.query_tree["columns"] = []
                self._set_status(f"Query OK, {cur.rowcount} row(s) affected")
                self.refresh_tables()
        except Exception as exc:
            messagebox.showerror("SQL Error", str(exc))
            self._set_status("Query failed.")


if __name__ == "__main__":
    app = DBManagerApp()
    app.mainloop()