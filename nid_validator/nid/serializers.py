from rest_framework import serializers

class NationalIdValidatorSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=14)
    birth_date = serializers.DateField()
    governorate = serializers.CharField() 
    gender = serializers.CharField()
