import csv
from connect import get_connection

# ---------------- CREATE ----------------
def insert_contact(name, phone):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s) ON CONFLICT (phone) DO NOTHING",
        (name, phone)
    )
    conn.commit()
    cur.close()
    conn.close()
    print("Contact added!")

# ---------------- CSV IMPORT ----------------
def import_from_csv(file_name):
    conn = get_connection()
    cur = conn.cursor()

    with open(file_name, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            name, phone = row
            cur.execute(
                "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s) ON CONFLICT (phone) DO NOTHING",
                (name, phone)
            )

    conn.commit()
    cur.close()
    conn.close()
    print("CSV imported!")

# ---------------- READ ----------------
def query_all():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM phonebook")
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()

def query_by_name(name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM phonebook WHERE first_name ILIKE %s", ('%' + name + '%',))
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()

def query_by_phone_prefix(prefix):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM phonebook WHERE phone LIKE %s", (prefix + '%',))
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()

# ---------------- UPDATE ----------------
def update_contact(old_phone, new_name=None, new_phone=None):
    conn = get_connection()
    cur = conn.cursor()

    if new_name:
        cur.execute(
            "UPDATE phonebook SET first_name=%s WHERE phone=%s",
            (new_name, old_phone)
        )

    if new_phone:
        cur.execute(
            "UPDATE phonebook SET phone=%s WHERE phone=%s",
            (new_phone, old_phone)
        )

    conn.commit()
    cur.close()
    conn.close()
    print("Contact updated!")

# ---------------- DELETE ----------------
def delete_contact_by_name(name):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM phonebook WHERE first_name=%s", (name,))
    conn.commit()

    cur.close()
    conn.close()
    print("Deleted!")

def delete_contact_by_phone(phone):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM phonebook WHERE phone=%s", (phone,))
    conn.commit()

    cur.close()
    conn.close()
    print("Deleted!")

# ---------------- MENU ----------------
def menu():
    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Add contact")
        print("2. Import from CSV")
        print("3. Show all contacts")
        print("4. Search by name")
        print("5. Search by phone prefix")
        print("6. Update contact")
        print("7. Delete by name")
        print("8. Delete by phone")
        print("9. Exit")

        choice = input("Choose: ")

        if choice == "1":
            name = input("Name: ")
            phone = input("Phone: ")
            insert_contact(name, phone)

        elif choice == "2":
            file = input("CSV file name: ")
            import_from_csv(file)

        elif choice == "3":
            query_all()

        elif choice == "4":
            name = input("Enter name: ")
            query_by_name(name)

        elif choice == "5":
            prefix = input("Enter prefix: ")
            query_by_phone_prefix(prefix)

        elif choice == "6":
            old_phone = input("Old phone: ")
            new_name = input("New name (or press Enter): ")
            new_phone = input("New phone (or press Enter): ")
            update_contact(old_phone, new_name or None, new_phone or None)

        elif choice == "7":
            name = input("Name: ")
            delete_contact_by_name(name)

        elif choice == "8":
            phone = input("Phone: ")
            delete_contact_by_phone(phone)

        elif choice == "9":
            break

        else:
            print("Invalid choice!")

if __name__ == "__main__":
    menu()