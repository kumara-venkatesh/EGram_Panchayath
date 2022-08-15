from django.http import request
from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Services, Certificates
from django.contrib import messages
import datetime
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
import csv, xlwt


# Create your views here.

def Home(request):
    return render(request, 'Services/Home.html')


def ServiceRequest(request):
    if request.method == 'POST':
        requested_by = request.user
        serv_name = request.POST.get('ReqName')
        serv_type = 'Service'
        doc_name = request.POST.get('DocName')
        state = request.POST.get('state_name')
        city = request.POST.get('city_name')
        location = request.POST.get('Location')
        applied_date = datetime.datetime.now()
        desc = request.POST.get('ReqDesc')

        if request.FILES.__contains__('file'):
            doc_proof = request.FILES['file']
            fs = FileSystemStorage()
            fs.save(doc_proof.name, doc_proof)
        

        if location:
            service_data = Services.objects.filter(Serv_State=state, Serv_City=city, Serv_Type=serv_type,
                                                   Serv_Name=serv_name, Serv_Applied_By=requested_by,
                                                   Serv_Location=location)
        else:
            service_data = Services.objects.filter(Serv_State=state, Serv_City=city, Serv_Type=serv_type,
                                                   Serv_Name=serv_name)
        if service_data.exists():
            messages.warning(request, f'Request Already Raised, please find the Request Details here')
        else:
            if location:
                serv_details = Services.objects.create(Serv_Type=serv_type, Serv_Name=serv_name, Serv_State=state,
                                                       Serv_City=city, Serv_Applied_By=requested_by,
                                                       Serv_Location=location, Serv_Approval_Status='pending',
                                                       Serv_Completion_Status='NA', Serv_Applied_Date=applied_date,
                                                       Serv_Doc_Name=doc_name, Serv_Doc_Proof=doc_proof,
                                                       Serv_Description=desc)
                
            else:
                serv_details = Services.objects.create(Serv_Type=serv_type, Serv_Name=serv_name, Serv_State=state,
                                                       Serv_City=city, Serv_Applied_By=requested_by,
                                                       Serv_Approval_Status='pending',
                                                       Serv_Completion_Status='NA', Serv_Applied_Date=applied_date,
                                                       Serv_Doc_Name=doc_name, Serv_Doc_Proof=doc_proof,
                                                       Serv_Description=desc)
            serv_details.save()
            messages.warning(request,'Service Request Submitted Successfully')


    return render(request, 'Services/Services.html')


def ServiceComplaint(request):
    if request.method == 'POST':
        requested_by = request.user
        serv_name = request.POST.get('ReqName')
        serv_type = 'Complaint'
        doc_name = request.POST.get('DocName')
        state = request.POST.get('state_name')
        city = request.POST.get('city_name')
        location = request.POST.get('Location')
        applied_date = datetime.datetime.now()
        desc = request.POST.get('ReqDesc')

        if request.FILES.__contains__('CImage'):
            Image = request.FILES['CImage']
            fs = FileSystemStorage()
            fs.save(Image.name, Image)
        
        if request.FILES.__contains__('doc_proof'):
            doc_proof = request.FILES['doc_proof']
            fs = FileSystemStorage()
            fs.save(doc_proof.name, doc_proof)

       
            service_data = Services.objects.filter(Serv_State=state, Serv_City=city, Serv_Type=serv_type,
                                                   Serv_Name=serv_name, Serv_Applied_By=requested_by,
                                                   Serv_Location=location)

        if service_data.exists():
            messages.warning(request, f'Request Already Raised, please find the Request Details here')
        else:
 
            serv_details = Services.objects.create(Serv_Type=serv_type, Serv_Name=serv_name, Serv_State=state,
                                                    Serv_City=city, Serv_Applied_By=requested_by,
                                                    Serv_Location=location, Serv_Approval_Status='pending',
                                                    Serv_Completion_Status='NA', Serv_Applied_Date=applied_date,
                                                    Serv_Doc_Name=doc_name, Serv_Doc_Proof=doc_proof,
                                                    Serv_Description=desc, Serv_Req_Image = Image)
                
          
            serv_details.save()
            messages.warning(request,'Service Request Submitted Successfully')
    return render(request, 'Services/Complaints.html')


def CertificateRequest(request):
    if request.method == 'POST':
        requested_by = request.user
        cert_name = request.POST.get('ReqName')
        cand_name = request.POST.get('fname') + ' ' + request.POST.get('lname')
        father_name = request.POST.get('father_name')
        mother_name = request.POST.get('mother_name')
        phone_no = request.POST.get('cnumber')
        complete_address = request.POST.get('Location')
        state_name = request.POST.get('state_name')
        city_name = request.POST.get('city_name')
        Comp_address = "State : {state}, City : {city}, Complete Address : {address}".format(state=state_name, city=city_name, address=complete_address)
        birth_date = request.POST.get('birthday')
        birth_place = request.POST.get('birthplace')
        death_date = request.POST.get('deathday')
        death_place = request.POST.get('deathplace')
        caste_name = request.POST.get('caste_name')
        caste_category = request.POST.get('caste_category')
        annual_income = request.POST.get('annualincome')
        doc_name = request.POST.get('DocName')
        applied_date = datetime.datetime.now()

        if request.FILES.__contains__('doc_proof'):
            doc_proof = request.FILES['doc_proof']
            fs = FileSystemStorage()
            fs.save(doc_proof.name, doc_proof)
        
        cert_details = Certificates.objects.create(Cert_Name=cert_name, Cand_Name=cand_name, Father_Name=father_name,
                                                   Mother_Name=mother_name, Address=Comp_address, doc_name=doc_name, 
                                                   Cert_Requested_By=requested_by, document_proof=doc_proof,
                                                   Birth_Date=birth_date, phoneno=phone_no, Birth_location=birth_place,
                                                   Death_Date=death_date, Death_location=death_place, 
                                                   Cast=caste_name, Cast_Category=caste_category, Income_Value=annual_income,
                                                   Remarks='', Approval_Status='pending', Completion_Status='NA',Cert_Applied_Date=applied_date)
        cert_details.save()
        messages.warning(request,'Certificate request applied successfully.')


    return render(request, 'Services/Certificates.html')

class My_Ser_Comp_Requests(ListView):
    model = Services
    template_name = "Services/MyServCompRequests.html"
    context_object_name = 'requests'
    paginate_by = 5

    def get_queryset(self):
        req = Services.objects.filter(Serv_Applied_By=self.request.user).order_by('-Serv_Applied_Date')

        def ExecQuery(req, Serv):
            key = list(Serv.keys())[0]
            if key=='Serv_Type':
                req = req.filter(Serv_Type=Serv[key]).order_by('-Serv_Applied_Date')
            if key=='Serv_Approval_Status':
                req = req.filter(Serv_Approval_Status=Serv[key]).order_by('-Serv_Applied_Date')
            if key=='Serv_Completion_Status':
                req = req.filter(Serv_Completion_Status=Serv[key]).order_by('-Serv_Applied_Date')
            return req

        if self.request.GET.get('idServType'):
            req = ExecQuery(req, {'Serv_Type':self.request.GET.get('idServType')})

        if self.request.GET.get('idAppStatus'):
            req = ExecQuery(req, {'Serv_Approval_Status':self.request.GET.get('idAppStatus')})
        
        if self.request.GET.get('idCompStatus'):
            req = ExecQuery(req, {'Serv_Completion_Status':self.request.GET.get('idCompStatus')})

        return req

class My_Cert_Requests(ListView):
    model = Certificates
    template_name = "Services/MyCertRequests.html"
    context_object_name = 'requests'
    paginate_by = 5

    def get_queryset(self):
        req = Certificates.objects.filter(Cert_Requested_By=self.request.user).order_by('-Cert_Applied_Date')

        def ExecQuery(req, Cert):
            key = list(Cert.keys())[0]
            if key=='Cert_Approval_Status':
                req = req.filter(Approval_Status=Cert[key]).order_by('-Cert_Applied_Date')
            if key=='Cert_Completion_Status':
                req = req.filter(Completion_Status=Cert[key]).order_by('-Cert_Applied_Date')
            return req

        if self.request.GET.get('idAppStatus'):
            req = ExecQuery(req, {'Cert_Approval_Status':self.request.GET.get('idAppStatus')})
        
        if self.request.GET.get('idCompStatus'):
            req = ExecQuery(req, {'Cert_Completion_Status':self.request.GET.get('idCompStatus')})

        return req

class CertificateDetailView(DetailView):
    model = Certificates
    template_name_suffix = '_details'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userinfo = self.request.user
        return context

class ServiceDetailView(DetailView):
    model = Services
    template_name_suffix = '_details'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userinfo = self.request.user
        return context

class ReceivedRequests(ListView):
    model = Services
    template_name = "Services/RequestsReceived.html"
    context_object_name = 'requests'
    paginate_by = 5
    
    def get_queryset(self):
        req = Services.objects.all()

        def ExecQuery(req, Serv):
            key = list(Serv.keys())[0]
            if key=='Serv_Type':
                req = req.filter(Serv_Type=Serv[key])
            if key=='Serv_Approval_Status':
                req = req.filter(Serv_Approval_Status=Serv[key])
            if key=='Serv_Completion_Status':
                req = req.filter(Serv_Completion_Status=Serv[key])
            return req

        if self.request.GET.get('idServType'):
            req = ExecQuery(req, {'Serv_Type':self.request.GET.get('idServType')})

        if self.request.GET.get('idAppStatus'):
            req = ExecQuery(req, {'Serv_Approval_Status':self.request.GET.get('idAppStatus')})
        
        if self.request.GET.get('idCompStatus'):
            req = ExecQuery(req, {'Serv_Completion_Status':self.request.GET.get('idCompStatus')})

        return req

class Cert_ReceivedRequests(ListView):
    model = Services
    template_name = "Services/CertificatesRequestsReceived.html"
    context_object_name = 'requests'
    paginate_by = 5
    
    def get_queryset(self):
        req = Certificates.objects.all()

        def ExecQuery(req, Cert):
            key = list(Cert.keys())[0]
            if key=='Cert_Approval_Status':
                req = req.filter(Approval_Status=Cert[key]).order_by('-Cert_Applied_Date')
            if key=='Cert_Completion_Status':
                req = req.filter(Completion_Status=Cert[key]).order_by('-Cert_Applied_Date')
            return req

        if self.request.GET.get('idAppStatus'):
            req = ExecQuery(req, {'Cert_Approval_Status':self.request.GET.get('idAppStatus')})
        
        if self.request.GET.get('idCompStatus'):
            req = ExecQuery(req, {'Cert_Completion_Status':self.request.GET.get('idCompStatus')})

        return req


class ProcessRequest(DetailView):
    model = Services
    template_name_suffix = '_process_request_details'
    def post(self, request, **kwargs):
        obj_id = request.POST.get('Object_id')
        
        #Approve/Reject Service/Complaint Requests
        value = request.POST.get('Approval_Submit')
        if value:
            current_process = Services.objects.get(id=obj_id)
            current_process.Serv_Remarks = request.POST.get('serv_remarks')
            if value == 'Approve':
                current_process.Serv_Approval_Status = "approved"
                current_process.Serv_Completion_Status = 'pending'
                messages.warning(request,"Request is Approved")
            if value == 'Reject':
                current_process.Serv_Approval_Status = "rejected"
                current_process.Serv_Completion_Status = 'rejected'
                messages.warning(request,"Request is rejected")
            current_process.save()
        submit_complete = request.POST.get('Completion_Submit')
        
        #Complete Service/Complaint Requests
        if submit_complete:
            current_process = Services.objects.get(id=obj_id)
            current_process.Serv_Remarks = request.POST.get('Completion_remarks')

            #Read Service Completion Image and store
            if request.FILES.__contains__('CImage'):
                CImage = request.FILES['CImage']
                fs = FileSystemStorage()
                fs.save(CImage.name, CImage)
            current_process.Serv_Comp_Image=CImage
            current_process.Serv_Completion_Status = 'completed'
            current_process.save()

            messages.warning(request,"Request Status is updated as Completed") 
        
        return redirect('ProcessRequestURL',pk=obj_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context

class ProcessCertRequest(DetailView):
    model = Certificates
    template_name_suffix = '_process_cert_request_details'
    def post(self, request, **kwargs):
        obj_id = request.POST.get('Object_id')
        value = request.POST.get('Approval_Submit')
        completion_value = request.POST.get('Completion_Submit')
        if value:
            current_process = Certificates.objects.get(id=obj_id)
            current_process.Remarks = request.POST.get('cert_remarks')
            if value == 'Approve':
                current_process.Approval_Status = 'approved'
                current_process.Completion_Status = 'pending'
                messages.warning(request,"Request is Approved")
            if value == 'Reject':
                current_process.Approval_Status = 'rejected'
                current_process.Completion_Status = 'rejected'
                messages.warning(request,"Request is rejected")
            current_process.save()
        if completion_value:
            messages.warning(request,obj_id)
            """current_process = Certificates.objects.get(id=obj_id)
            current_process.Remarks += request.POST.get('Comp_Remarks')
            current_process.Completion_Status = 'Completed'"""

            
        return redirect('ProcessCertRequestURL',pk=obj_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context

def About(request):
    return render(request, 'Services/about_us.html')

def export_service_requets_csv(request):
    respone = HttpResponse(content_type='text/csv')
    respone['Content-Disposition']='attachment; filename=Requests'+str(datetime.datetime.now())+'.csv'
    writer = csv.writer(respone)
    writer.writerow(['Request Type','Applied By','Applied For','Applied Date','Approval Status','Complete Status'])

    services = Services.objects.all()
    for element in services:
        writer.writerow([element.Serv_Type,element.Serv_Applied_By,element.Serv_Name,element.Serv_Applied_Date,element.Serv_Approval_Status,element.Serv_Completion_Status])

    return respone

def export_certificate_requets_csv(request):
    respone = HttpResponse(content_type='text/csv')
    respone['Content-Disposition']='attachment; filename=Requests'+str(datetime.datetime.now())+'.csv'
    writer = csv.writer(respone)
    writer.writerow(['Applied For','Applied By','Candidate Name','Applied Date','Approval Status','Complete Status'])

    certs = Certificates.objects.all()
    for element in certs:
        writer.writerow([element.Cert_Name,element.Cert_Requested_By,element.Cand_Name,element.Cert_Applied_Date,element.Approval_Status,element.Completion_Status])

    return respone

def view_certificate(request):
    context = {'certicate_name':'','name':'','body':'',}
    return render(request, 'Services/Certificate_template.html', context=context)