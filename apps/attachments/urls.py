from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'attachments'

urlpatterns = [   
    path('', views.FileAttachmentListView.as_view(), name='fileattachment_list'),
    path('<int:pk>/', views.FileAttachmentUpdateView.as_view(), name='fileattachment_update'),
    path('create/', views.FileAttachmentCreateView.as_view(), name='fileattachment_create'),
      
]