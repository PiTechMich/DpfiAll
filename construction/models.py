from django.db import models
from django.utils.timezone import now
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

# Create your models here.
class Province(models.Model):
    name =models.CharField(max_length=250)
    create_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Province de  {self.name}"
    
class Region(models.Model):
    name =models.CharField(max_length=250)
    province=models.ForeignKey('Province', on_delete=models.CASCADE,db_index=True)
    create_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Province de  {self.province.name} Region de : {self.name}"

class District(models.Model):
    name =models.CharField(max_length=250)
    region=models.ForeignKey('Region', on_delete=models.CASCADE,db_index=True)
    create_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Province de  {self.region.province.name} Region de : {self.region.name} District de : {self.name}"

class Commune(models.Model):
    name =models.CharField(max_length=250)
    district=models.ForeignKey('District', on_delete=models.CASCADE,db_index=True)
    create_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Province de  {self.district.region.province.name} Region de : {self.district.region.name} District de : {self.district.name} Commune de : {self.name}"

# Information Travaux

class Site(models.Model):
    objet =models.TextField()
    nomEtab =models.CharField(max_length=255)
    typeEt = [
        ('EPP', 'EPP'),
        ('CEG', 'CEG'),
        ('LYCEE', 'LYCEE'),
        ('ADMINISTRATIF', 'ADMINISTRATIF'),
        ('ESM', 'ESM'),
        ('AUTRES', 'AUTRES')
    ]
    TypeEtab = models.CharField(
        max_length=25,
        choices=typeEt,  # Ajout des choix
    )
    fokontany =models.CharField(max_length=255,null=True)
    commune=models.ForeignKey('Commune', on_delete=models.CASCADE,db_index=True)
    create_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ID {self.id} District de : {self.commune.district.name} Commune de : {self.commune.name} Nom Etablissement : {self.nomEtab} Objet : {self.objet}"

# Marche
class Marche(models.Model):
    numMarche =models.CharField(max_length=255,null=True)
    NbSalle =models.IntegerField(max_length=10)
    Titulaire =models.CharField(max_length=255,null=True)
    NumTitulaire=models.CharField(max_length=50,null=True)
    delaiEx=models.CharField(max_length=50,null=True)
    typeBat = [
        ('Administratif', 'Administratif'),
        ('Scolaire', 'Scolaire')
    ]
    batiment=models.CharField(
        max_length=25,
        choices=typeBat
        )
    typeTravaux = [
        ('Constr. Neuve', 'Constr. Neuve'),
        ('Rehabilitation', 'Rehabilitation')
    ]
    travaux=models.CharField(
        max_length=25,
        choices=typeTravaux
        )

    typefinancement = [
        ('RPI', 'RPI'),
        ('PAEB', 'PAEB')
    ]
    financement=models.CharField(
        max_length=25,
        choices=typefinancement
        )
    
    typeOs = [
        ('OS_2019', 'OS_2019'),
        ('OS_2020', 'OS_2020'),
        ('OS_2021', 'OS_2021'),
        ('OS_2022', 'OS_2022'),
        ('OS_2023', 'OS_2023'),
        ('OS_2024', 'OS_2024'),
        ('OS_2025', 'OS_2025'),
        ('OS_PAEB', 'OS_PAEB'),
    ]
    os=models.CharField(
        max_length=25,
        choices=typeOs
        )
    
    site=models.ForeignKey('Site', on_delete=models.CASCADE,db_index=True)
    create_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Objet de : {self.site.objet} District de : {self.site.commune.district.name} Nom Etablissement : {self.site.nomEtab} Nbre de Salle : {self.NbSalle} "

# Marche
class Avancement(models.Model):
    typeEtat = [
        ('Achevée', 'Achevée'),
        ('En arrêt', 'En arrêt'),
        ('En cours', 'En cours'),
        ('Non commencée', 'Non commencée')
    ]
    etat=models.CharField(
        max_length=25,
        choices=typeEtat
        )
    
    avancement = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Avancement en pourcentage (0 à 100)"
    )
    typeStat = [
        ('O', 'Oui'),
        ('N', 'Non')
    ]
    n_stat=models.CharField(
        max_length=2,
        choices=typeStat,
        default='O'
        )
    
    observation = models.TextField(null=True, blank=True)
    annee_achevement = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        validators=[
            RegexValidator(r'^\d{4}$', message="L'année doit comporter 4 chiffres.")
        ]
    )

    
    inau = [
        ('DEJA', 'DEJA'),
        ('OUI', 'OUI'),
        ('NON', 'NON')
    ]
    inaugurable=models.CharField(
        max_length=10,
        choices=inau,
        null=True
        )
    Niveau =models.TextField(null=True)
    TravauxRestant =models.TextField(null=True)
    photo1= models.ImageField(upload_to='constructionImg/',null=True, blank=True)
    photo2= models.ImageField(upload_to='constructionImg/',null=True, blank=True)
    photo3= models.ImageField(upload_to='constructionImg/',null=True, blank=True)
    photo4= models.ImageField(upload_to='constructionImg/',null=True, blank=True)
    site=models.ForeignKey('Site', on_delete=models.CASCADE,db_index=True)
    create_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avancement {self.avancement}% Objet de : {self.site.objet} District de : {self.site.commune.district.name} Nom Etablissement : {self.site.nomEtab} "

class Personnel(models.Model):
    im = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    tel = models.CharField(max_length=100, blank=True, null=True)
    fonction = models.CharField(max_length=100)
    typeSer = [
        ('Bureau Rattaché', 'Bureau Rattaché'),
        ('SCMIS', 'SCMIS'),
        ('SCMIA', 'SCMIA'),
        ('SDSA', 'SDSA'),
        ('PAEB', 'PAEB'),
    ]
    service = models.CharField(
        max_length=25,
        choices=typeSer,
        default="Bureau Rattaché")

    def __str__(self):
        return f"{self.im} - {self.nom} {self.prenom}"

class QuotaAnnuel(models.Model):
    utilisateur = models.ForeignKey(Personnel, on_delete=models.CASCADE)
    annee = models.PositiveIntegerField()
    quota_total = models.PositiveIntegerField(default=30)
    quota_utilise = models.PositiveIntegerField(default=0)
    fond = models.FileField(null=True, blank=True, upload_to='decision/')
    class Meta:
        unique_together = ('utilisateur', 'annee')

    def jours_restants(self):
        return self.quota_total - self.quota_utilise

    def __str__(self):
        return f"{self.utilisateur.nom} - {self.annee}: {self.jours_restants()} jours restants"


class TypeConge(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nom

class Conge(models.Model):
    STATUTS = [
        ('en_attente', 'En attente'),
        ('approuve', 'Approuvé'),
        ('rejete', 'Rejeté'),
    ]

    utilisateur = models.ForeignKey(Personnel, on_delete=models.CASCADE)
    type_conge = models.ForeignKey(TypeConge, on_delete=models.CASCADE)
    annee = models.PositiveIntegerField()  # Année spécifiée par l'utilisateur
    date_debut = models.DateField()
    date_fin = models.DateField()
    statut = models.CharField(max_length=20, choices=STATUTS, default='en_attente')
    justification = models.TextField(blank=True, null=True)

    fond = models.FileField(null=True, blank=True, upload_to='demandeconge/')
    def duree(self):
        return (self.date_fin - self.date_debut).days + 1

    def __str__(self):
        return f"{self.utilisateur.nom} - {self.type_conge.nom} ({self.annee} : {self.date_debut} à {self.date_fin})"