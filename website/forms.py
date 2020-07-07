from django import forms
from django.forms import ModelForm
from website.models import *
from django.contrib.auth.forms import UserCreationForm
from ckeditor.widgets import CKEditorWidget


class FournisseurForm(ModelForm):
    class Meta:
        model = Fournisseur
        widgets={
           'nom':forms.TextInput(attrs={'class':'form-control','placeholder':'Nom Fournisseur'}),
           'email':forms.TextInput(attrs={'class':'form-control','placeholder':'E-email'}),
           'tel':forms.TextInput(attrs={'class':'form-control','placeholder':"Télèphone"}),
           'fax':forms.TextInput(attrs={'class':'form-control','placeholder':"Fax"}),
           'adress':forms.TextInput(attrs={'class':'form-control','placeholder':"Adress"}),
           'ville':forms.TextInput(attrs={'class':'form-control ','placeholder':'Ville'}),
        }
        exclude = ['nom_pharma']
        fields = ['nom','email','tel','fax','adress','ville' ]

class RegisterForm(UserCreationForm):
    CHOICES = (
        ("","Etat Civil"),
        ("Mad","Madame"),
        ("Mon","Monsieur"),
        ("Made","Mademoiselle")
     )
    active=(
        ("","Activité"),
        ("phar","Pharmacien"),
        ("emp","Employée"),
        ("cl","Client")

     )
    
    email=forms.EmailField(max_length=60,help_text="Remarque , Ajouter une adresse email Valider")
    nom_pharmacie =forms.ModelChoiceField(widget = forms.Select(attrs={ 
                    'class':'custom-select' ,'id':'soso'}),
                    queryset = Pharmcie.objects.all(),empty_label="Ajouter Votre Pharmacie",required=False)
    etat_civile=forms.ChoiceField(widget = forms.Select(attrs={ 
                    'class':'custom-select'}),choices=CHOICES)
    activite=forms.ChoiceField(widget = forms.Select(attrs={ 
                    'class':'custom-select ','id':'soka'}),choices=active)
    date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}),input_formats=['%Y-%m-%d',      # '2006-10-25'
        '%m/%d/%Y',      # '10/25/2006'
        '%m/%d/%y']      # '10/25/06'
        , help_text="** Date de naissance"
        )
    date_obtention_de_diplome= forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date','id':'sos','value':'12/10/1999'}),input_formats=['%Y-%m-%d',      # '2006-10-25'
      '%m/%d/%Y',      # '10/25/2006'
      '%m/%d/%y']      # '10/25/06'
       , help_text="** Année d'obtention du diplôme ",initial=None,required=False
      )
    class Meta:
        model= Pharmacien
        fields=['etat_civile','first_name','last_name','email','username','activite','nom_pharmacie','date','date_obtention_de_diplome','adresse_professionnelle','pays','ville_exercice','telephone','gsm','password1','password2']
    
class PharmacieForm(forms.ModelForm):
    image=forms.ImageField(label=('Image'),required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput,help_text="* logo")
    nom=forms.CharField(widget = forms.TextInput(attrs={ 
                    'class':'form-control'}),help_text="* nom de pharmacie")
    code=forms.CharField(widget = forms.TextInput(attrs={ 
                    'class':'form-control'}),help_text="* code de register commerce")
    ville=forms.CharField(widget = forms.TextInput(attrs={ 
                    'class':'form-control'}),help_text="* la ville de Pharmacie")

    class Meta:
        model = Pharmcie
        fields=['nom','code','ville','image']
    def __init__(self, *args, **kwargs):
        super(PharmacieForm, self).__init__(*args, **kwargs)

class ProfileUser(forms.ModelForm):
    disabled_fields = ('nom_pharmacie','etat_civile','activite',)
  
    first_name =forms.CharField(widget = forms.TextInput(attrs={ 
                    'class':'form-control','Style':'position:initial;'}))
    last_name =forms.CharField(widget = forms.TextInput(attrs={ 
                    'class':'form-control','Style':'position:initial;'}))
    username =forms.CharField(widget = forms.TextInput(attrs={ 
                    'class':'form-control','Style':'position:initial;'}))
    email=forms.EmailField(max_length=60,help_text="Remarque , Ajouter une adresse email Valider",widget = forms.TextInput(attrs={ 
                    'class':'form-control','Style':'position:initial;'}))
    gsm=forms.CharField(widget = forms.TextInput(attrs={ 
                    'class':'form-control','Style':'position:initial;'}))
    ville_exercice =forms.CharField(widget = forms.TextInput(attrs={ 
                    'class':'form-control','Style':'position:initial;'}))
    pays =forms.CharField(widget = forms.TextInput(attrs={ 
                    'class':'form-control','Style':'position:initial;'}))
    telephone =forms.CharField(widget = forms.TextInput(attrs={ 
                    'class':'form-control','Style':'position:initial;'}))
    adresse_professionnelle =forms.CharField(widget = forms.TextInput(attrs={ 
                    'class':'form-control','Style':'position:initial;'}))
    etat_civile=forms.CharField(widget = forms.TextInput(attrs={ 
                    'class':'custom-select','Style':'position:initial;'}))
    nom_pharmacie =forms.ModelChoiceField(widget = forms.Select(attrs={ 
                    'class':'custom-select','Style':'position:initial;'}),
                    queryset = Pharmcie.objects.all())
    
    activite=forms.CharField(widget = forms.TextInput(attrs={ 
                    'class':'custom-select','Style':'position:initial;'}))
    date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date','class':'form-control','Style':'position:initial;'}),input_formats=['%Y-%m-%d',      # '2006-10-25'
    '%m/%d/%Y',      # '10/25/2006'
    '%m/%d/%y']      # '10/25/06'
    )
    profile_pic=forms.ImageField(label=('Image'),required=False, error_messages = {'invalid':("Image files only")}, widget=forms.widgets.FileInput(attrs={'Style':'position:initial;'}))
    class Meta:
        model=Pharmacien
        #fields='__all__'
        fields=['etat_civile','first_name','last_name','email','username','activite','nom_pharmacie','date','adresse_professionnelle','pays','ville_exercice','telephone','gsm','profile_pic','adresse_professionnelle']

    def __init__(self, *args, **kwargs):
        super(ProfileUser, self).__init__(*args, **kwargs)
        
        for field in self.disabled_fields:
            self.fields[field].disabled = True

class EmployeeForm(forms.ModelForm):
   
    class Meta:
        model=Pharmacien
        fields=['etat',] 
class  ArticleForm(forms.ModelForm):
    contenu = forms.CharField(widget=CKEditorWidget(attrs={'Style':' width: 435px;'}),help_text="** Contenu")
    description=forms.CharField(widget=CKEditorWidget(attrs={'Style':' width: 435px'}),help_text="** Description")
    public=forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'checkbox checkbox-primary '}),label="Public")
    image=forms.ImageField(label=('Image'),required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput(attrs={'class':'form-control'}),help_text="** Image d'article")
    class Meta:
        model=Article
        widgets={'titre':forms.TextInput(attrs={'class':'form-control','placeholder':"Titre d'article"}),}
        exclude = ['auteur']
        fields='__all__'
        
class MedicamentForm(forms.ModelForm):
    exp= forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date','class':'form-control'}),input_formats=['%Y-%m-%d',      # '2006-10-25'
    '%m/%d/%Y',      # '10/25/2006'
    '%m/%d/%y'] 
         # '10/25/06'
     , help_text="** Date d'expiration"
    )
    condtionnement=forms.CharField(widget=CKEditorWidget(attrs={'Style':' width: 356px;'}),help_text="** Conditionnement",required=False)
    img=forms.ImageField(label=('Image'),required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput(attrs={'class':'form-control'}),help_text="** Image Médicament")
    class Meta:
        model = Medicament
        widgets={
           'nom_c':forms.TextInput(attrs={'class':'form-control','placeholder':'Nom Commercial'}),
           'num_lot':forms.TextInput(attrs={'class':'form-control','placeholder':'Numéro de lot'}),
           
           'ppm':forms.TextInput(attrs={'class':'form-control','placeholder':"Prix Pobulaire de vente "}),
           'qte':forms.TextInput(attrs={'class':'form-control','placeholder':"Quantité"}),
           'dosage':forms.TextInput(attrs={'class':'form-control','placeholder':"Dosage"}),
           'famille':forms.TextInput(attrs={'class':'form-control','placeholder':'Formes des médicaments'}),
           
           
        }
        exclude = ['nom_pharma']
        fields=['img','nom_c','num_lot','exp','ppm','qte','dosage','condtionnement','famille','nom_pharma']
class StockForm(forms.ModelForm):
    qte_stock=forms.IntegerField(widget = forms.TextInput(attrs={ 
                    'class':'form-control ','placeholder':'Quantité au Stock'}))
    hors_stock=forms.IntegerField(widget = forms.TextInput(attrs={ 
                    'class':'form-control ','placeholder':'Quantité Hors Stock'}))
    alert_qte =forms.IntegerField(widget = forms.TextInput(attrs={ 
                    'class':'form-control ','placeholder':'Alert Quantité'}))
    class Meta: 
        model=Stock
        widgets={
           'nom_c':forms.Select(attrs={'class':'custom-select'})
        }
        fields='__all__'
    def __init__(self, request, *args, **kwargs):
        super(StockForm, self).__init__(*args, **kwargs)
        self.fields['nom_c'].queryset = Medicament.objects.filter(nom_pharma=request.user.nom_pharmacie)
        
 