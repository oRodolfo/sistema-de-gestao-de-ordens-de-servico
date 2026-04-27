from rest_framework import serializers
from predio.models import Predio

class PredioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Predio
        fields = '__all__'