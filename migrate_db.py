#!/usr/bin/env python3
"""
Database migration script to update existing tables with new columns
"""

from app import app, db
from sqlalchemy import text

def migrate_database():
    with app.app_context():
        print("Starting database migration...")
        
        try:
            # Check if new columns exist in user table
            result = db.session.execute(text("SHOW COLUMNS FROM user LIKE 'last_login'"))
            has_last_login = result.fetchone() is not None
            
            result = db.session.execute(text("SHOW COLUMNS FROM user LIKE 'is_active'"))
            has_is_active = result.fetchone() is not None
            
            result = db.session.execute(text("SHOW COLUMNS FROM user LIKE 'role'"))
            has_role = result.fetchone() is not None
            
            # Add missing columns to user table
            if not has_last_login:
                print("Adding last_login column to user table...")
                db.session.execute(text("ALTER TABLE user ADD COLUMN last_login DATETIME NULL"))
            
            if not has_is_active:
                print("Adding is_active column to user table...")
                db.session.execute(text("ALTER TABLE user ADD COLUMN is_active BOOLEAN DEFAULT TRUE"))
            
            if not has_role:
                print("Adding role column to user table...")
                db.session.execute(text("ALTER TABLE user ADD COLUMN role VARCHAR(20) DEFAULT 'user'"))
            
            # Check if activity_log table exists
            result = db.session.execute(text("SHOW TABLES LIKE 'activity_log'"))
            has_activity_log = result.fetchone() is not None
            
            if not has_activity_log:
                print("Creating activity_log table...")
                db.session.execute(text("""
                    CREATE TABLE activity_log (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT NOT NULL,
                        action VARCHAR(100) NOT NULL,
                        details TEXT NULL,
                        ip_address VARCHAR(45) NULL,
                        user_agent TEXT NULL,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES user(id)
                    )
                """))
            
            # Update existing users to have default values
            print("Updating existing users with default values...")
            db.session.execute(text("UPDATE user SET is_active = TRUE WHERE is_active IS NULL"))
            db.session.execute(text("UPDATE user SET role = 'user' WHERE role IS NULL"))
            
            db.session.commit()
            print("Database migration completed successfully!")
            
        except Exception as e:
            print(f"Error during migration: {e}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    migrate_database() 