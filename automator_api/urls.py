from django.urls import path, include
from rest_framework.routers import DefaultRouter

from automator_api import views

router = DefaultRouter(trailing_slash=False)
router.register(r'users', views.UsersView, 'user')
router.register(r'cohorts', views.CohortViewSet)
router.register(r'programs', views.ProgramViewSet)
router.register(r'projects', views.ProjectViewSet, 'project')
router.register(r'techs', views.TechViewSet, 'tech')

urlpatterns = [
    path('', include(router.urls)),
    path('register', views.register_user),
    path('github-auth', views.authenticate_github),
]
