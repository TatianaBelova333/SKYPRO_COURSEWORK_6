from rest_framework import serializers
from ads.models import Ad
from phonenumber_field.serializerfields import PhoneNumberField


class AdListSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(source='id')

    class Meta:
        model = Ad
        exclude = ['created_at', 'id']


class AdDetailSerializer(serializers.ModelSerializer):
    author_id = serializers.IntegerField(source='author.id', read_only=True)
    author_first_name = serializers.CharField(source='author.first_name')
    author_last_name = serializers.CharField(source='author.last_name')
    phone = PhoneNumberField(source='author.phone')
    pk = serializers.IntegerField(source='id')

    class Meta:
        model = Ad
        exclude = ["author", "id"]


class AdCreateSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(source='id', required=False)

    class Meta:
        model = Ad
        fields = '__all__'
