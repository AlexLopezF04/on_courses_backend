from django.db import models
from apps.users.models import User
from apps.courses.models import Course


class Cart(models.Model):
    """Carrito de compras. Un carrito por usuario (relación 1:1)."""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Usuario'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')

    class Meta:
        db_table = 'carritos'
        verbose_name = 'Carrito'
        verbose_name_plural = 'Carritos'

    def __str__(self):
        return f'Carrito de {self.user.username}'


class CartItem(models.Model):
    """Curso agregado al carrito."""
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Carrito'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name='Curso'
    )
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de agregado')

    class Meta:
        db_table = 'carritos_items'
        verbose_name = 'Ítem del carrito'
        verbose_name_plural = 'Ítems del carrito'
        unique_together = ['cart', 'course']

    def __str__(self):
        return f'{self.course.title} en carrito de {self.cart.user.username}'


class Coupon(models.Model):
    """Código de descuento para aplicar en órdenes."""
    code = models.CharField(max_length=50, unique=True, verbose_name='Código')
    description = models.TextField(blank=True, verbose_name='Descripción')
    discount_type = models.CharField(
        max_length=20,
        choices=[('percentage', 'Porcentaje'), ('fixed', 'Monto fijo')],
        default='percentage',
        verbose_name='Tipo de descuento'
    )
    discount_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Valor del descuento'
    )
    max_uses = models.PositiveIntegerField(default=100, verbose_name='Usos máximos')
    current_uses = models.PositiveIntegerField(default=0, verbose_name='Usos actuales')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de expiración')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')

    class Meta:
        db_table = 'cupones'
        verbose_name = 'Cupón'
        verbose_name_plural = 'Cupones'

    def __str__(self):
        return f'{self.code} ({self.get_discount_type_display()}: {self.discount_value})'


class Order(models.Model):
    """Orden de compra realizada por un usuario."""
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pendiente'
        PAID = 'paid', 'Pagada'
        CANCELLED = 'cancelled', 'Cancelada'
        REFUNDED = 'refunded', 'Reembolsada'

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Usuario'
    )
    coupon = models.ForeignKey(
        Coupon,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
        verbose_name='Cupón aplicado'
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Total'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name='Estado'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de pago')

    class Meta:
        db_table = 'ordenes'
        verbose_name = 'Orden'
        verbose_name_plural = 'Órdenes'
        ordering = ['-created_at']

    def __str__(self):
        return f'Orden {self.id} - {self.user.username} - {self.get_status_display()}'


class OrderItem(models.Model):
    """Curso comprado dentro de una orden."""
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Orden'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name='Curso'
    )
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Precio unitario'
    )

    class Meta:
        db_table = 'ordenes_items'
        verbose_name = 'Ítem de orden'
        verbose_name_plural = 'Ítems de orden'
        unique_together = ['order', 'course']

    def __str__(self):
        return f'{self.course.title} - ${self.unit_price}'


class SupportTicket(models.Model):
    """Ticket de soporte técnico creado por un usuario."""
    class Status(models.TextChoices):
        OPEN = 'open', 'Abierto'
        IN_PROGRESS = 'in_progress', 'En progreso'
        RESOLVED = 'resolved', 'Resuelto'
        CLOSED = 'closed', 'Cerrado'

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='support_tickets',
        verbose_name='Usuario'
    )
    subject = models.CharField(max_length=255, verbose_name='Asunto')
    description = models.TextField(verbose_name='Descripción')
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN,
        verbose_name='Estado'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última actualización')

    class Meta:
        db_table = 'tickets_soporte'
        verbose_name = 'Ticket de soporte'
        verbose_name_plural = 'Tickets de soporte'
        ordering = ['-created_at']

    def __str__(self):
        return f'[{self.get_status_display()}] {self.subject}'


class SupportMessage(models.Model):
    """Mensaje dentro de un ticket de soporte."""
    ticket = models.ForeignKey(
        SupportTicket,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Ticket'
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Remitente'
    )
    message = models.TextField(verbose_name='Mensaje')
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de envío')

    class Meta:
        db_table = 'mensajes_soporte'
        verbose_name = 'Mensaje de soporte'
        verbose_name_plural = 'Mensajes de soporte'
        ordering = ['sent_at']

    def __str__(self):
        return f'{self.sender.username} - {self.ticket.subject[:30]}'
