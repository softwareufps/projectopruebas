from __future__ import unicode_literals

from django.db import models

# Create your models here.


class tipo(models.Model):
	Descripcion=models.CharField(max_length=200,null=True)
	def __str__(self):
		#retornar cadena no tupla
		return (self.Descripcion.encode('utf8'))




class  ataque(models.Model):
	tipoataque=models.ForeignKey(tipo)
	definicion=models.TextField(null=True)
	comofunciona=models.TextField(null=True)
	comoevitarlo=models.TextField(null=True)
	tipos=models.TextField(null=True)
	video=models.CharField(max_length=200,null=True)
	recomendaciones=models.TextField(null=True)
	malaspracticas=models.TextField(null=True)


class aprobo(models.Model):
	tipoataque=models.ForeignKey(tipo)
	descripccion=models.TextField(null=True)
	nocaer=models.TextField(null=True)
	defininicion=models.TextField(null=True)


