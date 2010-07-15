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

	def exist_rotation():
		today = date.today()
		try:
			Rotation.objects.get(pk=today.strftime("%Y%m"))
			return True
		except Rotation.DoesNotExist:
			return False

	def current_rotation():
		today = date.today()
		try:
			return Rotation.objects.get(pk=today.strftime("%Y%m"))
		except Rotation.DoesNotExist:
			return False

	def create_rotation():
		pass

class Member(models.Model):
	rotation		= models.ForeignKey(Rotation)
	empno			= models.CharField("사번", max_length=7)
	name			= models.CharField("이름", max_length=50)
	company			= models.CharField("소속", blank=True, max_length=50)
	title			= models.CharField("호칭", blank=True, max_length=20)
	join_date		= models.CharField("가입일", max_length=10)
	club_role		= models.CharField("운영진", blank=True, max_length=20)
	email			= models.EmailField(max_length=100)
	cellular		= models.CharField("핸드폰번호", max_length=20)
	department		= models.CharField("소속부서", max_length=20)
	lesson_count	= models.IntegerField("레슨신청수", default=0)

	def __unicode__(self):
		return (self.empno + " " + self.name + " " + self.department)

	def build(self, fk, excel_row):
		self.rotation	= fk
		self.empno		= excel_row[3]
		self.name		= excel_row[2]
		self.company	= excel_row[4]
		self.title		= excel_row[5]
		self.join_date	= excel_row[6]
		self.club_role	= excel_row[7]
		self.email		= excel_row[10]
		self.cellular	= excel_row[11]
		self.department	= excel_row[12]
		self.lesson_count = 0
		return self

