from django.shortcuts import render, get_object_or_404
from django import forms
from .models import Product, Category, Pedido


def index(request):
    categoria_slug = request.GET.get('categoria')
    busqueda = request.GET.get('busqueda', '')
    categorias = Category.objects.all()
    productos = Product.objects.all()
    if categoria_slug:
        productos = productos.filter(category__slug=categoria_slug)
    if busqueda:
        productos = productos.filter(name__icontains=busqueda) | productos.filter(description__icontains=busqueda)
    return render(request, 'index.html', {
        'productos': productos,
        'categorias': categorias,
        'categoria_seleccionada': categoria_slug,
        'busqueda': busqueda,
    })


def producto_detalle(request, pk):
    producto = get_object_or_404(Product, pk=pk)
    return render(request, 'producto_detalle.html', {
        'producto': producto,
    })


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente_nombre', 'email', 'telefono', 'descripcion', 'fecha_necesaria', 'foto_referencia']
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
            return render(request, 'pedido_exito.html', {'pedido': pedido})
    else:
        form = PedidoForm()
    return render(request, 'pedido_form.html', {'form': form, 'producto': producto})


def pedido_seguimiento(request, token):
    pedido = get_object_or_404(Pedido, token=token)
    return render(request, 'pedido_seguimiento.html', {
        'pedido': pedido,
    })
