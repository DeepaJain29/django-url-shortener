# from django.shortcuts import render, redirect, get_object_or_404
# from .models import URL
# from django.http import HttpResponse

# # Create your views here.
# def shorten_url(request):
#     if request.method == 'POST':
#         original_url = request.POST.get('original_url', None)
#         url, created = URL.objects.get_or_create(original_url=original_url)
#         return render(request, 'shortener/shorten_url.html', {'short_code': url.short_code})
#     return render(request, 'shortener/shorten_url.html')

# def redirect_to_original(request, short_code):
#     url = get_object_or_404(URL, short_code=short_code)
#     return redirect(url.original_url)
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import URL
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import URLSerializer

# Create a short URL
def create_short_url(request):
    if request.method == "POST":
        original_url = request.POST.get("original_url")
        custom_code = request.POST.get("short_code", "").strip()
        expiration_date = request.POST.get("expiration_date", None)

        if not original_url:
            messages.error(request, "Please enter a URL.")
            return render(request, "shortener/index.html")

        # Check for custom short code conflicts
        if custom_code and URL.objects.filter(short_code=custom_code).exists():
            messages.error(request, "This custom short code is already taken.")
            return render(request, "shortener/index.html")

        # Create or save the URL object
        url = URL(
            original_url=original_url,
            short_code=custom_code if custom_code else None,
            expiration_date=expiration_date,
        )
        url.save()
        return render(request, "shortener/index.html", {"short_code": url.short_code})

    return render(request, "shortener/index.html")

# Redirect to the original URL
def redirect_view(request, short_code):
    url = get_object_or_404(URL, short_code=short_code)

    if url.is_expired():
        return HttpResponse("This link has expired.", status=410)

    url.click_count += 1
    url.save()
    return redirect(url.original_url)

# Analytics Dashboard
def analytics(request):
    print("Analytics view called")
    urls = URL.objects.all().order_by("-click_count")
    return render(request, "shortener/analytics.html", {"urls": urls})

# REST API for URL Shortening
class URLShortenerAPI(APIView):
    def post(self, request):
        serializer = URLSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, short_code=None):
        if short_code:
            url = URL.objects.filter(short_code=short_code).first()
            if url:
                return Response(URLSerializer(url).data, status=status.HTTP_200_OK)
            return Response({"error": "Short code not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            urls = URL.objects.all()
            return Response(URLSerializer(urls, many=True).data, status=status.HTTP_200_OK)
