# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import csrf
from classic.settings import *
from classic.master.models import Member, LegacyMember
from classic.master.metainfo import Master
from django.template import Context, loader
from datetime import date
from dateutil.relativedelta import *
from subprocess import *

import os
import xlrd

def main(request):
	today = date.today()
	next_month = today + relativedelta(months=+1)
	master = Master()

	t = loader.get_template("master.html")
	c = Context({
		"masters": master.read(),
		"next_month": next_month.strftime("%m"),
	})
	c.update(csrf(request))

	return HttpResponse(t.render(c))


def create_master(request):
	master = Master().archive()
	book = xlrd.open_workbook(file_contents=request.FILES["excel"].read(), encoding_override="cp949")
	rebuild_members(book.sheet_by_index(0))
	return HttpResponseRedirect('/manage')


def current_unregistered_members():
	unregistered_members = []
	for member in Member.objects.filter(club_role='비회원'):
		unregistered_members.append(LegacyMember(member))
	return unregistered_members


# http://docs.djangoproject.com/en/dev/topics/db/multi-db/#manually-selecting-a-database
def rebuild_members(excel_sheet):
	unregistered = current_unregistered_members()
	Member.objects.all().delete()
	for i in xrange(1, excel_sheet.nrows):
		row = excel_sheet.row_values(i)
		member = Member.build(row)
		member.save()
	for legacy in unregistered:
		member = legacy.populate()
		if not Member.objects.filter(pk=member.empid):
			member.save()

#http://www.numbergrinder.com/node/19
#Pulling data from Excel using Python, xlrd

