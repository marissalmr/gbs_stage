from clients.views import check_siret
from clients.views import prediag_view
from clients.views import homepage
from clients.views import questionnaire
from clients.views import api_questions
from clients.views import save_answer
from clients.views import save_contact
from clients.views import submit_final
from clients.views import book_appointement
from clients.views import get_booked_times_for_day





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
    path('homepage/', homepage),
    path('questionnaire/', questionnaire, name="questionnaire"),
    path("api/questions/", api_questions, name="api_questions"),
    path("api/check-siret/", check_siret, name="check_siret"),
    path("save_contact/", save_contact, name="save_contact"),
    path("save_answer/", save_answer, name="save_answer"),
    path("submit_final/", submit_final, name="submit_final"),
    path("book_appointment/", book_appointement, name="book_appointment"),
    path("get_booked_times_for_day/", get_booked_times_for_day, name="get_booked_times_for_day")

]
