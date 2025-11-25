"""Add scam_score and scam_flags columns to jobs table

This migration script adds the missing scam_score and scam_flags columns
to the jobs table to match the updated SQLAlchemy model.

Usage:
    1. Run this script directly to apply migration to your production database
    2. Or integrate with proper Alembic migrations if you use them

Revision ID: add_scam_columns
Create Date: 2025-11-26
"""

import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_db_connection():
    """Get database connection from environment variables."""
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        raise ValueError("DATABASE_URL not found in environment variables")
    
    # Handle both postgresql:// and postgres:// schemes
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    return psycopg2.connect(database_url)

def run_migration():
    """Apply migration to add scam_score and scam_flags columns."""
    
    conn = None
    cursor = None
    
    try:
        print("Connecting to database...")
        conn = get_db_connection()
        cursor = conn.cursor()
        
        print("Checking if migration is needed...")
        
        # Check if scam_score column exists
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='jobs' AND column_name='scam_score'
        """)
        scam_score_exist = cursor.fetchone() is not None
        
        # Check if scam_flags column exists
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='jobs' AND column_name='scam_flags'
        """)
        scam_flags_exist = cursor.fetchone() is not None
        
        # Check if scam_reason column exists (to be removed)
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='jobs' AND column_name='scam_reason'
        """)
        scam_reason_exists = cursor.fetchone() is not None
        
        # Add scam_score column if it doesn't exist
        if not scam_score_exist:
            print("Adding scam_score column...")
            cursor.execute("""
                ALTER TABLE jobs 
                ADD COLUMN scam_score INTEGER
                CHECK (scam_score >= 0 AND scam_score <= 100)
            """)
            print("[OK] scam_score column added successfully")
        else:
            print("[OK] scam_score column already exists")
        
        # Add scam_flags column if it doesn't exist
        if not scam_flags_exist:
            print("Adding scam_flags column...")
            cursor.execute("""
                ALTER TABLE jobs 
                ADD COLUMN scam_flags JSONB DEFAULT '[]'::jsonb
            """)
            print("[OK] scam_flags column added successfully")
        else:
            print("[OK] scam_flags column already exists")
        
        # Remove scam_reason column if it exists (optional - comment out if you want to keep data)
        if scam_reason_exists:
            print("WARNING: scam_reason column exists but is not in the model")
            print("You may want to migrate data from scam_reason to scam_flags before dropping it")
            # Uncomment the following lines to actually drop the column:
            # cursor.execute("ALTER TABLE jobs DROP COLUMN scam_reason")
            # print("[OK] scam_reason column dropped")
        
        # Commit changes
        conn.commit()
        print("\n[SUCCESS] Migration completed successfully!")
        
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"\n[ERROR] Migration failed: {str(e)}")
        raise
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        print("Database connection closed")

if __name__ == "__main__":
    print("=" * 60)
    print("Database Migration: Add scam_score and scam_flags columns")
    print("=" * 60)
    print()
    
    try:
        run_migration()
    except Exception as e:
        print(f"\nError: {str(e)}")
        exit(1)
