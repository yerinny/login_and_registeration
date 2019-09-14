from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from apps.my_app.models import *
import bcrypt
# Create your views here.
def index(request):
   
    return render(request, "index.html")

def register(request):
    #validations
    error = False
    if len(request.POST['f_name']) < 2:
        error = True        
        messages.error(request,"First Name must be greater than 3")

    if len(request.POST['l_name']) < 2:
        error = True
        messages.error(request,"Last Name must be greater than 3")

    if not request.POST['f_name'].isalpha():
        error = True
        messages.error(request,"first name cannot contain number or character")

    if not request.POST['l_name'].isalpha():
        error = True
        messages.error(request,"last name cannot contain number or character")

    if len(request.POST['email']) < 2:
        error = True
        messages.error(request,"Email must be greater than 3")
        
    if len(request.POST['password']) < 8:
        error = True
        messages.error(request,"Password must be greater than 8")

    if request.POST['password'] != request.POST['c_password']:
        error = True
        messages.error(request,"Passwords must match")
    
    if len(User.objects.filter(email = request.POST['email'])) > 0:
        error = True
        messages.error(request, "User already exits")

    # Email should be a valid email
    # if not EMAIL_REGEX.match(request.POST['email']):
    #     print("invalid email address")
    if error:
        messages.error(request, "there is error")
        return redirect('/')
    #if bad, redirect('/')
    #if good, encrypt password
    hashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    decoded_hash = hashed.decode('utf-8')
    #decode
    user = User.objects.create(first_name = request.POST['f_name'], last_name = request.POST['l_name'], email = request.POST['email'], password = decoded_hash)
    print(request.POST)
    #store in db
    #store something in session
    request.session['u_id'] = user.id
    #redirect ('/') or where appropriate

    return redirect ('/')

def login(request):
    user_list = User.objects.filter(email = request.POST['email'])

    if not user_list:
        messages.error(request, "Invalid credentials")
        return redirect('/')

    user = user_list[0]
    if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        request.session['u_id'] = user.id

        return redirect('/main') #return redirect to ('/main')
    else:
        messages.error(request, "incorrect password")
    return redirect('/')


def main(request):

    if 'u_id' not in request.session:
        messages.error(request, 'You need to log in to view that page')
        return redirect('/')
    
    else:
        return render(request,'main.html')
