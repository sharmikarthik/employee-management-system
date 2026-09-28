# Employee Management System

A Flask and SQLite web application to manage employee records.

## Features

- Admin login and logout
- Add, view, update, and delete employees
- Prevent duplicate employee IDs
- Restrict employee pages to logged-in users

## Run locally (Windows PowerShell)

1. Open a terminal in the project folder.
2. Create a virtual environment:

   ```powershell
   python -m venv venv
   ```

3. Install dependencies:

   ```powershell
   .\venv\Scripts\python -m pip install -r requirements.txt
   ```

4. Start the application:

   ```powershell
   .\venv\Scripts\python app.py
   ```

5. Open `http://127.0.0.1:5000/` in a browser.

The SQLite database is created automatically on the first run. Demo login details are defined in `app.py`; change them before using this application with real employee data.