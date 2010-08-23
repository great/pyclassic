# -*- coding: utf-8 -*-
from django.db import models
from classic.master.models import Member
from datetime import date
from dateutil.relativedelta import *

class Lesson(models.Model):
	name	= models.CharField("Lesson", max_length=50)
	alias	= models.CharField("레슨명", max_length=50)
	active	= models.BooleanField(default=True)

	def __unicode__(self):
		return self.name

	def teachers(self):
		return len(Teacher.objects.filter(lesson=self.id).filter(active=True))

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
		return len(LessonClass.objects.filter(teacher=self.id))


class LessonClass(models.Model):
	empid		= models.CharField("사번", max_length=7)
	teacher		= models.ForeignKey(Teacher)
	name		= models.CharField("이름", max_length=50)
	department	= models.CharField("소속부서", blank=True, max_length=50)
	base		= models.IntegerField("기본", default=0)
	operational	= models.IntegerField("운영", default=0)
	performance	= models.IntegerField("연주", default=0)

	def net(self):
		return self.base + self.operational + self.performance

	def is_member(self):
		return bool(Member.objects.filter(pk=self.empid))

	def applies(self):
		return len(LessonClass.objects.filter(empid=self.empid))


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


