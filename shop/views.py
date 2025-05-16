from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Cart, CartItem
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

def home(request):
    category_slug = request.GET.get('category')
    categories = Category.objects.all()

    if category_slug:
        products = Product.objects.filter(category__slug=category_slug, available=True)
        selected_category = category_slug
    else:
        products = Product.objects.filter(available=True)
        selected_category = None

    context = {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
    }
    return render(request, 'shop/home.html', context)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'shop/signup.html', {'form': form})

def product_list(request):
    category_id = request.GET.get('category')
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_id:
        products = products.filter(category_id=category_id)

    context = {
        'products': products,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None,
    }
    return render(request, 'shop/product_list.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    return render(request, 'shop/product_detail.html', {'product': product})

@login_required
@require_POST
def add_to_cart(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug, available=True)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_detail')

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('product').all()
    total_price = sum(item.get_total_price() for item in items)
    return render(request, 'shop/cart_detail.html', {'cart': cart, 'items': items, 'total_price': total_price})

@login_required
def remove_from_cart(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    cart, created = Cart.objects.get_or_create(user=request.user)
    CartItem.objects.filter(cart=cart, product=product).delete()
    return redirect('cart_detail')

@login_required
@require_POST
def update_cart_item(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    cart, created = Cart.objects.get_or_create(user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    cart_item = CartItem.objects.filter(cart=cart, product=product).first()
    if cart_item:
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('cart_detail')
