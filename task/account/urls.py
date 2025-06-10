from django.urls import path
from .views import FitnessClassListView, BookingCreateView, BookingListView

urlpatterns = [
    path('classes/', FitnessClassListView.as_view(), name='fitnessclass-list'),
    path('book/', BookingCreateView.as_view(), name='booking-create'),
    path('bookings/', BookingListView.as_view(), name='booking-list'),
]
