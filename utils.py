import random
import string

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.core.mail import send_mail,EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context


def generate_random_string(length):
    characters = string.ascii_uppercase + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

def reformatCart(data):
    id_list = []
    arrays = []
    arr = []
    c = 0
    for item in data:
        arr.append(data[item])
        if len(arr) == 2:
            arrays.append(arr)
            id_list.append(arr[0])
            arr = []
    return id_list, arrays

def getQuantity(id,quantity_array):
    for i in quantity_array:
        if int(i[0]) == id:
            return i[1]
    return 1

def getPriceDetails(items,quantity_array):
    subtotal = 0
    discount = 0
    print(quantity_array)
    for i in items:
        q = getQuantity(i["id"],quantity_array)
        print(q)
        subtotal += i["cutoff_price"]*int(q)
        discount += (i["cutoff_price"] - i["selling_price"])*int(q)
    return [
        {"label":"Subtotal","price":subtotal,"operation":""},
        {"label":"Discount","price":discount,"operation":"-"},
    ] , (subtotal - discount)

def send_email(subject,to_email_list,plaintext,htmly,d):
    try:
        from_email= 'support@indulgeindia.in'
        text_content = plaintext.render(d)
        html_content = htmly.render(d)
        msg = EmailMultiAlternatives(subject, text_content, from_email, to_email_list)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        print("Sent")
    except Exception as e:
        print(e)
