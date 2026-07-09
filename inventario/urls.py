from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('productos/', views.lista_productos, name='productos_lista'),
    path('productos/nuevo/', views.crear_producto, name='productos_crear'),
    path('productos/<int:pk>/editar/', views.editar_producto, name='productos_editar'),
    path('productos/<int:pk>/deshabilitar/', views.deshabilitar_producto, name='productos_deshabilitar'),

    path('proveedores/', views.lista_proveedores, name='proveedores_lista'),
    path('proveedores/nuevo/', views.crear_proveedor, name='proveedores_crear'),
    path('proveedores/<int:pk>/editar/', views.editar_proveedor, name='proveedores_editar'),
    path('proveedores/<int:pk>/deshabilitar/', views.deshabilitar_proveedor, name='proveedores_deshabilitar'),
]
