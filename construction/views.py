import os
from django.shortcuts import render, redirect, get_object_or_404
import pandas as pd
from django.http import HttpResponse, JsonResponse
from .forms import *
from .models import *
from django.utils.timezone import make_aware
from datetime import datetime
from django.contrib import messages
from django.forms import modelformset_factory
import openpyxl
from reportlab.lib.pagesizes import A4, letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from django.db.models import Max, Avg, Count,Subquery, OuterRef
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.conf import settings
from reportlab.lib.units import cm,mm
from reportlab.lib.utils import ImageReader
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth import logout

# Create your views here.
def test(request):
    return render(request, 'index.html')
# Import Data Excel Commune
def import_data(request):
    if request.method == "POST":
        excel_file = request.FILES["excel_file"]

        try:
            # Lire le fichier Excel
            df = pd.read_excel(excel_file)

            # Vérifier la présence des colonnes attendues
            required_columns = ["Province", "Region", "District", "Commune"]
            if not all(col in df.columns for col in required_columns):
                messages.error(request, "Les colonnes requises sont manquantes.")
                return redirect("import_data")

            # Parcourir les lignes du fichier
            for index, row in df.iterrows():
                # Insérer ou récupérer la Province
                province, created = Province.objects.get_or_create(name=row["Province"])

                # Insérer ou récupérer la Region
                region, created = Region.objects.get_or_create(
                    name=row["Region"], province=province
                )

                # Insérer ou récupérer le District
                district, created = District.objects.get_or_create(
                    name=row["District"], region=region
                )

                # Insérer ou récupérer la Commune
                Commune.objects.get_or_create(
                    name=row["Commune"], district=district
                )

            messages.success(request, "Données importées avec succès !")
        except Exception as e:
            messages.error(request, f"Une erreur est survenue lors de l'importation : {e}")

        return redirect("import_data")
    else:
            form = ExcelUploadForm()
    return render(request, "pages/import_data.html",{'form': form})
#Import Data Site 1 via Excel
def import_dataSite(request):
    if request.method == "POST":
        excel_file = request.FILES["excel_file"]

        try:
            # Lire le fichier Excel
            df = pd.read_excel(excel_file)

            # Vérifier la présence des colonnes attendues
            required_columns = ["Province", "Region", "District", "Commune","Fokontany","Objet","Type","NomEtablissement"]
            if not all(col in df.columns for col in required_columns):
                messages.error(request, "Les colonnes requises sont manquantes.")
                return redirect("import_dataSite")

            # Parcourir les lignes du fichier
            for index, row in df.iterrows():
                # Insérer ou récupérer la Province
                province, created = Province.objects.get_or_create(name=row["Province"])

                # Insérer ou récupérer la Region
                region, created = Region.objects.get_or_create(
                    name=row["Region"], province=province
                )

                # Insérer ou récupérer le District
                district, created = District.objects.get_or_create(
                    name=row["District"], region=region
                )

                # Insérer ou récupérer la Commune
                commune, created = Commune.objects.get_or_create(
                    name=row["Commune"], district=district
                )

                Site.objects.get_or_create(
                    objet=row["Objet"],
                    nomEtab =row["NomEtablissement"],
                    TypeEtab=row["Type"],
                    fokontany=row["Fokontany"],
                    commune=commune
                )

            messages.success(request, "Données importées avec succès !")
        except Exception as e:
            messages.error(request, f"Une erreur est survenue lors de l'importation : {e}")

        return redirect("importSite")
    else:
            form = ExcelUploadForm()
    return render(request, "pages/import_dataSite.html",{'form': form})

#Import Data Marche 1 via Excel
def import_dataMarche(request):
    if request.method == "POST":
        excel_file = request.FILES["excel_file"]

        try:
            # Lire le fichier Excel
            df = pd.read_excel(excel_file)

            # Vérifier la présence des colonnes attendues
            required_columns = [
                 "Province", 
                 "Region", 
                 "District", 
                 "Commune",
                 "Fokontany",
                 "Objet",
                 "Type",
                 "NomEtablissement",
                 "numMarche",
                 "NbSalles",
                 "Titulaire",
                 "NumeroEntreprise",
                 "Montant",
                 "DelaiExec",
                 "Batiment",
                 "Travaux",
                 "Financements",
                 "OS"
                 ]
            if not all(col in df.columns for col in required_columns):
                messages.error(request, "Les colonnes requises sont manquantes.")
                return redirect("import_dataSite")

            # Parcourir les lignes du fichier
            for index, row in df.iterrows():
                # Insérer ou récupérer la Province
                province, created = Province.objects.get_or_create(name=row["Province"])

                # Insérer ou récupérer la Region
                region, created = Region.objects.get_or_create(
                    name=row["Region"], province=province
                )

                # Insérer ou récupérer le District
                district, created = District.objects.get_or_create(
                    name=row["District"], region=region
                )

                # Insérer ou récupérer la Commune
                commune, created = Commune.objects.get_or_create(
                    name=row["Commune"], district=district
                )

                site, created =Site.objects.get_or_create(
                    objet=row["Objet"],
                    nomEtab =row["NomEtablissement"],
                    TypeEtab=row["Type"],
                    fokontany=row["Fokontany"],
                    commune=commune
                )

                Marche.objects.get_or_create(
                    numMarche=row["numMarche"],
                    NbSalle=row["NbSalles"],
                    Titulaire=row["Titulaire"],
                    NumTitulaire=row["NumeroEntreprise"],
                    delaiEx=row["DelaiExec"],
                    batiment=row["Batiment"],
                    travaux=row["Travaux"],
                    financement=row["Financements"],
                    os=row["OS"],
                    site=site
                )

            messages.success(request, "Données importées avec succès !")
        except Exception as e:
            messages.error(request, f"Une erreur est survenue lors de l'importation : {e}")

        return redirect("importMarche")
    else:
            form = ExcelUploadForm()
    return render(request, "pages/import_dataMarche.html",{'form': form})

#Import Data Avancement 1 via Excel
def import_dataAvancement(request):
    if request.method == "POST":
        excel_file = request.FILES["excel_file"]

        try:
            # Lire le fichier Excel
            df = pd.read_excel(excel_file)

            # Vérifier la présence des colonnes attendues
            required_columns = [
                "id", 
                "NomEtablissement",
                "Etat",
                "Avancement",
                "Observation",
                "AnneeAchevement",
                "Inaugurable",
                "Niveaux",
                "TravauxRestant"
                 ]
            if not all(col in df.columns for col in required_columns):
                messages.error(request, "Les colonnes requises sont manquantes.")
                print("Ato zaho ts mety")
                return redirect("importAvancement")

            # Parcourir les lignes du fichier
            for index, row in df.iterrows():
                print(type(row["id"]))
                site = Site.objects.get(id=row["id"])
                Avancement.objects.get_or_create(
                    etat=row["Etat"],
                    avancement=row["Avancement"],
                    observation=row["Observation"],
                    annee_achevement=row["AnneeAchevement"],
                    inaugurable=row["Inaugurable"],
                    Niveau=row["Niveaux"],
                    TravauxRestant=row["TravauxRestant"],
                    site=site
                )

            messages.success(request, "Données importées avec succès !")
        except Exception as e:
            messages.error(request, f"Une erreur est survenue lors de l'importation : {e}")

        return redirect("importAvancement")
    else:
            form = ExcelUploadForm()
    return render(request, "pages/import_dataAvancement.html",{'form': form})


def avancement_mass_update(request):
    # Récupérer tous les sites disponibles
    sites = Site.objects.all()
    
    # Générer un FormSet basé sur AvancementForm
    AvancementFormSet = modelformset_factory(
        Avancement,
        form=AvancementForm,
        extra=len(sites),  # Générer autant de formulaires que de sites
        #extra=1,
    )

    if request.method == 'POST':
        formset = AvancementFormSet(request.POST, request.FILES)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for i, instance in enumerate(instances):
                # Associer chaque avancement à un site spécifique
                instance.site = sites[i]
                instance.save()
            return redirect('success_page')  # Redirection après l'enregistrement
    else:
        # Pré-remplir les formulaires avec les sites
        initial_data = [{'site':site.objet} for site in sites]
        #print(f"Initial Data: {type(initial_data)}")
        formset = AvancementFormSet(queryset=Avancement.objects.none(), initial=initial_data)
        #formset = AvancementFormSet(queryset=Avancement.objects.none(), initial=[{"title": "Django is now open source","pub_date":'Now'}])
          
    return render(request, 'pages/avancement_mass_update.html', {'formset': formset, 'sites': sites})

def export_to_excel(request):
    # Créez un fichier Excel en mémoire
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "dataEsm"

    # Ajoutez les en-têtes des colonnes
    sheet.append([
        "ID", 
        "Province", 
        "Region", 
        "District", 
        "Commune",
        "Fokontany",
        "Objet",
        "Nom Etablissement",
        "TypeEtab",
        "NumMarche",
        "NbreSalle",
        "Titulaire",
        "Num Titulaire",
        "Delai Execution",
        "Batiment",
        "Travaux",
        "Financement",
        "OS",
        "Avancement",
        "Etats",
        "Observation",
        "Niveaux",
        "Travaux Restants"
        ])

    # Sous-requête pour obtenir le dernier "Marche" pour chaque "Site"
    latest_marche = Marche.objects.filter(
        site=OuterRef('pk')
    ).order_by('-create_on').values('id')[:1]

    # Sous-requête pour obtenir le dernier "Avancement" pour chaque "Site"
    latest_avancement = Avancement.objects.filter(
        site=OuterRef('pk')
    ).order_by('-create_on').values('id')[:1]

    # Récupérer les sites avec le dernier "Marche" et le dernier "Avancement"
    sites_with_latest_data = Site.objects.annotate(
        latest_marche_id=Subquery(latest_marche),
        latest_avancement_id=Subquery(latest_avancement)
    ).select_related('commune__district__region__province')

    # Optionnel : Récupérer les données complètes des derniers "Marche" et "Avancement"
    results = []
    for site in sites_with_latest_data:
        latest_marche = Marche.objects.filter(pk=site.latest_marche_id).first()
        latest_avancement = Avancement.objects.filter(pk=site.latest_avancement_id).first()

        results.append({
            'site': site,
            'latest_marche': latest_marche,
            'latest_avancement': latest_avancement
        })
    
    for item in results:
        site = item['site']
        latest_marche = item['latest_marche']
        latest_avancement = item['latest_avancement']
        
        sheet.append([
            site.id,
            site.commune.district.region.province.name,
            site.commune.district.region.name, 
            site.commune.district.name,
            site.commune.name,
            site.fokontany,
            site.objet,
            site.nomEtab,
            site.TypeEtab,
            latest_marche.numMarche,
            latest_marche.NbSalle,
            latest_marche.Titulaire,
            latest_marche.NumTitulaire,
            latest_marche.delaiEx,
            latest_marche.batiment,
            latest_marche.travaux,
            latest_marche.financement,
            latest_marche.os,
            latest_avancement.avancement,
            latest_avancement.etat,
            latest_avancement.observation,
            latest_avancement.Niveau,
            latest_avancement.TravauxRestant
            ])
    

    # Récupérez les données depuis la base
    #marches = Marche.objects.all()

    # Remplissez les lignes avec les données
    # for marche in marches:
    #     sheet.append([
    #         marche.site.id,
    #         marche.site.commune.district.region.province.name,
    #         marche.site.commune.district.region.name, 
    #         marche.site.commune.district.name,
    #         marche.site.commune.name,
    #         marche.site.fokontany,
    #         marche.site.objet,
    #         marche.site.nomEtab,
    #         marche.site.TypeEtab,
    #         marche.numMarche,
    #         marche.NbSalle,
    #         marche.Titulaire,
    #         marche.NumTitulaire,
    #         marche.delaiEx,
    #         marche.batiment,
    #         marche.travaux,
    #         marche.financement,
    #         marche.os
    #         ])

    # Préparez la réponse HTTP
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename="dataesm.xlsx"'

    # Enregistrez le fichier dans la réponse
    workbook.save(response)
    return response

def get_regions(request):
    province_id = request.GET.get('province_id')
    regions = Region.objects.filter(province_id=province_id).values('id', 'name')
    return JsonResponse(list(regions), safe=False)


def get_districts(request):
    region_id = request.GET.get('region_id')
    districts = District.objects.filter(region_id=region_id).values('id', 'name')
    return JsonResponse(list(districts), safe=False)

def formulaire_view(request):
    provinces = Province.objects.all()
    # Sous-requête pour obtenir le dernier "Marche" pour chaque "Site"
    latest_marche = Marche.objects.filter(
        site=OuterRef('pk')
    ).order_by('-create_on').values('id')[:1]

    # Sous-requête pour obtenir le dernier "Avancement" pour chaque "Site"
    latest_avancement = Avancement.objects.filter(
        site=OuterRef('pk')
    ).order_by('-create_on').values('id')[:1]

    # Récupérer les sites avec le dernier "Marche" et le dernier "Avancement"
    sites_with_latest_data = Site.objects.annotate(
        latest_marche_id=Subquery(latest_marche),
        latest_avancement_id=Subquery(latest_avancement)
    ).select_related('commune__district__region__province')

    # Optionnel : Récupérer les données complètes des derniers "Marche" et "Avancement"
    results = []
    for site in sites_with_latest_data:
        latest_marche = Marche.objects.filter(pk=site.latest_marche_id).first()
        latest_avancement = Avancement.objects.filter(pk=site.latest_avancement_id).first()

        results.append({
            'site': site,
            'latest_marche': latest_marche,
            'latest_avancement': latest_avancement
        })


    return render(request, 'pages/formulaire.html', {'provinces': provinces, 'resultats':results})

def get_sites_by_district(request):
    district_id = request.GET.get('district_id')
    sites = Site.objects.filter(commune__district_id=district_id).select_related('commune', 'commune__district')
    
    data = []
    for site in sites:
        # Récupérer le dernier avancement par date de création
        avancement = Avancement.objects.filter(site=site).order_by('-create_on').first()
        etat = avancement.etat if avancement else "N/A"
        avancement_value = f"{avancement.avancement}%" if avancement else "N/A"
        #Recupération Marche
        marche = Marche.objects.filter(site=site).order_by('-create_on').first()

        numMarche =marche.numMarche if marche else "N/A"
        NbSalle =marche.NbSalle if marche else "N/A"
        Titulaire =marche.Titulaire if marche else "N/A"
        NumTitulaire=marche.NumTitulaire if marche else "N/A"
        batiment=marche.batiment if marche else "N/A"
        travaux=marche.travaux if marche else "N/A"
        financement=marche.financement if marche else "N/A"
        os=marche.os if marche else "N/A"

        data.append({
            'id': site.id,
            'nomEtab': site.nomEtab,
            'TypeEtab': site.TypeEtab,
            'fokontany': site.fokontany or 'N/A',
            'objet': site.objet,
            'commune': site.commune.name,
            'district': site.commune.district.name,
            'region': site.commune.district.region.name,
            'province': site.commune.district.region.province.name,
            'created_on': site.create_on.strftime('%Y-%m-%d'),
            'etat': etat,  # État actuel
            'avancement': avancement_value,  # Dernier avancement
            'numMarche':numMarche,
            'Salle':NbSalle,
            'titulaire':Titulaire,
            'num_titulaire':NumTitulaire,
            'bati':batiment,
            'travaux':travaux,
            'finan':financement,
            'os':os
        })
    return JsonResponse(data, safe=False)

# Afficher les avancements
def view_avancement(request, site_id):
    site = get_object_or_404(Site, id=site_id)
    avancements = Avancement.objects.filter(site=site)
    marche = Marche.objects.filter(site=site).order_by('-create_on').first()
    return render(request, 'pages/avancement/view.html', {'site': site, 'avancements': avancements,"marche":marche})

# Modifier un avancement
def edit_avancement(request, site_id):
    avancement = Avancement.objects.filter(site_id=site_id).order_by('-create_on').first()
        
    if request.method =='POST':
        form = AvancementForm(request.POST, request.FILES, instance=avancement)
        #print(form)
        if form.is_valid():
            print("je suis ici")
            form.save()
            return redirect('view_avancement', site_id=site_id)
    else:
        
        form = AvancementForm(instance=avancement)
    return render(request, 'pages/avancement/edit.html', {'form': form})
# Modification Avancement selon Avancement
def edit_avan(request, avan_id,site_id):
    #avancement = Avancement.objects.filter(site_id=site_id).order_by('-create_on').first()
    pi = Avancement.objects.get(pk=avan_id) 
    if request.method =='POST':
        
        form = AvancementForm(request.POST, request.FILES, instance=pi)
        #print(form)
        if form.is_valid():
            print("je suis ici")
            form.save()
            return redirect('view_avancement', site_id=site_id)
    else:
        form = AvancementForm(instance=pi)
    return render(request, 'pages/avancement/edit.html', {'form': form})

def delete_avanok(request, avan_id,site_id):
    pi = Avancement.objects.get(pk=avan_id)
    pi.delete()
    return redirect('view_avancement', site_id=site_id)
  
def delete_avan(request, avan_id,site_id):
    site = get_object_or_404(Site, id=site_id)
    avancement = Avancement.objects.get(pk=avan_id)
    marche = Marche.objects.filter(site=site).order_by('-create_on').first()
    if request.method == 'POST' : 
        pi = Avancement.objects.get(pk=avan_id)
        pi.delete()
        return redirect('view_avancement', site_id=site_id)
  
    return render(request, 'pages/avancement/confirmationsupp.html', {'site': site, 'avancement': avancement,"marche":marche})
# Ajouter un nouvel avancement
def add_avancement(request, site_id):
    site = get_object_or_404(Site, id=site_id)
    if request.method == 'POST':
        form = AvancementForm(request.POST, request.FILES)
        if form.is_valid():
            avancement = form.save(commit=False)
            avancement.site = site
            avancement.save()
            return redirect('view_avancement', site_id=site_id)
    else:
        form = AvancementForm(initial={'site': Site.objects.get(id=site_id)})
    return render(request, 'pages/avancement/add.html', {'form': form, 'site': site})

# Modifier un avancement
def edit_site(request, site_id):
    if request.method == 'POST' :
        pi = Site.objects.get(pk=site_id)
        fm = SiteForm(request.POST, request.FILES,instance=pi)
        if fm.is_valid():
            fm.save()
            fm = SiteForm()
            return redirect('rapport')
    else : 
        pi = Site.objects.get(pk=site_id)
        fm =SiteForm(instance = pi)
    return render(request, 'pages/site/edit.html', {'form': fm})

# Afficher les avancements
def view_marche(request, site_id):
    site = get_object_or_404(Site, id=site_id)
    marches = Marche.objects.filter(site=site)
    avancement = Avancement.objects.filter(site=site).order_by('-create_on').first()
    return render(request, 'pages/marche/view.html', {'site': site, 'avancement': avancement,"marches":marches})

# Modifier un avancement
def edit_marche(request, site_id):
    marche = Marche.objects.filter(site_id=site_id).order_by('-create_on').first()
        
    if request.method =='POST':
        
        form = MarcheForm(request.POST, request.FILES, instance=marche)
        if form.is_valid():
            form.save()
            return redirect('view_marche', site_id=site_id)
    else:
        
        form = MarcheForm(instance=marche)
    return render(request, 'pages/marche/edit.html', {'form': form})

# Ajouter un nouvel avancement
def add_marche(request, site_id):
    site = get_object_or_404(Site, id=site_id)
    if request.method == 'POST':
        form = MarcheForm(request.POST, request.FILES)
        if form.is_valid():
            marche = form.save(commit=False)
            marche.site = site
            marche.save()
            return redirect('view_marche', site_id=site_id)
    else:
        form = MarcheForm(initial={'site': Site.objects.get(id=site_id)})
    return render(request, 'pages/marche/add.html', {'form': form, 'site': site})

# Modification Avancement selon Avancement
def edit_mar(request, marche_id,site_id):
    #avancement = Avancement.objects.filter(site_id=site_id).order_by('-create_on').first()
    pi = Marche.objects.get(pk=marche_id) 
    if request.method =='POST':
        
        form =MarcheForm(request.POST, request.FILES, instance=pi)
        #print(form)
        if form.is_valid():
            print("je suis ici")
            form.save()
            return redirect('view_marche', site_id=site_id)
    else:
        form = MarcheForm(instance=pi)
    return render(request, 'pages/marche/edit.html', {'form': form})

def delete_marok(request, marche_id,site_id):
    pi = Marche.objects.get(pk=marche_id)
    pi.delete()
    return redirect('view_marche', site_id=site_id)
  
def delete_mar(request, marche_id,site_id):
    site = get_object_or_404(Site, id=site_id)
    marche = Marche.objects.get(pk=marche_id)
    avancement = Avancement.objects.filter(site=site).order_by('-create_on').first()
    if request.method == 'POST' : 
        pi = Avancement.objects.get(pk=marche_id)
        pi.delete()
        return redirect('view_marche', site_id=site_id)
  
    return render(request, 'pages/marche/confirmationsupp.html', {'site': site, 'avancement': avancement,"marche":marche})


def rapport(request):
    provinces = Province.objects.all()
    if request.method == "POST":
        province = request.POST.get('province')
        etat = request.POST.get('etat')
        financement = request.POST.get('financement')
        #print("Kaiz eee")
        provinceName = Province.objects.get(pk=province)
        #print(province)
        ######
        # avancements = Avancement.objects.filter(
        #     site__commune__district__region__province__id=province,
        #     site__marche__financement=financement,
        #     etat=etat
        # )
        
        avancements = Avancement.objects.filter(
        site__commune__district__region__province=province
        )

        if etat:
            if etat == "N_Achevée":
                avancements = avancements.exclude(etat="Achevée")
            else:
                avancements = avancements.filter(etat=etat)

        if financement:
            avancements = avancements.filter(site__marche__financement=financement)
        
        # Trier les résultats par ordre croissant des régions
        avancements = avancements.order_by('site__commune__district__region__name')
        #Prendre elément concernant site selon recherche
          # Sous-requête pour obtenir le dernier "Marche" pour chaque "Site"
        
        # Optionnel : Récupérer les données complètes des derniers "Marche" et "Avancement"
        results = []
        for avancement in avancements :
            latest_marche = Marche.objects.filter(site__id=avancement.site.id).order_by('-create_on').first()
            latest_avancement = Avancement.objects.filter(site__id=avancement.site.id).order_by('-create_on').first()

            results.append({
                'site': avancement,
                'latest_marche': latest_marche,
                'latest_avancement': latest_avancement
            })
        request.session['filters'] = {
            'province': province,
            'etat': etat,
            'financement': financement
        }

        #generate_all_projects_report(avancements)
        #print(results)
        return render(request, 'pages/rapport.html',{'provinces': provinces, 'avancements':avancements,"provinceR":provinceName.name,"etatReq":etat,"financR":financement, "results":results})
    return render(request, 'pages/rapport.html',{'provinces': provinces})

def generate_multi_pdf(request):
    # Récupérer les filtres de la session
    filters = request.session.get('filters', {})
    province = filters.get('province')
    etat = filters.get('etat')
    financement = filters.get('financement')
    provinceName = Province.objects.get(pk=province)

    avancements = Avancement.objects.filter(
        site__commune__district__region__province=province
        )

    if etat:
        if etat == "N_Achevée":
                avancements = avancements.exclude(etat="Achevée")
        else:
                avancements = avancements.filter(etat=etat)

    if financement:
        avancements = avancements.filter(site__marche__financement=financement)
        
        # Trier les résultats par ordre croissant des régions
    avancements = avancements.order_by('site__commune__district__region__name')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Projets_{provinceName}.pdf"'
    # Canvas pour capturer les numéros de page
    doc_canvas = NumberedCanvas(response)
    # Définir la fonction pour le pied de page
    def add_page_number(canvas, doc):
            page_number = f"Page {doc.page}"
            canvas.saveState()
            canvas.setFont('TimesNewRoman', 10)
            canvas.drawCentredString(105 * mm, 15 * mm, page_number)  # Centré en bas
            canvas.restoreState()

        # Créer le document PDF
    doc = BaseDocTemplate(response, pagesize=letter)
    frame = Frame(
        doc.leftMargin,
        doc.bottomMargin,
        doc.width,
        doc.height - 20,  # Réduire légèrement pour le pied de page
        id='normal'
    )
    template = PageTemplate(id='test', frames=frame, onPage=add_page_number)
    doc.addPageTemplates([template])

    pdfmetrics.registerFont(TTFont('TimesNewRoman', 'times.ttf'))
    pdfmetrics.registerFont(TTFont('TimesNewRoman-Bold', 'timesbd.ttf'))  # Gras
    pdfmetrics.registerFont(TTFont('TimesNewRoman-Italic', 'timesi.ttf'))  # Italique
    pdfmetrics.registerFont(TTFont('TimesNewRoman-BoldItalic', 'timesbi.ttf'))  # Italique Gras

    style_title = ParagraphStyle(
            'TitleStyle',
            fontName='TimesNewRoman-Bold',
            fontSize=18,
            alignment=1,
            spaceBefore=2,
            spaceAfter=5,
            leading=22
        )

    style_section = ParagraphStyle(
            'SectionStyle',
            fontName='TimesNewRoman',
            fontSize=14,
            spaceBefore=8,
            spaceAfter=8,
            leading=18
        )

    style_body = ParagraphStyle(
        'BodyStyle',
        fontName='TimesNewRoman',
        fontSize=12,
        leading=15,
        spaceAfter=10
        )
    style_itabold = ParagraphStyle(
        'BodyStyle',
        fontName='TimesNewRoman-BoldItalic',
        fontSize=12,
        leading=15,
        spaceAfter=10
        )
    style_itaboldTR = ParagraphStyle(
        'BodyStyle',
        fontName='TimesNewRoman-BoldItalic',
        fontSize=10,
        leading=15,
        spaceAfter=5
        )
    
    style_bold = ParagraphStyle(
        'BodyStyle',
        fontName='TimesNewRoman-Bold',
        fontSize=15,
        leading=15,
        spaceAfter=10
        )

    elements = []
    
    for projet in avancements:
        
        project_elements = []
        marche = Marche.objects.filter(site=projet.site).order_by('-create_on').first()
        project_elements.append(Paragraph(projet.site.nomEtab.upper(), style_title))
        # Ajouter le titre au canvas
        doc_canvas.add_toc_entry(projet.site.nomEtab.upper(), len(elements) + 1)
        project_elements.append(Spacer(1, 0.5 * cm))
        
        project_elements.append(Paragraph("I. <u>DESCRIPTION DU PROJET </u>:", style_section))
        project_elements.append(Paragraph(f"<u>Marché </u>: {marche.numMarche}", style_itabold))
        project_elements.append(Paragraph(f"<u>Objet </u>: {projet.site.objet}", style_itabold))
        project_elements.append(Paragraph(f"<u>Titulaire des Travaux  </u>: {marche.Titulaire}", style_itabold))
        project_elements.append(Paragraph(f"<u>Ordre de Service </u>: {marche.os}", style_itabold))
        project_elements.append(Paragraph(f"<u>Délai d’exécution </u>: {marche.delaiEx}", style_itabold))
        project_elements.append(Paragraph(f"<u>Maître d'oeuvre  </u>: Ministère de l’Education Nationale", style_itabold))
        #project_elements.append(table_description)
        project_elements.append(Spacer(1, 0.2 * cm))
        project_elements.append(Paragraph("II. <u>CONSTATATION DES TRAVAUX </u>:", style_section))
        if projet.etat=="Achevée":
            project_elements.append(Paragraph(f"{projet.etat}", style_itabold))
        else : 
            if projet.TravauxRestant and projet.TravauxRestant!="nan": 
                data = [
                    [Paragraph(f"<u>Observation </u>: {projet.etat}", style_itaboldTR), Paragraph(f"<u>Avancement </u>: {projet.avancement}%", style_itaboldTR)],
                ]
                table = Table(data, colWidths=[6 * cm, 10 * cm])
                table.setStyle(TableStyle([
                    ('LINEBELOW', (0, 0), (-1, -1), 0, colors.white),  # Suppression des bordures
                    ('LINEABOVE', (0, 0), (-1, -1), 0, colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ]))
                project_elements.append(table)
                project_elements.append(Paragraph(f"<u>Travaux restants  </u>: {projet.TravauxRestant}", style_itaboldTR))
                
            else : 
                data = [
                    [Paragraph(f"<u>Observation </u>: {projet.etat}", style_itabold), Paragraph(f"<u>Avancement </u>: {projet.avancement}%", style_itabold)],
                ]
                table = Table(data, colWidths=[6 * cm, 10 * cm])
                table.setStyle(TableStyle([
                    ('LINEBELOW', (0, 0), (-1, -1), 0, colors.white),  # Suppression des bordures
                    ('LINEABOVE', (0, 0), (-1, -1), 0, colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ]))
                project_elements.append(table)

        #project_elements.append(table_constatation)

        project_elements.append(Spacer(1, 0.2 * cm))
        img_width = 7 * cm
        img_height = 4 * cm
        image_paths = [projet.photo1.path if projet.photo1 else None,
                projet.photo2.path if projet.photo2 else None,
                projet.photo3.path if projet.photo3 else None,
                projet.photo4.path if projet.photo4 else None]
        image_cells = [Image(img_path, width=img_width, height=img_height)
                for img_path in image_paths if img_path and os.path.exists(img_path)]
        if image_cells:
            image_table_data = [image_cells[i:i + 2] for i in range(0, len(image_cells), 2)]
            image_table = Table(
                    image_table_data,
                    colWidths=[img_width + 1 * cm] * 2,
                    rowHeights=[img_height + 1 * cm] * len(image_table_data)
                )
            image_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 5),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 5),
                    ('TOPPADDING', (0, 0), (-1, -1), 5),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ]))
            project_elements.append(image_table)

        elements.append(KeepTogether(project_elements))
        if projet != avancements.last():
            elements.append(PageBreak())
        
    #doc.build(elements)
    doc.build(elements, canvasmaker=NumberedCanvas)
    return response

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.toc_entries = []

    def add_toc_entry(self, title, page):
        self.toc_entries.append((title, page))

    def draw_toc(self):
        for title, page in self.toc_entries:
            self.drawString(100, 800 - (self.toc_entries.index((title, page)) * 20), f"{title} ........ {page}")

    def save(self):
        # Ajouter la table des matières avant d'enregistrer le fichier
        self.showPage()
        self.draw_toc()
        super().save()

@login_required
def demande_conge(request):
    if request.method == 'POST':
        form = CongeForm(request.POST)
        if form.is_valid():
            utilisateur = form.cleaned_data['utilisateur']
            annee = form.cleaned_data['annee']
            date_debut = form.cleaned_data['date_debut']
            date_fin = form.cleaned_data['date_fin']

            # Vérifier si le quota existe pour l'année
            try:
                print("Aiza eee")
                quota = QuotaAnnuel.objects.get(utilisateur=utilisateur, annee=annee)
            except QuotaAnnuel.DoesNotExist:
                messages.error(request, "Le quota pour cette année n'existe pas pour cet utilisateur.")
                return redirect('demande_conge')

            # Vérifier si le congé chevauche un autre congé pour le même utilisateur
            chevauchement = Conge.objects.filter(
                utilisateur=utilisateur,
                statut='approuve'
            ).filter(
                date_debut__lte=date_fin,
                date_fin__gte=date_debut
            )

            if chevauchement.exists():
                messages.error(request, "Le congé chevauche un autre congé existant.")
                return redirect('demande_conge')

            # Vérifier si la durée du congé dépasse le quota restant
            duree_conge = (date_fin - date_debut).days + 1
            if duree_conge<0 :
                messages.error(request, "La date de début devrait être inférieur date de fin.")
                return redirect('demande_conge')
            if duree_conge > quota.jours_restants():
                messages.error(request, "La durée du congé dépasse le quota restant.")
                return redirect('demande_conge')

            # Si tout est valide, créer le congé
            conge = form.save(commit=False)
            conge.statut = 'en_attente'  # Le statut initial est en attente
            conge.save()

            # Mettre à jour le quota
            # quota.quota_utilise += duree_conge
            # quota.save()
            messages.success(request, "Le congé a été ajouté avec succès.")
            return redirect('liste_conge')
    else:
        form = CongeForm()
        return render(request, 'conges/demande_conge.html', {'form': form})

@login_required
def liste_conges(request):
    conges = Conge.objects.all()

    # Vérification du quota de congé restant pour chaque utilisateur
    for conge in conges:
        quota = QuotaAnnuel.objects.get(utilisateur=conge.utilisateur, annee=conge.annee)
        # Vérifier si la durée du congé est supérieure au quota restant
        if conge.duree() > quota.jours_restants():
            conge.statut = 'rejete'
            conge.save()
            messages.warning(request, f"Le congé de {conge.utilisateur.nom} dépasse le quota disponible et a été rejeté.")
    
    return render(request, 'conges/liste_conges.html', {'conges': conges})

def modifier_statut_conge(request, conge_id):
    conge = get_object_or_404(Conge, id=conge_id)

    if request.method == 'POST':
        statut = request.POST.get('statut')

        # Vérifier si le statut est "approuvé"
        if statut == 'approuve':
            # Calculer la durée du congé
            duree_conge = (conge.date_fin - conge.date_debut).days + 1

            # Vérifier si la durée du congé ne dépasse pas le quota restant
            quota = QuotaAnnuel.objects.get(utilisateur=conge.utilisateur, annee=conge.annee)
            if duree_conge <= quota.jours_restants():
                # Mettre à jour le statut du congé
                conge.statut = 'approuve'
                conge.save()

                # Mettre à jour le quota de l'utilisateur
                quota.quota_utilise += duree_conge
                quota.save()

                messages.success(request, f"Le congé de {conge.utilisateur.nom} a été approuvé et le quota a été mis à jour.")
            else:
                messages.error(request, f"Le congé de {conge.utilisateur.nom} dépasse le quota restant. Il ne peut pas être approuvé.")
        
        elif statut == 'rejete':
            # Mettre à jour le statut du congé
            conge.statut = 'rejete'
            conge.save()
            messages.success(request, f"Le congé de {conge.utilisateur.nom} a été rejeté.")
        
        else:
            messages.error(request, "Statut inconnu.")

    return redirect('liste_conge')

def liste_constructions(request):
    form = FiltreConstruction(request.GET)
    #queryset = Marche.objects.all()
    queryset = Avancement.objects.filter(
        n_stat='O'
        )
    if form.is_valid():
        # Construire des conditions Q dynamiques
        filter_conditions = Q()

        # Filtrer par plusieurs conditions pour "État"
        etat = form.cleaned_data.get('etat')
        if etat:
            etat_conditions = Q()
            for etat_value in etat:
                etat_conditions |= Q(etat=etat_value)
            filter_conditions &= etat_conditions

        # Filtrer par plusieurs conditions pour "Type d'Établissement"
        type_etablissement = form.cleaned_data.get('type_etablissement')
        if type_etablissement:
            type_etablissement_conditions = Q()
            for type_value in type_etablissement:
                type_etablissement_conditions |= Q(site__TypeEtab=type_value)
            filter_conditions &= type_etablissement_conditions

        # Filtrer par plusieurs conditions pour "Financement"
        financement = form.cleaned_data.get('financement')
        if financement:
            financement_conditions = Q()
            for financement_value in financement:
                financement_conditions |= Q(site__marche__financement=financement_value)
            filter_conditions &= financement_conditions

        # Filtrer par plusieurs conditions pour "Ordre de Service"
        os = form.cleaned_data.get('os')
        if os:
            os_conditions = Q()
            for os_value in os:
                os_conditions |= Q(site__marche__os=os_value)
            filter_conditions &= os_conditions

        # Filtrer par plusieurs conditions pour "Nombre de Salles"
        NbSalle = form.cleaned_data.get('NbSalle')
        if NbSalle:
            NbSalle_conditions = Q()
            for salle_value in NbSalle:
                NbSalle_conditions |= Q(site__marche__NbSalle=salle_value)
            filter_conditions &= NbSalle_conditions

        queryset = queryset.filter(filter_conditions)
        queryset = queryset.order_by('site__commune__district__region__name','site__commune__district__name')
        results = []
        for avancement in queryset :
            latest_marche = Marche.objects.filter(site__id=avancement.site.id).order_by('-create_on').first()
            latest_avancement = Avancement.objects.filter(site__id=avancement.site.id).order_by('-create_on').first()

            results.append({
                'site': avancement,
                'latest_marche': latest_marche,
                'latest_avancement': latest_avancement
            })
        # Appliquer les conditions si elles existent
        
        return render(request, 'pages/filtre.html', {'form': form, 'results': results})
    else :
        #form = FiltreConstruction(request.GET) 
        return render(request, 'pages/filtre.html',{'form':form})
    #return render(request, 'pages/filtre.html',{'form':form})

class CustomLoginView(LoginView):
    template_name = 'connexion/login.html'  # Le template HTML à utiliser
    redirect_authenticated_user = True  # Rediriger si déjà connecté

    def get_success_url(self):
        """Récupère l'URL de redirection après connexion"""
        next_url = self.request.GET.get('next')
        return next_url if next_url else reverse_lazy('home')
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')  # Redirigez après déconnexion
    return render(request, 'connexion/logout_confirmation.html')

class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "Vous avez été déconnecté avec succès !")
        return super().dispatch(request, *args, **kwargs)