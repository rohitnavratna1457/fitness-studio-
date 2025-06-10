import pytz
from rest_framework import serializers
from .models import FitnessClass, Booking

class FitnessClassSerializer(serializers.ModelSerializer):

    class Meta:
        model = FitnessClass
        fields = '__all__'

    def validate_date_time(self, value):
        # Assume input datetime in IST, convert to UTC for DB storage
        ist = pytz.timezone('Asia/Kolkata')
        if value.tzinfo is None:
            value = ist.localize(value)
        return value.astimezone(pytz.UTC)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        tz_name = request.query_params.get('timezone', 'UTC') if request else 'UTC'
        try:
            user_tz = pytz.timezone(tz_name)
        except Exception:
            user_tz = pytz.UTC

        utc_dt = instance.date_time
        local_dt = utc_dt.astimezone(user_tz)
        data['date_time'] = local_dt.isoformat()
        return data

class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = '__all__'

    def validate(self, data):
        fitness_class = data['fitness_class']
        if fitness_class.available_slots <= 0:
            raise serializers.ValidationError("No slots available for this class.")
        return data
