from django.contrib import admin
from django.urls import path
from . import views
from .views import CertificateDetailView, My_Ser_Comp_Requests, ServiceDetailView, ReceivedRequests, My_Cert_Requests

admin.site.site_header = 'E-Gram Panchayath - Administration'
admin.site.index_title = 'E-Gram Panchayath Admin'

urlpatterns = [
    path('', views.Home, name= 'Home'),
    path('ServiceRequest/', views.ServiceRequest, name= 'ServiceReq'),
    path('services/<int:pk>/', ServiceDetailView.as_view(), name='service-detail'),
    path('certificates/<int:pk>/', CertificateDetailView.as_view(), name='certificate-detail'),
    path('ServiceComplaint/', views.ServiceComplaint, name= 'ComplaintReq'),
    path('CertificateRequest/', views.CertificateRequest, name= 'CertificateReq'),
    path('My_Ser_Comp_Requests/', My_Ser_Comp_Requests.as_view(), name='MySerCompRequests'),
    path('My_Cert_Requests/', My_Cert_Requests.as_view(), name='MyCertRequests'),
    path('About_Us/', views.About, name='AboutUs'), 
    path('Received_Requests/', ReceivedRequests.as_view(), name='ReqReceived'),
    path('process_request/<int:pk>/', views.ProcessRequest.as_view(), name='ProcessRequestURL'), 
]
