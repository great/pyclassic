# -*- coding: utf-8 -*-
from django.http import HttpResponse
from classic.utils import *
from classic.master.models import Master, Member
from classic.lesson.models import Lesson, Teacher, Student
from django.template import Context, loader
from datetime import date
from classic.extjs import grids, utils


def lesson_dashboard(request):
	mapping = {}
	for teacher in Teacher.objects.filter(active=True).order_by('name'):
		#if not teacher.students(): continue
		lesson = teacher.lesson
		students = list(Student.objects.filter(teacher=teacher.id).filter(active=True).order_by('empid'))
		if mapping.has_key(lesson): mapping[lesson][teacher] = students
		else: mapping[lesson] = {teacher: students}

	t = loader.get_template("lesson_dashboard.html")
	c = Context({
		"mapping": mapping,
		'members': len(Member.objects.exclude(club_role='비회원')),
	})
	return HttpResponse(t.render(c))


def lesson_applies(request, lesson_id, teacher_id=None):
	teachers = Teacher.objects.filter(lesson=lesson_id).filter(active=True)
	if (teacher_id): teachers = teachers.filter(pk=teacher_id)

	datasource = {}
	for teacher in teachers:
		datasource[teacher] = Student.objects.filter(teacher=teacher.id).order_by('empid')

	t = loader.get_template("lesson_applies.html")
	c = Context({
		"lesson": Lesson.objects.get(pk=lesson_id),
		"datasource": datasource,
	})
	return HttpResponse(t.render(c))


def lesson_aggregation(request):
	teachers = Teacher.objects.filter(active=True).order_by('lesson')

	students = 0
	fee = 0
	for teacher in teachers:
		students += teacher.students()
		fee += teacher.fee()

	t = loader.get_template('lesson_aggregation.html')
	c = Context({
		'teachers': teachers,
		'students': students,
		'fee': fee,
		
	})
	return HttpResponse(t.render(c))


def frontpage(request):
	lessons = Lesson.objects.all()
	datasource = {}
	for lesson in lessons: datasource[lesson] = Teacher.objects.filter(lesson=lesson.id).filter(active=True)
	t = loader.get_template("lessons.html")
	c = Context({
		"datasource": datasource,
	})
	return HttpResponse(t.render(c))

def lessons(request):
	lessons = Lesson.objects.all()
	datasource = {}
	for lesson in lessons: datasource[lesson] = Teacher.objects.filter(lesson=lesson.id)
	t = loader.get_template("lessons_detailed.html")
	c = Context({
		"datasource": datasource,
	})
	return HttpResponse(t.render(c))


def simple_all_classes(request):
	t = loader.get_template("lesson_classes.html")
	c = Context({
		"classes": Student.objects.all().order_by('teacher', 'name'),
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
	grid = grids.ModelGrid(Student)
	students = Student.objects.all()
	json = grid.to_grid(students, limit=100)
	print 'test run!!!!!'
	return utils.JsonResponse(json)

def contact(request):
	if request.method == 'POST': # If the form has been submitted...
		form = ContactForm(request.POST) # A form bound to the POST data
		if form.is_valid(): # All validation rules pass
			# Process the data in form.cleaned_data
			# ...
			return HttpResponseRedirect('/thanks/') # Redirect after POST
	else:
		form = ContactForm() # An unbound form

	return render_to_response('contact.html', {
		'form': form,
	})

def roweditor(request):
	c = Context({
	})
	t = loader.get_template("grid_way.html")
	return HttpResponse(t.render(c))

