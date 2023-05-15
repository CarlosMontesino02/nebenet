from nebenet_app.models import Category
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        cats = [
        'CPU',
        'GPU',
        'Scheda madre',
        'HDD',
        'SSD',
        'M.2',
        'RAM',
        'Caso',
        'Alimentazione elettrica',
        'Ventilazione',
        'Periferica',
        'Computer',
        'computer portatile',
        'none',
    ]
        for i in cats:
            Category.objects.create(name=i)