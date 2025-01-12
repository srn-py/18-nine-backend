from django.urls import path

from applications.store.views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]