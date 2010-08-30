from django.conf.urls.defaults import *
from classic.settings import *

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
	(r'^manage$', 'classic.master.views.main'),
	(r'^manage/create$', 'classic.master.views.create_master'),
	#	(r'^master/arrange$', 'classic.master.views.arrange_lesson'),
	(r'^lesson/teachers$', 'classic.lesson.views.teachers'),
	(r'^lesson/dashboard$', 'classic.lesson.views.lesson_dashboard'),
	(r'^lesson/(?P<lesson_id>\d+)$', 'classic.lesson.views.lesson_applies'),
	(r'^lesson/(?P<lesson_id>\d+)/(?P<teacher_id>\d+)$', 'classic.lesson.views.lesson_applies'),
	(r'^lessons$', 'classic.lesson.views.lessons'),
	(r'^test$', 'classic.lesson.views.test'),
	(r'^roweditor/', 'classic.lesson.views.roweditor'),
	(r'^resources/(?P<path>.*)$', 'django.views.static.serve', {'document_root': APP_BASE + '/classic/resources'}),

)
