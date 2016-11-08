"""pruebas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from appsoft import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^sqli/$',views.vistasqli),
    url(r'^xss/$',views.vistaxss),
    url(r'^server/$',views.vistaserver),
    url(r'xss/rexss/$',views.vistainfosqli),
    url(r'pivoting/$',views.vistapivoting),
    url(r'pivoting/info/$',views.infopivoting),
    url(r'^links/$',views.vistalinkscaidos),
    url(r'^server/info/$', views.infoserver),
    url(r'^$', views.vistaxss),
    url(r'^links/info/$',views.infolinks),

]
