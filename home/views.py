from django.shortcuts import render
from django.contrib import messages
import json
from home.forms import SearchForm

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, request
from home.models import Setting, ContactForm, ContactMessage
from product.models import Product,Category
# Create your views here.
def index(request):
    setting = Setting.objects.all().order_by('-id')[:1]
    category = Category.objects.all()



    products_slider = Product.objects.all().order_by('id')[:4]  #first 4 products
    products_latest = Product.objects.all().order_by('-id')[:4]  # last 4 products
    products_picked = Product.objects.all().order_by('?')[:4]   #Random selected 4 products



    page="home"
    context={
        'setting':setting,
        'category':category,
        'page':page,
        'products_picked':products_picked,
        'products_slider':products_slider,
        'products_latest':products_latest,
    }

    return render(request,'index.html',context)


def aboutus(request):
    #category = categoryTree(0,'',currentlang)
    setting = Setting.objects.get()
    category = Category.objects.all()

    
    context={
        'setting':setting,
        'category':category
    }
 
    return render(request, 'about.html',context)

def contactus(request):
    setting = Setting.objects.get()
    category = Category.objects.all()

    if request.method == 'POST': # check post
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage() #create relation with model
            data.name = form.cleaned_data['name'] # get form input data
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  #save data to table
            messages.success(request,"Your message has ben sent. Thank you for your message.")
            return HttpResponseRedirect('/contact')
    form = ContactForm
    context={
        'setting':setting,
        'form':form ,
        'category':category,
    }    
    return render(request, 'contactus.html',context)

def category_products(request,id,slug):
    
    category = Category.objects.all()
    products = Product.objects.filter(category_id=id) #default language
    
    context={'products': products,
             #'category':category,
             'category':category }
    return render(request,'category_products.html',context)



def search(request):
    if request.method == 'POST': # check post
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query'] # get form input data
            catid = form.cleaned_data['catid']
            if catid==0:
                products=Product.objects.filter(title__icontains=query)  #SELECT * FROM product WHERE title LIKE '%query%'
            else:
                products = Product.objects.filter(title__icontains=query,category_id=catid)

            category = Category.objects.all()
            context = {'products': products,
                        'query':query,
                       'category': category }
            return render(request, 'search_products.html', context)

    return HttpResponseRedirect('/')


def search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        products = Product.objects.filter(title__icontains=q)

        results = []
        for rs in products:
            product_json = {}
            product_json = rs.title +" > " + rs.category.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
