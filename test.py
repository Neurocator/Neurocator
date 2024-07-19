import os
import psycopg2
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Database connection parameters
db_params = {
    'dbname': os.environ.get('PGDATABASE', 'neurocator'),
    'user': os.environ.get('PGUSER', 'neurocator_owner'),
    'password': os.environ.get('PGPASSWORD', '3j1HgiIuwVoO'),
    'host': os.environ.get('PGHOST', 'ep-autumn-scene-a6huvqfz.us-west-2.aws.neon.tech'),
    'port': os.environ.get('PGPORT', '5432'),
    'sslmode': 'require'
}

conn = psycopg2.connect(**db_params)
cur = conn.cursor()
query = "SELECT id, username, title, content, date FROM posts"
cur.execute(query)
conn.commit()
rows = cur.fetchall()
posts = []
for row in rows:
    post = {
        'id': row[0], 
        'username': row[1],
        'title': row[2],
        'content': row[3],
        'date': row[4]
        }
    posts.append(post)
print(posts)

# def insert_data():
#     conn = None
#     cur = None
#     try:
#         logging.info("Connecting to the database...")
#         conn = psycopg2.connect(**db_params)
#         cur = conn.cursor()

#         logging.info("Connected successfully")

#         # Example INSERT query
#         query = "INSERT INTO test (name) VALUES (%s)"
#         data = ('test',)

#         logging.info("Executing INSERT query...")
#         cur.execute(query, data)

#         conn.commit()
#         logging.info("Data inserted successfully")

#     except psycopg2.Error as e:
#         logging.error(f"Database error: {e}")
#         if conn:
#             conn.rollback()
#     except Exception as e:
#         logging.error(f"An error occurred: {e}")
#     finally:
#         if cur:
#             cur.close()
#         if conn:
#             conn.close()
#         logging.info("Database connection closed")

# if __name__ == "__main__":
#     insert_data()


