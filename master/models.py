# -*- coding: utf-8 -*-
from django.db import models
from datetime import date
from dateutil.relativedelta import *
from dateutil.parser import *

# To play with interactive shell:
#http://docs.djangoproject.com/en/dev/intro/tutorial01/#playing-with-the-api
class Master(models.Model):
	rotation		= models.CharField("레슨 차수", primary_key=True, max_length=6)
	creation_date 	= models.DateField("자료생성일", auto_now=True, auto_now_add=True)
	database		= models.CharField(max_length=255)

	def __unicode__(self):
		return self.rotation

	@staticmethod
	def current_key():
		return Master.objects.order_by('-rotation')[0].rotation

	@staticmethod
	def next_key():
		tmp_date = parse(Master.current_key() + '01')
		next = tmp_date + relativedelta(months=+1)
		return next.strftime("%Y%m")


class Member(models.Model):
	COMPANY_CHOICES = ('NHN Business Corpopration', 'NHN Corporation', 'NHN I&S', '재단법인 해피빈')
	CLUB_ROLE_CHOICES = ('회장', '감사', '총무', '회원', '비회원')
	empid			= models.CharField("사번", max_length=7, primary_key=True)
	name			= models.CharField("이름", max_length=50)
	company			= models.CharField("소속", blank=True, max_length=50)
	title			= models.CharField("호칭", blank=True, max_length=20)
	join_date		= models.CharField("가입일", blank=True, max_length=10)
	club_role		= models.CharField("운영진", max_length=20)
	email			= models.EmailField(blank=True, max_length=100)
	cellular		= models.CharField("핸드폰번호", blank=True, max_length=20)
	department		= models.CharField("소속부서", blank=True, max_length=50)
	lesson_count	= models.IntegerField("레슨신청수", default=0)

	def __unicode__(self):
		return self.empid

	def is_member(self):
		return bool(unicode(u'비회원') != self.club_role)

	@staticmethod
	def build(excel_row):
		m = Member()
		m.empid			= excel_row[3]
		m.name			= excel_row[2]
		m.company		= excel_row[4]
		m.title			= excel_row[5]
		m.join_date		= excel_row[6]
		m.club_role		= excel_row[7]
		m.email			= excel_row[10]
		m.cellular		= excel_row[11]
		m.department	= excel_row[12]
		return m

