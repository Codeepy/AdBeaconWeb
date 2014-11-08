__author__ = 'Abdu'
from django import forms
from publish.models import CompanyDetail, BeaconDevice, Advertisement

class AdvForm(forms.Form):
    class Meta:
        model = Advertisement
        fields = ['company', 'category',  'pic', 'from_date', 'to_date', 'beacon']
    '''
    company = forms.ForeignKey(CompanyDetail)
    category = forms.CharField(max_length=30)
    pic = forms.FileField(upload_to="advs_images/")
    upload_date = forms.DateField(auto_now_add=True)
    from_date = forms.DateField()
    to_date = forms.DateField()
    beacon = forms.ManyToManyField(BeaconDevice)
'''
