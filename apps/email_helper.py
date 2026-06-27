from django.conf import settings
from django.core.mail import send_mail


def send_welcome_email(user):
    """Envía correo de bienvenida al registrarse."""
    subject = 'Bienvenido a OnCourses'
    message = (
        f'Hola {user.username},\n\n'
        f'Gracias por registrarte en OnCourses.\n'
        f'Ya puedes explorar los cursos disponibles y comenzar a aprender.\n\n'
        f'¡Éxitos en tu aprendizaje!\n'
        f'El equipo de OnCourses'
    )
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )


def send_enrollment_email(user, course):
    """Notifica al estudiante que se inscribió en un curso."""
    subject = f'Inscripción confirmada: {course.title}'
    message = (
        f'Hola {user.username},\n\n'
        f'Te has inscrito exitosamente en el curso "{course.title}".\n'
        f'Ya puedes acceder a los módulos y lecciones desde tu panel.\n\n'
        f'¡A seguir aprendiendo!\n'
        f'El equipo de OnCourses'
    )
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )


def send_certificate_email(user, course):
    """Notifica al estudiante que obtuvo un certificado."""
    subject = f'¡Felicidades! Has obtenido un certificado de {course.title}'
    message = (
        f'Hola {user.username},\n\n'
        f'Has completado exitosamente el curso "{course.title}".\n'
        f'Tu certificado ya está disponible en tu perfil.\n\n'
        f'¡Sigue así!\n'
        f'El equipo de OnCourses'
    )
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
