from django.urls import path,include, re_path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [

    path('test/', views.test, name='test'),
    path('import/', views.import_data, name='import_data'),
    path('importSite/', views.import_dataSite, name='importSite'),
    path('importMarche/', views.import_dataMarche, name='importMarche'),
    path('importAvancement/', views.import_dataAvancement, name='importAvancement'),
    path('avancement/', views.avancement_mass_update, name='avancement_mass_update'),
    path('export-excel/', views.export_to_excel, name='export-excel'),

    #Formulaire Pour requete 
    path('formulaire/', views.formulaire_view, name='formulaire'),
    path('', views.formulaire_view, name='home'),
    path('get_regions/', views.get_regions, name='get_regions'),
    path('get_districts/', views.get_districts, name='get_districts'),
    path('get_sites/', views.get_sites_by_district, name='get_sites'),
    #Voir Information Avancement 
    # URLs pour gérer les avancements
    path('avancement/view/<int:site_id>/', views.view_avancement, name='view_avancement'),
    path('avancement/edit/<int:site_id>/', views.edit_avancement, name='edit_avancement'),
    path('avancement/add/<int:site_id>/', views.add_avancement, name='add_avancement'),
    path('avancementUni/edit/<int:avan_id>/<int:site_id>', views.edit_avan, name='edit_avan'),
    path('avancementUni/delete/<int:avan_id>/<int:site_id>', views.delete_avan, name='delete_avan'),
    path('avancementUni/deleteok/<int:avan_id>/<int:site_id>', views.delete_avanok, name='delete_avanok'),
    # URLs pour gérer les site
    path('site/edit/<int:site_id>/', views.edit_site, name='edit_site'),
    # Urls Marche
    path('marche/view/<int:site_id>/', views.view_marche, name='view_marche'),
    path('marche/edit/<int:site_id>/', views.edit_marche, name='edit_marche'),
    path('marche/add/<int:site_id>/', views.add_marche, name='add_marche'),
    path('marcheUni/edit/<int:marche_id>/<int:site_id>', views.edit_mar, name='edit_mar'),
    path('marcheUni/delete/<int:marche_id>/<int:site_id>', views.delete_mar, name='delete_mar'),
    path('marcheUni/deleteok/<int:marche_id>/<int:site_id>', views.delete_marok, name='delete_marok'),

    #Rapport Génération
    path('rapport/', views.rapport, name='rapport'),
    #path('get_filtered_sites/', views.get_filtered_sites, name='get_filtered_sites'),
    path('generationpdf/', views.generate_multi_pdf, name='generationpdf'),
   
    #Congé Personnel
    path('demande_conge/', views.demande_conge, name='demande_conge'),
    path('liste_conge/', views.liste_conges, name='liste_conge'),
    path('modifier_statut_conge/<int:conge_id>/', views.modifier_statut_conge, name='modifier_statut_conge'),

    path('filtre/', views.liste_constructions, name='filtre'),

    path('login/', views.CustomLoginView.as_view(), name='login'),

    path('logout/', views.logout_view, name='logout'),
    path('omadd/', views.creer_om, name='omadd'),
    path('liste-om/', views.liste_om, name='liste_om'),
    path('modifier-om/<int:om_id>/', views.modifier_om, name='modifier_om'),
    path('supprimer-om/<int:om_id>/', views.supprimer_om, name='supprimer_om'),
]