from django.contrib import admin
from django.utils.html import format_html
from .models import (
	Category,
	Product,
	Insumo,
	Pedido,
)


class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'category', 'price', 'featured', 'vista_foto1')
	list_filter = ('category', 'featured')
	search_fields = ('name', 'description')

	def vista_foto1(self, obj):
		if obj.foto1:
			return format_html("<img src={} width=50 height=50 />", obj.foto1.url)
		return "-"
	vista_foto1.short_description = "Foto 1"


class PedidoAdmin(admin.ModelAdmin):
	list_display = ('id', 'cliente_nombre', 'plataforma', 'estado', 'estado_pago', 'creado_en', 'vista_foto')
	list_filter = ('plataforma', 'estado', 'estado_pago')
	search_fields = ('cliente_nombre', 'email', 'telefono', 'token')
	readonly_fields = ('token', 'creado_en', 'actualizado_en')

	def vista_foto(self, obj):
		if obj.foto_referencia:
			return format_html("<img src={} width=50 height=50 />", obj.foto_referencia.url)
		return "-"
	vista_foto.short_description = "Foto Referencia"

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
