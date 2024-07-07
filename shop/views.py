from django.shortcuts import render, redirect
from shop.models import Category, Product, Cart, Favourite
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
from shop.form import CustomUserForm
from django.contrib.auth import authenticate,login,logout
import json

# Create your views here.
def home(request):
    products = Product.objects.filter(Trending=1)
    return render(request, 'shop/index.html',{'products': products})

def remove_fav(request,fid):
  item = Favourite.objects.get(id=fid)
  item.delete()
  return redirect("favviewpage")

def favviewpage(request):
    if request.user.is_authenticated:
        fav = Favourite.objects.filter( user = request.user)
        return render(request, 'shop/fav.html',{'fav': fav})
    else:
        return redirect('home')

def fav_page(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
    if request.user.is_authenticated:
      data=json.load(request)
      product_id=data['pid']
      product_status=Product.objects.get(id=product_id)
      if product_status:
         if Favourite.objects.filter(user=request.user.id,product_id=product_id):
          return JsonResponse({'status':'Product Already in Favourite'}, status=200)
         else:
          Favourite.objects.create(user=request.user,product_id=product_id)
          return JsonResponse({'status':'Product Added to Favourite'}, status=200)
    else:
      return JsonResponse({'status':'Login to Add Favourite'}, status=200)
   else:
    return JsonResponse({'status':'Invalid Access'}, status=200)

def remove_cart(request,cid):
  cartitem=Cart.objects.get(id=cid)
  cartitem.delete()
  return redirect("/cart")

def cart_page(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter( user = request.user)
        return render(request, 'shop/cart.html',{'cart': cart})
    else:
        return redirect('home')


def add_to_cart(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            try:
                data = json.load(request)
                product_qty = (data['product_qty'])
                product_id = (data['pid'])
                # print(request.user.id)
                product_status = Product.objects.get(id = product_id )
                if product_status:
                    if Cart.objects.filter(user= request.user,product_id = product_id):
                        return JsonResponse({'status': 'Product Already in cart'}, status=200)
                    else:
                        if product_status.quantity>=product_qty:
                            Cart.objects.create(user= request.user,product_id = product_id, product_qty = product_qty)
                            return JsonResponse({'status': 'Product Added to Cart successfully'}, status=200)
                        else:
                            return JsonResponse({'status': 'Product Stock out of Market'}, status=200)

               
            except json.JSONDecodeError:
                return JsonResponse({'status': 'Invalid JSON data'}, status=400)
        else:
            return JsonResponse({'status': 'Log in to Add Cart'}, status=200)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=200)



def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged Out Successfully")
    return redirect('home')


def login_page(request):
  if request.user.is_authenticated:
    return redirect('home')
  else:
    if request.method=='POST':
      name=request.POST.get('username')
      pwd=request.POST.get('password')
      user=authenticate(request,username=name,password=pwd)
      if user is not None:
        login(request,user)
        messages.success(request,"Logged in Successfully")
        return redirect("/")
      else:
        messages.error(request,"Invalid User Name or Password")
        return redirect("/login")
    return render(request,"shop/login.html")

      
def register(request):
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration Success, You can Login Now...!😃")
            return redirect('login')

    return render(request, 'shop/register.html', {'form':form})

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

