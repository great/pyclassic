from classic.lesson.models import Member, Lesson, Teacher
from django.contrib import admin

class MultiDBModelAdmin(admin.ModelAdmin):
	# A handy constant for the name of the alternate database.
	using = 'slot'

	def save_model(self, request, obj, form, change):
		# Tell Django to save objects to the 'other' database.
		obj.save(using=self.using)

	def queryset(self, request):
		# Tell Django to look for objects on the 'other' database.
		return super(MultiDBModelAdmin, self).queryset(request).using(self.using)

	def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
		# Tell Django to populate ForeignKey widgets using a query
		# on the 'other' database.
		return super(MultiDBModelAdmin, self).formfield_for_foreignkey(db_field, request=request, using=self.using, **kwargs)

	def formfield_for_manytomany(self, db_field, request=None, **kwargs):
		# Tell Django to populate ManyToMany widgets using a query
		# on the 'other' database.
		return super(MultiDBModelAdmin, self).formfield_for_manytomany(db_field, request=request, using=self.using, **kwargs)

from django.db import connections
cursor = connections['slot'].cursor()

admin.site.register(Member, MultiDBModelAdmin)
admin.site.register(Lesson, MultiDBModelAdmin)
admin.site.register(Teacher, MultiDBModelAdmin)
