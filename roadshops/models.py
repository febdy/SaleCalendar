from django.db import models

# Create your models here.


class Roadshops(models.Model):
    ETUDE = 'ETUDE_HOUSE'
    THE_FACE_SHOP = 'THE_FACE_SHOP'
    SKIN_FOOD = 'SKIN_FOOD'
    MISSHA = 'MISSHA'
    ARITAUM = 'ARITAUM'
    INNISFREE = 'INNISFREE'
    THE_SAEM = 'THE_SAEM'
    ITS_SKIN = 'ITS_SKIN'
    NATURE_REPUBLIC = 'NATURE_REPUBLIC'
    TONYMOLY = 'TONYMOLY'

    ROADSHOP_CHOICE = (
        (ETUDE, 'ETUDE_HOUSE'),
        (THE_FACE_SHOP, 'THE_FACE_SHOP'),
        (SKIN_FOOD, 'SKIN_FOOD'),
        (MISSHA, 'MISSHA'),
        (ARITAUM, 'ARITAUM'),
        (INNISFREE, 'INNISFREE'),
        (THE_SAEM, 'THE_SAEM'),
        (ITS_SKIN, 'ITS_SKIN'),
        (NATURE_REPUBLIC, 'NATURE_REPUBLIC'),
        (TONYMOLY, 'TONYMOLY'),
    )

    event_name = models.CharField(max_length=200)
    roadshop_name = models.CharField(max_length=20, choices=ROADSHOP_CHOICE)

    describe = models.CharField(max_length=300, null=True, blank="")
    image_url = models.CharField(max_length=300, null=True, blank="")
    link_url = models.CharField(max_length=300, null=True, blank="")

    start_date = models.DateTimeField(null=True, blank="")
    end_date = models.DateTimeField(null=True, blank="")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.CharField(max_length=20, default='N')
