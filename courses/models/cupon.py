from django.db import models


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
