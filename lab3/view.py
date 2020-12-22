def main_menu():
	item = input("1. INSERT\n2. DELETE\n3. UPDATE\n4. EXIT\n>")
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
	cond_column = input("Enter conditional column:")
	cond_value = input("Enter conditional value:")
	return [t_name, column, value, (cond_column, cond_value)]
