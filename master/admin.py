from classic.master.models import Member
from django.contrib import admin

class MemberAdmin(admin.ModelAdmin):
	list_display = ('empid', 'name', 'company', 'title',  'join_date', 'club_role', 'email', 'cellular', 'department', 'lesson_count',)
	list_filter = ('company', 'lesson_count',)

admin.site.register(Member, MemberAdmin)
