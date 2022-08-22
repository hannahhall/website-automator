from django.urls import path, include
from rest_framework.routers import DefaultRouter

from automator_api import views

router = DefaultRouter(trailing_slash=False)
router.register(r'users', views.UsersView, 'user')

urlpatterns = [
   path('', include(router.urls))
]
