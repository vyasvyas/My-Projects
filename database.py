# ✅ FIXED: put this at the top of the file
# db_config.py
import mysql.connector
def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',  # ✅ try 'root' or your actual MySQL password
        database='crop_db',
        port=3306
    )

if __name__ == "__main__":
    try:
        conn = get_connection()
        if conn.is_connected():
            print("✅ Database connection successful!")
            conn.close()
        else:
            print("❌ Failed to connect to the database.")
    except mysql.connector.Error as e:
        print("❌ Error:", e)
