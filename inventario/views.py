from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Producto, Proveedor
from .forms import ProductoForm, ProveedorForm


def lista_productos(request):
    # RF03: los productos deshabilitados no aparecen en la vista principal
    qs = Producto.objects.select_related('categoria', 'proveedor_principal') \
        .filter(estado='activo').order_by('nombre')
    paginator = Paginator(qs, 10)  # 10 productos por página
    productos = paginator.get_page(request.GET.get('page'))
    return render(request, 'inventario/productos_lista.html', {'productos': productos})


def crear_producto(request):
    if request.method == 'POST':  # el usuario envió el formulario
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventario:productos_lista')
    else:  # GET: mostrar el formulario vacío
        form = ProductoForm()
    return render(request, 'inventario/productos_formulario.html',
                  {'form': form, 'titulo': 'Nuevo producto'})


def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('inventario:productos_lista')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'inventario/productos_formulario.html',
                  {'form': form, 'titulo': f'Editar producto {producto.sku}'})


def deshabilitar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':  # llega solo si el usuario pulsó "Aceptar"
        producto.estado = 'inactivo'
        producto.save()
        return redirect('inventario:productos_lista')


def lista_proveedores(request):
    # RF05: los proveedores deshabilitados no aparecen en la vista principal
    qs = Proveedor.objects.filter(estado='activo').order_by('nombre_comercial')
    paginator = Paginator(qs, 10)  # 10 proveedores por página
    proveedores = paginator.get_page(request.GET.get('page'))
    return render(request, 'inventario/proveedores_lista.html', {'proveedores': proveedores})


def crear_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventario:proveedores_lista')
    else:
        form = ProveedorForm()
    return render(request, 'inventario/proveedores_formulario.html',
                  {'form': form, 'titulo': 'Nuevo proveedor'})


def editar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect('inventario:proveedores_lista')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'inventario/proveedores_formulario.html',
                  {'form': form, 'titulo': f'Editar proveedor {proveedor.nombre_comercial}'})


def deshabilitar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        proveedor.estado = 'inactivo'
        proveedor.save()
        return redirect('inventario:proveedores_lista')
