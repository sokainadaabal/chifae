from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager
from django.utils.translation import ugettext_lazy as _

from autoslug.fields import AutoSlugField
from ckeditor.fields import RichTextField

from datetime import datetime
from django.urls import reverse
from django.conf import settings

# Create your models here.
#for search medicament I create a class Tag and in Class Medicament I ising thatdatetime A combination of a date and a that  
# tags = models.ManyToManyField(Tag)
class Pharmcie(models.Model):
    nom=models.CharField( max_length=100,unique=True) 
    code=models.CharField( max_length=100,unique=True)
    ville=models.CharField( max_length=100)
    image=models.ImageField(default="profile-img.png",null=True, blank=True)
    def __str__(self):
    		return self.nom
    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
	                                
class PharmcienManager(BaseUserManager):
    def create_user(self,email,username,password=None):
        if not email:
            raise ValueError("Users must have an email adress")
        if not username:
             raise ValueError("Users must have an Username")
        
        user= self.model(email=self.normalize_email(email),
        username=username)
        user.set_password(password)
       
        user.save(using=self._db)
        return user
    def create_superuser(self,email,username,password):
        user= self.create_user(email=self.normalize_email(email),
        password=password,
        username=username)
        
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user

class Pharmacien(AbstractBaseUser):
    #personel data 
    etat_civile = models.CharField(max_length=100,null=True)
    first_name=models.CharField( max_length=100,null=True)
    last_name=models.CharField( max_length=255,null=True)
    email=models.EmailField( max_length=254,unique=True)
    username=models.CharField( max_length=255,null=True)
    date=models. DateField(auto_now=False, auto_now_add=False,null=True)
    activite= models.CharField(max_length=100,null=True)
    date_obtention_de_diplome=models. DateField(auto_now=False, auto_now_add=False,null=True)
    nom_pharmacie=models.ForeignKey(Pharmcie,on_delete=models.CASCADE,null=True)
    adresse_professionnelle=models.CharField( max_length=255,null=True)
    ville_exercice=models.CharField( max_length=255,null=True)
    pays=models.CharField( max_length=255,null=True)
    telephone=models.CharField( max_length=255,null=True)
    gsm=models.CharField( max_length=255,null=True)
    date_joined = models.DateTimeField(verbose_name="date joind",auto_now_add=True)
    profile_pic=models.ImageField(default="profile-img.png",null=True, blank=True)
    etat=models.BooleanField(editable=True,default=False)
    last_login= models.DateTimeField(verbose_name="Last Login",auto_now=True)
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
   
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects=PharmcienManager()
    def __str__(self):
        return self.username
    def has_perm(self,perm,obj=None):
        return self.is_admin
    def has_module_perms(self,app_label):
        return True
    @property
    def image_url(self):
        if self.profile_pic and hasattr(self.profile_pic, 'url'):
            return self.profile_pic.url
 
class Fournisseur(models.Model):
    nom=models.CharField( max_length=100,null=True)
    email=models.EmailField( max_length=254,unique=True,null=True)
    tel=models.CharField(max_length=100,null=True)
    fax=models.CharField(max_length=100,null=True)
    adress=models.CharField(max_length=100,null=True)
    ville=models.CharField(max_length=100,null=True)
    nom_pharmacie=models.ForeignKey(Pharmcie,on_delete=models.CASCADE,null=True)
    date_created=models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
             return self.nom

class Article(models.Model):
    titre = models.CharField(_('titre'), max_length=255,null=True)
    slug = AutoSlugField(_('slug'), populate_from='titre', unique=True)
    image = models.ImageField( blank=True, null=True)
    contenu =RichTextField(_('contenu'))
    description =RichTextField(_('description'), blank=True, null=True)
    public = models.BooleanField(_('public'), default=False)
    auteur=models.ForeignKey(Pharmacien,on_delete=models.CASCADE,null=True)
    creation = models.DateTimeField(_('creation'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    pub_date = models.DateTimeField(_('publish date'), blank=True, null=True)
    def save(self, *args, **kwargs):
        """
        Set publish date to the date when post's published status is switched to True, 
        reset the date if post is unpublished
        """
        if self.public and self.pub_date is None:
            self.pub_date = datetime.now()
        elif not self.public and self.pub_date is not None:
            self.pub_date = None
        super().save(*args, **kwargs)
    def __str__(self):
         return self.titre
    def image_url(self):
            if self.image and hasattr(self.image, 'url'):
                return self.image.url

class Medicament(models.Model):
    nom_c=models.CharField(max_length=255,null=True)
    num_lot=models.IntegerField(null=True)
    img=models.ImageField(_('img'),null=True, blank=True)
    exp=models. DateField(auto_now=False, auto_now_add=False,null=True)
    ppm=models.FloatField(max_length=100,null=True)
    qte=models.IntegerField(null=True)
    dosage=models.CharField(max_length=255,null=True)
    condtionnement=RichTextField(_('condtionnement'))
    famille=models.CharField(max_length=255,null=True)
    nom_pharma=models.ForeignKey(Pharmcie,on_delete=models.CASCADE,null=True, blank=True)       
    nom_stock=models.CharField(max_length=255,null=True)
    digital = models.BooleanField(default=False,null=True, blank=True)
    def __str__(self):
        return self.nom_c +' ' + self.dosage
    @property
    def image_url(self):
            try:
                url = self.img.url
            except:
                url = ''
            return url
class Stock(models.Model):
    nom_c=models.ForeignKey(Medicament,on_delete=models.CASCADE,null=True, blank=True)
    qte_stock=models.IntegerField(null=True)
    hors_stock=models.IntegerField(null=True)
    alert_qte=models.IntegerField(null=True)
    def __str__(self):
        return self.nom_c.nom_stock

class Order(models.Model):
    pharmacien=models.ForeignKey(Pharmacien, on_delete=models.SET_NULL, null=True, blank=True)
    date_orde=models.DateTimeField(auto_now=False, auto_now_add=True,null=True)
    complete=models.BooleanField(blank=True, null=True,default=False)
    transaction_id=models.CharField(max_length=255,null=True)

    def __str__(self):
            return str(self.id)
    @property
    def get_vendre_total(self):
        ventes=self.vente_set.all()
        total=sum([item.get_total for item in ventes])
        return total
    @property
    def get_vendre_articl(self):
        ventes=self.vente_set.all()
        total=sum([item.qte_vendre for item in ventes])
        return total
class Vente(models.Model):
        medicament=models.ForeignKey(Medicament, on_delete=models.SET_NULL, null=True)
        order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
        qte_vendre = models.IntegerField(default=0, null=True, blank=True)
        date_added = models.DateTimeField(auto_now_add=True)

        @property
        def get_total(self):
            total=self.medicament.ppm*self.qte_vendre
            return total

class OrderCommande(models.Model):
    pharmacien=models.ForeignKey(Pharmacien, on_delete=models.SET_NULL, null=True, blank=True)
    fournisseur=models.ForeignKey(Fournisseur, on_delete=models.SET_NULL, null=True, blank=True)
    date_orde=models.DateTimeField(auto_now=False, auto_now_add=True,null=True)
    complete=models.BooleanField(blank=True, null=True,default=False)
    transaction_id=models.CharField(max_length=255,null=True)

    def __str__(self):
            return str(self.id)
    @property
    def get_commande_articl(self):
        ventes=self.commande_set.all()
        total=sum([item.qte_commande for item in ventes])
        return total
class Commande(models.Model):
        medicament=models.ForeignKey(Medicament, on_delete=models.SET_NULL, null=True)
        order = models.ForeignKey(OrderCommande, on_delete=models.SET_NULL, null=True)
        qte_commande = models.IntegerField(default=0, null=True, blank=True)
        date_added = models.DateTimeField(auto_now_add=True)
####su
class Orderonline(models.Model):
    pharmacien=models.ForeignKey(Pharmacien, on_delete=models.SET_NULL, null=True, blank=True)
    date_orde=models.DateTimeField(auto_now=False, auto_now_add=True,null=True)
    complete=models.BooleanField(blank=True, null=True,default=False)
    transaction_id=models.CharField(max_length=255,null=True)
    def __str__(self):
            return str(self.id)
    @property
    def get_vendre_total(self):
        ventes=self.venteonline_set.all()
        total=sum([item.get_total for item in ventes])
        return total
    @property
    def get_vendre_articl(self):
        ventes=self.venteonline_set.all()
        total=sum([item.qte_vendre for item in ventes])
        return total
class VenteOnline(models.Model):
        medicament=models.ForeignKey(Medicament, on_delete=models.SET_NULL, null=True)
        order = models.ForeignKey(Orderonline, on_delete=models.SET_NULL, null=True)
        qte_vendre = models.IntegerField(default=0, null=True, blank=True)
        date_added = models.DateTimeField(auto_now_add=True)

        @property
        def get_total(self):
            total=self.medicament.ppm*self.qte_vendre
            return total
