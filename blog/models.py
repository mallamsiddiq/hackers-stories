from django.db import models
from django.utils import timezone


class Items(models.Model):
	api_id = models.IntegerField(unique=True,null=True,blank=True) #
	deleted =models.BooleanField(default=False,blank=True) #
	type = models.CharField(max_length=200)#
	by =models.CharField(blank=True,null=True,max_length=200)
	time=models.DateTimeField(default=timezone.now, blank=True,null=True)
	dead=models.BooleanField(default=False,blank=True)
	kids = models.CharField(max_length=20000, blank=True,null=True)

	parts =models.CharField(max_length=200, default='', blank=True,null=True)
	order_frm =models.CharField(max_length=200, default='earlier', blank=True,null=True)
	descendants = models.IntegerField(null=True,blank=True)
	parent = models.IntegerField(null=True,blank=True)
	score = models.IntegerField(default=0,blank=True)
	title = models.TextField()
	text = models.TextField()
	url =models.CharField(max_length=1000, blank=True,null=True)
	#from_api =models.BooleanField(default=True,blank=True,null=True) 


	class Meta:
		ordering = ['-id']
	def __str__(self):
		return (f"{self.title if self.title!='None' else self.text},---{self.api_id}")
	def get_absolute_url(self):
		return reverse('item-detail', kwargs={'pk': self.pk})



