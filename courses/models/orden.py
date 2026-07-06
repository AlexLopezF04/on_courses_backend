from django.db import models
from .curso import Course
from .usuario import User
from .cupon import Coupon


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
