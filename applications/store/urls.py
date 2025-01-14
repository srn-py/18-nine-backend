from django.urls import path

from applications.store.views import HomeView

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
]