from django.db import models
from .curso import Course
from .usuario import User


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
