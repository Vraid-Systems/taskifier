from django.conf.urls.defaults import patterns

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
                       (r'^_ah/warmup$', 'djangoappengine.views.warmup'),
                       (r'^$',
                        'django.views.generic.simple.direct_to_template',
                        {'template': 'home.html'}),
                       (r'^data/(\w+)$', 'taskifier.taskrouter'),
                       (r'^data/(\w+)/(\d+)$', 'taskifier.taskrouter'),)
