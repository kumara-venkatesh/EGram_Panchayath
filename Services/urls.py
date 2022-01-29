from django.contrib import admin
from django.urls import path
from . import views
from .views import MyRequests, ServiceDetailView, ReceivedRequests

admin.site.site_header = 'E-Gram Panchayath - Administration'
admin.site.index_title = 'E-Gram Panchayath Admin'

urlpatterns = [
    path('', views.Home, name= 'Home'),
    path('ServiceRequest/', views.ServiceRequest, name= 'ServiceReq'),
    path('services/<int:pk>/', ServiceDetailView.as_view(), name='service-detail'),
    path('ServiceComplaint/', views.ServiceComplaint, name= 'ComplaintReq'),
    path('CertificateRequest/', views.CertificateRequest, name= 'CertificateReq'),
    path('MyRequests/', MyRequests.as_view(), name='MyRequests'),
    path('About_Us/', views.About, name='AboutUs'), 
    path('Received_Requests/', ReceivedRequests.as_view(), name='ReqReceived'),
    path('process_request/<int:pk>/', views.ProcessRequest.as_view(), name='ProcessRequestURL'), 
]
