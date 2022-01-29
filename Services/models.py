from django.db import models
from django.db.models.fields import NullBooleanField
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
class Services(models.Model):
    Serv_Type = models.CharField(max_length=20)
    Serv_Name = models.CharField(max_length=50)
    Serv_Description = models.TextField()
    Serv_Applied_Date = models.DateTimeField(default=timezone.now)
    Serv_Applied_By = models.ForeignKey(User, on_delete=models.CASCADE)
    Serv_Req_Image = models.ImageField(default='default_image.png', upload_to='Serv_Comp_pics/')
    Serv_State = models.CharField(max_length=100, default=None)
    Serv_City = models.CharField(max_length=100, default=None)
    Serv_Location = models.CharField(default=None,max_length=300, null=True, blank=True)
    Serv_Approval_Status = models.CharField(max_length=20)
    Serv_Remarks = models.TextField(default=None,null=True, blank=True)
    Serv_Estimated_Completion_Date = models.DateField(default=None, null=True, blank=True)
    Serv_Completion_Status = models.CharField(max_length=20,null=True, blank=True)
    Serv_Comp_Image = models.ImageField(default='default_image.png', upload_to='Serv_Comp_pics/', blank=True)
    Serv_Doc_Name = models.CharField(max_length=100, null=True)
    Serv_Doc_Proof = models.FileField(upload_to='Files/')

    def __str__(self):
        return self.Serv_Type + ' ' +self.Serv_Name 


class Certificates(models.Model):
    Cert_Type = models.CharField(max_length=50)
    Cand_Name = models.CharField(max_length=50)
    Father_Name = models.CharField(max_length=50)
    Mother_Name = models.CharField(max_length=50)
    Address = models.CharField(max_length=300)
    govt_id = models.CharField(max_length=30)
    govt_proof_document = models.FileField(upload_to='Files/')
    Birth_Date = models.DateField()
    Birth_location = models.CharField(max_length=200, default=None, null=True, blank=True)
    Death_Date = models.DateField(default=None, null=True, blank=True)
    Death_location = models.CharField(max_length=200, default=None, null=True, blank=True)
    Cast = models.CharField(max_length=50, default=None, null=True, blank=True)
    Cast_Category = models.CharField(max_length=10, default=None, null=True, blank=True)
    Income_Value = models.CharField(max_length=20, default=None, null=True, blank=True)
    document_proof = models.FileField(upload_to='Files/', default=None, null=True, blank=True)
    Remarks = models.TextField()
    Approval_Status = models.CharField(max_length=20)

    def __str__(self) -> str:
        return super().__str__()
