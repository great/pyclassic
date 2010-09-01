from classic.lesson.models import *
from django.contrib import admin

# http://docs.djangoproject.com/en/dev/ref/contrib/admin/
class LessonAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'alias', 'desc', 'manager', 'active',)

class TeacherAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'lesson', 'active',)
	list_filter = ('lesson',)

class StudentAdmin(admin.ModelAdmin):
	list_display = ('empid', 'name', 'teacher', 'base', 'operational', 'performance')
	list_filter = ('teacher',)

class ExpenseAdmin(admin.ModelAdmin):
	list_display = ('teacher', 'item', 'desc', 'amount',)

class PerformerAdmin(admin.ModelAdmin):
	list_display = ('empid', 'desc', 'applied',)


class OperatorAdmin(admin.ModelAdmin):
	list_display = ('empid', 'item', 'desc', 'amount',)

admin.site.register(Lesson, LessonAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Performer, PerformerAdmin)
admin.site.register(Operator, OperatorAdmin)

