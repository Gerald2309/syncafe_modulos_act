from django import forms
from .models import Producto, Proveedor


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        # id_producto, fecha_creacion y fecha_actualizacion NO van: son automáticos
        fields = [
            'sku', 'nombre', 'descripcion', 'categoria', 'proveedor_principal',
            'unidad_medida', 'costo_compra', 'precio_venta',
            'stock_actual', 'stock_minimo', 'estado',
        ]
        widgets = {
            'sku': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'proveedor_principal': forms.Select(attrs={'class': 'form-select'}),
            'unidad_medida': forms.Select(attrs={'class': 'form-select'}),
            'costo_compra': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'precio_venta': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock_actual': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock_minimo': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'sku': 'SKU',
            'descripcion': 'Descripción',
            'proveedor_principal': 'Proveedor principal',
            'unidad_medida': 'Unidad de medida',
            'costo_compra': 'Costo de compra',
            'precio_venta': 'Precio de venta',
            'stock_actual': 'Stock actual',
            'stock_minimo': 'Stock mínimo',
        }

    def clean(self):
        cleaned = super().clean()
        costo_compra = cleaned.get('costo_compra')
        precio_venta = cleaned.get('precio_venta')
        # Regla de negocio: el precio de venta no puede ser menor al costo de compra
        if costo_compra is not None and precio_venta is not None and precio_venta < costo_compra:
            raise forms.ValidationError(
                'El precio de venta no puede ser menor al costo de compra.')
        return cleaned


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        # id_proveedor NO va: es automático
        fields = [
            'nombre_comercial', 'razon_social', 'nit', 'email',
            'telefono', 'direccion', 'ciudad', 'pais', 'estado',
        ]
        widgets = {
            'nombre_comercial': forms.TextInput(attrs={'class': 'form-control'}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control'}),
            'nit': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'pais': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'nombre_comercial': 'Nombre comercial',
            'razon_social': 'Razón social',
            'nit': 'NIT',
        }
