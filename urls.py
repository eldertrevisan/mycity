from django.conf.urls import url, handler404
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from mysite.mycity import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^confirm/(?P<validation_key>\w+)/$', views.register_confirm),
    #url(r'^confirm_expired/$', views.confirm_expired),
    url(r'^forgot_password/$', views.forgot_password, name='forgot_password'),
    url(r'^change_password/(?P<validation_key>\w+)/$', views.change_password, name='change_password'),
    url(r'^404/$', views.handler404),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)