from restaurant.utils import menu


def get_restaurant_context(request):
    return {'mainmenu': menu}
