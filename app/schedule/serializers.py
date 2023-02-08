from rest_framework import serializers
from core.models import Selection as SelectionModel
from django.contrib.auth import get_user_model

from user.serializers import UserSerializer


class SelectionSerializer(serializers.ModelSerializer):
    """
    Selection Serializer
    """
    usder = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SelectionModel
        fields = "__all__"  # ['id','name','user']
        read_only_fields = ["id"]

    # def get_user(self, obj):
    #     # print('ASDASDSA')
    #     # print(obj.user)

    #     print('ASDASDSA2')
    #     print(obj)

    #     user = UserSerializer(obj.user, many=False)
    #     return user.data["username"]

    # def create(self, validated_data, user):
        # payload = {
        #     "name": user,
        #     "user": get_user_model().objects.create(first_name="first_name",
        #                                             last_name="last_name",
        #                                             email="usasder@example.com",
        #                                             username="sdsdds",
        #                                             password="password"),
        # }
        # return SelectionModel.objects.create(**payload)

    def create(self, validated_data):
        print(validated_data)
        selection = SelectionModel(
            apartment=validated_data['selection'],
            user=self.context['request'].user
        )
        print(self.context['request'].user)
        # favoriteApartment.save()
        return selection
