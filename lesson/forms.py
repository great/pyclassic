from django.forms import *

class ContactForm(Form):
	subject = CharField(max_length=100)
	message = CharField()
	sender = EmailField()
	cc_myself = BooleanField(required=False)


class StudentForm(Form):
	empid		= CharField(max_length=7)
	name		= CharField(max_length=100)
	department	= CharField(max_length=100)
	base		= IntegerField()
	operational	= IntegerField()
	performance	= IntegerField()
	#teacher		= HiddenField()
