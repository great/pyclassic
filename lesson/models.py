# -*- coding: utf-8 -*-
from django.db import models
from classic.master.models import Member
from datetime import date
from dateutil.relativedelta import *

class Lesson(models.Model):
	name	= models.CharField("Lesson", max_length=50)
	alias	= models.CharField("레슨명", max_length=50)

	def __unicode__(self):
		return self.name

	def teachers(self):
		return len(Teacher.objects.filter(lesson=self.id).filter(active=True))

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
	empid		= models.ForeignKey(Member)
	teacher		= models.ForeignKey(Teacher)
	name		= models.CharField("이름", max_length=50)
	department	= models.CharField("소속부서", blank=True, max_length=50)
	base		= models.IntegerField("기본", default=0)
	operational	= models.IntegerField("운영", default=0)
	performance	= models.IntegerField("연주", default=0)

	def net(self):
		return self.base + self.operational + self.performance


class Performer(models.Model):
	empid	= models.CharField("사번", max_length=7, primary_key=True)
	desc	= models.CharField("연주내용", max_length=500)
	applied	= models.BooleanField("반영여부", default=False)

class Operator(models.Model):
	empid	= models.ForeignKey(Member)
	desc	= models.CharField("내용", max_length=100)
