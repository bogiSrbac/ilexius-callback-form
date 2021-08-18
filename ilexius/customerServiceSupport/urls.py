from django.urls import path
from . import views

app_name = 'customerServiceSupport'

urlpatterns = [
    path('', views.index, name='index'),
    path('customer-service-support/', views.createCustomerView, name='customer-create-form'),
    path('free-terms-check/', views.checkFreeTermsFunction, name='free-terms-check'),
    path('free-terms-ten-days/', views.tenDaysFunction, name='free-terms-ten-days'),
    path('customer-list/', views.CustomerCallbackList.as_view(), name='customer-list'),
    path('update-comment/<int:pk>/', views.getCustomerInformation, name='update-comment'),
    path('update-comment-new/<int:pk>/', views.updateComment, name='update-comment-new'),
    path('archive/', views.makeCallbacksRealized, name='archive'),
]