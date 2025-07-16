from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime, timedelta
from sqlalchemy import inspect, func, text
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'

# Use environment variable or fallback to default MySQL/MariaDB connection
DB_URI = os.getenv('DB_URI', 'mysql+pymysql://root:@127.0.0.1:3306/localostport')
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

print("[DEBUG] Using database URI:", app.config['SQLALCHEMY_DATABASE_URI'])

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    role = db.Column(db.String(20), default='user')  # user, admin
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Activity Log model for analytics
class ActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(100), nullable=False)  # login, logout, create_table, etc.
    details = db.Column(db.Text, nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='activities')

# Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            
            # Update last login
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            # Log activity
            log_activity(user.id, 'login', f'User {username} logged in', request.remote_addr, request.user_agent.string)
            
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Validation
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return render_template('register.html')
        
        # Create new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        # Log activity
        log_activity(new_user.id, 'register', f'New user registered: {username}', request.remote_addr, request.user_agent.string)
        
        print(f"[DEBUG] User registered: username={new_user.username}, email={new_user.email}")
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = db.session.get(User, session['user_id'])
    
    # Get quick stats
    total_users = User.query.count()
    total_tables = len(inspect(db.engine).get_table_names())
    
    # Get recent activities
    recent_activities = ActivityLog.query.order_by(ActivityLog.created_at.desc()).limit(5).all()
    
    return render_template('dashboard.html', user=user, total_users=total_users, 
                         total_tables=total_tables, recent_activities=recent_activities)

@app.route('/logout', methods=['POST'])
def logout():
    if 'user_id' in session:
        # Log activity before clearing session
        log_activity(session['user_id'], 'logout', f'User {session["username"]} logged out', 
                    request.remote_addr, request.user_agent.string)
    
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

# User Profile and Settings Routes
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = db.session.get(User, session['user_id'])
    return render_template('profile.html', user=user)

@app.route('/edit_password', methods=['GET', 'POST'])
def edit_password():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = db.session.get(User, session['user_id'])
    
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        # Validate current password
        if not user.check_password(current_password):
            flash('Current password is incorrect', 'error')
            return render_template('edit_password.html', user=user)
        
        # Validate new password
        if new_password != confirm_password:
            flash('New passwords do not match', 'error')
            return render_template('edit_password.html', user=user)
        
        if len(new_password) < 6:
            flash('New password must be at least 6 characters long', 'error')
            return render_template('edit_password.html', user=user)
        
        # Update password
        user.set_password(new_password)
        db.session.commit()
        
        # Log activity
        log_activity(user.id, 'password_change', 'Password changed successfully', 
                    request.remote_addr, request.user_agent.string)
        
        flash('Password updated successfully!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('edit_password.html', user=user)

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = db.session.get(User, session['user_id'])
    
    if request.method == 'POST':
        email = request.form['email']
        
        # Check if email is already taken by another user
        existing_user = User.query.filter_by(email=email).first()
        if existing_user and existing_user.id != user.id:
            flash('Email is already registered by another user', 'error')
            return render_template('edit_profile.html', user=user)
        
        # Update profile
        user.email = email
        db.session.commit()
        
        # Log activity
        log_activity(user.id, 'profile_update', 'Profile updated', 
                    request.remote_addr, request.user_agent.string)
        
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('edit_profile.html', user=user)

# Analytics Routes
@app.route('/analytics', methods=['GET', 'POST'])
def analytics():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Get database statistics
    tables = inspect(db.engine).get_table_names()
    table_stats = []
    total_rows = 0
    
    for table in tables:
        try:
            row_count = db.session.execute(text(f'SELECT COUNT(*) FROM `{table}`')).scalar()
            total_rows += row_count
            table_stats.append({
                'name': table,
                'rows': row_count
            })
        except:
            table_stats.append({
                'name': table,
                'rows': 0
            })
    
    # Get user statistics
    total_users = User.query.count()
    active_users = User.query.filter_by(is_active=True).count()
    recent_users = User.query.filter(User.created_at >= datetime.utcnow() - timedelta(days=7)).count()
    
    # Get activity statistics
    total_activities = ActivityLog.query.count()
    recent_activities = ActivityLog.query.filter(
        ActivityLog.created_at >= datetime.utcnow() - timedelta(days=7)
    ).count()
    
    # Get activity by type
    try:
        activity_types_result = db.session.query(
            ActivityLog.action, 
            func.count(ActivityLog.id).label('count')
        ).group_by(ActivityLog.action).order_by(func.count(ActivityLog.id).desc()).all()
        
        # Convert Row objects to dictionaries
        activity_types = [{'action': item.action, 'count': int(item.count)} for item in activity_types_result]
    except Exception as e:
        print(f"Error getting activity types: {e}")
        activity_types = []
    
    # Get recent activities
    try:
        recent_logs = ActivityLog.query.order_by(ActivityLog.created_at.desc()).limit(10).all()
    except Exception as e:
        print(f"Error getting recent logs: {e}")
        recent_logs = []
    
    return render_template('analytics.html', 
                         table_stats=table_stats,
                         total_tables=len(tables),
                         total_rows=total_rows,
                         total_users=total_users,
                         active_users=active_users,
                         recent_users=recent_users,
                         total_activities=total_activities,
                         recent_activities=recent_activities,
                         activity_types=activity_types,
                         recent_logs=recent_logs)

@app.route('/analytics/data', methods=['GET', 'POST'])
def analytics_data():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'})
    
    try:
        # Get data for charts
        # User registration over time (last 30 days)
        user_registrations = db.session.query(
            func.date(User.created_at).label('date'),
            func.count(User.id).label('count')
        ).filter(
            User.created_at >= datetime.utcnow() - timedelta(days=30)
        ).group_by(func.date(User.created_at)).all()
        
        # Activity over time (last 30 days)
        activity_over_time = db.session.query(
            func.date(ActivityLog.created_at).label('date'),
            func.count(ActivityLog.id).label('count')
        ).filter(
            ActivityLog.created_at >= datetime.utcnow() - timedelta(days=30)
        ).group_by(func.date(ActivityLog.created_at)).all()
        
        return jsonify({
            'user_registrations': [(str(item.date), int(item.count)) for item in user_registrations],
            'activity_over_time': [(str(item.date), int(item.count)) for item in activity_over_time]
        })
    except Exception as e:
        print(f"Error in analytics_data: {e}")
        return jsonify({
            'user_registrations': [],
            'activity_over_time': []
        })

# System Settings Routes
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if session.get('role') != 'admin':
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    # Get system information
    system_info = {
        'database_uri': DB_URI,
        'total_users': User.query.count(),
        'total_tables': len(inspect(db.engine).get_table_names()),
        'total_activities': ActivityLog.query.count(),
        'app_version': '1.0.0'
    }
    
    return render_template('settings.html', system_info=system_info)

@app.route('/settings/users', methods=['GET', 'POST'])
def manage_users():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if session.get('role') != 'admin':
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('manage_users.html', users=users)

@app.route('/settings/users/<int:user_id>/toggle_status', methods=['POST'])
def toggle_user_status(user_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'})
    
    if session.get('role') != 'admin':
        return jsonify({'error': 'Admin privileges required'})
    
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'error': 'User not found'})
    
    user.is_active = not user.is_active
    db.session.commit()
    
    # Log activity
    log_activity(session['user_id'], 'user_status_change', 
                f'User {user.username} status changed to {"active" if user.is_active else "inactive"}',
                request.remote_addr, request.user_agent.string)
    
    return jsonify({'success': True, 'is_active': user.is_active})

# Activity Log Routes
@app.route('/activity_log', methods=['GET', 'POST'])
def activity_log():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    page = request.form.get('page', 1, type=int)
    per_page = 20
    
    activities = ActivityLog.query.order_by(ActivityLog.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('activity_log.html', activities=activities)

# Helper function to log activities
def log_activity(user_id, action, details=None, ip_address=None, user_agent=None):
    try:
        activity = ActivityLog(
            user_id=user_id,
            action=action,
            details=details,
            ip_address=ip_address,
            user_agent=user_agent
        )
        db.session.add(activity)
        db.session.commit()
    except Exception as e:
        print(f"Error logging activity: {e}")

# Database Management Routes (using SQLAlchemy only)
@app.route('/admin/database', methods=['GET', 'POST'])
def database_manager():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Get all table names
    tables = inspect(db.engine).get_table_names()
    table_info = []
    for table in tables:
        # Get columns
        columns = inspect(db.engine).get_columns(table)
        # Get row count
        row_count = db.session.execute(db.text(f'SELECT COUNT(*) FROM `{table}`')).scalar()
        table_info.append({
            'name': table,
            'columns': [(col['name'], str(col['type'])) for col in columns],  # Convert types to strings
            'row_count': row_count
        })
    return render_template('database_manager.html', tables=table_info, db_path=DB_URI)

@app.route('/admin/database/table/<table_name>', methods=['GET', 'POST'])
def view_table(table_name):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    # Get columns
    columns = inspect(db.engine).get_columns(table_name)
    # Get data
    result = db.session.execute(db.text(f'SELECT * FROM `{table_name}`'))
    data = [list(row) for row in result.fetchall()]  # Convert Row objects to lists
    # Convert column types to strings for JSON serialization
    column_info = [(col['name'], str(col['type'])) for col in columns]
    return render_template('view_table.html', table_name=table_name, columns=column_info, data=data)

@app.route('/admin/database/create_table', methods=['POST'])
def create_table():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        table_name = request.form['table_name']
        columns = request.form.getlist('column_name')
        types = request.form.getlist('column_type')
        nullables = request.form.getlist('nullable')
        primaries = request.form.getlist('primary_key')
        
        # Validate that we have the required data
        if not table_name.strip():
            flash('Table name is required', 'error')
            return redirect(url_for('create_table'))
        
        if not columns or not any(col.strip() for col in columns):
            flash('At least one column is required', 'error')
            return redirect(url_for('create_table'))
        
        # Build CREATE TABLE SQL
        sql = f"CREATE TABLE `{table_name}` ("
        column_definitions = []
        for i, col_name in enumerate(columns):
            if col_name.strip():
                # Safely get type, nullable, and primary key settings
                col_type = types[i] if i < len(types) else 'VARCHAR(255)'
                is_nullable = i < len(nullables) and 'not_null' in nullables[i]
                is_primary = i < len(primaries) and 'primary' in primaries[i]
                
                col_def = f"`{col_name}` {col_type}"
                if is_nullable:
                    col_def += " NOT NULL"
                if is_primary:
                    col_def += " PRIMARY KEY"
                column_definitions.append(col_def)
        
        if not column_definitions:
            flash('No valid columns defined', 'error')
            return redirect(url_for('create_table'))
            
        sql += ", ".join(column_definitions) + ")"
        
        try:
            db.session.execute(db.text(sql))
            db.session.commit()
            
            # Log activity
            log_activity(session['user_id'], 'create_table', f'Table "{table_name}" created', 
                        request.remote_addr, request.user_agent.string)
            
            flash(f'Table "{table_name}" created successfully!', 'success')
        except Exception as e:
            flash(f'Error creating table: {str(e)}', 'error')
        return redirect(url_for('database_manager'))
    return render_template('create_table.html')

@app.route('/admin/database/execute_sql', methods=['GET', 'POST'])
def execute_sql():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'})
    sql = request.form['sql']
    try:
        result = db.session.execute(db.text(sql))
        if sql.strip().upper().startswith('SELECT'):
            columns = list(result.keys())
            data = [list(row) for row in result.fetchall()]  # Convert Row objects to lists
            return jsonify({
                'success': True,
                'columns': columns,
                'data': data
            })
        else:
            db.session.commit()
            
            # Log activity
            log_activity(session['user_id'], 'execute_sql', f'SQL executed: {sql[:100]}...', 
                        request.remote_addr, request.user_agent.string)
            
            return jsonify({
                'success': True,
                'message': 'Query executed successfully'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=3333) 