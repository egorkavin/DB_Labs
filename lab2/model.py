import psycopg2
from psycopg2 import sql


def connect():
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="whatawonderfulday", host="localhost",
                            port="5432")
    cur = conn.cursor()
    return conn, cur


def insert(t_name: str, columns: tuple, values: tuple):
    conn, cur = connect()
    try:
        cur.execute(
            sql.SQL("INSERT INTO {table} ({columns}) VALUES({values})").format(
                table=sql.Identifier(t_name),
                columns=sql.SQL(',').join(map(sql.Identifier, columns)),
                values=sql.SQL(',').join(map(sql.Literal, values))))
        conn.commit()
    except psycopg2.Error as e:
        print(e)
    cur.close()
    conn.close()


def insert_teacher(values):
    insert("teacher", ("teacher_id", "first_name", "last_name"), values)


def insert_teacher_lesson(values):
    insert("teacher_lesson", ("teacher_id", "subject"), values)


def insert_lesson(values: tuple):
    insert("lesson", ("subject",), values)


def insert_group(values: tuple):
    insert("group", ("group_id", "group_name"), values)


def insert_student(values: tuple):
    insert("student", ("student_id", "group_id", "first_name", "last_name"), values)


def insert_student_lesson(values: tuple):
    insert("student_lesson", ("subject", "student_id", "grade"), values)


def delete(t_name, column, value):
    conn, cur = connect()
    try:
        cur.execute(
            sql.SQL("DELETE FROM {table} WHERE {column}={value}").format(
                table=sql.Identifier(t_name),
                column=sql.Identifier(column),
                value=sql.Literal(value)))
        conn.commit()
    except psycopg2.Error as e:
        print(e)
    cur.close()
    conn.close()


def update(t_name, column, value, cond):
    conn, cur = connect()
    try:
        cur.execute(
            sql.SQL("UPDATE {} SET {} = {} WHERE {}").format(
                sql.Identifier(t_name),
                sql.Identifier(column),
                sql.Literal(value),
                sql.SQL(cond)
            )
        )
        conn.commit()
    except psycopg2.Error as e:
        print(e)
    cur.close()
    conn.close()


def choose_sql_random(type):
    if type == "int":
        return sql.SQL("trunc(random() * 9 + 1)::int")
    elif type == "char":
        return sql.SQL("chr(trunc(65 + random()*26)::int)||chr(trunc(65 + random()*26)::int)")
    else:
        return sql.SQL("(SELECT {} FROM {} ORDER BY RANDOM() LIMIT 1)").format(
            sql.Identifier(type[0]), sql.Identifier(type[1])
        )


def random(t_name, columns, value_types, rows_number):
    conn, cur = connect()
    try:
        cur.execute(
            sql.SQL(
                "INSERT INTO {table} ({columns}) SELECT {values} FROM generate_series(1, {n}) ON CONFLICT DO NOTHING").format(
                table=sql.Identifier(t_name),
                columns=sql.SQL(',').join(map(sql.Identifier, columns)),
                values=sql.SQL(',').join(map(choose_sql_random, value_types)),
                n=sql.Literal(rows_number),
            )
        )
        conn.commit()
        return cur.query.decode("utf-8")
    except psycopg2.Error as e:
        print(e)


def random_teacher(rows_number):
    return random("teacher", ("first_name", "last_name"), ("char", "char"), rows_number)


def random_teacher_lesson(rows_number):
    return random("teacher_lesson", ("teacher_id", "subject"), (["teacher_id", "teacher"], ["subject", "lesson"]),
                  rows_number)


def random_lesson(rows_number):
    return random("lesson", ("subject",), ("char",), rows_number)


def random_group(rows_number):
    return random("group", ("group_name",), ("char",), rows_number)


def random_student(rows_number):
    return random("student", ("group_id", "first_name", "last_name"), (["group_id", "group"], "char", "char"),
                  rows_number)


def random_student_lesson(rows_number):
    return random("student_lesson", ("subject", "student_id", "grade"),
                  (["subject", "lesson"], ["student_id", "student"], "int"), rows_number)


def student_grade(first_name, last_name, grade_min, grade_max):
    conn, cur = connect()
    try:
        cur.execute("""
                SELECT s.first_name, s.last_name, sl.subject, sl.grade 
                FROM student s 
                INNER JOIN student_lesson sl on s.student_id = sl.student_id 
                WHERE sl.grade>%s AND sl.grade<%s AND s.first_name LIKE %s AND s.last_name LIKE %s
            """, (grade_min, grade_max, first_name, last_name))
        return [cur.query.decode("utf-8"), cur.fetchall()]
    except psycopg2.Error as e:
        print(e)


def teacher_subject(first_name, last_name, subject):
    conn, cur = connect()
    try:
        cur.execute("""
                SELECT t.first_name, t.last_name, tl.subject FROM teacher as t
                INNER JOIN teacher_lesson as tl
                ON t.teacher_id = tl.teacher_id
                WHERE t.first_name LIKE %s and t.last_name LIKE %s and tl.subject LIKE %s
            """, (first_name, last_name, subject))
        return [cur.query.decode("utf-8"), cur.fetchall()]
    except psycopg2.Error as e:
        print(e)


def student_teacher_subject(s_last_name, t_last_name, subject):
    conn, cur = connect()
    try:
        cur.execute("""
                SELECT s.last_name, t.last_name, tl.subject FROM student as s
                INNER JOIN student_lesson as sl
                    ON s.student_id = sl.student_id
                INNER JOIN teacher_lesson as tl
                    ON sl.subject = tl.subject
                INNER JOIN teacher as t
                    ON tl.teacher_id = t.teacher_id
                WHERE s.last_name LIKE %s and t.last_name LIKE %s and tl.subject LIKE %s
            """, (s_last_name, t_last_name, subject))
        return [cur.query.decode("utf-8"), cur.fetchall()]
    except psycopg2.Error as e:
        print(e)
