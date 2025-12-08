"""
Database Migration Script
Adds recyclability columns to existing classifications table
"""
import sqlite3

def migrate_database():
    """Add recyclability columns to classifications table"""
    conn = sqlite3.connect('waste_sorting.db')
    c = conn.cursor()
    
    # Check if columns already exist
    c.execute("PRAGMA table_info(classifications)")
    columns = [column[1] for column in c.fetchall()]
    
    # Add recyclable column if it doesn't exist
    if 'recyclable' not in columns:
        print("Adding 'recyclable' column...")
        c.execute('ALTER TABLE classifications ADD COLUMN recyclable BOOLEAN')
        print("✅ Added 'recyclable' column")
    
    # Add recyclable_confidence column if it doesn't exist
    if 'recyclable_confidence' not in columns:
        print("Adding 'recyclable_confidence' column...")
        c.execute('ALTER TABLE classifications ADD COLUMN recyclable_confidence REAL')
        print("✅ Added 'recyclable_confidence' column")
    
    # Add eco_score column if it doesn't exist
    if 'eco_score' not in columns:
        print("Adding 'eco_score' column...")
        c.execute('ALTER TABLE classifications ADD COLUMN eco_score INTEGER')
        print("✅ Added 'eco_score' column")
    
    conn.commit()
    conn.close()
    print("\n✅ Database migration completed successfully!")

if __name__ == '__main__':
    migrate_database()
