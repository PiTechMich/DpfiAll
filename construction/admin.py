from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Province)
# Register your models here.
admin.site.register(Region)
#admin.site.register(District)
#admin.site.register(Commune)
#admin.site.register(Site)
admin.site.register(Marche)
admin.site.register(Avancement)

@admin.register(Commune)
class CommuneAdmin(admin.ModelAdmin):
    list_display = ('district__region__name','district__name', 'name')
    search_fields = ('district__region__name','district__name', 'name')
    list_filter = ('district__region__name', 'district__name')

@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('commune__district__region__name','commune__district__name','commune__name', 'objet','nomEtab','TypeEtab')
    search_fields = ('commune__district__region__name','commune__district__name', 'TypeEtab')
    list_filter = ('commune__district__region__name','commune__district__name', 'TypeEtab')

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('region__name', 'name')
    search_fields = ('region__name', 'name')
    list_filter = ('region__name',)


@admin.register(Personnel)
class PersonnelAdmin(admin.ModelAdmin):
    list_display = ('im', 'nom', 'prenom', 'fonction', 'service')
    search_fields = ('nom', 'prenom', 'im')

@admin.register(CorpsGrade)
class CorpsGradeAdmin(admin.ModelAdmin):
    list_display = ('indice', 'corps', 'grade')
    list_filter = ('indice',)
    

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

@admin.register(Carriere)
class CarriereAdmin(admin.ModelAdmin):
    list_display = ('personnel', 'indice', 'date_debut','create_on')
    list_filter = ('personnel__im', 'indice__indice', 'indice__corps')
    search_fields = ('personnel__im', 'indice__indice')

@admin.register(OM)
class OMAdmin(admin.ModelAdmin):
    list_display = ('personnel', 'lieu', 'dureedep','motif','datedep')
    list_filter = ('personnel__im', 'lieu', 'dureedep')
    search_fields = ('personnel__im', 'lieu')