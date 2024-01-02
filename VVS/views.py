from django.shortcuts import render, redirect
from my_app.models import Category, Product
from django.contrib import messages

def index(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        'categories': categories,
        'products': products,
    }

    if request.method == "GET":
        filter_key = request.GET.get('filter')
        if filter_key and filter_key != "All":
            products = Product.objects.filter(category__name=filter_key)
            context['products'] = products
            context['filter'] = filter_key
            return render(request, 'index.html', context)
    return render(request, 'index.html', context)

def addItem(request):
    if request.method == "POST":
        try:
            name = request.POST.get('name')
            price = request.POST.get('price')
            category = request.POST.get('category')
            stock = request.POST.get('stock')
            category = Category.objects.get(name=category)
            #check the name if already exist, don't add the Item
            if Product.objects.filter(name=name).exists():
                messages.error(request, "Product already exist")
                return redirect('index')
            product = Product(name=name, price=price, category=category, stock=stock)
            product.save()
            messages.success(request, "Product added successfully")
        except:
            messages.error(request, "Error adding product")
        return redirect('index')

def updateItem(request):
    if request.method == "POST":
        try:
            name = request.POST.get('name')
            price = request.POST.get('price')
            stock = request.POST.get('stock')
            print(request.POST)
            print(name, price, stock)
            product = Product.objects.get(name=name)
            product.name = name
            product.price = price
            product.stock = stock
            
            product.save()
            messages.success(request, "Product updated successfully")
        except:
            import sys
            print(sys.exc_info()[0])
            messages.error(request, "Error updating product")
        return redirect('index')