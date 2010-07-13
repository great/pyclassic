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

	(r'^admin/', include(admin.site.urls)),
	(r'^manage$', 'classic.basis.views.list_basis'),
	#	(r'^basis/arrange$', 'classic.basis.views.arrange_lesson'),
	(r'^manage/create$', 'classic.basis.views.create_basis'),
	(r'^basis/create$', 'classic.basis.views.create_lesson'),
	(r'^basis/members$', 'classic.basis.views.list_members'),
)
