from django.shortcuts import render
from django.views.generic import*
from django.views.generic import ListView
from .models import Messages
from .models import *
# Create your views here.


# class Base(TemplateView):
#     template_name = "base.html"

class Show(ListView):
    template_name = "show.html"
    model = API_Model
    context_object_name = "appui"

class Message(ListView):
    template_name = "base.html"
    model = Messages
    context_object_name = "appui"

    def get_queryset(self):
        
        query = self.request.GET.get('q')
        if query:
            return Messages.objects.filter(name__icontains=query) | Messages.objects.filter(api__icontains=query)
        else:
            return Messages.objects.all()