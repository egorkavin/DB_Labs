import view
import modelORM

while True:
	menu_item = view.main_menu()
	print(menu_item)
	if menu_item == '1':
		attrs = view.insert_menu()
		try:
			getattr(modelORM, f'insert_{attrs[0]}')(attrs[1].split(','))
		except:
			print("Oops, table doesn't exists")
	elif menu_item == '2':
		attrs = view.delete_menu()
		modelORM.delete(*attrs)
	elif menu_item == '3':
		attrs = view.update_menu()
		modelORM.update(*attrs)
	elif menu_item == '4':
		break
	else:
		continue
