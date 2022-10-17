from django.urls import path, include
from rest_framework.routers import DefaultRouter

from automator_api import views

router = DefaultRouter(trailing_slash=False)
router.register(r'users', views.UsersView, 'user')
router.register(r'cohorts', views.CohortViewSet)
router.register(r'programs', views.ProgramViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register', views.register_user)
]
