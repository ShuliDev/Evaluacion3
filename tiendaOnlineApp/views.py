from django.shortcuts import render


from .models import Product, Category

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
