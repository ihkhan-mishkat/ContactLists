from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework.authtoken import views

from apps.contacts.urls import router

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', ensure_csrf_cookie(TemplateView.as_view(template_name='index.html'))),
    # API
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^api-token-auth/', views.obtain_auth_token)
]
