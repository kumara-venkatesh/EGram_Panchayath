from django.http import request
from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Services, Certificates
from django.contrib import messages
import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import redirect


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
    return render(request, 'Services/Certificates.html')

class MyRequests(ListView):
    model = Services
    template_name = "Services/MyRequests.html"
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


class ServiceDetailView(DetailView):
    model = Services
    template_name_suffix = '_details'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userinfo = self.request.user
        #UserName = userinfo.first_name + ' ' + userinfo.last_name
        #applyjob = self.request.GET.get('applyjob')
        '''if self.request.method == "GET":

            if applyjob:
                postby = Post.objects.get(id=applyjob)
                email = postby.Creator
                check = JobApplication.objects.filter(AppliedFor=postby, AppliedBy=userinfo)
                if check.exists():
                    messages.warning(self.request, f'You have already applied for this job')
                else:
                    apply_job = JobApplication.objects.create(AppliedBy=userinfo, AppliedFor=postby)
                    apply_job.save()
                    messages.success(self.request, 'Job Applied Successfully')
                    msg_body = "You have received an Application for the Job Post {} from {}, \n Applicant Email : {}".format(postby, UserName, userinfo.email)
                    send_mail('Application Received', msg_body,
                              settings.EMAIL_HOST_USER, [email], fail_silently=False, )'''
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

class ProcessRequest(DetailView):
    model = Services
    template_name_suffix = '_process_request_details'
    def post(self, request, **kwargs):
        obj_id = request.POST.get('Object_id')
        value = request.POST.get('Approval_Submit')
        if value:
            current_process = Services.objects.get(id=obj_id)
            current_process.Serv_Approval_Status = value
            current_process.Serv_Remarks = request.POST.get('serv_remarks')
            if value == 'approved':
                current_process.Serv_Completion_Status = 'pending'
                messages.warning(request,"Request is rejected")
            if value == 'rejected':
                current_process.Serv_Completion_Status = 'rejected'
                messages.warning(request,"Request is rejected")
            current_process.save()
            
        return redirect('ProcessRequestURL',pk=obj_id)
        #return HttpResponseRedirect(self.request.path_info)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context
    

def About(request):
    return render(request, 'Services/about_us.html')