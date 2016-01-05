from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from models import Url
from django.template.loader import get_template
from shortener.base62 import *
from django.template import Context
# Create your views here.

def shortenUrl(request):
	if request.method == "GET":
		t = get_template("index.html")
		return HttpResponse(t.render())
	if request.method == "POST":
		url = request.POST.get("urlToShorten","")
		if url == "":
			return HttpResponseRedirect("/")
		mUrl = Url()
		url = url.replace("http://","")
		url = url.replace("https://","")
		mUrl.actualUrl = url
		mUrl.save()
		# mUrl.shortenedUrl = shorten(url)
		t = get_template("shortened.html")

		return HttpResponse(t.render(Context({"actual_url":url, "shortened_url":dehydrate(mUrl.id)})))

def redirect(request):
	idInDB = saturate(request.path_info.replace("/",""))
	QuerySet = Url.objects.all().filter(id=idInDB)
	if(len(QuerySet)==0):
		return HttpResponseRedirect("/")
	else:
		return HttpResponseRedirect("http://"+QuerySet[0].actualUrl)
	return HttpResponse(request.path_info)