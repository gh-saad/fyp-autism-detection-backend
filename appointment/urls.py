from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConsultantViewSet, ConsultantWithSlotsView, SlotViewSet, AppointmentViewSet

router = DefaultRouter()
router.register(r'consultants', ConsultantViewSet)
router.register(r'slots', SlotViewSet)
router.register(r'appointments', AppointmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('consultants-with-slots/', ConsultantWithSlotsView.as_view(), name='consultants-with-slots'),
]