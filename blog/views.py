from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
from django.shortcuts import render,get_object_or_404,redirect
import json
import datetime
from .serializers import ItemsSerializer
from .models import Items
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.edit import CreateView
from django.views.decorators.cache import cache_page
from . filters import ItemsFilter, ItemsApiFilter
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib import messages
from .tasks import create_items_from_api, dowload_trending

from django.db import connection
from sqlalchemy import create_engine
import pandas as pd

def error_404(request, exception):
    data = {'code':404}
    return render(request,'blog/error.html', data)

def home(request):
    items= Items.objects.filter(parent=None) # get all top level items
    if Items.objects.all().count()==0:
        dowload_trending.delay()
        return HttpResponse("<h1>{}</h1>".format('kindly wait while  the db is being seeded and latest stories is beign downloaded'))


    if request.GET.get('item_type'):
        try:
            items=Items.objects.filter(type=request.GET.get('item_type'))
        except Exception as e:
            return HttpResponse("<h1>{}</h1>".format(e))
        if len (items)<1:
             return HttpResponse("""<h1>you input an unavailable object type - <i>'{}'</i>.</h1>
                <h3> this may also happen if this object type is not created with us yet. Thanks </h3><br>
                <span> kindly input valid parameter.</span>""".format(request.GET.get('item_type')))  # i made changes to this line earlier

    filter_form = ItemsFilter(request.GET, queryset=items)
    paginator = Paginator(filter_form.qs, 100)
    if len (filter_form.qs)<1:
             return HttpResponse("<h1>no quyery matches your search's preference </i>.</h1><span> kindly input valid parameter.</span>")
    page_number = request.GET.get('page') if request.GET.get('page') else 1
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/home.html', {'page_obj':page_obj,'my_filter':filter_form})

def details(request, id):
    try:
        object_data=Items.objects.get(id=id)
    except Exception as e:
        return HttpResponse("<h1>no quyery matches your search </i>.</h1><span> kindly input valid parameter other than.</span> <h5>{}</h5>".format(id))
    # kids_list=list(((object_data.kids).strip("'")).strip('"').split(',') )
    # print(kids_list)
    kids=Items.objects.filter(parent=object_data.api_id) if object_data.api_id else Items.objects.filter(parent=object_data.id,api_id=None) #Items.objects.filter(id__in=kids_list) # i get the kids from parent to avoid conflicting kid nort downloaded yet

    paginator = Paginator(kids, 100)
    page_number = request.GET.get('page') if request.GET.get('page') else 1
    kids = paginator.get_page(page_number)
    item_parent=None
    if object_data.parent:
        try:
            item_parent=Items.objects.get(api_id=object_data.parent)
        except Exception as e:
            pass
    context = {'item':object_data,'kids':kids,'item_parent':item_parent}
    return render(request, 'blog/details.html', context)



class ItemView(generics.ListAPIView):
    queryset = Items.objects.all()
    serializer_class = ItemsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ItemsApiFilter
    def post(self, request, format=None): 
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            serializer.save(api_id=None)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(self.request.data, status=status.HTTP_400_BAD_REQUEST)

class item_detail_api(APIView):
    serializer_class = ItemsSerializer
    def get_object(self, pk):
        try:
            return Items.objects.get(pk=pk)
        except Exception as e:
            return None
    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        if snippet:
            serializer = ItemsSerializer(snippet)
            return Response(serializer.data)
        else:
            return HttpResponse("<h1>no quyery matches your search </i>.</h1><span> kindly input valid object parameter other than.</span> <b>{}</b>".format(pk))
    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        if not snippet.api_id:
            serializer = self.serializer_class(data=self.request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer=None
            return Response('you are unauthorised to update this item',status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        if not snippet.api_id:
            snippet.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('you are unauthorised to delete this item',status=status.HTTP_400_BAD_REQUEST)

def author_review(request, slug):
    authors_post=Items.objects.filter(by=slug).order_by('-score','-descendants')
    paginator = Paginator(authors_post, 100)
    page_number = request.GET.get('page') if request.GET.get('page') else 1
    authors_post = paginator.get_page(page_number)
    context = {'username':slug,'kids':authors_post}
    return render(request, 'blog/author_review.html', context)