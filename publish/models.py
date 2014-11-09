from django.db import models
#from enum import Enum

# Create your models here.
class BeaconDevice(models.Model):
    uuid = models.CharField(max_length=30, primary_key=True)
    location = models.CharField(max_length=250)
    postcode = models.CharField(max_length=10)
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)

    def __unicode__(self):
        return self.uuid

class CompanyDetail(models.Model):
    company_name = models.CharField(max_length=50, primary_key=True)
    address = models.CharField(max_length=250)
    email = models.EmailField()
    mobile = models.IntegerField()

    def __unicode__(self):
        return self.company_name

    @classmethod
    def create(cls, name, address, email, phone):
        company = cls(company_name=name, address=address, email=email, mobile=phone)
        # do something with the book
        return company

class Advertisement(models.Model):
    company = models.ForeignKey(CompanyDetail)
    category = models.CharField(max_length=30)
    pic = models.FileField(upload_to="advs_images/")
    upload_date = models.DateField(auto_now_add=True)
    from_date = models.DateField()
    to_date = models.DateField()
    beacon = models.ManyToManyField(BeaconDevice)

    def __unicode__(self):
        return self.pic.url



