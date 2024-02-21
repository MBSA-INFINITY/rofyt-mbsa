import psycopg2
from psycopg2 import OperationalError

# Database connection parameters
db_host = 'mbsa.c1um4umwej1a.ap-south-1.rds.amazonaws.com'
db_port = '5432'  # Default PostgreSQL port
db_name = 'jlpmyride'
db_user = 'postgres'
db_password = 'OEoUxYcVE525bTGY6EDL'

try:
    # Establish a connection to the database
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )

    # Create a cursor object
    cursor = conn.cursor()

except OperationalError as e:
    print(f"Error: {e}")

# finally:
#     # Close the cursor and connection
#     if cursor:
#         cursor.close()
#     if conn:
#         conn.close()
