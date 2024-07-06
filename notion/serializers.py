from rest_framework import serializers

class CreateDjangoUserSerializer(serializers.Serializer):
    user =serializers.CharField(max_length= 50 )
    password = serializers.CharField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    group = serializers.CharField()
    phone = serializers.CharField()
    
    
class GetDjangoUserSerializer(serializers.Serializer):
    user = serializers.CharField(max_length= 50 )


class CreateDjangoGroupSerializer(serializers.Serializer):
    name = serializers.CharField()
    group_key = serializers.CharField()

class GetDjangoGroupSerializer(serializers.Serializer):
    group = serializers.CharField(max_length= 50 )
    group_key = serializers.CharField()

