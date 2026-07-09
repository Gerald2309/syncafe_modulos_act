# Plan de pruebas manual — Syncafe (GA7-220501096-AA2-EV02)

Módulo probado: Inventario (Productos y Proveedores).
Servidor: `python manage.py runserver` → http://127.0.0.1:8000/productos/

| ID | Caso de prueba | Pasos | Resultado esperado | Resultado obtenido | Estado |
|----|----|----|----|----|----|
| CP-01 | Crear producto con datos válidos | Llenar formulario completo (SKU, nombre, categoría, costo, precio, stock) y Guardar | El producto se guarda y aparece en la lista | Se creó "CAF-002 — Café molido 500g" y apareció en la lista | ✔ Cumple |
| CP-02 | Validación: precio de venta menor al costo de compra | Ingresar costo_compra=1000, precio_venta=500 y Guardar | No guarda; muestra "El precio de venta no puede ser menor al costo de compra." | Se mostró el mensaje y el producto TEST-001 no se guardó | ✔ Cumple |
| CP-03 | Editar un producto | Abrir un producto, cambiar el stock y Guardar | El cambio queda reflejado en la lista | Stock de "Vaso 12oz" se actualizó de 300 a 50 | ✔ Cumple |
| CP-04 | Semáforo de stock (RF06) | Observar el color del badge de stock según stock_actual vs stock_minimo | Verde si stock > mínimo, amarillo si stock <= mínimo, rojo si stock = 0 | "Vaso 12oz" con stock 50 (mínimo 100) mostró badge amarillo; productos con stock por encima del mínimo mostraron verde | ✔ Cumple |
| CP-05 | Deshabilitar un producto (RF03) | Pulsar "Deshabilitar" y aceptar la confirmación | El producto no se borra de la base de datos, pero desaparece de la lista principal | "CAF-002" pasó a estado='inactivo' en la base de datos y dejó de listarse | ✔ Cumple |
| CP-06 | Crear proveedor con datos válidos | Llenar formulario de proveedor (nombre, NIT, email, ciudad) y Guardar | El proveedor se guarda y aparece en la lista | Se creó "Lácteos del Quindío" y apareció en la lista | ✔ Cumple |
| CP-07 | Listar productos paginados | Abrir la lista con más de 10 productos | Muestra 10 por página y controles de paginación | No probado en vivo: el catálogo actual tiene menos de 10 productos. La paginación está implementada con `Paginator(qs, 10)` (ver `inventario/views.py`), pendiente de verificar visualmente cuando el inventario crezca | ⚠ Pendiente de verificar con más datos |
| CP-08 | Reportes de inventario (RF07) | Pulsar botón de generar reporte PDF | Se descarga un PDF con el detalle de movimientos | No implementado en esta entrega — queda fuera del alcance de la capa CRUD básica (formularios/GET-POST/plantillas) que exige esta evidencia | ✘ No cumple (funcionalidad pendiente, fuera de alcance de esta entrega) |

## Notas

- CP-07 y CP-08 quedan documentados honestamente como pendientes, tal como recomienda la guía de la Entrega 3: no todo tiene que salir "✔ Cumple"; lo importante es dejarlo registrado.
- CP-08 (reportes) corresponde a RF07 de la especificación de requisitos, pero no es parte del alcance de esta evidencia (GA7-AA2-EV02, capa web CRUD). Se deja como mejora futura.
