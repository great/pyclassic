# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.core.context_processors import csrf
from classic.settings import *
from classic.master.models import Master
from classic.lesson.models import Member
from django.template import Context, loader
from datetime import date
from dateutil.relativedelta import *
from subprocess import *

import os
import xlrd

def main(request, init_slot=None):
	today = date.today()
	next_month = today + relativedelta(months=+1)
	#next_rotation = Master.objects.filter(pk=next_month.strftime("%Y%m"))

	#rotations = Master.objects.exclude(archive=False).order_by("-rotation")[:12]
	masters = Master.objects.order_by("-rotation")[:12]

	t = loader.get_template("master.html")
	c = Context({
		"masters": masters,
		"next_month": next_month.strftime("%m"),
		"init_slot": init_slot,
	})
	c.update(csrf(request))

	return HttpResponse(t.render(c))


def create_master(request):
	today = date.today()
	#current_key = Master.current_key()
	next_key = Master.next_key()
	book = xlrd.open_workbook(file_contents=request.FILES["excel"].read(), encoding_override="cp949")
	sheet = book.sheet_by_index(0)
	if (os.path.exists(ROTATIONAL_DATABASE)):
		archived_database = ROTATIONAL_DATABASE + '.' + next_key
		Popen(['cp', ROTATIONAL_DATABASE, archived_database])
		Master(rotation=next_key, creation_date=today, database = archived_database).save()
		rebuild_members(sheet)
		init_slot=None
	else:
		init_slot = init_slot_database()

	return main(request, init_slot)

def init_slot_database():
	command = './manage.py sqlall lesson | ./manage.py dbshell --database=slot'
	#Popen(command)
	return "Database newly Initialized."

#http://docs.djangoproject.com/en/dev/topics/db/multi-db/#manually-selecting-a-database
def rebuild_members(excel_sheet):
	Member.objects.using('slot').all().delete()
	for i in xrange(1, excel_sheet.nrows):
		row = excel_sheet.row_values(i)
		member = Member(
			empid = row[3],
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
		member.save(using='slot')


#http://www.numbergrinder.com/node/19
def create_lesson(request):
	today = date.today()
	book = xlrd.open_workbook(APP_BASE + "/test_members.xls", encoding_override="cp949")
	sheet = book.sheet_by_index(0)

	rotation = Master(rotation="201007", creation_date=today)
	rebuild_members(rotation, sheet)

	t = loader.get_template("members.html")

	c = Context({
		"members": sheet,
	})
	return HttpResponse(t.render(c))

