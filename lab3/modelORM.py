import sys

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


class Group(Base):
	__tablename__ = 'group'
	group_id = Column(Integer, primary_key=True)
	group_name = Column(String)
	students = relationship('Student')

	def __repr__(self):
		return "<Group(group_id='{}', group_name='{}')>" \
			.format(self.group_id, self.group_name)


class Student(Base):
	__tablename__ = 'student'
	student_id = Column(Integer, primary_key=True)
	group_id = Column(Integer, ForeignKey('group.group_id'))
	first_name = Column(String)
	last_name = Column(String)
	students_lessons = relationship('StudentLesson')


class Lesson(Base):
	__tablename__ = 'lesson'
	subject = Column(String, primary_key=True)
	students_lessons = relationship('StudentLesson')
	teachers_lessons = relationship('TeacherLesson')


class StudentLesson(Base):
	__tablename__ = 'student_lesson'
	student_id = Column(String, ForeignKey('lesson.subject'), primary_key=True)
	subject = Column(Integer, ForeignKey('student.student_id'), primary_key=True)
	grade = Column(Integer)


class Teacher(Base):
	__tablename__ = 'teacher'
	teacher_id = Column(Integer, primary_key=True)
	first_name = Column(String)
	last_name = Column(String)
	teachers_lessons = relationship('TeacherLesson')


class TeacherLesson(Base):
	__tablename__ = 'teacher_lesson'
	id = Column(Integer, primary_key=True)
	teacher_id = Column(Integer, ForeignKey('teacher.teacher_id'))
	subject = Column(String, ForeignKey('lesson.subject'))


DATABASE_URI = 'postgres+psycopg2://postgres:whatawonderfulday@localhost:5432/postgres'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
s = Session()


def insert_group(values: tuple):
	try:
		group = Group(group_id=values[0], group_name=values[1])
		s.add(group)
		s.commit()
	except SQLAlchemyError as e:
		print(e)


def insert_teacher(values: tuple):
	try:
		teacher = Teacher(teacher_id=values[0], first_name=values[1], last_name=values[2])
		s.add(teacher)
		s.commit()
	except SQLAlchemyError as e:
		print(e)


def insert_student(values: tuple):
	try:
		student = Student(student_id=values[0], group_id=values[1], first_name=values[2], last_name=values[3])
		s.add(student)
		s.commit()
	except SQLAlchemyError as e:
		print(e)


def insert_lesson(values: tuple):
	try:
		lesson = Lesson(subject=values[0])
		s.add(lesson)
		s.commit()
	except SQLAlchemyError as e:
		print(e)


def insert_student_lesson(values: tuple):
	try:
		student_lesson = StudentLesson(subject=values[0], student_id=values[1], grade=values[2])
		s.add(student_lesson)
		s.commit()
	except SQLAlchemyError as e:
		print(e)


def insert_teacher_lesson(values: tuple):
	try:
		teacher_lesson = TeacherLesson(id=values[0], teacher_id=values[1], subject=values[2])
		s.add(teacher_lesson)
		s.commit()
	except SQLAlchemyError as e:
		print(e)


def delete(t_name, column, value):
	try:
		t_class = getattr(sys.modules[__name__], t_name.capitalize())
		t_class_col = getattr(t_class, column)
		s.query(t_class).filter(t_class_col == value).delete()
		s.commit()
	except SQLAlchemyError as e:
		print(e)


def update(t_name, column, value, cond):
	try:
		t_class = getattr(sys.modules[__name__], t_name.capitalize())
		t_class_col = getattr(t_class, column)
		t_class_cond_col = getattr(t_class, cond[0])
		s.query(t_class).filter(t_class_cond_col == cond[1]).update({t_class_col: value})
		s.commit()
	except SQLAlchemyError as e:
		print(e)
