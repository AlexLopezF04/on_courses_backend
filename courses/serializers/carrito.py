from rest_framework import serializers
from courses.models import Cart, CartItem, OrderItem


class CartItemSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    course_price = serializers.DecimalField(
        source='course.price', read_only=True,
        max_digits=10, decimal_places=2,
    )

    class Meta:
        model = CartItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = '__all__'

    def get_total(self, obj) -> float:
        return float(sum(item.course.price for item in obj.items.all()))


class CartItemWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['course']

    def validate_course(self, value):
        user = self.context['request'].user
        if OrderItem.objects.filter(order__user=user, course=value, order__status='paid').exists():
            raise serializers.ValidationError('Ya compraste este curso')
        return value
