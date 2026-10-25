# DB Manager

A lightweight SQLite database management application built using Python and Tkinter. It provides a graphical interface inspired by SQL Server Management Studio (SSMS), allowing users to create databases, manage tables, perform CRUD operations, and execute SQL queries.

This project is part of the `python-development` repository and demonstrates practical Python GUI development, database connectivity, and SQL operations.

## Features

- Create and open SQLite database files.
- Browse database tables through a sidebar.
- View table records in a spreadsheet-style grid.
- Add, edit, and delete table records.
- Create tables with custom columns, data types, primary keys, and `NOT NULL` constraints.
- Drop existing tables with confirmation.
- Execute SQL queries through a built-in query editor.
- View query results and affected row counts.
- Execute SQL queries using the `F5` keyboard shortcut.
- Enable foreign key constraints for SQLite connections.
- Run without third-party Python packages.

## Technologies Used

- **Programming Language:** Python
- **GUI Framework:** Tkinter, `ttk`
- **Database:** SQLite
- **Database Connectivity:** Python `sqlite3` module
- **Tools:** Git, GitHub

## Project Structure

```
db-manager/
├── db_manager.py
├── my_database.db
└── PROJECT_OVERVIEW.md
```

`my_database.db` is the local SQLite database file. If you distribute the project, consider providing a sanitized sample database instead of your personal development database.

## Getting Started

### Prerequisites

- Python 3.10 or newer.
- Tkinter support enabled in your Python installation.

### 1. Navigate to the project directory

If you have already cloned the main repository, run:

```
cd python-development/gui/db-manager
```

### 2. Run the application

```
python db_manager.py
```

On some systems, use:

```
python3 db_manager.py
```

No third-party Python packages are required.

### 3. Start Managing Databases

- Select **File → New Database** to create a database file.
- Select **File → Open Database** to open an existing SQLite database.
- Use the sidebar to browse available tables.
- Use the **Table Data** tab to manage records.
- Open the **SQL Query** tab to execute SQL statements.

## Database Support

DB Manager currently supports SQLite databases. Future support for PostgreSQL, MySQL, and Microsoft SQL Server would require compatible database drivers and database-specific query handling.

## Learning Objectives

- Strengthen Python programming fundamentals.
- Explore desktop GUI development using Tkinter.
- Understand relational databases and SQL operations.
- Implement CRUD (Create, Read, Update, Delete) functionality.
- Practice database connectivity using Python's `sqlite3` module.
- Apply exception handling and database transaction management.
- Develop a practical desktop application with an interactive interface.

## Future Improvements

- Add SQL syntax highlighting and autocomplete.
- Implement query history.
- Support CSV import and export.
- Add search and filtering for table records.
- Enable inline editing of table cells.
- Introduce database backup and restore functionality.
- Explore support for additional database management systems.

## Author

**Anuj Singh**

BCA Student | Software Developer | AI/ML Learner

I enjoy building software while understanding the engineering principles behind modern systems.

## Connect With Me

- **LinkedIn:** [ianujsingh](https://linkedin.com/in/ianujsingh)
- **GitHub:** [i-am-anujsingh](https://github.com/i-am-anujsingh)

---

This project reflects my ongoing learning in Python development, GUI programming, and database management through practical implementation.