# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.core.context_processors import csrf
from classic.basis.models import Rotation, Member
from django.template import Context, loader
from datetime import date
from dateutil.relativedelta import *

import os
import xlrd

APP_BASE = os.environ["HOME"] + "/com.nhn.club"

def rotations(request):
	today = date.today()
	next_month = today + relativedelta(months=+1)

	current_rotation = Rotation.objects.filter(pk=today.strftime("%Y%m"))
	next_rotation = Rotation.objects.filter(pk=next_month.strftime("%Y%m"))
	rotations = Rotation.objects.exclude(archive=False).order_by("-rotation")[:12]

	t = loader.get_template("rotations.html")
	c = Context({
		"current_rotation": current_rotation,
		"next_rotation": next_rotation,
		"rotations": rotations,
		"today": today,
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

def import_excel(request):
	today = date.today()
	book = xlrd.open_workbook(file_contents=request.FILES["excel"].read(), encoding_override="cp949")
	sheet = book.sheet_by_index(0)
	rotation = Rotation(rotation="200907", creation_date=today)
	import_members(rotation, sheet)
	
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
	try:
		rotation = Rotation.objects.get(pk="201007")
	except Rotation.DoesNotExist:
		rotation = Rotation()
	members = Member.objects.filter(rotation="201007")
	t = loader.get_template("members.html")
	c = Context({
		"rotation": rotation,
		"members": members,
	})
	c.update(csrf(request))
	return HttpResponse(t.render(c))


def prepare_rotation(request):
	today = date.today()
	next_month = today + relativedelta(months=+1)

def test_here(request):
	today = Rotation.next()
	if today:
		print today
	else:
		print "NULL"
	t = loader.get_template("test_here.html")
	c = Context({
	})
	return HttpResponse(t.render(c))

