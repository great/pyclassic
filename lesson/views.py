# -*- coding: utf-8 -*-
from django.http import HttpResponse
from classic.master.models import Master
from classic.lesson.models import Lesson, Teacher, LessonClass
from django.template import Context, loader
from datetime import date

import os

APP_BASE = os.environ["HOME"] + "/com.nhn.club"

def classes(request):
	lessons = Lesson.objects.filter(active=True)
	teachers = {}
	for lesson in lessons:
		teachers[lesson] = list(Teacher.objects.filter(lesson=lesson.id))
	clss_map = {}
	# http://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python
	# OR, http://docs.python.org/library/functions.html#reduce
	for teacher in reduce(lambda x,y: x+y,teachers.values()):
		clss_map[teacher] = LessonClass.objects.filter(teacher=teacher.id)
	t = loader.get_template("lesson_classes.html")
	c = Context({
		"lessons": lessons,
		"teachers": teachers,
		"clss_map": clss_map,
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
