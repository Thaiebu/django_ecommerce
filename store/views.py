from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime

# Create your views here.

from .models import *
from .utils import cookiCart,cartData,guestOrder

def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        #get_or_create is used to get the data if not create it
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
        # print(items)
    else:
        try:
           cart = json.loads(request.COOKIES['cart'])
        except:
            cart={}
        items=[]
        order = {'get_cart_total':0,'get_cart_item':0,'shipping':False}
        cartItems = order['get_cart_item']
        for i in cart:
            cartItems += cart[i]['quantity']

    products = Product.objects.all()
    context = {
        "products":products,"cartItems":cartItems
    }

    return render(request,'store/store.html',context)

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = { "items":items, "order":order,"cartItems":cartItems }
    return render(request,'store/cart.html',context)

def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = { "items":items, "order":order,"cartItems":cartItems }
    return render(request,'store/checkout.html',context)

def update_item(request):
    data = json.loads(request.body)
    # print(data)
    productid = data['productId']
    action = data['action']
    # print(productid,action)
    customer = request.user.customer
    product = Product.objects.get(id=productid)
    order,created = Order.objects.get_or_create(customer=customer,complete=False)

    orderItem,created = OrderItem.objects.get_or_create(order=order,product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <=0:
        orderItem.delete()
    return JsonResponse("Item added",safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete = False)


    else:
        try:
            customer,order=guestOrder(request,data)
        except:
            pass
        # print("user not logged in")

        # print("COOKIES",request.COOKIES)
        # name = data['form']['name']
        # email = data['form']['email']

        # cookieData= cookiCart(request)
        # items =cookieData['items']
        # customer, created =Customer.objects.get_or_create(
        # email =email,
        # )
        # customer.name = name
        # customer.save()
        # order =Order.objects.create(
        #     customer= customer,
        #     complete=False)
        # for item in items:
        #     product= Product.objects.get(id=item['product']['id'])
        #     orderItem= OrderItem.objects.create(
        #         product=product,
        #         order=order,
        #         quantity = item['quantity'])
            
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()
    if order.shipping == True:
        ShippingAddress.objects.create(
                customer=customer,
                order = order,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode = data['shipping']['zipcode'],
        )



    return JsonResponse("payment submitted",safe=False)



