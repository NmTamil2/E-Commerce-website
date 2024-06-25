from django.shortcuts import render, redirect
from shop.models import Category, Product
from django.contrib import messages
from django.http import HttpResponse

# Create your views here.
def home(request):
    product = Product.objects.filter(Trending=1)
    return render(request, 'shop/index.html',{'product': product})

def register(request):
    return render(request, 'shop/register.html')

def collections(request):
    category = Category.objects.filter(status=0)
    return render(request, 'shop/collections.html', {'category': category})

def collectionsview(request, name):
    if Category.objects.filter(name=name, status=0).exists():
        products = Product.objects.filter(category__name=name)  # Changed to lowercase
        return render(request, 'shop/products/index.html', {'products': products, "category_name":name})
    else:
        messages.warning(request, "No Such Category Found")
        return redirect('collections')

def product_details(request,cname,pname):
    if(Category.objects.filter(name=cname,status=0)):
        if(Product.objects.filter(name=pname,status=0)):
            product = Product.objects.filter(name=pname,status=0).first()
            return render(request,'shop/products/product_details.html',{'product':product})
        else:
            messages.warning(request, "No Such Product")
            return redirect ('collections')
    else:
        messages.warning(request, "No Such Category")
        return redirect ('collections')

