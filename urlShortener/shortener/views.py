from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from models import Url
from shortener.base62 import *
# Create your views here.

def shortenUrl(request):
	if request.method == "GET":
		return HttpResponse("GOT")
	if request.method == "POST":
		url = request.POST.get("urlToShorten","")
		if url == "":
			return HttpResponseRedirect("/")
		mUrl = Url()
		mUrl.actualUrl = url
		mUrl.save()
		# mUrl.shortenedUrl = shorten(url)

		return HttpResponse(dehydrate(mUrl.id))

def redirect(request):
	idInDB = saturate(request.path_info.replace("/",""))
	QuerySet = Url.objects.all().filter(id=idInDB)
	if(len(QuerySet)==0):
		return HttpResponseRedirect("/")
	else:
		return HttpResponseRedirect("http://www.google.com")
	return HttpResponse(request.path_info)