import logging
from django.utils.timezone import now
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from .models import FitnessClass, Booking
from .serializers import FitnessClassSerializer, BookingSerializer

logger = logging.getLogger(__name__)

class FitnessClassListView(generics.ListAPIView):
    serializer_class = FitnessClassSerializer

    def get_queryset(self):
        return FitnessClass.objects.filter(date_time__gte=now()).order_by('date_time')


class BookingCreateView(generics.CreateAPIView):
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()

    def perform_create(self, serializer):
        fitness_class = serializer.validated_data['fitness_class']
        if fitness_class.available_slots <= 0:
            logger.warning(f"Booking attempt on full class {fitness_class.id}")
            raise ValidationError("No slots available")

        fitness_class.available_slots -= 1
        fitness_class.save()
        serializer.save()
        logger.info(f"Booking created for {serializer.validated_data['client_email']} in class {fitness_class.id}")


class BookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()


    def get_queryset(self):
        email = self.request.query_params.get('email')
        if email:
            return Booking.objects.filter(client_email=email)
        else:
            return Booking.objects.all




import logging
from rest_framework.exceptions import ValidationError
from django.utils.timezone import now
from rest_framework import generics
from .models import FitnessClass, Booking
from .serializers import FitnessClassSerializer, BookingSerializer

logger = logging.getLogger('fitness')

class FitnessClassListView(generics.ListAPIView):
    serializer_class = FitnessClassSerializer

    def get_queryset(self):
        logger.info("Fetching all upcoming fitness classes.")
        return FitnessClass.objects.filter(date_time__gte=now()).order_by('date_time')


class BookingCreateView(generics.CreateAPIView):
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()

    def perform_create(self, serializer):
        fitness_class = serializer.validated_data['fitness_class']
        if fitness_class.available_slots <= 0:
            logger.warning(f"Booking attempt on full class {fitness_class.id}")
            raise ValidationError("No slots available")

        fitness_class.available_slots -= 1
        fitness_class.save()
        serializer.save()
        logger.info(f"Booking created for {serializer.validated_data['client_email']} in class {fitness_class.id}")


class BookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        email = self.request.query_params.get('email')
        if email:
            logger.info(f"Fetching bookings for client email: {email}")
            return Booking.objects.filter(client_email=email)
        else:
            logger.info("Fetching all bookings (no email filter).")
            return Booking.objects.all()


from rest_framework.exceptions import ValidationError
from rest_framework import generics
from .models import Booking
from .serializers import BookingSerializer

class BookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        email = self.request.query_params.get('email')
        if not email:
            raise ValidationError({'error': 'Email query parameter is required'})
        return Booking.objects.filter(client_email=email)
