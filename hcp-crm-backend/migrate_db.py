#!/usr/bin/env python3
from sqlalchemy import text
from database import engine

def migrate_database():
    with engine.connect() as connection:
        try:
            # Check if columns exist
            result = connection.execute(text("SHOW COLUMNS FROM interactions LIKE 'materials_shared'"))
            if not result.fetchone():
                print("Adding materials_shared column...")
                connection.execute(text("ALTER TABLE interactions ADD COLUMN materials_shared TEXT"))
                connection.commit()
                print("✓ materials_shared column added")
            else:
                print("✓ materials_shared column already exists")

            result = connection.execute(text("SHOW COLUMNS FROM interactions LIKE 'samples_distributed'"))
            if not result.fetchone():
                print("Adding samples_distributed column...")
                connection.execute(text("ALTER TABLE interactions ADD COLUMN samples_distributed TEXT"))
                connection.commit()
                print("✓ samples_distributed column added")
            else:
                print("✓ samples_distributed column already exists")
                
        except Exception as e:
            print(f"Error during migration: {e}")

if __name__ == "__main__":
    migrate_database()