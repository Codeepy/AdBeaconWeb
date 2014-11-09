import braintree
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
from publish.models import Advertisement, BeaconDevice, CompanyDetail
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

    if request.method == "POST":
        adv = AdvForm(request.POST, request.FILES)
        if adv.is_valid():
            adv.save()
            return HttpResponseRedirect('/payment/')
        else:
            return render(request, 'advertisement.html', {'form': adv, 'error': 'true'})
    else:
        adv = AdvForm()
        images = Advertisement.objects.all()
        beacons = BeaconDevice.objects.all()
        company = CompanyDetail.objects.get(email__iexact=request.user.email)
        return render(request, 'advertisement.html', {'form': adv, 'images': images, 'beacons': beacons, 'company': company})

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
        company = request.POST['company']
        address = request.POST['address']
        phone = request.POST['phone']
        if username != "" and email != "" and password1 != "":
            if password1 == password2:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                comp = CompanyDetail.create(name=company, address=address, email=email, phone=phone)
                comp.save()
                return HttpResponseRedirect('/')
            else:
                return render(request, "register.html", {"error": "Password is not matched!", "style": "display: block"})
        else:
            return render(request, "register.html", {"error": "Username, Email, and Password cannot be blank!", "style": "display: block"})

    return render(request, "register.html", {"style": "display: none"})

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

            return render(request, "result.html", {"status": "Payment successful", "detail": ""})
        else:
            return render(request, "result.html", {"status": result.errors.deep_errors, "detail": ""})
