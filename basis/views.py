from django.http import HttpResponse
from classic.basis.models import Round
from django.template import Context, loader
from datetime import date
from dateutil.relativedelta import *

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

