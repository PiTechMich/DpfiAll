from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Province)
# Register your models here.
admin.site.register(Region)
admin.site.register(District)
admin.site.register(Commune)
admin.site.register(Site)
admin.site.register(Marche)
admin.site.register(Avancement)

@admin.register(Personnel)
class PersonnelAdmin(admin.ModelAdmin):
    list_display = ('im', 'nom', 'prenom', 'fonction', 'service')
    search_fields = ('nom', 'prenom', 'im')

@admin.register(QuotaAnnuel)
class QuotaAnnuelAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'annee', 'quota_total', 'quota_utilise', 'jours_restants')
    list_filter = ('annee',)

@admin.register(TypeConge)
class TypeCongeAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description')

@admin.register(Conge)
class CongeAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'type_conge', 'annee', 'date_debut', 'date_fin', 'statut')
    list_filter = ('statut', 'annee', 'type_conge')
    search_fields = ('utilisateur__nom', 'utilisateur__prenom')