from django.shortcuts import render

def index(request):
    return render(request, "register.html")

def account(request, id):
    return render(request, "account.html")

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