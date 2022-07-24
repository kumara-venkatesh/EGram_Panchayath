from django.contrib import admin
from django.urls import path
from . import views
from .views import CertificateDetailView, My_Ser_Comp_Requests, ServiceDetailView, ReceivedRequests, My_Cert_Requests, Cert_ReceivedRequests

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
    path('Certicates_Received_Requests/', Cert_ReceivedRequests.as_view(), name='CertReqReceived'),
    path('process_request/<int:pk>/', views.ProcessRequest.as_view(), name='ProcessRequestURL'),
    path('process_cert_request/<int:pk>/', views.ProcessCertRequest.as_view(), name='ProcessCertRequestURL'), 
    path('export_service_requests',views.export_service_requets_csv,name='export-service-requets-csv'),
    path('export_certificate_requests',views.export_certificate_requets_csv,name='export-certificate-requets-csv'),
    path('view_certificate/', views.view_certificate, name='view-certificate'), 
]
