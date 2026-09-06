import sqlite3

# Connect to your database (use full path if needed)
conn = sqlite3.connect(r"C:\Users\SREENIDHI\OneDrive\Desktop\Quantum Project\patients.db")
c = conn.cursor()

# Fetch all patient records
c.execute("SELECT * FROM patients")
rows = c.fetchall()

# Print each record
for row in rows:
    print(row)

conn.close()
