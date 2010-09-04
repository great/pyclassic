from django.template import Library
from classic.utils import *

register = Library()


def sum(students):
	s=0
	for student in students: s+= student.net()
	return s

def payment(teacher, students):
	s=0
	for expense in teacher.additional(): s+= expense.amount
	for student in students: s+= student.net()
	return s

def lesson_total(mapping):
	return len(mapping)

def teacher_total(mapping):
	s = 0
	for lesson in mapping.keys():
		s += lesson.teachers()
	return s

def student_total(mapping):
	s = 0
	for lesson in mapping.keys():
		s += lesson.students()
	return s

def fee_total(mapping):
	s = 0
	dict_list = []
	for teacher_map in mapping.values():
		for teacher, students in teacher_map.items():
			s += payment(teacher, students)
	return formatted(s)

def reduced(base, amount):
	return base / amount

def formatnum(num):
	return formatted(num)


register.filter(sum)
register.filter(payment)
register.filter(lesson_total)
register.filter(teacher_total)
register.filter(student_total)
register.filter(fee_total)
register.filter(reduced)
register.filter(formatnum)
