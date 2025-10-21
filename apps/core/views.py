from django.shortcuts import render

from exercise.version import __version__


def homepage(request):
    return render(request, "homepage.html", {'current_page': 'homepage', 'version': __version__})
