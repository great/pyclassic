# -*- coding: utf-8 -*-
from django.db import models
from datetime import date
from dateutil.relativedelta import *

class Rotation(models.Model):
	rotation		= models.CharField("레슨 차수", primary_key=True, max_length=6)
	creation_date 	= models.DateField("자료생성일", auto_now=True, auto_now_add=True)
	archive			= models.BooleanField(default=False)

	def __unicode__(self):
		return self.rotation

	@staticmethod
	def exist_current():
		today = date.today()
		try:
			Rotation.objects.get(pk=today.strftime("%Y%m"))
			return True
		except Rotation.DoesNotExist:
			return False

	@staticmethod
	def current():
		today = date.today()
		try:
			return Rotation.objects.get(pk=today.strftime("%Y%m"))
		except Rotation.DoesNotExist:
			pass

	@staticmethod
	def next():
		today = date.today()
		next = today + relativedelta(months=+1)
		try:
			return Rotation.objects.get(pk=next.strftime("%Y%m"))
		except Rotation.DoesNotExist:
			pass

	@staticmethod
	def create():
		pass

class Member(models.Model):
	rotation		= models.ForeignKey(Rotation)
	empno			= models.CharField("사번", max_length=7)
	name			= models.CharField("이름", max_length=50)
	company			= models.CharField("소속", blank=True, max_length=50)
	title			= models.CharField("호칭", blank=True, max_length=20)
	join_date		= models.CharField("가입일", max_length=10)
	club_role		= models.CharField("운영진", blank=True, max_length=20)
	email			= models.EmailField(blank=True, max_length=100)
	cellular		= models.CharField("핸드폰번호", blank=True, max_length=20)
	department		= models.CharField("소속부서", blank=True, max_length=20)
	lesson_count	= models.IntegerField("레슨신청수", default=0)

	class Meta:
		unique_together = (("rotation", "empno"),)

	def __unicode__(self):
		return (self.empno + " " + self.name + " " + self.department)

	@staticmethod
	def build(fk, xlrow):
		m = Member(rotation=fk)
		m.empno			= xlrow[3]
		m.name			= xlrow[2]
		m.company		= xlrow[4]
		m.title			= xlrow[5]
		m.join_date		= xlrow[6]
		m.club_role		= xlrow[7]
		m.email			= xlrow[10]
		m.cellular		= xlrow[11]
		m.department	= xlrow[12]
		m.save()

