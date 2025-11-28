def pedido_seguimiento(request, token):
	pedido = get_object_or_404(Pedido, token=token)
	imagenes = pedido.images.all()
	return render(request, 'pedido_seguimiento.html', {
		'pedido': pedido,
		'imagenes': imagenes,
	})
from django import forms
from .models import Pedido
class PedidoForm(forms.ModelForm):
	class Meta:
		model = Pedido
		fields = ['cliente_nombre', 'email', 'telefono', 'descripcion', 'fecha_necesaria']
		widgets = {
			'fecha_necesaria': forms.DateInput(attrs={'type': 'date'}),
		}

def pedido_solicitud(request, producto_id):
	producto = get_object_or_404(Product, pk=producto_id)
	if request.method == 'POST':
		form = PedidoForm(request.POST, request.FILES)
		if form.is_valid():
			pedido = form.save(commit=False)
			pedido.producto = producto
			pedido.plataforma = 'web'
			pedido.estado = 'solicitado'
			pedido.estado_pago = 'pendiente'
			pedido.save()
			# TODO: manejar imágenes de referencia
			return render(request, 'pedido_exito.html', {'pedido': pedido})
	else:
		form = PedidoForm()
	return render(request, 'pedido_form.html', {'form': form, 'producto': producto})
from django.shortcuts import render


from .models import Product, Category
from django.shortcuts import get_object_or_404

def index(request):
	categoria_slug = request.GET.get('categoria')
	categorias = Category.objects.all()
	productos = Product.objects.all()
	if categoria_slug:
		productos = productos.filter(category__slug=categoria_slug)
	return render(request, 'index.html', {
		'productos': productos,
		'categorias': categorias,
		'categoria_seleccionada': categoria_slug,
	})

def producto_detalle(request, pk):
	producto = get_object_or_404(Product, pk=pk)
	imagenes = producto.images.all()
	return render(request, 'producto_detalle.html', {
		'producto': producto,
		'imagenes': imagenes,
	})
