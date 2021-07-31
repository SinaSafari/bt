from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .choices import price_choices, bedroom_choices, state_choices

from .models import Listing

def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True) #get all published listings, ordered by newest first

    paginator = Paginator(listings, 6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'listings': paged_listings
    }

    return render(request, 'listings/listings.html', context)

def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id) #Return 404 error if no object found
    other_images = []
    
    # iterate over photo_1 up to but not including photo_7 (doesn't exist)
    # append the url, only if it exists on the object. We get a ValueError
    # if it doesn't. The try/except block helps us mitigate this while
    # still throwing errors for other unexpected problems.
    for n in range(1, 7):
        try:
            other_images.append(getattr(listing, f'photo_{n}').url)
        except ValueError:
            continue

    # We should now have a list with a variable length of 1-6 to pass 
    # onto the Django template. Pass it along with the listing in the 
    # context.
    context = {
        'listing': listing,
        'other_images': other_images
    }
    return render(request, 'listings/listing.html', context=context)

def search(request):
    #Get initial selection sorted by date
    queryset_list = Listing.objects.order_by('-list_date')

    #Filter by contains Keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)

    #Filter by exact city
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)

    #Filter by exact state
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_list = queryset_list.filter(state__iexact=state)

    #Filter by max bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

    #Filter by max price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__lte=price)

    context = {
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'listings': queryset_list,
        'values': request.GET
    }
    return render(request, 'listings/search.html', context)