from django import forms
from classic.lesson.models import LessonClass, Teacher


class ContactForm(forms.Form):
	subject = forms.CharField(max_length=100)
	message = forms.CharField()
	sender = forms.EmailField()
	cc_myself = forms.BooleanField(required=False)


class LessonClassForm(forms.ModelForm):
	class Meta:
		model = LessonClass


class TeacherForm(forms.Teacher):
	class Teacher:
		model = Teacher
		fields = ('name',)
