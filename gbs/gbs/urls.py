from clients.views import prediag_view
from clients.views import check_siret
from clients.views import prediagnostique_page
from clients.views import homepage

"""
URL configuration for gbs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('prediagnostic/', prediagnostique_page, name='prediagnostic'),
    path('prediagnostic/check-siret/', check_siret, name='check_siret'),
    path('homepage/', homepage, name='homepage',)
    
]
