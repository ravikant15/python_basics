# Database Connection Code Explanation

## 🔗 **Database Connection Overview**

Your Flask application uses **TWO different database connection methods**:

1. **Flask-SQLAlchemy** (ORM) - For main application operations
2. **Direct SQLite3** - For database management features

---

## 📍 **1. Flask-SQLAlchemy Connection Setup**

### **Location: Lines 1-15 in app.py**

```python
# Line 1-2: Import required libraries
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy  # ← ORM for database operations

# Line 7-8: Flask app configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'

# Line 9: DATABASE CONNECTION STRING
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # ← This creates the connection!
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Line 11: DATABASE OBJECT CREATION
db = SQLAlchemy(app)  # ← This is your main database connection object
```

### **What this does:**
- **`sqlite:///users.db`** - Tells Flask-SQLAlchemy to connect to a SQLite database file named `users.db`
- **`db = SQLAlchemy(app)`** - Creates a database object that handles all ORM operations
- **Database file location:** `instance/users.db` (Flask's default instance folder)

---

## 📍 **2. User Model Definition**

### **Location: Lines 16-28 in app.py**

```python
# Line 16: Define User table structure
class User(db.Model):  # ← Inherits from db.Model (SQLAlchemy)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

### **What this does:**
- **`db.Model`** - Tells SQLAlchemy this is a database table
- **`db.Column()`** - Defines table columns with types and constraints
- **Automatic table creation** when you run the app

---

## 📍 **3. Database Table Creation**

### **Location: Lines 235-237 in app.py**

```python
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # ← Creates all tables defined in models
    app.run(debug=True, host='0.0.0.0', port=5000)
```

### **What this does:**
- **`db.create_all()`** - Creates the `users.db` file and all tables if they don't exist
- **Runs automatically** when you start the application

---

## 📍 **4. ORM Database Operations (Main App)**

### **Location: Various routes in app.py**

#### **Registration (Lines 75-76):**
```python
db.session.add(new_user)      # ← Add user to database session
db.session.commit()           # ← Save changes to database
```

#### **Login (Line 42):**
```python
user = User.query.filter_by(username=username).first()  # ← Query database using ORM
```

#### **Dashboard (Line 85):**
```python
user = db.session.get(User, session['user_id'])  # ← Get user by ID using ORM
```

---

## 📍 **5. Direct SQLite3 Connections (Database Manager)**

### **Location: Database management routes**

#### **Database Manager (Lines 95-120):**
```python
# Line 95: Database file path
db_path = 'instance/users.db'

# Line 97-98: DIRECT SQLITE CONNECTION
conn = sqlite3.connect(db_path)  # ← Direct connection to SQLite file
cursor = conn.cursor()           # ← Create cursor for SQL operations

# Line 100: Execute SQL query
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")

# Line 120: Close connection
conn.close()  # ← Always close the connection!
```

#### **View Table (Lines 125-140):**
```python
# Line 127: Direct connection
conn = sqlite3.connect('instance/users.db')
cursor = conn.cursor()

# Line 129-130: Get table structure
cursor.execute(f"PRAGMA table_info({table_name})")
columns = cursor.fetchall()

# Line 133-134: Get table data
cursor.execute(f"SELECT * FROM {table_name}")
data = cursor.fetchall()

# Line 136: Close connection
conn.close()
```

#### **Create Table (Lines 165-170):**
```python
# Line 165: Direct connection
conn = sqlite3.connect('instance/users.db')
cursor = conn.cursor()

# Line 166: Execute CREATE TABLE
cursor.execute(sql)

# Line 167: Commit changes
conn.commit()

# Line 168: Close connection
conn.close()
```

#### **Execute SQL (Lines 185-210):**
```python
# Line 187: Direct connection
conn = sqlite3.connect('instance/users.db')
cursor = conn.cursor()

# Line 188: Execute any SQL
cursor.execute(sql)

# Line 190-195: Handle SELECT queries
if sql.strip().upper().startswith('SELECT'):
    columns = [description[0] for description in cursor.description]
    data = cursor.fetchall()
    conn.close()
    return jsonify({'success': True, 'columns': columns, 'data': data})

# Line 197-200: Handle other queries
else:
    conn.commit()  # ← Save changes
    conn.close()   # ← Close connection
    return jsonify({'success': True, 'message': 'Query executed successfully'})
```

---

## 🔄 **Connection Flow Summary**

### **1. Application Startup:**
```
app.py → Flask-SQLAlchemy → sqlite:///users.db → instance/users.db
```

### **2. Main App Operations (ORM):**
```
User.query.filter_by() → db.session → SQLAlchemy → SQLite
```

### **3. Database Management (Direct SQL):**
```
sqlite3.connect('instance/users.db') → Direct SQLite connection
```

---

## 📁 **Database File Location**

```
C:\wamp64\www\python_demo\
├── app.py                    # ← Main application
├── instance/                 # ← Flask instance folder
│   └── users.db             # ← Your SQLite database file
├── templates/               # ← HTML templates
└── requirements.txt         # ← Python dependencies
```

---

## 🛠️ **Key Differences**

| **Flask-SQLAlchemy (ORM)** | **Direct SQLite3** |
|---------------------------|-------------------|
| Used for main app operations | Used for database management |
| Automatic connection handling | Manual connection management |
| Object-oriented queries | Raw SQL queries |
| `User.query.filter_by()` | `cursor.execute("SELECT...")` |
| `db.session.commit()` | `conn.commit()` |
| No need to close connections | Must call `conn.close()` |

---

## 🔧 **How to Change Database**

### **To use a different database:**

#### **1. Change SQLAlchemy URI (Line 9):**
```python
# For MySQL:
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:pass@localhost/dbname'

# For PostgreSQL:
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/dbname'

# For different SQLite file:
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'
```

#### **2. Update Direct Connections (Lines 95, 127, 165, 187):**
```python
# Change all instances of:
conn = sqlite3.connect('instance/users.db')

# To your new database path:
conn = sqlite3.connect('path/to/your/database.db')
```

---

## ✅ **Best Practices**

1. **Always close direct connections** with `conn.close()`
2. **Use ORM for main app operations** (safer, easier)
3. **Use direct SQL only for database management** (more control)
4. **Handle exceptions** in database operations
5. **Use transactions** for multiple related operations

---

## 🎯 **Summary**

Your application uses **two database connection methods**:

1. **Flask-SQLAlchemy ORM** - For user authentication, registration, dashboard
2. **Direct SQLite3** - For the database manager features

Both connect to the same `instance/users.db` file but serve different purposes!