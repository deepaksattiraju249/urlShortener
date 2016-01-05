from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from models import Url
from django.template.loader import get_template
from shortener.base62 import *
from django.template import Context
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
# Create your views here.
val = URLValidator()
def shortenUrl(request):
	if request.method == "GET":
		t = get_template("index.html")
		return HttpResponse(t.render())
	if request.method == "POST":
		url = request.POST.get("urlToShorten","")
		if url == "":
			return HttpResponseRedirect("/")
		try:
			if not ("http://" in url) or not ("https://" in url):
				url="http://"+url
			val(url)
		except ValidationError,e:
			t = get_template("invalid.html")
			return HttpResponse(t.render())

		url = url.replace("http://","")
		url = url.replace("https://","")
		QS = Url.objects.all().filter(actualUrl=url)
		if(len(QS)>0):
			UrlObject = QS[0]
			t = get_template("shortened.html")
			return HttpResponse(t.render(Context({"actual_url":url, "shortened_url":dehydrate(UrlObject.id)})))	

		mUrl = Url()
		
		mUrl.actualUrl = url
		mUrl.save()
		# mUrl.shortenedUrl = shorten(url)
		t = get_template("shortened.html")

		return HttpResponse(t.render(Context({"actual_url":url, "shortened_url":dehydrate(mUrl.id)})))

def redirect(request):
	if(request.path_info=="/"):
		return HttpResponseRedirect("/")

	idInDB = saturate(request.path_info.replace("/",""))
	QuerySet = Url.objects.all().filter(id=idInDB)
	if(len(QuerySet)==0):
		return HttpResponseRedirect("/")
	else:
		return HttpResponseRedirect("http://"+QuerySet[0].actualUrl)
	return HttpResponse(request.path_info)