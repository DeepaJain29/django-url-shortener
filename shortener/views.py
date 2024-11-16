from django.shortcuts import render, redirect, get_object_or_404
from .models import URL
from django.http import HttpResponse

# Create your views here.
def shorten_url(request):
    if request.method == 'POST':
        original_url = request.POST.get('original_url', None)
        url, created = URL.objects.get_or_create(original_url=original_url)
        return render(request, 'shortener/shorten_url.html', {'short_code': url.short_code})
    return render(request, 'shortener/shorten_url.html')

def redirect_to_original(request, short_code):
    url = get_object_or_404(URL, short_code=short_code)
    return redirect(url.original_url)
