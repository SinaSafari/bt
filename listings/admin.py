from django.contrib import admin
import locale

from .models import Listing

class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_published', 'toman_price', 'list_date', 'realtor') #display dollar amount rather than price
    list_display_links = ('id', 'title')
    list_filter = ('realtor',)
    list_editable = ('is_published',)
    search_fields = ('title', 'description', 'address', 'city', 'state', 'zipcode', 'price')
    list_per_page = 25

    def toman_price(self, obj): #Used to render a $ in front of each price, and add commas in for readability
        return "تومان {:,}".format(obj.price)
    toman_price.short_description = 'price'

admin.site.register(Listing, ListingAdmin)