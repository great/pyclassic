from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	# Example:
	# (r'^classic/', include('classic.foo.urls')),

	# Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
	# to INSTALLED_APPS to enable admin documentation:
	# (r'^admin/doc/', include('django.contrib.admindocs.urls')),

	(r'^__import__$', 'classic.basis.views.create_lesson'),

	(r'^admin/', include(admin.site.urls)),
	(r'^manage$', 'classic.basis.views.rotations'),
	#	(r'^basis/arrange$', 'classic.basis.views.arrange_lesson'),
	(r'^manage/prepare$', 'classic.basis.views.list_members'),
	(r'^manage/import$', 'classic.basis.views.import_excel'),
)
