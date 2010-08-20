# -*- coding: utf-8 -*-
from django.http import HttpResponse
from classic.master.models import Master
from classic.lesson.models import Lesson, Teacher, LessonClass
from django.template import Context, loader
from datetime import date


# for reduce() expression:
# http://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python
# OR, http://docs.python.org/library/functions.html#reduce
def classes(request):
#	lesson_map = {}
#	for lesson in Lesson.objects.filter(active=True):
#		teachers = list(Teacher.objects.filter(lesson=lesson.id))
#		if teachers: lesson_map[lesson] = teachers

#	teacher_map = {}
#	for teacher in reduce(lambda x,y: x+y,lesson_map.values()):
#		members = list(LessonClass.objects.filter(teacher=teacher.id))
#		if members: teacher_map[teacher] = members



	lesson_teacher = {}
	teacher_student = {}
	for teacher in Teacher.objects.all():
		if not teacher.students(): continue
		lesson = teacher.lesson
		if lesson_teacher.has_key(lesson): lesson_teacher[lesson].append(teacher)
		else: lesson_teacher[lesson] = [teacher]
		teacher_student[teacher] = list(LessonClass.objects.filter(teacher=teacher.id))



	mapping = {}
	for teacher in Teacher.objects.all():
		if not teacher.students(): continue
		lesson = teacher.lesson
		students = list(LessonClass.objects.filter(teacher=teacher.id))
		if mapping.has_key(lesson): mapping[lesson][teacher] = students
		else: mapping[lesson] = {teacher: students}

	t = loader.get_template("lesson_classes.html")
	c = Context({
		"lesson_teacher": lesson_teacher,
		"teacher_student": teacher_student,
		"mapping": mapping,
		"classes": LessonClass.objects.all().order_by('teacher', 'name'),
	})
	return HttpResponse(t.render(c))


def simple_all_classes(request):

	t = loader.get_template("lesson_classes.html")
	c = Context({
		"classes": LessonClass.objects.all().order_by('teacher', 'name'),
	})
	return HttpResponse(t.render(c))



def teachers(request):
	c = Context({
		"teachers": Teacher.objects.all(),
	})
	t = loader.get_template("teachers.html")
	return HttpResponse(t.render(c))


def test(request):
	c = Context({
		"listing": ['a', 'b', 'c', 'd'],
	})
	t = loader.get_template("testing.html")
	return HttpResponse(t.render(c))
