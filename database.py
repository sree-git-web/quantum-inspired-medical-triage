import sqlite3  # This allows Python to use a database

# Function to create database and patients table
def create_database():
    # Step 1: Connect to the database file (creates it if it doesn't exist)
    conn = sqlite3.connect('patients.db')
    
    # Step 2: Create a cursor (like a pen to write in the database)
    c = conn.cursor()
    
    # Step 3: Create the patients table if it doesn't exist
    c.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        age INTEGER,
        severity INTEGER,
        heart_rate INTEGER,
        bp_systolic INTEGER,
        bp_diastolic INTEGER,
        oxygen INTEGER,
        consciousness TEXT,
        symptoms TEXT,
        priority TEXT
    )
    ''')
    
    # Step 4: Save changes
    conn.commit()
    
    # Step 5: Close the connection
    conn.close()

# Step 6: Run the function to create the database
create_database()
print("Database created successfully!")
