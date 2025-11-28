from django.db import models
from django.utils import timezone
import uuid


class Category(models.Model):
	name = models.CharField(max_length=100)
	slug = models.SlugField(max_length=120, unique=True)

	class Meta:
		verbose_name = 'Categoría'
		verbose_name_plural = 'Categorías'

	def __str__(self):
		return self.name


class Product(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
	price = models.DecimalField(max_digits=10, decimal_places=2)
	featured = models.BooleanField(default=False)

	class Meta:
		verbose_name = 'Producto'
		verbose_name_plural = 'Productos'

	def __str__(self):
		return self.name


def product_image_upload_to(instance, filename):
	return f'products/{instance.product.id}/{filename}'


class ProductImage(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
	image = models.ImageField(upload_to=product_image_upload_to)
	alt_text = models.CharField(max_length=150, blank=True)

	class Meta:
		verbose_name = 'Imagen de producto'
		verbose_name_plural = 'Imágenes de producto'

	def __str__(self):
		return f"Imagen #{self.id} - {self.product.name}"


class Insumo(models.Model):
	name = models.CharField(max_length=200)
	tipo = models.CharField(max_length=100, blank=True)
	cantidad = models.DecimalField(max_digits=10, decimal_places=3)
	unidad = models.CharField(max_length=50, blank=True)
	marca = models.CharField(max_length=100, blank=True)
	color = models.CharField(max_length=50, blank=True)

	class Meta:
		verbose_name = 'Insumo'
		verbose_name_plural = 'Insumos'

	def __str__(self):
		return self.name


PLATFORM_CHOICES = [
	('facebook', 'Facebook'),
	('instagram', 'Instagram'),
	('whatsapp', 'WhatsApp'),
	('presencial', 'Presencial'),
	('web', 'Sitio Web'),
	('otra', 'Otra'),
]

ORDER_STATUS = [
	('solicitado', 'Solicitado'),
	('aprobado', 'Aprobado'),
	('en_proceso', 'En proceso'),
	('realizada', 'Realizada'),
	('entregada', 'Entregada'),
	('finalizada', 'Finalizada'),
	('cancelada', 'Cancelada'),
]

PAYMENT_STATUS = [
	('pendiente', 'Pendiente'),
	('parcial', 'Parcial'),
	('pagado', 'Pagado'),
]


class Pedido(models.Model):
	token = models.CharField(max_length=64, unique=True, blank=True, editable=False)
	cliente_nombre = models.CharField(max_length=200)
	email = models.EmailField(blank=True)
	telefono = models.CharField(max_length=80, blank=True)
	producto = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
	descripcion = models.TextField(blank=True)
	plataforma = models.CharField(max_length=20, choices=PLATFORM_CHOICES, default='web')
	fecha_necesaria = models.DateField(null=True, blank=True)
	estado = models.CharField(max_length=20, choices=ORDER_STATUS, default='solicitado')
	estado_pago = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pendiente')
	creado_en = models.DateTimeField(default=timezone.now)
	actualizado_en = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = 'Pedido'
		verbose_name_plural = 'Pedidos'

	def __str__(self):
		return f"Pedido {self.id} - {self.cliente_nombre} ({self.get_estado_display()})"

	def save(self, *args, **kwargs):
		if not self.token:
			# generar un token único
			self.token = uuid.uuid4().hex
		super().save(*args, **kwargs)


def pedido_image_upload_to(instance, filename):
	return f'pedidos/{instance.pedido.id}/{filename}'


class PedidoImage(models.Model):
	pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='images')
	image = models.ImageField(upload_to=pedido_image_upload_to)
	alt_text = models.CharField(max_length=150, blank=True)

	class Meta:
		verbose_name = 'Imagen de pedido'
		verbose_name_plural = 'Imágenes de pedido'

	def __str__(self):
		return f"Imagen #{self.id} - Pedido {self.pedido.id}"

