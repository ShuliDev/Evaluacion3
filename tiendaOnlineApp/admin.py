from django.contrib import admin
from .models import (
	Category,
	Product,
	ProductImage,
	Insumo,
	Pedido,
	PedidoImage,
)


class ProductImageInline(admin.TabularInline):
	model = ProductImage
	extra = 1


class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'category', 'price', 'featured')
	list_filter = ('category', 'featured')
	search_fields = ('name', 'description')
	inlines = [ProductImageInline]


class PedidoImageInline(admin.TabularInline):
	model = PedidoImage
	extra = 1


class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente_nombre', 'plataforma', 'estado', 'estado_pago', 'creado_en')
    list_filter = ('plataforma', 'estado', 'estado_pago')
    search_fields = ('cliente_nombre', 'email', 'telefono', 'token')
    readonly_fields = ('token', 'creado_en', 'actualizado_en')
    inlines = [PedidoImageInline]

    def save_model(self, request, obj, form, change):
        # Validar que no se pueda finalizar sin pago completo
        if obj.estado == 'finalizada' and obj.estado_pago != 'pagado':
            raise ValueError("No se puede finalizar un pedido sin pago completo.")
        super().save_model(request, obj, form, change)
class InsumoAdmin(admin.ModelAdmin):
	list_display = ('name', 'tipo', 'cantidad', 'unidad', 'marca', 'color')
	search_fields = ('name', 'marca', 'color')


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Insumo, InsumoAdmin)
admin.site.register(Pedido, PedidoAdmin)
