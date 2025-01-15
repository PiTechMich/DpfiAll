from django import forms
from .models import *
class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField()

class AvancementForm(forms.ModelForm):
    observation = forms.CharField(label='Observation',widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),required=False)
    annee_achevement = forms.CharField(label='Année Achèvement',widget=forms.TextInput(attrs={'class': 'form-control'}),max_length=4,required=False)
    Niveau = forms.CharField(label='Niveaux',widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),required=False)
    TravauxRestant = forms.CharField(label='Travaux Restant',widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),required=False)
    photo1 = forms.FileField(label='Photo 1',widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),required=False)
    photo2 = forms.FileField(label='Photo 2',widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),required=False)
    photo3 = forms.FileField(label='Photo 3',widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),required=False)
    photo4 = forms.FileField(label='Photo 4',widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),required=False)
    class Meta:
        model = Avancement
        fields = [
            'etat',
            'avancement',
            'observation',
            'annee_achevement',
            'inaugurable',
            'Niveau',
            'TravauxRestant',
            'photo1',
            'photo2',
            'photo3',
            'photo4',
            'site'
        ]
        widgets = {
            'etat': forms.Select(attrs={'class': 'form-control'}),
            'avancement': forms.TextInput(attrs={'class': 'form-control'}),     
            'inaugurable': forms.Select(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
            super(AvancementForm, self).__init__(*args, **kwargs)
            self.fields['site'].label_from_instance = lambda obj: "ID : %s  Region : %s District %s Commune : %s Nom Etab :%s" % (obj.id, obj.commune.district.region.name, obj.commune.district.name, obj.commune.name, obj.nomEtab) # Display only the author's name
            
            #Mise en form
    site = forms.ModelChoiceField(queryset=Site.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), label='Site')

class SiteForm(forms.ModelForm):
    fokontany = forms.CharField(label='Observation',widget=forms.TextInput(attrs={'class': 'form-control', 'rows': 3}),required=False)
   
    class Meta:
        model = Site
        fields = [
            'objet',
            'nomEtab',
            'TypeEtab',
            'fokontany',
            'commune'
        ]
        widgets = {
            'TypeEtab': forms.Select(attrs={'class': 'form-control'}),
            'objet': forms.Textarea(attrs={'class': 'form-control'}),     
            'nomEtab': forms.TextInput(attrs={'class': 'form-control'}), 
        }
    def __init__(self, *args, **kwargs):
            super(SiteForm, self).__init__(*args, **kwargs)
            self.fields['commune'].label_from_instance = lambda obj: "Region : %s District %s Commune : %s" % (obj.district.region.name, obj.district.name, obj.name) # Display only the author's name
            
            #Mise en form
    commune = forms.ModelChoiceField(queryset=Commune.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), label='Commune')


class MarcheForm(forms.ModelForm):
    delaiEx = forms.CharField(label='Delai Exécution',widget=forms.TextInput(attrs={'class': 'form-control', 'rows': 3}),required=False)
    Titulaire = forms.CharField(label='Titulaire',widget=forms.TextInput(attrs={'class': 'form-control'}),required=False)
    NumTitulaire = forms.CharField(label='Numéros Titulaire',widget=forms.TextInput(attrs={'class': 'form-control'}),max_length=15,required=False)
    numMarche = forms.CharField(label='Numéros du Marché',widget=forms.TextInput(attrs={'class': 'form-control', 'rows': 2}),required=False)
    class Meta:
        model = Marche
        fields = [
            'numMarche',
            'NbSalle',
            'Titulaire',
            'NumTitulaire',
            'delaiEx',
            'batiment',
            'travaux',
            'financement',
            'os',
            'site'
        ]
        widgets = {
            'os': forms.Select(attrs={'class': 'form-control'}),
            'financement': forms.Select(attrs={'class': 'form-control'}),
            'travaux': forms.Select(attrs={'class': 'form-control'}),
            'batiment': forms.Select(attrs={'class': 'form-control'}),
            'NbSalle': forms.TextInput(attrs={'class': 'form-control'}),     
            'inaugurable': forms.Select(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
            super(MarcheForm, self).__init__(*args, **kwargs)
            self.fields['site'].label_from_instance = lambda obj: "ID : %s  Region : %s District %s Commune : %s Nom Etab :%s" % (obj.id, obj.commune.district.region.name, obj.commune.district.name, obj.commune.name, obj.nomEtab) # Display only the author's name
            
            #Mise en form
    site = forms.ModelChoiceField(queryset=Site.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), label='Site')

class CongeForm(forms.ModelForm):
    class Meta:
        model = Conge
        fields = ['utilisateur', 'type_conge', 'annee', 'date_debut', 'date_fin', 'statut', 'justification', 'fond']
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date','class': 'form-control'}),
            'date_fin': forms.DateInput(attrs={'type': 'date','class': 'form-control'}),
            'type_conge': forms.Select(attrs={'class': 'form-control'}),
            'statut': forms.Select(attrs={'class': 'form-control'}),
            'annee': forms.TextInput(attrs={'class': 'form-control'}),
            'justification': forms.Textarea(attrs={'class': 'form-control'}),  
        }
    def __init__(self, *args, **kwargs):
            super(CongeForm, self).__init__(*args, **kwargs)
            self.fields['utilisateur'].label_from_instance = lambda obj: "IM : %s  Nom : %s Prenom %s " % (obj.im, obj.nom, obj.prenom) # Display only the author's name
            
            #Mise en form
    utilisateur = forms.ModelChoiceField(queryset=Personnel.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), label='Personnel')

class FiltreCongeForm(forms.Form):
    type_conge = forms.ModelMultipleChoiceField(
        queryset=TypeConge.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Type de Congé'
    )
    annees = forms.MultipleChoiceField(
        choices=[(str(i), str(i)) for i in range(2000, 2030)],  # Liste d'années possibles
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Années'
    )
    statut = forms.ChoiceField(
        choices=[('en_attente', 'En attente'), ('approuve', 'Approuvé'), ('rejete', 'Rejeté')],
        required=False,
        label='Statut'
    )

class FiltreConstruction(forms.Form):
    # Etat
    etat = forms.MultipleChoiceField(
        choices=Avancement.typeEtat,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Etat'
    )
    # Type d'établissement
    type_etablissement = forms.MultipleChoiceField(
        choices=Site.typeEt,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Type d\'Établissement'
    )
    # Financement
    financement = forms.MultipleChoiceField(
        choices=Marche.typefinancement,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Type de financement'
    )
    # Ordre de service
    os = forms.MultipleChoiceField(
        choices=Marche.typeOs,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Ordre de Services'
    )
    # Nombre de Salles
    NbSalle = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Nombre de Salles'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Charger les valeurs distinctes de la colonne 'NbSalle'
        nbrSalle_distincts = (
            Marche.objects.values_list('NbSalle', flat=True)
            .distinct()
            .order_by('NbSalle')
        )
        # Supprimer les valeurs nulles ou None
        nbrSalle_distincts = [f for f in nbrSalle_distincts if f is not None]
        # Définir les choix pour le champ NbSalle
        self.fields['NbSalle'].choices = [(str(f), str(f)) for f in nbrSalle_distincts]
