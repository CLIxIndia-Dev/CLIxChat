from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the bot index.")
#
# from django.core.context_processors import csrf
# from django.shortcuts import render_to_response
#
# def my_view(request):
#     c = {}
#     c.update(csrf(request))
#     # ... view code here
#     return render_to_response("a_template.html", c)