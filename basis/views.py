from django.http import HttpResponse
from classic.basis.models import Round
from django.template import Context, loader

def list(request):
	lesson_rounds = Round.objects.all().order_by("-month")[:12]
	t = loader.get_template("rounds.html")
	c = Context({
		"lesson_rounds": lesson_rounds,
	})

	return HttpResponse(t.render(c))

