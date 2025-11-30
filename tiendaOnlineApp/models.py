from django.db import models
from django.utils import timezone
from django.utils.html import format_html
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
	description = models.TextField(max_length=2000)
	category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
	price = models.DecimalField(max_digits=10, decimal_places=2)
	featured = models.BooleanField(default=False)
	foto1 = models.ImageField(upload_to='productos', null=True, blank=True)
	foto2 = models.ImageField(upload_to='productos', null=True, blank=True)
	foto3 = models.ImageField(upload_to='productos', null=True, blank=True)

	class Meta:
		verbose_name = 'Producto'
		verbose_name_plural = 'Productos'

	def __str__(self):
		return self.name


class Insumo(models.Model):
	name = models.CharField(max_length=200)
	tipo = models.CharField(max_length=100)
	cantidad = models.DecimalField(max_digits=10, decimal_places=3)
	unidad = models.CharField(max_length=50, blank=True)
	marca = models.CharField(max_length=100)
	color = models.CharField(max_length=50)

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
	token = models.CharField(max_length=64, unique=True, editable=False)
	cliente_nombre = models.CharField(max_length=200)
	email = models.EmailField(max_length=200)
	telefono = models.CharField(max_length=80)
	producto = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	descripcion = models.TextField()
	plataforma = models.CharField(max_length=20, choices=PLATFORM_CHOICES, default='web')
	fecha_necesaria = models.DateField(null=True, blank=True)
	foto_referencia1 = models.ImageField(upload_to='pedidos', null=True)
	foto_referencia2 = models.ImageField(upload_to='pedidos', null=True, blank=True)
	foto_referencia3 = models.ImageField(upload_to='pedidos', null=True, blank=True)
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
			self.token = uuid.uuid4().hex
		super().save(*args, **kwargs)


