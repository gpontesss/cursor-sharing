from django.shortcuts import render


def index(request):
    """docs here."""
    return render(request, "cursor/index.html")
