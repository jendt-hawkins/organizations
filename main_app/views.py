from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt
from django.db.models import Count

def form(request):
    return render(request, 'login.html')

def homepage(request): 
    context = {
        "user": User.objects.get(id=request.session['user_id']),
        "member_count": Organization.objects.annotate(num_views=Count('joined_by')).order_by('-num_views'),
    }
    return render(request, 'homepage.html', context)

def registered(request):

    errors = User.objects.basic_validator(request.POST)

    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")

    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash)

        request.session['user_id'] = user.id

        return redirect("/homepage")

def logout(request):
    request.session.flush()
    return redirect('/')

def login(request):

    email = request.POST['email']
    password = request.POST['password']
    user = User.objects.filter(email=email)

    if len(user) == 0:
        messages.error(request,"User not recognized")
        return redirect('/')
    else:
        if ( bcrypt.checkpw(password.encode(), user[0].password.encode()) ):
            request.session['user_id'] = user[0].id
            return redirect('/homepage')
        else:
            messages.error(request,'Invalid password.')
            return redirect('/')


def add_org(request):
    errors = Organization.objects.organization_validator(request.POST)

    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/homepage')
    
    else:
        user = User.objects.get(id=request.session['user_id'])
        new_org = Organization.objects.create(
                name=request.POST['name'], 
                description = request.POST['description'],
                uploaded_by = user,
            )
        request.session['org_id'] = new_org.id
        new_org.save()
        user.joined_organizations.add(new_org)
        
        return redirect('/homepage')    

def org_info(request, org_id):
    context = {
        "user": User.objects.get(id=request.session['user_id']),
        "org": Organization.objects.get(id=org_id),
    }
    return render (request, 'org_info.html', context)

def delete_org(request, org_id):
    Organization.objects.get(id=org_id).delete()
    return redirect('/homepage')

def join_org(request, org_id):
    user=User.objects.get(id=request.session['user_id'])
    this_org = Organization.objects.get(id=org_id)
    user.joined_organizations.add(this_org)

    return redirect(f"/org/{org_id}")

def leave_org(request, org_id):
    user=User.objects.get(id=request.session['user_id'])
    this_org = Organization.objects.get(id=org_id)
    user.joined_organizations.remove(this_org)

    return redirect(f"/org/{org_id}")