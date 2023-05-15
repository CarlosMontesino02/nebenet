from nebenet_app.models import Brand
from django.core.management.base import BaseCommand
import os
from pathlib import Path
from django.core.files import File
class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        brands = [
        'NVIDIA',
        'AMD',
        'RAZER',
        'HP',
        'DELL',
        'Kingston',
        'Intel',
        'D-Link',
        ]
        links = [
        'https://www.nvidia.com/en-us/',
        'https://www.amd.com/en.html',
        'https://www.razer.com/',
        'https://www.hp.com/it-it/shop/?gclsrc=ds&gclsrc=ds',
        'https://www.dell.com/it-it',
        'https://www.kingston.com/es',
        'https://www.intel.com/content/www/us/en/homepage.html',
        'https://eu.dlink.com/it/it',
        ]
        #Cambiar en producción
        images = [
        '/home/carlosmofe/projects/nebenet/logos/nvidia.png',
        '/home/carlosmofe/projects/nebenet/logos/AMD.avif',
        '/home/carlosmofe/projects/nebenet/logos/razer.png',
        '/home/carlosmofe/projects/nebenet/logos/hp.png',
        '/home/carlosmofe/projects/nebenet/logos/dell.png',
        '/home/carlosmofe/projects/nebenet/logos/kingston.png',
        '/home/carlosmofe/projects/nebenet/logos/intel.png',
        '/home/carlosmofe/projects/nebenet/logos/dlink.png',
        ]
        cont = 0
        for brand in brands:
                Brand.objects.create(bra_name=brand, bra_contact=links[cont])
                cont +=1
                print('Marca', brand , 'creada')
        cont1 = 0
        for brand in brands:
            p = File(open(images[cont1], 'rb'))
            brand = Brand.objects.get(bra_name=brand)
            brand.bra_img.save('test.jpg',p)
            cont1 +=1