from django import forms
from classic.lesson.models import LessonStudent, Teacher


class ContactForm(forms.Form):
	subject = forms.CharField(max_length=100)
	message = forms.CharField()
	sender = forms.EmailField()
	cc_myself = forms.BooleanField(required=False)


class StudentForm(forms.ModelForm):
	class Meta:
		model = Student


class TeacherForm(forms.Teacher):
	class Teacher:
		model = Teacher
		fields = ('name',)
