import json
from .models import *

def cookieCart(request):
    #We ue try catch becoz if there is no cart or cart is deleted, we don't wana get error.
    try:
        cart = json.loads(request.COOKIES['cart'])  #seek car from th browser's apllication.
    except:
        cart = {}

    print('Cart:', cart)
    items = []  #user not logged in case total and cart item 0
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping':False }
    cartItems = order['get_cart_items']  


#LOGIC FOR STORING CART NUMBER IN CART BUTTON.
    for i in cart:
        try:  # we did this becoz if we logged in and adda item then logour and reload the page #it's ggonna appear in cart.. and again if we log in and delet the product then reload its gonna generate error so we did this           
            cartItems += cart[i]["quantity"]  #give the quantity at the iteration
               
            product = Product.objects.get(id=i)  #for  each no of product  get total
            total = (product.price * cart[i]["quantity"])

            order['get_cart_total'] += total  #displaying total value in Cart
            order['get_cart_items'] += cart[i]["quantity"] #displaying Item value in Cart

            item = {             #WE are creating item dicitonary in order to render them in Cart page.
                'product' :{
                'id':product.id,
                'name':product.name,
                'price':product.price,
                'imageURL':product.imageURL,                   
                },
              'quantity': cart[i]["quantity"],
              'digital' :product.digital,
              'get_total': total
                   },

            items.append(item)   #appending item dicitonary 
 
            if product.digital == False:
                order['shipping']= True

        except:
            pass   
    return {'cartItems':cartItems, 'order':order, 'Items':items}

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items  #v.imp for displaying no of item in red circle of cart icon in eachpage.
    else:
        cookieData=cookieCart(request)       #for unauthencticate users.
        order = cookieData['order']
        items = cookieData['Items']
        cartItems = cookieData['cartItems']  #u can erase this.

    return{ 'cartItems':cartItems, 'items':items, 'order':order}

def guestOrder(request, data):

    print('User not logged in...')
    print('COOKIES:', request.COOKIES )
    name = data['form']['name']  
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(
            email=email,
            )
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False,
        )   
    for item in items:
        product = Product.objects.get(id=item['product']['id'])  
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']  #quantity is a attribute
            ) 
    return customer,order

    '''
OUTPUT-
[
    {
        'id':2,
        'product':{
            'id':2,
            'name':"Explosion1.mp4",
            'imageURL':'/videos/video.mp4',
        },
        'quantity': 2,
        'digital': False,
        'get_total':29    

    },

    {
        'id':3,
        'product':{
            'id':3,
            'name':"Explosion4.mp4",
            'imageURL':'/videos/video2.mp4',
        },
        'quantity': 5,
        'digital': False,
        'get_total':30    

    },
]  
'''   