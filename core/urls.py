"""
URL configuration for core project.

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
from django.urls import path, include
from backoffice import views # Import your views

urlpatterns = [
    path('aparatai/', views.aparatai_view, name='aparatai'),
    path('admin/run-scrape/', views.run_scrape, name='run_scrape'),
    path('admin/run-bot/', views.trigger_bot_script, name='run_bot_trigger'),
    path('admin/stop-bot/', views.stop_bot_script, name='stop_bot_script'),
    path('', views.dashboard, name='home'), # Now the front door is the NICE dashboard
    path('admin/', admin.site.urls),
]

