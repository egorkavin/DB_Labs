def main_menu():
    item = input("1. INSERT\n2. DELETE\n3. UPDATE\n4. RANDOM\n5. SELECT\n6. EXIT\n>")
    return item


def insert_menu():
    t_name = input("Enter table name:")
    values = input("Enter comma-separated values:")
    return [t_name, values]


def delete_menu():
    t_name = input("Enter table name:")
    column = input("Enter column:")
    value = input("Enter value:")
    return [t_name, column, value]


def update_menu():
    t_name = input("Enter table name:")
    column = input("Enter column:")
    value = input("Enter value:")
    cond = input("Enter condition:")
    return [t_name, column, value, cond]


def random_menu():
    t_name = input("Enter table name:")
    rows_number = input("Enter rows number:")
    return [t_name, rows_number]


def show_random_query(query):
    print(query)

def select_menu():
    item = input("""
        Choose query:
        1. Select student with grade in range
        2. Select teacher with subject
        3. Select student, teacher and subject
        >""")
    values = input("Enter values:")
    return [item, values]


def show_select(query, rows, time):
    print(query)
    for r in rows:
        print(r)
    print(f"Search time: {time}ms")
