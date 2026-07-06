from django.db import models
from .usuario import User


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
    messages = models.JSONField(
        default=list,
        verbose_name='Mensajes del ticket',
        help_text='Lista: [{"sender_id": 1, "sender_name": "...", "message": "...", "sent_at": "ISO"}]'
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
