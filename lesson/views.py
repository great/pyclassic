# -*- coding: utf-8 -*-
from django.http import HttpResponse
from classic.master.models import Master
from classic.lesson.models import Lesson, Teacher, LessonClass
from django.template import Context, loader
from datetime import date

import os

APP_BASE = os.environ["HOME"] + "/com.nhn.club"

def lesson_classes(request):
	lessons = Lesson.objects.using('slot').all()
	teachers = Teacher.objects.using('slot').all()
	classes = LessonClass.objects.using('slot').all()
	#t = loader.get_template("members.html")
	t = loader.get_template("teachers.html")
	c = Context({
		"lessons": lessons,
	})
	return HttpResponse(t.render(c))

def teachers(request):
	c = Context({
		"teachers": Teacher.objects.using('slot').all(),
	})
	t = loader.get_template("teachers.html")
	return HttpResponse(t.render(c))

def test(request):

	c = Context({
		"listing": ['a', 'b', 'c', 'd'],
	})
	t = loader.get_template("testing.html")
	return HttpResponse(t.render(c))
