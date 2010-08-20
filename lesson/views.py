# -*- coding: utf-8 -*-
from django.http import HttpResponse
from classic.master.models import Master
from classic.lesson.models import Lesson, Teacher, LessonClass
from django.template import Context, loader
from datetime import date


def classes(request):
	mapping = {}
	for teacher in Teacher.objects.all():
		if not teacher.students(): continue
		lesson = teacher.lesson
		students = list(LessonClass.objects.filter(teacher=teacher.id))
		if mapping.has_key(lesson): mapping[lesson][teacher] = students
		else: mapping[lesson] = {teacher: students}

	t = loader.get_template("lesson_classes.html")
	c = Context({
		"mapping": mapping,
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
