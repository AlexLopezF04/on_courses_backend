from django.db import models

from .usuario import User


class Achievement(models.Model):
    """Definición de un logro que los estudiantes pueden desbloquear."""

    name = models.CharField(max_length=200, unique=True, verbose_name="Nombre")
    description = models.TextField(blank=True, verbose_name="Descripción")
    icon = models.ImageField(upload_to="achievements/", blank=True, null=True, verbose_name="Ícono")
    criteria = models.CharField(
        max_length=255, blank=True, verbose_name="Criterio de desbloqueo (ej: completar 5 cursos)"
    )

    class Meta:
        db_table = "logros"
        verbose_name = "Logro"
        verbose_name_plural = "Logros"

    def __str__(self):
        return self.name


class UserAchievement(models.Model):
    """Relación muchos a muchos: logros obtenidos por cada usuario."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="achievements", verbose_name="Usuario"
    )
    achievement = models.ForeignKey(
        Achievement, on_delete=models.CASCADE, related_name="users", verbose_name="Logro"
    )
    earned_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de obtención")

    class Meta:
        db_table = "logros_usuarios"
        verbose_name = "Logro de usuario"
        verbose_name_plural = "Logros de usuarios"
        unique_together = ["user", "achievement"]

    def __str__(self):
        return f"{self.user.username} → {self.achievement.name}"
