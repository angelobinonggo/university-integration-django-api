from rest_framework.routers import DefaultRouter
from .views import LibraryRecordViewSet

router = DefaultRouter()
router.register(r'library', LibraryRecordViewSet, basename='library')

urlpatterns = router.urls
