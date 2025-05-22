from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product
import json

def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/products.html', {'products': products})

# def cart_view(request):
#     cart = request.session.get('cart', [])
#     cart_items = Product.objects.filter(id__in=cart)
#     return render(request, 'shop/cart.html', {'cart': cart_items})
# def cart_view(request):
#     # Sessiondagi noto‘g‘ri formatdagi cartni tozalab tashlaymiz
#     if isinstance(request.session.get('cart'), list):
#         del request.session['cart']

#     cart = request.session.get('cart', {})
#     cart_items = []

#     for product_id, quantity in cart.items():
#         try:
#             product = Product.objects.get(id=product_id)
#             product.quantity = quantity
#             cart_items.append(product)
#         except Product.DoesNotExist:
#             pass

#     return render(request, 'shop/cart.html', {'cart': cart_items})
# bu ihslaydi
# def cart_view(request):
#     cart = request.session.get('cart', {})
#     cart_items = []

#     for product_id, quantity in cart.items():
#         product = get_object_or_404(Product, id=product_id)
#         cart_items.append({
#             'id': product.id,
#             'name': product.name,
#             'description': product.description,
#             'price': product.price,
#             'image': product.image.url,
#             'quantity': quantity,
#         })

#     return render(request, 'shop/cart.html', {'cart': cart_items})

def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []

    for product_id, item in cart.items():
        cart_items.append({
            'id': product_id,
            'name': item['name'],
            'description': item['description'],
            'price': item['price'],
            'image': item['image'],
            'quantity': item['quantity'],
        })

    return render(request, 'shop/cart.html', {'cart': cart_items})


# @csrf_exempt
# def add_to_cart(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         product_id = data.get('product_id')
#         cart = request.session.get('cart', [])
#         if product_id not in cart:
#             cart.append(product_id)
#             request.session['cart'] = cart
#         return JsonResponse({'cart_size': len(cart)})
#     return JsonResponse({'error': 'Invalid request'}, status=400)
# @csrf_exempt
# def add_to_cart(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         product_id = str(data.get('product_id'))
#         cart = request.session.get('cart', {})

#         if product_id in cart:
#             cart[product_id] += 1
#         else:
#             cart[product_id] = 1

#         request.session['cart'] = cart
#         return JsonResponse({'message': 'Product added to cart'})
@csrf_exempt  # agar fetch uchun csrf token ishlatilmagan bo‘lsa
def add_to_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        product = Product.objects.get(id=product_id)

        cart = request.session.get('cart', {})

        if str(product_id) in cart:
            cart[str(product_id)]['quantity'] += 1
        else:
            cart[str(product_id)] = {
                'name': product.name,
                'description': product.description,
                'price': float(product.price),
                'image': product.image.url,
                'quantity': 1
            }

        request.session['cart'] = cart
        return JsonResponse({'message': f"{product.name} added to cart!"})
    return JsonResponse({'message': 'Invalid request'}, status=400)





# @csrf_exempt
# def remove_from_cart(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         product_id = data.get('product_id')
#         cart = request.session.get('cart', [])
#         if product_id in cart:
#             cart.remove(product_id)
#             request.session['cart'] = cart
#         return JsonResponse({'cart_size': len(cart)})
#     return JsonResponse({'error': 'Invalid request'}, status=400)
# @csrf_exempt
# def remove_from_cart(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         product_id = str(data.get('product_id'))
#         cart = request.session.get('cart', {})

#         if product_id in cart:
#             del cart[product_id]
#             request.session['cart'] = cart

#         return JsonResponse({'message': 'Product removed from cart'})
@csrf_exempt
def remove_from_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = str(data.get('product_id'))

        cart = request.session.get('cart', {})
        if product_id in cart:
            del cart[product_id]
            request.session['cart'] = cart
            return JsonResponse({'message': 'Item removed from cart'})

        return JsonResponse({'message': 'Item not found in cart'}, status=404)

# ---------------- ADMIN PANEL VIEWS ----------------

def admin_panel(request):
    products = Product.objects.all()
    return render(request, 'shop/admin.html', {'products': products})

def add_product(request):
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        quantity = request.POST['quantity']
        image = request.FILES.get('image')
        Product.objects.create(name=name, price=price, quantity=quantity, image=image)
        return redirect('admin_panel')
    return render(request, 'shop/add_product.html')

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.name = request.POST['name']
        product.price = request.POST['price']
        product.quantity = request.POST['quantity']
        if request.FILES.get('image'):
            product.image = request.FILES['image']
        product.save()
        return redirect('admin_panel')
    return render(request, 'shop/edit_product.html', {'product': product})

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('admin_panel')
