import view
import model
import time

while True:
    menu_item = view.main_menu()
    print(menu_item)
    if menu_item == '1':
        attrs = view.insert_menu()
        try:
            getattr(model, f'insert_{attrs[0]}')(attrs[1].split(','))
        except:
            print("Oops, table doesn't exists")

    elif menu_item == '2':
        attrs = view.delete_menu()
        model.delete(*attrs)
    elif menu_item == '3':
        attrs = view.update_menu()
        model.update(*attrs)
    elif menu_item == '4':
        attrs = view.random_menu()
        try:
            view.show_random_query(getattr(model, f'random_{attrs[0]}')(int(attrs[1])))
        except:
            print("Oops, table doesn't exists")
    elif menu_item == '5':
        attrs = view.select_menu()
        f_name = ['student_grade', 'teacher_subject', 'student_teacher_subject'][int(attrs[0]) - 1]
        time_before = time.time()
        try:
            query, rows = getattr(model, f_name)(*attrs[1].split(','))
            time_after = time.time()
            view.show_select(query, rows, round((time_after - time_before) * 1000))
        except:
            print("Oops, table doesn't exists")
    elif menu_item == '6':
        break
    else:
        continue
