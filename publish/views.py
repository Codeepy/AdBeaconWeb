import braintree

braintree.Configuration.configure(braintree.Environment.Sandbox,
                                  merchant_id="4nvngnk2nqdy9pvk",
                                  public_key="jzzbz76c9r7nnjzj",
                                  private_key="ce7fe085f1c98cced6e187122eea64b0")

from datetime import datetime
from django.shortcuts import render
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

def account(request, id):
    return render(request, "account.html")

def payment(request):
    return render(request, "payment.html", {"client_token": braintree.ClientToken.generate(), "msg": "lala"})

def checkout(request):
    client_token = braintree.ClientToken.generate()
    return client_token

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


def advertisement(request):
    return render(request, "advertisement.html")


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
        ads = Advertisement.objects.filter(beacon__uuid__iexact=param)
        serializer = AdvtSerializer(ads, many=True)
        return JSONResponse(serializer.data)

def makeAdvs(request):
    '''
    if request.method=="POST":
        adv = AdvForm(request.POST, request.FILES)
        if adv.is_valid():
            adv.save()
            return HttpResponseRedirect(reverse('imageupload'))
    else:
    '''
    adv=AdvForm()
    images=Advertisement.objects.all()
    return render(request,'publishAdvt.html',{'form':adv,'images':images})