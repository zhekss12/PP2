import psycopg2
import csv
from config import config

def create_tables():
    """ Create the phonebook table """
    commands = (
        """
        CREATE TABLE IF NOT EXISTS phonebook (
            contact_id SERIAL PRIMARY KEY,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255),
            phone_number VARCHAR(20) UNIQUE NOT NULL
        )
        """,
    )
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        cur.close()
        conn.commit()
        print("Table created successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_from_console():
    """ Insert data via console input """
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    phone = input("Enter phone number: ")
    
    sql = """INSERT INTO phonebook(first_name, last_name, phone_number)
             VALUES(%s, %s, %s) RETURNING contact_id;"""
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, (first_name, last_name, phone))
        contact_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        print(f"Contact added with ID: {contact_id}")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def upload_from_csv(file_path):
    """ Insert data from a CSV file """
    sql = "INSERT INTO phonebook(first_name, last_name, phone_number) VALUES(%s, %s, %s)"
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            next(reader) # Skip header
            for row in reader:
                cur.execute(sql, row)
        conn.commit()
        cur.close()
        print("Data uploaded from CSV successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def update_contact(phone_number, new_first_name=None, new_phone=None):
    """ Update first name or phone number by current phone number """
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        
        if new_first_name:
            cur.execute("UPDATE phonebook SET first_name = %s WHERE phone_number = %s", (new_first_name, phone_number))
        if new_phone:
            cur.execute("UPDATE phonebook SET phone_number = %s WHERE phone_number = %s", (new_phone, phone_number))
            
        conn.commit()
        print(f"Updated {cur.rowcount} row(s).")
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def query_contacts(filter_type, value):
    """ Query data with different filters (first_name, phone_number, etc.) """
    sql = f"SELECT * FROM phonebook WHERE {filter_type} ILIKE %s"
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, (f'%{value}%',))
        rows = cur.fetchall()
        for row in rows:
            print(row)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def delete_contact(identifier):
    """ Delete contact by first_name OR phone_number """
    sql = "DELETE FROM phonebook WHERE first_name = %s OR phone_number = %s"
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, (identifier, identifier))
        conn.commit()
        print(f"Deleted {cur.rowcount} row(s).")
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    create_tables()
    # Example Usage:
    # insert_from_console()
    # upload_from_csv('contacts.csv')
    # update_contact('123-456', new_first_name='John')
    # query_contacts('first_name', 'John')
    # delete_contact('John')