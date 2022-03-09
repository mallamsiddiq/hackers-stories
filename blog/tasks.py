from . models import Items

from celery import shared_task
import requests
import datetime
from django.db import IntegrityError


@shared_task
def create_items_from_api(startt,endd):
	def get_val(valu,def_val=None):
		try:
			return query[valu]
		except:
			return def_val
	for i in range(startt,endd):
		try:
			query =requests.get(f'https://hacker-news.firebaseio.com/v0/item/{i}.json?print=pretty').json()
			items_instance = Items(api_id=get_val('id'),deleted=get_val('deleted',False),type=get_val('type'),by=get_val('by'),
				time=datetime.datetime.fromtimestamp(get_val('time',0)),dead=get_val('dead',False),kids=get_val('kids',[]),parts=get_val('parts'),
				descendants=get_val('descendants',0), score=get_val('score',0), title=get_val('title','None'), text=get_val('text','None'),
				url=get_val('url'),parent=get_val('parent'),order_frm=get_val('latest'))
			items_instance.save()
			print('hurray!! {} saved successfully'.format(items_instance))
		except IntegrityError as e:
			print ('oops!! this is an err {} '.format(e))
		except:
			return('oops!! this is an err {} '.format('it might be not null constraint, kindly confirm all fields'))
			break
	print ('{} Items from API created with success!'.format(items_instance.api_id-startt))

@shared_task
def create_items_from_api_beat_latest():  
	latest_api_item_key= requests.get('https://hacker-news.firebaseio.com/v0/maxitem.json?print=pretty').json()
	latest_database_object_api_key=int(Items.objects.latest('api_id').api_id)
	off_limitts=latest_database_object_api_key+101 if latest_api_item_key<latest_database_object_api_key+101 else latest_api_item_key+1
	if latest_database_object_api_key < latest_api_item_key:
		create_items_from_api(latest_database_object_api_key+1,off_limitts)
	else:
		print('no latest item other than we have')
	
	print('this is celery beat')

@shared_task
def dowload_trending():
	latest_items= list(requests.get('https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty').json())
	latest_items.sort()
	create_items_from_api(latest_items[0],latest_items[len(latest_items)-1])
