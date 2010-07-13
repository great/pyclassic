from django.http import HttpResponse
from classic.basis.models import Round
from django.template import Context, loader
from datetime import date
from dateutil.relativedelta import *

import os
import xlrd

APP_BASE = os.environ["HOME"] + "/com.nhn.club"

def list(request):
	today = date.today()
	next_month = today + relativedelta(months=+1)

	lesson_rounds = Round.objects.all().order_by("-month")[:12]
	t = loader.get_template("rounds.html")
	c = Context({
		"lesson_rounds": lesson_rounds,
		"today": today,
		"current_year": today.strftime("%Y"),
		"current_month": today.strftime("%m"),
		"next_month": next_month.strftime("%m"),
	})

	return HttpResponse(t.render(c))

#http://www.numbergrinder.com/node/19
def create_lesson(request):
	today = date.today()
	book = xlrd.open_workbook(APP_BASE + "/test_members.xls")	# encoding_override="cp949"
	sheet = book.sheet_by_index(0)

	t = loader.get_template("members.html")
	for i in xrange(sheet.nrows):
		print sheet.row_values(i)

	c = Context({
		"members": sheet,
	})
	return HttpResponse(t.render(c))

