from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from rest_framework import routers
from publish import views
from publish.models import Advertisement

router = routers.DefaultRouter()
router.register(r'advs', views.AdvtViewSet)
router.register(r'beacons', views.BeaconViewSet)
urlpatterns = patterns('',
    url(r'^$', 'AdBeacon.views.home', name='home'),
    url(r'^api/',include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^publish/', include('publish.urls')),
    url(r'^ads/(?P<param>[\w|\W]+)/$', views.adv_detail_by_loc_id, name='adv_detail_by_loc_id'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
