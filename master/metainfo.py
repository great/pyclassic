# -*- coding: utf-8 -*-
from classic.settings import *
from datetime import date
from dateutil.relativedelta import *
from dateutil.parser import *
from subprocess import *
import glob

class Master():
	catalog = []

	def __init__(self):
		self.catalog = glob.glob(DATABASE + '.*')
		self.catalog.sort()

	def archive(self):
		key = self.nextkey()
		target = DATABASE + '.' + key
		Popen(['cp', DATABASE, target])
		self.catalog.append(target)
		return key

	def read(self):
		return tuple(self.catalog)

	def nextkey(self):
		if (self.catalog):
			tmp_date = parse(self.catalog[-1].split('.')[-1] + '01')
			next = tmp_date + relativedelta(months=+1)
			return next.strftime("%Y%m")
		else:
			return (date.today() + relativedelta(months=+1)).strftime("%Y%m")

