from django.shortcuts import render

def exercises(request):
    return render(request, "exercises.html")