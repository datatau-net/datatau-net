"""datatau URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('app.urls')),
    path('robots.txt', lambda x: HttpResponse("Sitemap: https://datatau.net/sitemap.xml \nUser-agent:* \nDisallow: ",
                                              content_type="text/plain"),
         name="robots_file")
]
