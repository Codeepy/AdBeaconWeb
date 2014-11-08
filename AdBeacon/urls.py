from django.conf.urls import patterns, include, url
from django.contrib import admin

router = routers.DefaultRouter()
router.register(r'advs', views.AdvtViewSet)
router.register(r'beacons', views.BeaconViewSet)
urlpatterns = patterns('',
    url(r'^$', 'AdBeacon.views.home', name='home'),
    url(r'^api/',include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^publish/', include('publish.urls')),
)
