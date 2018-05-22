from .models import Category


def category_tree(request):
    return {'category_tree': Category.objects.all()}
