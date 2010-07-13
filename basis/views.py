# -*- coding: utf-8 -*-
from django.http import HttpResponse
from classic.basis.models import Rotation, Member
from django.template import Context, loader
from datetime import date
from dateutil.relativedelta import *

import os
import xlrd

APP_BASE = os.environ["HOME"] + "/com.nhn.club"

def list_basis(request):
	today = date.today()
	next_month = today + relativedelta(months=+1)

	rotations = Rotation.objects.all().order_by("-rotation")[:12]
	t = loader.get_template("rotations.html")
	c = Context({
		"rotations": rotations,
		"today": today,
		"current_year": today.strftime("%Y"),
		"current_month": today.strftime("%m"),
		"next_month": next_month.strftime("%m"),
	})

	return HttpResponse(t.render(c))

#http://www.numbergrinder.com/node/19
def create_lesson(request):
	today = date.today()
	book = xlrd.open_workbook(APP_BASE + "/test_members.xls", encoding_override="cp949")
	sheet = book.sheet_by_index(0)

	rotation = Rotation(rotation="201007", creation_date=today)
	import_members(rotation, sheet)

	t = loader.get_template("members.html")

	c = Context({
		"members": sheet,
	})
	return HttpResponse(t.render(c))

def import_members(rotation, excel_sheet):
	for i in xrange(1, excel_sheet.nrows):
		row = excel_sheet.row_values(i)
		member = Member(
			rotation = rotation,
			empno = row[3],
			name = row[2],
			company = row[4],
			title = row[5],
			join_date = row[6],
			club_role = row[7],
			email = row[10],
			cellular = row[11],
			department = row[12],
			lesson_count = 0,
		)
		member.save()

def list_members(request):
	members = Member.objects.filter(rotation="201007")
	t = loader.get_template("members.html")
	c = Context({
		"members": members,
	})

	return HttpResponse(t.render(c))

