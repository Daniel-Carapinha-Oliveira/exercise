from django.shortcuts import render

from exercise.version import __version__


def homepage(request):
    """
    Renders the homepage view of the website using the "homepage.html" template.

    Receives the HTTP request object.

    Returns an HttpResponse object containing the rendered homepage.
    Passes a context dictionary containing:
        - current_page: identifies the active page as 'homepage'
        - version: the current application version number
    """
    return render(request, "homepage.html", {'current_page': 'homepage', 'version': __version__})
