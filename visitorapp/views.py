from django.shortcuts import render,HttpResponse,get_object_or_404
from django.contrib import admin,auth
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash,login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.dispatch import receiver
from django.contrib.auth import login,authenticate
from .models import *
from django.core.mail import send_mail,EmailMessage
from datetime import datetime
from config import *
from twilio.rest import Client
def home(request):
    if request.method=='POST':
        name=request.POST.get('id_name', None)
        email=request.POST.get('id_email', None)
        phone=request.POST.get('id_phone', None)
        host=request.POST.get('id_host', None)
        
        if not (name and email and phone and host):
            return HttpResponse('failed')

        host=str(host)
        if User.objects.filter(username=email).exists():
            user=User.objects.get(username=email)
            login(request,user)
            up=UserProfile.objects.get(user=user)
            up.phone=phone
            up.save()
            now=datetime.now()
            h=Host.objects.get(host_email=host)
            visit=Visit.objects.create(user=request.user,host_name=h.host_name,host_email=h.host_email,host_phone=h.host_phone,checkin=now,checkout=now)
            
            subject='Appointment'
            
            visit.checkin=now
            visit.checkout=now
            visit.save()
            dt=now.strftime("%d/%m/%Y %H:%M:%S")
            message='Customer '+name+' wants to meet you his details are: \n'+'name-'+name+'\nemail-'+email+'\ncheckin time-'+str(dt)
            temail=EmailMessage(subject,message,to=[h.host_email])
            temail.send()
            client=Client(account_sid,auth_token)
            try:
                mssg=client.messages.create(
                    from_='+12568278416',
                    body=message,
                    to=str(h.host_phone)
                    )
            except Exception as e:
                pass
            return redirect('/')
        else:
            user=User.objects.create_user(username=email,password=email,email=email)
            user.save()
            login(request,user)
            up=UserProfile.objects.get(user=user)
            up.phone=phone
            up.save()
            h=Host.objects.get(host_email=host)
            now=datetime.now()
            visit=Visit.objects.create(user=request.user,host_name=h.host_name,host_email=h.host_email,host_phone=h.host_phone,checkin=now,checkout=now)
            
            subject='Appointment'
            
            visit.checkin=now
            visit.checkout=now
            visit.save()
            dt= now.strftime("%d/%m/%Y %H:%M:%S")
            message='Customer '+name+' has wants to meet you his details are: \n'+'name-'+name+'\nemail-'+email+'\ncheckin time-'+str(dt)
            temail=EmailMessage(subject,message,to=[h.host_email])
            temail.send()
            client=Client(account_sid,auth_token)
            try:
                mssg=client.messages.create(
                    from_='+12568278416',
                    body=message,
                    to=str(h.host_phone)
                    )
            except Exception as e:
                pass
            return redirect('/')
        return HttpResponse('success')
    else:
        if request.user.is_authenticated:
            visit=Visit.objects.filter(user=request.user).order_by('-checkin')
            now=visit[0].checkin
            dt= now.strftime("%d/%m/%Y %H:%M:%S")
            args={'host_name':visit[0].host_name,'host_phone':visit[0].host_phone,'host_email':visit[0].host_email,'checkin':visit[0].checkin}
            return render(request,'visitorapp/checkout.html',args)
        hosts=Host.objects.all().order_by('host_name')
        args={'hosts':hosts}
    return render(request,'visitorapp/checkin.html',args)

def checkout(request):
    if request.user.is_authenticated == False:
        return redirect('/')
    user=request.user
    up=UserProfile.objects.get(user=request.user)
    visit=Visit.objects.filter(user=request.user).order_by('-checkin')
    hn=visit[0].host_name
    he=visit[0].host_email
    hp=visit[0].host_phone
    now=datetime.now()
    dt= now.strftime("%d/%m/%Y %H:%M:%S")
    subject="Feedback"
    message="You visited to Mr. "+hn +" at "+str(visit[0].checkin.strftime("%d/%m/%Y %H:%M:%S"))+"you checkout at "+str(dt)
    temail=EmailMessage(subject,message,to=[user.email])
    temail.send()
    v=visit[0].id
    v=Visit.objects.get(id=v)
    v.checkout=now
    v.save()
    auth.logout(request)
    return redirect('/')
