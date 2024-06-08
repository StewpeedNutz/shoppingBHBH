from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib import messages
from django.views import View
from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from .models.cart import Cart
import re
from django.db.models import Q


# ====================================== HOME ======================================
def home(request):
    products = None
    name = ''
    totalitem = 0

    if request.session.has_key('username_or_email'):
        username_or_email = request.session['username_or_email']
        if request.session.has_key('password'):
            password = request.session['password']

        category = Category.get_all_categories()

        # Check if the customer exists with the given email or username and password
        customer = Customer.objects.filter(
            (Q(email=username_or_email) | Q(username=username_or_email)) & Q(password=password)
        ).first()

        totalitem = len(Cart.objects.filter(username=username_or_email))

        if customer:
            username = customer.username

        categoryID = request.GET.get('category')
        if categoryID:
            products = Product.get_all_product_by_category_id(categoryID)

        else:
            products = Product.get_all_products()

        data = {}
        data['username'] = username
        data['product'] = products
        data['category'] = category
        data['totalitem'] = totalitem
        #print('You are', request.session.get('username_or_email'))
        return render(request,'home.html', data)

    else:
        return redirect('login')

# ====================================== SIGN UP ======================================
class Signup(View):
    def get(self,request):
        return render(request, 'signup.html')

    def post(self, request):
        postDATA = request.POST
        name = postDATA.get('name')
        username = postDATA.get('username')
        email = postDATA.get('email')
        phone = postDATA.get('phone')
        password = postDATA.get('password')
        # print(name,username,email,phone,pass)

        error_message = None

        value = {
            'username': username,
            'email': email,
            'phone': phone,
            'password': password
        }

        customer = Customer(name=name,
                            username=username,
                            email=email,
                            phone=phone,
                            password=password)

        if (not name):
            error_message = "Name is required"

        elif not username:
            error_message = "Username is required"

        elif len(username) > 20:
            error_message = "Password must not exceed 20 character long"

        elif customer.isExist():
            error_message = "Username is already exists!"

        elif not email:
            error_message = "Email is required"

        elif customer.isExist():
            error_message = "Email is already exists!"

        elif not phone:
            error_message = "Phone number is required"

        elif len(phone) < 10:
            error_message = "Phone number must at least 10 character long or more"

        elif customer.isExist():
            error_message = "Phone number is already exists!"

        elif not password:
            error_message = "Password is required"

        elif len(password) > 20:
            error_message = "Password must not exceed 20 character long"

        elif not re.search(r'[A-Z]', password):
            error_message = "Password must contain at least one uppercase letter"

        elif not re.search(r'[a-z]', password):
            error_message = "Password must contain at least one lowercase letter"

        elif not re.search(r'[0-9]', password):
            error_message = "Password must contain at least one digit"

        elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            error_message = "Password must contain at least one special character"

        if not error_message:
            messages.success(request, 'Congratulation!! Registration Successfull')

            customer.register()
            return redirect('signup')
        else:
            data = {
                'error': error_message,
                'value': value
            }
            return render(request, 'signup.html', data)

# ====================================== LOGIN ======================================
class Login(View):
    def get(self,request):
        return render(request, 'login.html')

    def post(self,request):
        postDATAA = request.POST
        username_or_email = postDATAA.get('username_or_email')
        password = postDATAA.get('password')
        # print(username,email,pass)
        error_message = None
        value = {
            'username_or_email': username_or_email,
            'password': password
        }
        # Check if the input is an email
        if '@' in username_or_email:
            customer = Customer.objects.filter(email=username_or_email).first()
        else:
            # Check if the input is a username
            customer = Customer.objects.filter(username=username_or_email).first()

        if customer:

            # Check if the password is correct
            if customer.password == password:
                # Redirect to the homepage upon successful login
                request.session['username_or_email'] = username_or_email
                request.session['password'] = password
                return redirect('homepage')
            else:
                error_message = "Invalid password!"
                data = {
                    'error': error_message,
                    'value': value
                }
        else:
            error_message = "Invalid username or email!"
            data = {
                'error': error_message,
                'value': value
            }

        # If login fails, render the login page with an error message
        return render(request, 'login.html', data)

# ====================================== PRODUCT DETAIL ======================================
def productdetail(request, pk):
    totalitem = 0
    name = ''
    product = Product.objects.get(pk=pk)
    item_already_in_cart = False

    if 'username_or_email' in request.session:
        username_or_email = request.session['username_or_email']
        totalitem = len(Cart.objects.filter(username=username_or_email))
        item_already_in_cart = Cart.objects.filter(product=product.id, username=username_or_email).exists()
        customer = Customer.objects.filter(Q(username=username_or_email) | Q(email=username_or_email)).first()
        if customer:
            name = customer.name

    data = {
        'product': product,
        'item_already_in_cart': item_already_in_cart,
        'name': name,
        'totalitem': totalitem
    }

    return render(request, 'productdetail.html', data)




# ====================================== LOGOUT ======================================
def logout(request):
    if request.session.has_key('username_or_email'):
        del request.session["username_or_email"]
        return redirect('login')
    if request.session.has_key('password'):
        del request.session["password"]
        return redirect('login')
    else:
        return redirect('login')

# ====================================== ADD TO CART ======================================
def add_to_cart(request):
    if 'username_or_email' in request.session:
        username_or_email = request.session['username_or_email']

        # Get the customer using username or email
        customer = Customer.objects.filter(Q(email=username_or_email) | Q(username=username_or_email)).first()

        if customer:
            username = customer.username
            product_id = request.GET.get('prod_id')

            try:
                product = Product.objects.get(id=product_id)
                Cart(username=username, product=product, image=product.image, price=product.price).save()
                messages.success(request, "Item added to cart!")
                return redirect(f"/product-detail/{product_id}")

            except Product.DoesNotExist:
                messages.error(request, "The product does not exist.")
                return redirect('homepage')
        else:
            messages.error(request, "User not found.")
            return redirect('login')
    else:
        messages.error(request, "You must be logged in to add items to the cart.")
        return redirect('login')

# ====================================== CART ======================================
def show_cart(request):
    totalitem = 0
    if 'username_or_email' in request.session:
        username_or_email = request.session['username_or_email']
        totalitem = len(Cart.objects.filter(username=username_or_email))

        customer = Customer.objects.filter(Q(username=username_or_email) | Q(email=username_or_email)).first()
        if customer:
            username = customer.username

            cart = Cart.objects.filter(username=username_or_email)
            data = {
                'username': username,
                'totalitem': totalitem,
                'cart': cart
            }
            if cart:
                return render(request, 'show_cart.html',data)
            else:
                pass


def plus_cart(request):
    if request.session.has_key('username_or_email'):
        username_or_email = request.session["username_or_email"]
        product_id = request.GET['prod_id']
        cart = Cart.objects.get(Q(product=product_id) & Q(username=username_or_email))
        cart.quantity += 1
        cart.save()

        data = {
            'quantity': cart.quantity,  # Return the updated quantity
        }
        return JsonResponse(data)