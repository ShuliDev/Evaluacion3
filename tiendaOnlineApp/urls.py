from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('producto/<int:pk>/', views.producto_detalle, name='producto_detalle'),
    path('solicitar/<int:producto_id>/', views.pedido_solicitud, name='pedido_solicitud'),
    path('seguimiento/<str:token>/', views.pedido_seguimiento, name='pedido_seguimiento'),
]
