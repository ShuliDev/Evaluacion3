from django.shortcuts import render


def index(request):
	"""Página de inicio (catálogo placeholder)."""
	return render(request, 'index.html')
