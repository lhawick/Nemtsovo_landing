from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
import landing.views

urlpatterns = [
    path('', landing.views.index, name='index'),
    path('events', landing.views.events, name='events'),
    path('news', landing.views.news, name='news'),
    path('products', landing.views.our_products, name='our_products'),
    path('add-booking', landing.views.add_booking, name='add_booking'),
    path('get-booked-days/<int:booking_identifier_id>', landing.views.get_booked_days, name='get_booked_days'),
    path("get-promo-banner", landing.views.get_promo_banner, name='get_promo_banner')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)