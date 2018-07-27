from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.forms import UserCreationForm


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('learning_logs:index'))


# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(data = request.POST)
#         if form.is_valid():
#             new_user = form.save()
#             user = authenticate(username = new_user.username,
#             password = request.POST['password1'])
#             login(request,user)
#             return HttpResponseRedirect(reverse('learning_logs:index'))

#     else:
#         form = UserCreationForm()
    
#     context = {'form':form,}
#     return render(request,'users/register.html',context)


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username, password = password)
            login(request, user)
            return redirect('/')
    else:
            form = UserCreationForm()
            
    return render(request,'registration/signup.html',{'form':form})