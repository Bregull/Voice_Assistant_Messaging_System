from django.shortcuts import render
from django.http import HttpResponse



def index(response):
    return HttpResponse("<h1> TEST 1 </h1>")
