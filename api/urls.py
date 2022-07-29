from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('receipt', views.APIReceiptView.as_view(), name='receipt'),
    path('user/<str:user>/', views.UserProductsView.as_view(), name='user'),
    path('shop/<str:user>/', views.UserShopsView.as_view(), name='shop'),
    path('sum/<int:time_from>/<int:time_to>/', views.SumPerTimeView.as_view(), name='sum'),
    path('get/<int:time_from>/<int:time_to>/', views.ReceiptsPerTimeView.as_view(), name='get'),
]