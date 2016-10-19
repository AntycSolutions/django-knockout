from rest_framework import serializers

from app import models


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Person
        fields = '__all__'


class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reminder
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Task
        fields = '__all__'

    reminder = ReminderSerializer(read_only=True)
    reminder_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Reminder.objects.all(),
        source='reminder',
        write_only=True,
    )


class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Description
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Item
        fields = '__all__'

    description = DescriptionSerializer(read_only=True)
    description_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Description.objects.all(),
        source='description',
        write_only=True,
    )


class ShoppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Shopping
        fields = '__all__'

    items = ItemSerializer(
        many=True, read_only=True
    )
