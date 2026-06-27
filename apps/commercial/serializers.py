from rest_framework import serializers

from apps.commercial.models import (
    Cart,
    CartItem,
    Coupon,
    Order,
    OrderItem,
    SupportMessage,
    SupportTicket,
)


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


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    coupon_code = serializers.CharField(source='coupon.code', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class OrderWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['coupon']


class SupportMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.get_full_name', read_only=True)

    class Meta:
        model = SupportMessage
        fields = '__all__'


class SupportTicketSerializer(serializers.ModelSerializer):
    messages = SupportMessageSerializer(many=True, read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = SupportTicket
        fields = '__all__'


class SupportTicketWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportTicket
        fields = ['subject', 'description']
