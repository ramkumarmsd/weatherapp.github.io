from django.shortcuts import render,redirect
from .form import cityform
from .models import city

from django.contrib import messages
import requests
# Create your views here.

def home(request):
        
    url='http://api.openweathermap.org/data/2.5/weather?q={},&appid=534e86e8f8ba05a64e85368128fd58cb&units=metric'
    
    if request.method =='POST':
        form=cityform(request.POST)
        if form.is_valid():
            ncity=form.cleaned_data['name']
            ccity=city.objects.filter(name=ncity).count()
            if ccity==0:

                res=requests.get(url.format(ncity)).json() 
                               
                if res['cod']== 200:
                    form.save()
                    messages.success(request,ncity+" Added succesfully.....!!!")
                else:
                    messages.error(request,"City does not exists...!!!")
            else:
                messages.success(request,"City already exists...!!")


    form=cityform()
    cities=city.objects.all()
    data = []    
    for City in cities:
        res=requests.get(url.format(City)).json() 
        city_weather = {
            'city': City,
            'temperature': res['main']['temp'],
            'description': res['weather'][0]['description'],
            'country':res['sys']['country'],
            'icon': res['weather'][0]['icon'],
        }
        data.append(city_weather)
    context={'data':data,'form':form}
    return render(request,'weather.html',context)

def deletedt(request,cname):    
    city.objects.get(name=cname).delete()
    return redirect('home')