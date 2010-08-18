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
	def exist_current():
		today = date.today()
		try:
			Master.objects.get(pk=today.strftime("%Y%m"))
			return True
		except Master.DoesNotExist:
			return False

	@staticmethod
	def next():
		today = date.today()
		next = today + relativedelta(months=+1)
		try:
			return Master.objects.get(pk=next.strftime("%Y%m"))
		except Master.DoesNotExist:
			pass

	@staticmethod
	def current_key():
		return Master.objects.order_by('-rotation')[0].rotation

	@staticmethod
	def next_key():
		tmp_date = parse(Master.current_key() + '01')
		next = tmp_date + relativedelta(months=+1)
		return next.strftime("%Y%m")

	@staticmethod
	def create():
		pass
