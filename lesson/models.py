# -*- coding: utf-8 -*-
from django.db import models
from datetime import date
from dateutil.relativedelta import *

class Member(models.Model):
	empid			= models.CharField("사번", max_length=7, primary_key=True)
	name			= models.CharField("이름", max_length=50)
	company			= models.CharField("소속", blank=True, max_length=50)
	title			= models.CharField("호칭", blank=True, max_length=20)
	join_date		= models.CharField("가입일", max_length=10)
	club_role		= models.CharField("운영진", blank=True, max_length=20)
	email			= models.EmailField(blank=True, max_length=100)
	cellular		= models.CharField("핸드폰번호", blank=True, max_length=20)
	department		= models.CharField("소속부서", blank=True, max_length=50)
	lesson_count	= models.IntegerField("레슨신청수", default=0)

	def __unicode__(self):
		return (self.empid + " " + self.name + " " + self.department)

	@staticmethod
	def build(xls_rowvalue):
		m = Member()
		m.empid			= xls_rowvalue[3]
		m.name			= xls_rowvalue[2]
		m.company		= xls_rowvalue[4]
		m.title			= xls_rowvalue[5]
		m.join_date		= xls_rowvalue[6]
		m.club_role		= xls_rowvalue[7]
		m.email			= xls_rowvalue[10]
		m.cellular		= xls_rowvalue[11]
		m.department	= xls_rowvalue[12]
		m.save()

class Lesson(models.Model):
	name	= models.CharField("Lesson", max_length=50)
	alias	= models.CharField("레슨명", max_length=50)

	def __unicode__(self):
		return self.name

class Teacher(models.Model):
	name	= models.CharField("이름", max_length=50)
	email	= models.EmailField(blank=True, max_length=100)
	lesson	= models.ForeignKey(Lesson)

	def __unicode__(self):
		return self.name

class LessonClass(models.Model):
	empid		= models.ForeignKey(Member)
	teacher		= models.ForeignKey(Teacher)
	name		= models.CharField("이름", max_length=50)
	department	= models.CharField("소속부서", blank=True, max_length=50)
	base		= models.IntegerField("기본", default=0)
	operational	= models.IntegerField("운영", default=0)
	performance	= models.IntegerField("연주", default=0)

class Performer(models.Model):
	empid	= models.CharField("사번", max_length=7, primary_key=True)
	desc	= models.CharField("연주내용", max_length=500)
	applied	= models.BooleanField("반영여부", default=False)

class Operator(models.Model):
	empid	= models.ForeignKey(Member)
	desc	= models.CharField("내용", max_length=100)
