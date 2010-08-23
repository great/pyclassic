# -*- coding: utf-8 -*-
from django.http import HttpResponse
from classic.master.models import Master
from classic.lesson.models import Lesson, Teacher, LessonClass
from django.template import Context, loader
from datetime import date
from classic.extjs import grids, utils


def lesson_full_sheet(request):
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

def lesson_applies(request, lesson_id, teacher_id=None):
	teachers = Teacher.objects.filter(lesson=lesson_id)
	if (teacher_id): teachers = teachers.filter(pk=teacher_id)

	mapping = {}
	for teacher in teachers: mapping[teacher] = LessonClass.objects.filter(teacher=teacher.id)

	t = loader.get_template("lesson_applies.html")
	c = Context({
		"lesson": Lesson.objects.get(pk=lesson_id),
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


def plain_python(request):
	c = Context({
		"listing": ['a', 'b', 'c', 'd'],
	})
	t = loader.get_template("testing.html")
	return HttpResponse(t.render(c))

def test(request):
	grid = grids.ModelGrid(LessonClass)
	students = LessonClass.objects.all()
	json = grid.to_grid(students, limit=100)
	return utils.JsonResponse(json)
