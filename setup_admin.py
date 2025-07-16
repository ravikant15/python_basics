#!/usr/bin/env python3
"""
Setup script to create an admin user for testing
Run this script to create an admin user with username 'admin' and password 'admin123'
"""

from app import app, db, User
from werkzeug.security import generate_password_hash

def create_admin_user():
    with app.app_context():
        # Check if admin user already exists
        admin_user = User.query.filter_by(username='admin').first()
        
        if admin_user:
            print("Admin user already exists!")
            print(f"Username: {admin_user.username}")
            print(f"Email: {admin_user.email}")
            print(f"Role: {admin_user.role}")
            return
        
        # Create admin user
        admin_user = User(
            username='admin',
            email='admin@example.com',
            role='admin',
            is_active=True
        )
        admin_user.set_password('admin123')
        
        db.session.add(admin_user)
        db.session.commit()
        
        print("Admin user created successfully!")
        print("Username: admin")
        print("Password: admin123")
        print("Email: admin@example.com")
        print("Role: admin")

if __name__ == '__main__':
    create_admin_user() 