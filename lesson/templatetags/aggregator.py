from django.template import Library


register = Library()


def sum(students):
	s=0
	for student in students: s+= student.net()
	return s


def lesson_total(datasource):
	return len(datasource)

def teacher_total(datasource):
	s = 0
	for lesson in datasource.keys():
		s += lesson.teachers()
	return s

def student_total(reduced):
	return len(reduced)

def fee_total(reduced):
	s = 0
	for student in reduced:
		s += student.net()
	return s * 10000


register.filter(sum)
register.filter(lesson_total)
register.filter(teacher_total)
register.filter(student_total)
register.filter(fee_total)

