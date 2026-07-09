from django.db import models


class Categoria(models.Model):
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('inactiva', 'Inactiva'),
    ]

    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=8, choices=ESTADO_CHOICES, default='activa')

    class Meta:
        managed = False
        db_table = 'categoria'

    def __str__(self):
        return self.nombre


class Proveedor(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]

    id_proveedor = models.AutoField(primary_key=True)
    nombre_comercial = models.CharField(max_length=150)
    razon_social = models.CharField(max_length=180, blank=True, null=True)
    nit = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=150, unique=True, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    pais = models.CharField(max_length=80, default='Colombia')
    estado = models.CharField(max_length=8, choices=ESTADO_CHOICES, default='activo')

    class Meta:
        managed = False
        db_table = 'proveedor'

    def __str__(self):
        return self.nombre_comercial


class Producto(models.Model):
    UNIDAD_MEDIDA_CHOICES = [
        ('unidad', 'Unidad'),
        ('kg', 'Kilogramo'),
        ('litro', 'Litro'),
        ('caja', 'Caja'),
        ('paquete', 'Paquete'),
    ]
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]

    id_producto = models.AutoField(primary_key=True)
    sku = models.CharField(max_length=40, unique=True)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    categoria = models.ForeignKey(
        Categoria, on_delete=models.PROTECT, db_column='id_categoria',
        related_name='productos')
    proveedor_principal = models.ForeignKey(
        Proveedor, on_delete=models.SET_NULL, db_column='id_proveedor_principal',
        related_name='productos', blank=True, null=True)
    unidad_medida = models.CharField(max_length=7, choices=UNIDAD_MEDIDA_CHOICES, default='unidad')
    costo_compra = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    precio_venta = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    stock_actual = models.IntegerField(default=0)
    stock_minimo = models.IntegerField(default=0)
    estado = models.CharField(max_length=8, choices=ESTADO_CHOICES, default='activo')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'producto'

    def __str__(self):
        return f'{self.sku} - {self.nombre}'

    @property
    def nivel_stock(self):
        """Semáforo de stock (RF06): verde / amarillo / rojo."""
        if self.stock_actual <= 0:
            return 'rojo'
        if self.stock_actual <= self.stock_minimo:
            return 'amarillo'
        return 'verde'


class ProveedorProducto(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]

    id_proveedor_producto = models.AutoField(primary_key=True)
    proveedor = models.ForeignKey(
        Proveedor, on_delete=models.CASCADE, db_column='id_proveedor',
        related_name='vinculos_producto')
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, db_column='id_producto',
        related_name='vinculos_proveedor')
    costo_referencia = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tiempo_entrega_dias = models.IntegerField(default=0)
    estado = models.CharField(max_length=8, choices=ESTADO_CHOICES, default='activo')

    class Meta:
        managed = False
        db_table = 'proveedor_producto'
        unique_together = (('proveedor', 'producto'),)


class Usuario(models.Model):
    ROL_CHOICES = [
        ('admin', 'Administrador'),
        ('bodega', 'Bodega'),
        ('consulta', 'Consulta'),
    ]

    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(max_length=150, unique=True)
    rol = models.CharField(max_length=8, choices=ROL_CHOICES, default='consulta')
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'usuario'

    def __str__(self):
        return f'{self.nombre} {self.apellido}'


class MovimientoInventario(models.Model):
    TIPO_CHOICES = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
        ('ajuste', 'Ajuste'),
    ]
    MOTIVO_CHOICES = [
        ('compra', 'Compra'),
        ('venta', 'Venta'),
        ('devolucion', 'Devolución'),
        ('merma', 'Merma'),
        ('ajuste_manual', 'Ajuste manual'),
        ('inventario_inicial', 'Inventario inicial'),
    ]

    id_movimiento = models.BigAutoField(primary_key=True)
    producto = models.ForeignKey(
        Producto, on_delete=models.PROTECT, db_column='id_producto',
        related_name='movimientos')
    usuario = models.ForeignKey(
        Usuario, on_delete=models.PROTECT, db_column='id_usuario',
        related_name='movimientos')
    tipo_movimiento = models.CharField(max_length=7, choices=TIPO_CHOICES)
    motivo = models.CharField(max_length=18, choices=MOTIVO_CHOICES)
    cantidad = models.IntegerField()
    costo_unitario = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    referencia = models.CharField(max_length=100, blank=True, null=True)
    observacion = models.CharField(max_length=255, blank=True, null=True)
    fecha_movimiento = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'movimiento_inventario'


class NegocioConfiguracion(models.Model):
    id_config = models.AutoField(primary_key=True)
    nombre_negocio = models.CharField(max_length=120, unique=True)
    nit = models.CharField(max_length=30, unique=True, blank=True, null=True)
    correo = models.CharField(max_length=150, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    pais = models.CharField(max_length=80, default='Colombia')
    moneda = models.CharField(max_length=3, default='COP')
    zona_horaria = models.CharField(max_length=60, default='America/Bogota')
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'negocio_configuracion'

    def __str__(self):
        return self.nombre_negocio
