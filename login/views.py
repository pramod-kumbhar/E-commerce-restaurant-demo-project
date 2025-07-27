from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import Userdata

def login(request):
    if request.method == "POST":
        if request.POST['form_type'] == 'register':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            address = request.POST['address']
            username = request.POST['username']
            email = request.POST['email']
            phone = request.POST['phone']
            password = request.POST['password']
            
            if Userdata.objects.filter(username=username).exists():
                messages.error(request, "Username already taken!")
                return redirect('loginapp:login')
            if Userdata.objects.filter(email=email).exists():
                messages.error(request, "Email already registered!")
                return redirect('loginapp:login')
            
            hashed_password = make_password(password)
            user = Userdata(
                first_name=first_name,
                last_name=last_name,
                address=address,
                username=username,
                email=email,
                phone=phone,
                password=hashed_password
            )
            user.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect('loginapp:login')
        
        elif request.POST['form_type'] == 'login':
            username = request.POST['username']
            password = request.POST['password']

            try:
                user = Userdata.objects.get(username=username)
                
                if check_password(password, user.password):
                    request.session['user_id'] = user.id
                    request.session['username'] = user.username
                    messages.success(request, f"Welcome {user.username}!")
                    return redirect('hotelapp:home')
                else:
                    messages.error(request, "Invalid password.")
            
            except Userdata.DoesNotExist:
                messages.error(request, "User not found. Please register.")

    return render(request, "login/login.html")

def logout(request):
    request.session.flush()
    messages.success(request, "You have been logged out.")
    return redirect('loginapp:login')

def userinfo(request):
    try:
        user = get_object_or_404(Userdata, id=request.session.get("user_id"))

        if request.method == "POST":
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            phone = request.POST.get("phone")
            address = request.POST.get("address")
            old_password = request.POST.get("old_password")
            new_password = request.POST.get("new_password")

            if first_name and first_name != user.first_name:
                user.first_name = first_name
            if last_name and last_name != user.last_name:
                user.last_name = last_name

            if address and address != user.address:
                user.address = address
            if phone and phone != user.phone:
                user.phone = phone

            if old_password and new_password:
                if check_password(old_password, user.password):
                    if old_password != new_password:
                        user.password = make_password(new_password)
                        messages.success(request, "Password updated successfully!")
                    else:
                        messages.error(request, "New password cannot be the same as the old password.")
                        return redirect("login:userinfo")
                else:
                    messages.error(request, "Old password is incorrect.")
                    return redirect("login:userinfo")
                
            user.save()
            messages.success(request, "Your data has been updated successfully!")
            return redirect("hotelapp:home")

    except Exception as e:
        messages.error(request, f"Something went wrong : {str(e)}")
        return redirect("login:userinfo")
    return render(request, "login/user.html", {"user": user})
