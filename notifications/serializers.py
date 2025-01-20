from rest_framework import serializers

class NotificationSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    body = serializers.CharField(max_length=1000)
    token = serializers.CharField(max_length=255, required=False, allow_null=True)
    topic = serializers.CharField(max_length=255, required=False, allow_null=True)

    def validate(self, data):
        """
        Check that either token or topic is provided
        """
        if not data.get('token') and not data.get('topic'):
            raise serializers.ValidationError("Either token or topic must be provided")
        return data
