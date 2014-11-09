import braintree
import sendgrid
from sendgrid import SendGridError, SendGridClientError, SendGridServerError
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

braintree.Configuration.configure(braintree.Environment.Sandbox,
                                  merchant_id="4nvngnk2nqdy9pvk",
                                  public_key="jzzbz76c9r7nnjzj",
                                  private_key="ce7fe085f1c98cced6e187122eea64b0")

from datetime import datetime
from django.shortcuts import render, render_to_response
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from publish.serializers import AdvtSerializer, DevSerializer
from publish.models import Advertisement, BeaconDevice
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.renderers import JSONRenderer
from publish.forms import AdvForm
from django.core.urlresolvers import reverse

def index(request):
    return render(request, "register.html")

class AdvtViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Advertisement.objects.all()
    serializer_class = AdvtSerializer


class BeaconViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = BeaconDevice.objects.all()
    serializer_class = DevSerializer

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

def adv_detail_by_loc_id(request, param):
    if request.method == 'GET':
        present = datetime.now()
        ads = Advertisement.objects.filter(beacon__uuid__iexact=param, from_date__lte = present, to_date__gte = present)
        serializer = AdvtSerializer(ads, many=True)
        return JSONResponse(serializer.data)

@login_required(login_url='/login/')
def advertisement(request):

    if request.method=="POST":
        adv = AdvForm(request.POST, request.FILES)
        if adv.is_valid():
            print "Hi1"
            adv.save()
            #send_payment_confirmation_email()
            return render(request, 'payment.html')
        else:
            return render(request, 'advertisement.html', {'form': adv, 'error': 'true'})
    else:
        print "Hi3"
        adv = AdvForm()
        images = Advertisement.objects.all()
        beacons = BeaconDevice.objects.all()
        return render(request, 'advertisement.html', {'form': adv, 'images': images, 'beacons': beacons})

def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
    return render_to_response('login.html', context_instance=RequestContext(request))

@login_required(login_url='/login/')
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')

def register_user(request):
    from django.contrib.auth.models import User

    if request.POST:
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            print 'Registration successful'
            return HttpResponseRedirect('/')
        else:
            print 'Password is not matched!'

    return render(request, "register.html")

@login_required(login_url='/login/')
def account(request, id):
    return render(request, "account.html")

@login_required(login_url='/login/')
def payment(request):
    return render(request, "payment.html", {"client_token": braintree.ClientToken.generate()})

@login_required(login_url='/login/')
def checkout(request):
    client_token = braintree.ClientToken.generate()
    return client_token

@login_required(login_url='/login/')
def create_purchase(request):
    if request.method == 'POST':
        nonce = request.POST["payment_method_nonce"]
        result = braintree.Transaction.sale({
            "amount": "10.00",
            "payment_method_nonce": nonce,
            "options": {
                "submit_for_settlement": True
            }
        })

        if result.is_success:
            transaction = result.transaction
            if transaction.status == "processor_declined":
                return render(request, "result.html", {"status": transaction.status, "detail": result.transaction.processor_response_text})
            elif transaction.status == "settlement_declined":
                return render(request, "result.html", {"status": transaction.status, "detail": result.transaction.processor_settlement_response_text})
            elif transaction.status == "gateway_rejected":
                return render(request, "result.html", {"status": transaction.status, "detail": result.transaction.gateway_rejection_reason})

            return render(request, "result.html", {"status": transaction.status, "detail": ""})
        else:
            return render(request, "result.html", {"status": result.errors.deep_errors, "detail": ""})

def send_payment_confirmation_email(request):
    sg = sendgrid.SendGridClient('abdushHussein', 'hackath0n', raise_errors=True)
    message = sendgrid.Mail()
    message.add_to('abdush4ever@hotmail.com')
    message.set_subject('Payment Confirmation')
    message.set_html('Body')
    message.set_text('Body')
    #message.set_html('font-family: verdana, tahoma, sans-serif; color: #fff;"> <tr> <td> <h2>Hi!</h2> <p>This is to confirm that your payment was completed successfully.</p>')
    #message.set_text('Hi! This is to confirm that your payment was completed successfully.')
    message.set_from('')
    try:
        status, msg = sg.send(message)
        print status, msg
        return
    except SendGridClientError:
        print 'client error'
        return
    except SendGridServerError:
        print 'server error'
        return
