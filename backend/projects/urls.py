from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, MilestoneViewSet

router = DefaultRouter()

router.register('projects', ProjectViewSet, basename='project')
router.register('milestones', MilestoneViewSet, basename='milestone')

urlpatterns = router.urls