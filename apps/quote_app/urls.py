from django.conf.urls import url 
from . import views              
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^success$', views.success),
    url(r'^addQuote$', views.addQuote),
    url(r'^quote$', views.success),
    url(r'^users/(?P<id>\d+)$', views.showuser),
    url(r'^moveToFav/(?P<quote_id>\d+)/(?P<user_id>\d+)$', views.moveToFav),
    url(r'^moveToQuotes/(?P<quote_id>\d+)/(?P<user_id>\d+)$', views.moveToQuotes),
]