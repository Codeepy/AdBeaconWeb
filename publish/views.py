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
    return render(request, "payment.html")

def checkout(request):
    import braintree

    braintree.Configuration.configure(
        braintree.Environment.Sandbox,
        '4nvngnk2nqdy9pvk',
        'jzzbz76c9r7nnjzj',
        'ce7fe085f1c98cced6e187122eea64b0'
    )

    client_token = braintree.ClientToken.generate()
    return client_token

def create_purchase(request):
    if request.method == 'POST':
        nonce = request.form["payment_method_nonce"]
        result = braintree.Transaction.sale({
            "amount": "10.00",
            "payment_method_nonce": nonce
        })
        return result



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