from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail,EmailMultiAlternatives
from django.utils.html import strip_tags
from django.core import mail
import json
import datetime
from django.contrib.auth import login,authenticate,logout
from django.http import JsonResponse
from django.template.loader import render_to_string
#pour pagination 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
#for login and register
from django.contrib import messages
from django import forms
from datetime import date
#session 
from django.contrib.auth.decorators import login_required
# app file create by me 
from website.models import *
from website.forms import *
from website.decorators import *
import csv
from django.views.generic import *


from website.utils import render_to_pdf
from time import gmtime, strftime
# Create your views here.
def index(request):
    medicaments=Medicament.objects.all()
    context = {'medicaments':medicaments}
    return render(request,'store.html',context)

@unauthenticated_user
def loginpage(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        util=Pharmacien.objects.get(email=email)
        if util.activite=='emp':
            if util.etat == False :
                messages.error(request,'le compte de utilisateur avec ce email ' +email +"  n'a pas autorisé  :)")
            else:
                user=authenticate(request,email=email,password=password)
                if user is not None:
                    login(request,user)
                    return redirect('homeP')
                else:
                        messages.error(request,'Utilisateur avec ce email ' +email +"n'exist pas :)")
        if util.activite=='phar':
                user=authenticate(request,email=email,password=password)
                if user is not None:
                    login(request,user)
                    return redirect('home')
                else:
                        messages.error(request,'Utilisateur avec ce email ' +email +"n'exist pas :)")
        if util.activite == 'cl':
                user=authenticate(request,email=email,password=password)
                if user is not None:
                    login(request,user)
                    return redirect('homeC')
                else:
                        messages.error(request,'Utilisateur avec ce email ' +email +"n'exist pas :)")
      
    context={}
    return render(request,'Connexion/Login.html',context)

def register(request): 
    context={}
    if  request.user.is_authenticated:
        return redirect('home')
    else:
        if request.POST:           
            form=RegisterForm(request.POST ) 
            form2=PharmacieForm(request.POST)
            if form.is_valid():
                nom=form.cleaned_data.get('nom_pharmacie')
                active=form.cleaned_data.get('activite') 
                nom_phar=Pharmcie.objects.get(nom=nom)
                pharamcien=Pharmacien.objects.filter(nom_pharmacie=nom)
                if active == "phar":
                        if   nom_phar:
                            if  pharamcien:
                                messages.error(request,'cette pharamcie avez un gérant')
                                return redirect('register')
                            else:
                                form.save()
                                username=form.cleaned_data.get('first_name')
                                messages.success(request,'le Compte est crée par success  '  + username)
                                return redirect('login') 
                        else:
                                messages.error(request,"Sélectionner le nom de votre pharmacie si il existe , ou cliquer sur + pour ajouter" )
                                return redirect('register')
                if  active == "emp": 
                        if nom_phar:
                            form.save()
                            username=form.cleaned_data.get('first_name')
                            messages.success(request,"le Compte est crée par success "  + username +"mais attendez l'acceptation de votre Gérant")
                            return redirect('register')
                        else:
                            
                            messages.error(request,"Sélectionner le nom de votre pharmacie")
                            return redirect('register')
                        
                if  active == "cl": 
                    form.save()
                    username=form.cleaned_data.get('first_name')
                    messages.success(request,"le Compte est crée par success "  + username +" Bienvenue à Chifaesite")
                    return redirect('register')          
            if form2.is_valid():
                form2.save()
                return redirect('register')   
            else:
                context['form']=form
        else:
            form=RegisterForm()
            form2=PharmacieForm()
            context={
                'form':form,
                'form2':form2
            }
    
    return render(request,'Connexion/Register.html',context)

               
def logoutUser(request):
    logout(request)
    return redirect('login')
@login_required(login_url='login')

def homeC(request):
    medicaments=Medicament.objects.filter(nom_pharma=request.user.nom_pharmacie)
    cartItems=0
    if request.user.is_authenticated:
        pharmacien = request.user.id
        order,created= Orderonline.objects.get_or_create(pharmacien_id=request.user.id, complete=False)
        order.save()
        cartItems=order.get_vendre_articl
    else: 
        order={'get_vendre_total':0 ,'get_vendre_articl':0}
        cartItems=order['get_vendre_artic']
   
    context = {'medicaments':medicaments,'cartItems':cartItems}
    return render(request,'client/store.html',context) 
# home page 
@login_required(login_url='login')
@admin_only
def home(request):
    user=request.user 
    fournisseur=Fournisseur.objects.filter(nom_pharmacie=user.nom_pharmacie)
    total=fournisseur.count() 
    
    stock=Stock.objects.filter(nom_c__nom_pharma=request.user.nom_pharmacie).order_by('id')
   
    total2=stock.count()
    pharmcien=Pharmacien.objects.filter(nom_pharmacie=user.nom_pharmacie).order_by('id')
    c=0
    a=0
    b=0
    myobject = Vente.objects.filter(medicament__nom_pharma=request.user.nom_pharmacie)[:5]
    ie    = Order.objects.filter(pharmacien__nom_pharmacie=request.user.nom_pharmacie)[:5]
    emp   =   Vente.objects.filter(order__pharmacien__activite="emp",order__pharmacien__nom_pharmacie=request.user.nom_pharmacie)[:5]
    gerant=  Vente.objects.filter(order__pharmacien__activite="phar",order__pharmacien__nom_pharmacie=request.user.nom_pharmacie)[:5]
    print(myobject,gerant)
    for i in pharmcien:
        if i.activite=='emp':
            c=c+1
            if i.etat==False:
                a=a+1
            else :
                b=b+1
    context={'total':total,'a':a,'b':b,'c':c,'total2':total2, 'myobject':myobject,
                        'emp':emp,
                        'gerant':gerant,'ie':ie}
    return render(request,'pharmacien/dashboard.html',context) 
def get_data(request,*args,**kwargs):
    vente=Vente.objects.filter(medicament__nom_pharma=request.user.nom_pharmacie)
    vente=vente.count()
    gerant=Order.objects.filter(pharmacien__activite="phar")
    gerant=gerant.count()
    emp=Order.objects.filter(pharmacien__activite="emp").count()
    datadb=[vente,gerant,emp]
    label=["Vente", "Gérant","Employée"]
    context={'data':datadb}
    return context
@login_required(login_url='login')
def profilePhar(request):
    user=request.user
    pharmacies=Pharmcie.objects.get(nom=user.nom_pharmacie)
    form = ProfileUser(instance=user)
    form_is=PharmacieForm(instance=pharmacies)
    
    if request.method =='POST':
        form=ProfileUser(request.POST,request.FILES,instance=user)
        form_is=PharmacieForm(request.POST,request.FILES,instance=user)
        if form.is_valid() :
            form.save()
        if form_is.is_valid():
            form_is.save()
    context={'form':form,'form_is':form_is,'pharmcies':pharmacies}
    return render(request,'pharmacien/Gestion_Profile/profile.html',context)

@login_required(login_url='login')
def homeEmploye(request):
    ie=Order.objects.filter(pharmacien__nom_pharmacie=request.user.nom_pharmacie,pharmacien=request.user.id)[:5]
    emp=Vente.objects.filter(order__pharmacien__id=request.user.id,order__pharmacien__nom_pharmacie=request.user.nom_pharmacie)[:5]
    total_vendu=Vente.objects.filter(order__pharmacien__id=request.user.id,order__pharmacien__nom_pharmacie=request.user.nom_pharmacie).count()
    medicament=Medicament.objects.filter(nom_pharma=request.user.nom_pharmacie).count()
    stock=Stock.objects.filter(nom_c__nom_pharma=request.user.nom_pharmacie).count()
    total=Vente.objects.filter(order__pharmacien__nom_pharmacie=request.user.nom_pharmacie).count()
    context={'ie':ie,'emp':emp,'total_vendu': total_vendu,'medicament':medicament,'stock':stock,'total':total}
    return render(request,'Employee/dashboard.html',context)

@login_required(login_url='login')
def profile(request):
    user=request.user
    form = ProfileUser(instance=user)
    if request.method=='POST':
        form=ProfileUser(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
    context={'form':form}
    return render(request,'Employee/Gestion_Profile/profile.html',context)

# tous fuctions Concernat class pharmacien avec Activite Employée

@login_required(login_url='login')
def employee(request):
    pha=request.user.nom_pharmacie
    pharmacien=Pharmacien.objects.filter(activite='emp',nom_pharmacie=pha).order_by('id')
    pharmacien_non=Pharmacien.objects.filter(activite='emp',nom_pharmacie=pha,etat=False).order_by('id')
    search_term = request.GET.get("srh")
    search_ter = request.GET.get("srh")
    if  search_term or  search_ter :
        pharmacien = pharmacien.filter(
        Q(email__startswith=search_term)|
        Q(username__startswith=search_term)|Q(first_name__startswith=search_term)
        |Q(telephone__startswith=search_term)|Q(last_name__startswith=search_term)
        |Q(etat_civile__startswith=search_term)|Q(date__startswith=search_term)
        |Q(gsm__startswith=search_term)|Q(pays__startswith=search_term)
        |Q(adresse_professionnelle__startswith=search_term)
        |Q(ville_exercice__startswith=search_term)
    )
        pharmacien_non = pharmacien_non.filter(Q(email__startswith=search_ter)|
        Q(username__startswith=search_ter)|Q(first_name__startswith=search_ter)
        |Q(telephone__startswith=search_ter)|Q(last_name__startswith=search_ter)
        |Q(etat_civile__startswith=search_ter)|Q(date__startswith=search_ter)
        |Q(gsm__startswith=search_ter)|Q(pays__startswith=search_ter)|Q(adresse_professionnelle__startswith=search_ter)
        |Q(ville_exercice__startswith=search_ter)
       ) 
    page = request.GET.get('page', 1)
    pag = request.GET.get('page', 1)
    paginator = Paginator(pharmacien, 4)
    paginato = Paginator(pharmacien_non, 4)
    try:
       pharmacien = paginator.page(page)
       pharmacien_non = paginato.page(pag)
    except PageNotAnInteger:
        pharmacien = paginator.page(1)
        pharmacien_non = paginato.page(1)
    except EmptyPage:
        pharamcien = paginator.page(paginator.num_pages)
        pharamcien_non = paginato.page(paginato.num_pages)
   
    context={'pharmacien':pharmacien,'pharmacien_non':pharmacien_non}
    return render(request,'pharmacien/Gestion_Employe/employee.html',context)

def save_employee_form(request, form, template_name):
    data = dict()
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            pha=request.user.nom_pharmacie
            pharmacien=Pharmacien.objects.filter(activite='emp',nom_pharmacie=pha).order_by('id')
            pharmacien_non=Pharmacien.objects.filter(activite='emp',nom_pharmacie=pha,etat=False).order_by('id')
            context={'pharmacien':pharmacien,'pharmacien_non':pharmacien_non}
            data['html_employee'] = render_to_string('pharmacien/Gestion_Employe/employee_list.html',context, request=request,)
            data['html_employee_non'] = render_to_string('pharmacien/Gestion_Employe/employee_list_non.html',context, request=request,)
        else:
            data['form_is_valid'] = False
            
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
   
    return JsonResponse(data)
    
def employeeAccept(request,id):
        pharmacie= get_object_or_404(Pharmacien,id=id)
        if request.method == 'POST':
                form = EmployeeForm(request.POST,instance=pharmacie)
        else:
                form = EmployeeForm(instance=pharmacie)
        return save_employee_form(request,form,'pharmacien/Gestion_Employe/employee_accept.html')

def employeeBloquer(request,id):
        pharmacie= get_object_or_404(Pharmacien,id=id)
        if request.method == 'POST':
                form = EmployeeForm(request.POST,instance=pharmacie)
        else:
                form = EmployeeForm(instance=pharmacie)
        return save_employee_form(request,form,'pharmacien/Gestion_Employe/employee_accept.html')

# all fouction  consernat class Fournisseur :
@login_required(login_url='login')
def fournisseur(request):
    search_term = ''
    fournisseur=Fournisseur.objects.filter(nom_pharmacie=request.user.nom_pharmacie)
    search_term = request.GET.get("srh")
    if  search_term:
        fournisseur = fournisseur.filter(Q(nom__startswith=search_term)|Q(email__startswith=search_term)|
        Q(tel__startswith=search_term)|Q(fax__startswith=search_term)|Q(adress__startswith=search_term)|
        Q(ville__startswith=search_term)) 
    page = request.GET.get('page', 1)
    paginator = Paginator(fournisseur, 4)
    try:
        fournisseur = paginator.page(page)
    except PageNotAnInteger:
        fournisseur = paginator.page(1)
    except EmptyPage:
        fournisseur = paginator.page(paginator.num_pages)
    return render(request,'pharmacien/Fournisseur/fournisseur.html',{'fournisseur':fournisseur})

def save_fournisseur_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            fournisseur=form.save(commit=False)
            fournisseur.nom_pharmacie=request.user.nom_pharmacie
            fournisseur.save()
            data['form_is_valid'] = True
            fournisseur=Fournisseur.objects.filter(nom_pharmacie=request.user.nom_pharmacie)
            page = request.GET.get('page', 1)
            paginator = Paginator(fournisseur, 2)
            try:
                fournisseur = paginator.page(page)
            except PageNotAnInteger:
                fournisseur = paginator.page(1)
            except EmptyPage:
                fournisseur = paginator.page(paginator.num_pages)
            data['html_fournisseur'] = render_to_string('pharmacien/Fournisseur/fournisseur_list.html',{'fournisseur': fournisseur})
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)
  
def fournisseur_create(request):
	if request.method == 'POST':
		form = FournisseurForm(request.POST)
	else:
		form = FournisseurForm()
	return save_fournisseur_form(request, form, 'pharmacien/Fournisseur/fournisseur_create.html')

def fournisseur_update(request,id):
	fournisseur = get_object_or_404(Fournisseur,id=id)
	if request.method == 'POST':
			form = FournisseurForm(request.POST,instance=fournisseur)
	else:
			form = FournisseurForm(instance=fournisseur)
	return save_fournisseur_form(request,form,'pharmacien/Fournisseur/fournisseur_update.html')

def fournisseur_delete(request,id):
    fournisseurs = get_object_or_404(Fournisseur,id=id)
    data = dict()
    if request.method == 'POST':
            fournisseurs.delete()
            data['form_is_valid'] = True
            fournisseur = Fournisseur.objects.filter(nom_pharmacie=request.user.nom_pharmacie)
            page = request.GET.get('page', 1)
            paginator = Paginator(fournisseur, 2)
            try:
                fournisseur = paginator.page(page)
            except PageNotAnInteger:
                fournisseur = paginator.page(1)
            except EmptyPage:
                fournisseur = paginator.page(paginator.num_pages)
            data['html_fournisseur'] = render_to_string('pharmacien/Fournisseur/fournisseur_list.html',{'fournisseur': fournisseur})
    else:
        context = {'fournisseurs':fournisseurs}
        data['html_form'] = render_to_string('pharmacien/Fournisseur/fournisseur_delete.html', context, request=request)
    return JsonResponse(data)

def fournisseur_show(request,id):
    data=dict()
    fournisseur = get_object_or_404(Fournisseur,id=id)
    data['html_form'] =render_to_string('pharmacien/Fournisseur/fournisseur_show.html',{'fournisseur': fournisseur}, request=request)
    return JsonResponse(data)

def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;             filename="users.csv"'
    writer = csv.writer(response)
    writer.writerow(['Nom', 'Email', 'Tél', 'Fax',' address','ville'])
    users = Fournisseur.objects.all().values_list('nom', 'email', 'tel', 'fax','adress','ville')
    for user in users:
        writer.writerow(user)    
    return response
#end

# all fouction  consernat class Article :
@login_required(login_url='login')
def article(request):
    post=Article.objects.filter(auteur=request.user).order_by('id')
    search_term = request.GET.get("srh")
    if  search_term:
        post = post.filter(Q(titre__startswith=search_term)|Q(description__icontains=search_term)|
        Q(contenu__icontains=search_term)) 
    page = request.GET.get('page', 1)
    paginator = Paginator(post, 2)
    try:
        post = paginator.page(page)
    except PageNotAnInteger:
        post = paginator.page(1)
    except EmptyPage:
        post = paginator.page(paginator.num_pages)
    context={'post':post}
    return render(request,'pharmacien/Gestion_Article/article.html',context)
@login_required(login_url='login')
def save_article_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False)
            post.auteur = request.user
            post.image = request.FILES.get('image')
            post.save()
            data['form_is_valid'] = True
            post=Article.objects.filter(auteur=request.user)
            page = request.GET.get('page', 1)
            paginator = Paginator(post, 2)
            try:
                post = paginator.page(page)
            except PageNotAnInteger:
                post = paginator.page(1)
            except EmptyPage:
                post = paginator.page(paginator.num_pages)
            data['html_article'] = render_to_string('pharmacien/Gestion_Article/article_list.html',{'post': post})
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

def add_article(request): 
    if request.method == 'POST':
    		form = ArticleForm(request.POST)
    else:
		    form = ArticleForm()
    return save_article_form(request, form, 'pharmacien/Gestion_Article/article_add.html')

def article_update(request,id):
	post = get_object_or_404(Article,id=id)
	if request.method == 'POST':
			form = ArticleForm(request.POST,request.FILES,instance=post)
	else:
			form = ArticleForm(instance=post )
	return save_article_form(request,form,'pharmacien/Gestion_Article/article_update.html')

def article_show(request,id):
    data=dict()
    post= get_object_or_404(Article,id=id)
    data['html_form'] =render_to_string('pharmacien/Gestion_Article/article_show.html',{'post': post}, request=request)
    return JsonResponse(data)

def article_delete(request,id):
    posts = get_object_or_404(Article,id=id)
    data = dict()
    if request.method == 'POST':
            posts.delete()
            data['form_is_valid'] = True
            post=Article.objects.get(auteur=request.user)
            page = request.GET.get('page', 1)
            paginator = Paginator(post, 2)
            try:
                post = paginator.page(page)
            except PageNotAnInteger:
                post = paginator.page(1)
            except EmptyPage:
                post = paginator.page(paginator.num_pages)
            data['html_article'] = render_to_string('pharmacien/Gestion_Article/article_list.html',{'post': post})
    else:
        context = {'posts':posts}
        data['html_form'] = render_to_string('pharmacien/Gestion_Article/article_delete.html', context, request=request)
    return JsonResponse(data)

# all fouction  consernat class Medicament :
def medicament(request):
    medicament=Medicament.objects.filter(nom_pharma=request.user.nom_pharmacie).order_by('id')
    search_term = request.GET.get("srh")
    if  search_term:
        medicament = medicament.filter(Q(nom_c__startswith=search_term)|Q(dosage__startswith=search_term)|Q(num_lot__startswith=search_term)|
        Q(exp__startswith=search_term)|Q(ppm__startswith=search_term)|Q(qte__startswith=search_term)|
        Q(famille__startswith=search_term)|Q(condtionnement__icontains=search_term)|Q(nom_stock__icontains=search_term)) 
    page = request.GET.get('page', 1)
    paginator = Paginator(medicament, 4)
    try:
        medicament = paginator.page(page)
    except PageNotAnInteger:
        medicament = paginator.page(1)
    except EmptyPage:
        medicament = paginator.page(paginator.num_pages)
    context={'medicament':medicament}
    if request.user.activite=="phar":
        return render(request,'pharmacien/Gestion_Medicament/medicament.html',context)
    if request.user.activite =="emp":
        return render(request,'Employee/Gestion_Medicament/medicament.html',context)
@login_required(login_url='login')
def save_medicament_form(request, form, template_name):
    data = dict()
    nom_phar=Pharmcie.objects.get(nom=request.user.nom_pharmacie)
    if request.method == 'POST':
        if form.is_valid(): 
            nom_c=form.cleaned_data.get('nom_c')
            dosage=form.cleaned_data.get('dosage')
            medicament = form.save(commit=False)
            medicament.nom_pharma =nom_phar
            medicament.nom_stock=nom_c+' '+dosage
            medicament.save()
            data['form_is_valid'] = True
            medicament=Medicament.objects.filter(nom_pharma=nom_phar)
            page = request.GET.get('page', 1)
            paginator = Paginator(medicament, 4)
            try:
                medicament = paginator.page(page)
            except PageNotAnInteger:
                medicament = paginator.page(1)
            except EmptyPage:
                medicament = paginator.page(paginator.num_pages)
            data['html_medicament'] = render_to_string('pharmacien/Gestion_Medicament/medicament_list.html',{'medicament': medicament})
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

def medicament_add(request):
    if request.method == 'POST' :
        	form = MedicamentForm(request.POST , request.FILES)
    else:
		    form =MedicamentForm()
    return save_medicament_form(request, form,'pharmacien/Gestion_Medicament/medicament_add.html')

def medicament_show(request,id):
    data=dict()
    medicament= get_object_or_404(Medicament,id=id)
    if request.user.activite=="phar":
        data['html_form'] =render_to_string('pharmacien/Gestion_Medicament/medicament_show.html',{'medicament':medicament}, request=request)
    if request.user.activite =="emp":
       data['html_form'] =render_to_string('Employee/Gestion_Medicament/medicament_show.html',{'medicament':medicament}, request=request)

    
    return JsonResponse(data)

def medicament_update(request,id):
        medicament= get_object_or_404(Medicament,id=id)
        if request.method == 'POST':
                form =MedicamentForm(request.POST,request.FILES,instance=medicament)
        else:
                form = MedicamentForm(instance=medicament)
      
        return save_medicament_form(request,form,'pharmacien/Gestion_Medicament/medicament_update.html')

def medicament_delete(request,id):
    medicament = get_object_or_404(Medicament,id=id)
    data = dict()
    if request.method == 'POST':
            medicament.delete()
            data['form_is_valid'] = True
            medicament=Medicament.objects.filter(nom_pharma=request.user.nom_pharmacie)
            page = request.GET.get('page', 1)
            paginator = Paginator(medicament, 4)
            try:
                medicament = paginator.page(page)
            except PageNotAnInteger:
                medicament = paginator.page(1)
            except EmptyPage:
                medicament = paginator.page(paginator.num_pages)
            data['html_medicament'] = render_to_string('pharmacien/Gestion_Medicament/medicament_list.html',{'medicament': medicament})
    else:
        context = {'medicament':medicament}
        data['html_form'] = render_to_string('pharmacien/Gestion_Medicament/medicament_delete.html', context, request=request)
    return JsonResponse(data)

@login_required(login_url='login')
def export_csv_medicament(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;  filename="medicaments.csv"'
    writer = csv.writer(response)
    writer.writerow(['Nom  de Commerce', 'numéro de lot', "Date d'expiration ", 'Prix Pobulaire de Vente ',' Quantité ','Dosage','Conditionnement','Famille'])
    medicaments = Medicament.objects.filter(nom_pharma=request.user.nom_pharmacie).values_list('nom_c', 'num_lot', 'exp', 'ppm','qte','dosage','condtionnement','famille')
    for medicament in medicaments:
        writer.writerow(medicament)    
    return response
#end

# stock 
@login_required(login_url='login')

def stock(request):
    stock=Stock.objects.filter(nom_c__nom_pharma=request.user.nom_pharmacie)
    context={'stock':stock}
    return render(request,'pharmacien/Gestion_Stock/stock.html',context)
def save_medicament_stock_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid(): 
            stock = form.save(commit=False)
            nom_c=form.cleaned_data.get('nom_c')
            qte_stock=form.cleaned_data.get('qte_stock')
            hors_stock=form.cleaned_data.get('hors_stock') 
            alert=form.cleaned_data.get('alert_qte')
            medicament=Medicament.objects.filter(nom_stock=nom_c)
            stockage=Stock.objects.filter(nom_c__id=medicament[0].id)
            if stockage :
                if stockage[0].qte_stock !=qte_stock or stockage[0].hors_stock!=hors_stock or stockage[0].alert_qte!=alert: 
                    if qte_stock < medicament[0].qte :
                        if hors_stock == medicament[0].qte - qte_stock:
                            if alert < qte_stock:
                                stock.save()
                                data['form_is_valid'] = True
                                stock=Stock.objects.filter(nom_c__nom_pharma=request.user.nom_pharmacie)
                                data['html_stock'] = render_to_string('pharmacien/Gestion_Stock/stock_list.html',{'stock': stock})
                            else:
                                data['form_is_valid'] = False
                                messages.error(request,"pour que system en vous notifcation pour faire demande \n le nombre alert quantité < quantité au stock") 
                        else :
                            data['form_is_valid'] = False
                            messages.error(request,"n'a pas la quantité  atteder au hors stoks") 
                    else :
                        data['form_is_valid'] = False
                        messages.error(request,"n'a pas cette quantite de produit ") 
                else:
                    data['form_is_valid'] = False
                    messages.error(request,"ce produit existe dans le stock") 
            else :
                if qte_stock < medicament[0].qte :
                    if hors_stock == medicament[0].qte - qte_stock:
                        if alert < qte_stock:
                            stock.save()
                            data['form_is_valid'] = True
                            stock=Stock.objects.filter(nom_c__nom_pharma=request.user.nom_pharmacie)
                            data['html_stock'] = render_to_string('pharmacien/Gestion_Stock/stock_list.html',{'stock': stock})
                        else:
                            data['form_is_valid'] = False
                            messages.error(request,"pour que system en vous notifcation pour faire demande \n le nombre alert quantité < quantité au stock") 
                
                    else :
                        data['form_is_valid'] = False
                        messages.error(request,"n'a pas la quantité  atteder au hors stoks") 
                else :
                    data['form_is_valid'] = False
                    messages.error(request,"n'a pas cette quantite de produit ") 
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

@login_required(login_url='login')
def stock_add(request): 
        if request.method == 'POST' :
                form = StockForm(request,request.POST)   
        else:
                form =StockForm(request=request)

        return save_medicament_stock_form(request, form,'pharmacien/Gestion_Stock/stock_add.html')
def stock_update(request,id):
        stock= get_object_or_404(Stock,id=id)
        if request.method == 'POST':
                form =StockForm(request,request.POST,instance=stock)
        else:
                form = StockForm(request=request,instance=stock)
      
        return save_medicament_stock_form(request,form,'pharmacien/Gestion_Stock/stock_update.html')

def stock_show(request,id):
    data=dict()
    stock= get_object_or_404(Stock,id=id)
    data['html_form'] =render_to_string('pharmacien/Gestion_Stock/stock_show.html',{'stock':stock}, request=request)
    return JsonResponse(data)

def stock_delete(request,id):
    stocks = get_object_or_404(Stock,id=id)
    data = dict()
    if request.method == 'POST':
            stocks.delete()
            data['form_is_valid'] = True
            stock=Stock.objets.filter(nom_c__nom_pharma=request.user.nom_pharmacie)  
            data['html_stock'] = render_to_string('pharmacien/Gestion_Stock/stock_list.html',{'stock': stock})
    else:
        context = {'stocks':stocks}
        data['html_form'] = render_to_string('pharmacien/Gestion_Stock/stock_delete.html', context, request=request)
    return JsonResponse(data)

@login_required(login_url='login')
def vente(request):
    pharmacie = request.user.nom_pharmacie
    order= Order.objects.filter(pharmacien__nom_pharmacie=pharmacie,complete=True)
    gerant= Order.objects.filter(pharmacien__nom_pharmacie=pharmacie,pharmacien=request.user.id,complete=True)
    employee= Order.objects.filter(pharmacien__nom_pharmacie=pharmacie,pharmacien__activite="emp",complete=True)    
    context={'order':order,'gerant':gerant,'employee':employee}
    
    if request.user.activite=="phar":
        return render(request,'pharmacien/Gestion_Vente/vente.html',context)
    if request.user.activite=="emp":
        employee= Order.objects.filter(pharmacien__nom_pharmacie=pharmacie,pharmacien__activite="emp",pharmacien__id=request.user.id,complete=True)    
        context1={'employee':employee}
        return render(request,'Employee/Gestion _Vente/vente.html',context1)
def vente_add(request):
    medicaments= Medicament.objects.filter(nom_pharma=request.user.nom_pharmacie) 
    if request.user.is_authenticated:
        pharmacien = request.user.id
        order,created= Order.objects.get_or_create(pharmacien_id=request.user.id, complete=False)
        order.save()
        items = order.vente_set.all() 
    else: 
        items=[]
        order={'get_vendre_total':0 ,'get_vendre_articl':0}
       
    context={'items':items,'order':order,'medicaments':medicaments}
    if request.user.activite=="phar":
        return render(request,'pharmacien/Gestion_Vente/vente_add.html',context)
    if request.user.activite=="emp":
        return render(request,'Employee/Gestion _Vente/vente_add.html',context)
def vente_update(request,id):
    order,created= Order.objects.get_or_create(id=id)    
    items = order.vente_set.all()  
    context={'items':items,'order':order}
    if request.user.activite=="phar":
        return render(request,'pharmacien/Gestion_Vente/vente_update.html',context)
    if request.user.activite=="emp":
        return render(request,'Employee/Gestion _Vente/vente_update.html',context)
   
def updateItem(request):
        data = json.loads(request.body.decode('utf-8'))
        itemId = data['itemId']
        action = data['action']
        print('Action:', action)
        print('Product:', itemId)
        pharmacien = request.user.id
        medicament = Medicament.objects.get(id=itemId)
        order, created = Order.objects.get_or_create(pharmacien =pharmacien , complete=False)
        vente, created =Vente.objects.get_or_create(order=order, medicament=medicament)
        if action == 'add':
                if medicament.qte>0:
                   vente.qte_vendre = (vente.qte_vendre + 1)
                   medicament.qte=(medicament.qte-1)
        elif action == 'remove':
            vente.qte_vendre = (vente.qte_vendre- 1)
            medicament.qte=(medicament.qte+1)
        vente.save()
        medicament.save()
        if vente.qte_vendre <= 0:
           vente.delete()

        return JsonResponse ('Medicament est ajoute',safe=False)
def process_order(request):
    transaction_id=datetime.now().timestamp()
    data=json.loads(request.body.decode('utf-8'))
    if request.user.is_authenticated:
       pharmacien = request.user.id
       order,created=Order.objects.get_or_create(pharmacien_id=pharmacien,complete=False)
       total=float(data['form']['total'])
       order.transaction_id=transaction_id
       if total==float(order.get_vendre_total):
           order.complete=True
       order.save()
    else:
         print('Error')
    return JsonResponse('Payemnet effctue avec succes ',safe=False)
def updateArticle(request):
        data = json.loads(request.body.decode('utf-8'))
        itemId = data['itemId']
        action = data['action']
        print('Action:', action)
        print('Product:', itemId)
        pharmacien = request.user.id
        medicament = Medicament.objects.get(id=itemId)
        order=Order.objects.get_or_create(pharmacien_id=pharmacien)
        vente=Vente.objects.get(medicament=medicament.id)
        if action == 'add':
               if medicament.qte>0:
                   vente.qte_vendre = (vente.qte_vendre + 1)
                   medicament.qte=(medicament.qte-1)
        elif action == 'remove':
            vente.qte_vendre = (vente.qte_vendre- 1)
            medicament.qte=(medicament.qte+1)
        vente.save()
        medicament.save()
        if vente.qte_vendre <= 0:
           vente.delete()

        return JsonResponse ('Medicament est ajoute',safe=False)

def vente_delete(request):
    data=json.loads(request.body.decode('utf-8'))
    itemId = data['itemId']
    order=Order.objects.get(id=itemId)
    vendre=Vente.objects.filter(order_id=order.id)
    for i in Vente.objects.filter(order_id=order.id):
         medicament=Medicament.objects.get(id=i.medicament_id)
         medicament.qte=medicament.qte+i.qte_vendre
         medicament.save()
    vendre.delete()
    order.delete()

    return JsonResponse('cette vendre est supprimer',safe=False)
def pdf(request,id):
        if request.user.activite=="phar":
            template = 'pharmacien/Gestion_Vente/invoice.html'
        if request.user.activite=="emp":
            template = 'Employee/Gestion _Vente/invoice.html'
        pharamcie=request.user.nom_pharmacie 
        phar=Pharmcie.objects.get(nom=pharamcie)
        pharm=Pharmacien.objects.get(nom_pharmacie=pharamcie, activite="phar")
        order = Order.objects.get(id=id)
        vente =Vente.objects.filter(order=order.id)
        data = {
              'today':date.today(),
              'time': strftime(" %H:%M:%S  H", gmtime()),
              'vente':vente,
              'order':order,
              'nom_pharmacie':phar,
              'pharmacie':pharm

        }
        pdf = render_to_pdf('pharmacien/Gestion_Vente/invoice.html', data)
        
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %("12341231")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")

def commande(request):
    pharmacie = request.user.nom_pharmacie
    order= OrderCommande.objects.filter(pharmacien__nom_pharmacie=pharmacie,complete=True)
    context={'order':order}
    return render(request,'pharmacien/Gestion_Commande/commande.html',context)
def commande_add(request):
    medicaments= Medicament.objects.filter(nom_pharma=request.user.nom_pharmacie) 
    if request.user.is_authenticated:
        fournisseur=Fournisseur.objects.filter(nom_pharmacie=request.user.nom_pharmacie)
        pharmacien = request.user.id
        order,created= OrderCommande.objects.get_or_create(pharmacien_id=request.user.id, complete=False)
        order.save()
        items = order.commande_set.all() 
    else: 
        items=[]
    context={'items':items,'medicaments':medicaments,'order':order,'fournisseur':fournisseur}

    return render(request,'pharmacien/Gestion_Commande/commande_add.html',context)
def updatecommande(request):
        data = json.loads(request.body.decode('utf-8'))
        itemId = data['itemId']
        action = data['action']
        print('Action:', action)
        print('Product:', itemId)
        pharmacien = request.user.id
        medicament = Medicament.objects.get(id=itemId)
        order, created = OrderCommande.objects.get_or_create(pharmacien =pharmacien , complete=False)
        vente, created = Commande.objects.get_or_create(order=order, medicament=medicament)
        if action == 'add':
                if medicament.qte>0:
                   vente.qte_commande = (vente.qte_commande + 1)
                   
        elif action == 'remove':
            vente.qte_commande = (vente.qte_commande- 1)
        vente.save()
        if vente.qte_commande <= 0:
           vente.delete()
        return JsonResponse ('Medicament est ajoute',safe=False)

def process_commande(request):
    transaction_id=datetime.now().timestamp()
    data=json.loads(request.body.decode('utf-8'))
    if request.user.is_authenticated:
        pharmacien = request.user.id
        order,created=OrderCommande.objects.get_or_create(pharmacien=pharmacien,complete=False)
        total=float(data['form']['total'])
        order.transaction_id=transaction_id
        fournisseur=data['form']['fournisseur']
        order.fournisseur=Fournisseur.objects.get(nom=fournisseur)
        if total==float(order.get_commande_articl):
                    order.complete=True
        order.save()
    else:
         print('Error')
    return JsonResponse('Commande est ajouter avec succes',safe=False)
def send_eamil(request,id):
    pharamcie=request.user.nom_pharmacie 
    phar=Pharmcie.objects.get(nom=pharamcie)
    pharm=Pharmacien.objects.get(nom_pharmacie=pharamcie, activite="phar")
    order = OrderCommande.objects.get(id=id)
    vente =Commande.objects.filter(order=order.id)
    data = {
              'today':date.today(),
              'time': strftime(" %H:%M:%S  H", gmtime()),
              'vente':vente,
              'order':order,
              'nom_pharmacie':phar,
              'pharmacie':pharm
            }
    html_message = render_to_string('pharmacien/Gestion_Commande/email.html',data)
    plain_message = strip_tags(html_message)
    from_email = 'sokainadaabal@gmail.com' 
    to = order.fournisseur.email
    subject = "Commande à Le Fournisseur "+ order.fournisseur.nom
    mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
    messages.success(request,"l'email   a envoyé par success  à  "  + order.fournisseur.nom )
    return redirect('commande_add')


def venteonline_add(request):
    if request.user.is_authenticated:
        pharmacien = request.user.id
        order,created= Orderonline.objects.get_or_create(pharmacien_id=request.user.id, complete=False)
        order.save()
        items = order.venteonline_set.all() 
        cartItems=order.get_vendre_articl
    else: 
        items=[]
        order={'get_vendre_total':0 ,'get_vendre_articl':0}
        cartItems=order['get_vendre_artic']
    context={'items':items,'order':order,'cartItems':cartItems}
    return render(request,'client/vente_add.html',context)

def updateOnline(request):
        data = json.loads(request.body.decode('utf-8'))
        itemId = data['itemId']
        action = data['action']
        print('Action:', action)
        print('Product:', itemId)
        pharmacien = request.user.id
        medicament = Medicament.objects.get(id=itemId)
        order, created = Orderonline.objects.get_or_create(pharmacien =pharmacien , complete=False)
        vente, created = VenteOnline.objects.get_or_create(order=order, medicament=medicament)
        if action == 'add':
                if medicament.qte>0:
                   vente.qte_vendre = (vente.qte_vendre+ 1)
        elif action == 'remove':
            vente.qte_vendre = (vente.qte_vendre- 1)
        vente.save()
        if vente.qte_vendre <= 0:
           vente.delete()
        return JsonResponse ('Medicament est ajoute',safe=False)
def online_order(request):
    transaction_id=datetime.now().timestamp()
    data=json.loads(request.body.decode('utf-8'))
    if request.user.is_authenticated:
       pharmacien = request.user.id
       order,created=Orderonline.objects.get_or_create(pharmacien_id=pharmacien,complete=False)
       total=float(data['form']['total'])
       order.transaction_id=transaction_id
       if total==float(order.get_vendre_total):
           order.complete=True
       order.save()
    else:
         print('Error')
    return JsonResponse('Payemnet effctue avec succes ',safe=False)  
def Showarticle(request):
       articles=Article.objects.filter(auteur__nom_pharmacie=request.user.nom_pharmacie)
       order,created= Orderonline.objects.get_or_create(pharmacien_id=request.user.id, complete=False)
       cartItems=order.get_vendre_articl
       context={
           'articles':articles,
           'cartItems':cartItems
       }
       return render(request,'client/article.html',context)
def sho_article(request,id):
    article=Article.objects.get(id=int(id))
    order,created= Orderonline.objects.get_or_create(pharmacien_id=request.user.id, complete=False)
    cartItems=order.get_vendre_articl
       
    context={
        'article':article,
        'cartItems':cartItems
    }
    return render(request,'client/show_article.html',context)
