from helpers import create_user, create_professor, create_admin, auth_client, unauth_client
from courses.models import Category, Course


def create_category(name='Backend', slug='backend'):
    """Crea una categoría de prueba."""
    return Category.objects.create(name=name, slug=slug)


def create_course(category=None, professor=None, title='Curso Test', price=50, slug='curso-test'):
    """Crea un curso de prueba."""
    if category is None:
        category = create_category()
    if professor is None:
        professor = create_professor()
    return Course.objects.create(
        category=category,
        professor=professor,
        title=title,
        price=price,
        slug=slug
    )
