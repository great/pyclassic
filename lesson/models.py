# -*- coding: utf-8 -*-
from django.db import models
from classic.master.models import Member
from datetime import date
from dateutil.relativedelta import *


class Lesson(models.Model):
	name	= models.CharField("Lesson", max_length=50)
	alias	= models.CharField("레슨명", max_length=50)
	# pseudo-FK. null enabled(who knows manage it?)
	manager	= models.CharField("레슨담당자 사번", max_length=7, blank=True)
	desc	= models.TextField("설명", blank=True)
	active	= models.BooleanField(default=True)

	# http://markmail.org/message/3v3walw2qpszbi56
	def __init__(self, *args, **kwargs):
		super(Lesson, self).__init__(*args, **kwargs) 
		self.member = None

	def init_member(self):
		if self.manager and not self.member:
			self.member = Member.objects.get(pk=self.manager)

	def lesson_manager(self):
		self.init_member()
		return self.member

	def has_manager(self):
		self.init_member()
		return bool(self.member)

	def __unicode__(self):
		return self.name

	def teachers(self):
		return len(Teacher.objects.filter(lesson=self.id).filter(active=True))

	def has_teachers(self):
		return bool(self.teachers())

	def safe_rowspan(self):
		counts = len(Teacher.objects.filter(lesson=self.id).filter(active=True))
		if counts > 0:
			return counts
		else:
			return 1

	def students(self):
		teachers = Teacher.objects.filter(lesson=self.id).filter(active=True)
		students = 0
		for teacher in teachers: students += teacher.students()
		return students


class Teacher(models.Model):
	name		= models.CharField("이름", max_length=50)
	cellular	= models.CharField("핸드폰번호", blank=True, max_length=20)
	email		= models.EmailField(blank=True, max_length=100)
	lesson		= models.ForeignKey(Lesson)
	active		= models.BooleanField(default=True)

	def __unicode__(self):
		return self.name

	def students(self):
		return len(Student.objects.filter(teacher=self.id))

''' for the practical reason, FK not used:
when members deleted from Member model, automatically deleted from Student.
To prevent it, FK should be cut.
'''
class Student(models.Model):
	# exactly FK
	empid		= models.CharField("사번", max_length=7)
	teacher		= models.ForeignKey(Teacher)
	base		= models.IntegerField("기본", default=0)
	operational	= models.IntegerField("운영", default=0)
	performance	= models.IntegerField("연주", default=0)

	def __init__(self, *args, **kwargs):
		super(Student, self).__init__(*args, **kwargs) 
		self.member = None

	def init_member(self):
		if not self.member: self.member = Member.objects.get(pk=self.empid)

	def member(self):
		self.init_member()
		return self.member

	def name(self):
		self.init_member()
		return self.member.name

	def department(self):
		self.init_member()
		return self.member.department

	def net(self):
		return self.base + self.operational + self.performance

	def is_member(self):
		self.init_member()
		return self.member.is_member()

	def applies(self):
		return len(Student.objects.filter(empid=self.empid))


class Expense(models.Model):
	ITEM_CHOICES = (
		('GROUP', 'Group Lesson'),
		('PARKING', 'Parking fee'),
	)
	teacher	= models.ForeignKey(Teacher)
	item	= models.CharField(max_length=10, choices=ITEM_CHOICES)
	desc	= models.CharField('내용', max_length=200, blank=True)
	amount	= models.IntegerField('금액')


class Performer(models.Model):
	empid	= models.CharField("사번", max_length=7, primary_key=True)
	desc	= models.CharField("연주내용", max_length=500)
	applied	= models.BooleanField("반영여부", default=False)


class Operator(models.Model):
	OPERATOR_CHOICES = (
		('CLUB_CHIEF', '동호회 회장'),
		('ACCOUNT_MANAGER', '회계'),
		('LESSON_MANAGER', '레슨관리'),
		('MEETING_MANAGER', '정모담당'),
		('LESSON_CHIEF', '레슨대표'),
	)
	empid	= models.ForeignKey(Member)
	item	= models.CharField(max_length=50, choices=OPERATOR_CHOICES)
	desc	= models.CharField("내용", max_length=100)
	amount	= models.IntegerField('금액')


