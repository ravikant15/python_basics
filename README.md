# Flask Login System

A modern, secure login system built with Flask that includes user registration, authentication, and a dashboard.

## Features

- 🔐 Secure user authentication with password hashing
- 📝 User registration with email validation
- 🎨 Modern, responsive UI with Bootstrap 5
- 📱 Mobile-friendly design
- 🔒 Session management
- 💾 MySQL/MariaDB database for user storage
- ⚡ Flash messages for user feedback

## Installation

1. **Clone or download the project files**

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your MySQL/MariaDB database:**
   - Create a database (e.g., `python_demo`)
   - Update the connection string in `app.py` or set the `DB_URI` environment variable:
     ```python
     DB_URI = os.getenv('DB_URI', 'mysql+pymysql://root:yourpassword@127.0.0.1:3306/yourdbname')
     ```

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Open your browser and go to:**
   ```
   http://localhost:5000
   ```

## Usage

### First Time Setup
1. The application will automatically create the tables when you first run it
2. Visit `http://localhost:5000` to access the login page
3. Click "Register here" to create a new account
4. Fill in your username, email, and password
5. After registration, you'll be redirected to the login page
6. Sign in with your credentials

### Features Available
- **Login Page**: Secure authentication with username and password
- **Registration Page**: Create new accounts with validation
- **Dashboard**: Personalized dashboard after successful login
- **Logout**: Secure session termination

## Project Structure

```
python_demo/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   └── dashboard.html    # User dashboard
```

## Security Features

- Password hashing using Werkzeug's security functions
- Session-based authentication
- Form validation and sanitization
- SQL injection protection through SQLAlchemy ORM
- CSRF protection (built into Flask)

## Customization

### Changing the Secret Key
In `app.py`, change the `SECRET_KEY`:
```python
app.config['SECRET_KEY'] = 'your-new-secret-key-here'
```

### Database Configuration
The application uses MySQL/MariaDB by default. To use a different database:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'your-database-url-here'
```

### Styling
The application uses Bootstrap 5 and custom CSS. You can modify the styles in `templates/base.html`.

## Troubleshooting

### Port Already in Use
If port 5000 is already in use, you can change it in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change port number
```

### Database Issues
If you encounter database issues, check your MySQL/MariaDB connection and credentials.

## Requirements

- Python 3.7 or higher
- Flask 2.3.3
- Flask-SQLAlchemy 3.0.5
- Werkzeug 2.3.7
- PyMySQL 1.1.0
- MySQL/MariaDB server

## License

This project is open source and available under the MIT License. 

# to run any pyton file write the below path in the terminal
<!-- C:\Users\Admin\AppData\Local\Microsoft\WindowsApps\python.exe programs.py -->