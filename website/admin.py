from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
# Register your models here.
from .models import *

    


admin.site.register(Fournisseur)
admin.site.register(Pharmcie)
admin.site.register(Pharmacien)
admin.site.register(Article)
admin.site.register(Medicament)
admin.site.register(Stock)
admin.site.register(Order)
admin.site.register(Vente)
admin.site.register(OrderCommande)
admin.site.register(Commande)
admin.site.register(Orderonline)
admin.site.register(VenteOnline)
