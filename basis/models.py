# -*- coding: utf-8 -*-
from django.db import models

class Round(models.Model):
	month 			= models.CharField("레슨 차수", unique_for_month="creation_date", max_length=6)
	creation_date 	= models.DateField("자료생성일", auto_now=True, auto_now_add=True)
	active			= models.BooleanField("모집상태", default=True)

	def __unicode__(self):
		return self.month

class Member(models.Model):
	month			= models.ForeignKey(Round)
	empno			= models.CharField("사번", max_length=7)
	name			= models.CharField("이름", max_length=50)
	company			= models.CharField("소속", max_length=50)
	title			= models.CharField("호칭", max_length=20)
	join_date		= models.DateField("가입일")
	club_role		= models.CharField("운영진", max_length=20)
	email			= models.CharField(max_length=100)
	cellular		= models.CharField("핸드폰번호", max_length=20)
	department		= models.CharField("소속부서", max_length=20)
	lesson_count	= models.IntegerField("레슨신청수")

	def __unicode__(self):
		return self.month + self.empno

