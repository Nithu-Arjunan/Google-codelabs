import streamlit as st
import psycopg2

# CONFIGURATION (Replace with your IP)
DB_HOST = "35.223.21.182"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "alloydb"

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS
    )

def query_database(user_name):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            # THE SECURITY HANDSHAKE
            # We tell the database: "For this transaction, I am acting as..."
            cur.execute(f"SET app.active_user = '{user_name}';")
            
            # THE BLIND QUERY
            # We ask for EVERYTHING. The database silently filters it.
            cur.execute("SELECT name, salary, performance_review FROM employees;")
            return cur.fetchall()
    finally:
        conn.close()

# UI
st.title("🛡️ The Private Vault")
user = st.sidebar.radio("Act as User:", ["Alice", "Bob", "Charlie", "Eve"])

if st.button("Access Data"):
    results = query_database(user)
    if not results:
        st.error("🚫 Access Denied.")
    else:
        st.success(f"Viewing data as {user}")
        for row in results:
            st.write(row)