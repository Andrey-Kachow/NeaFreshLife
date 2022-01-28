from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from food.models import Food
from random import sample


def addfood(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/accounts/login')
    # Suggestion block part
    suggest_list = []
    possible_suggestions = Food.objects.all()  # query
    already_favored_list = list(request.user.favourite_food.all())
    ignore_list = list(request.user.ignored_food.all())
    possible_suggestions = possible_suggestions.exclude(name__in=already_favored_list)
    possible_suggestions = possible_suggestions.exclude(name__in=ignore_list)

    length = len(possible_suggestions)  # length of narrowed list
    if length:
        if length > 3:
            random_indices = sample(range(length), 3)
            for i in random_indices:
                suggest_list.append(possible_suggestions[i])
        else:
            suggest_list = possible_suggestions
    # Search block part
    queryset_list = Food.objects.all().order_by("name")
    query = request.GET.get('query')
    if query:
        queryset_list = queryset_list.filter(name__icontains=query)
    context = {
        "suggest_list": suggest_list,
        "query": query,
        "query_list": queryset_list
    }
    return render(request, 'food/food.html', context)


def food_item(request, pk):
    item = Food.objects.get(pk=pk)
    context = {'item': item}
    return render(request, 'food/food_item.html', context)


# Icons in food.html
def add_to_favourite(request, pk):
    Food.objects.get(pk=pk).loved_by.add(request.user)
    Say("add_to_favourite")
    return HttpResponse('')

def remove_from_favourite(request, pk):
    Food.objects.get(pk=pk).loved_by.remove(request.user)
    Say("remove_from_favourite")
    return HttpResponse('')

def add_to_ignore(request, pk):
    Food.objects.get(pk=pk).ignored_by.add(request.user)
    Say("add_to_ignore")
    return HttpResponse('')

def remove_from_ignore(request, pk):
    Food.objects.get(pk=pk).ignored_by.remove(request.user)
    Say("remove_from_ignore")
    return HttpResponse('')

def Say(Speech):
    print("\n", Speech, "\n")


# def remove_from_favourite(request, pk):
#     user = request.user
#     food = Food.objects.get(pk=pk)
#     if user in food.loved_by.all():
#         food.loved_by.remove(user)
#     return HttpResponse('')
#
# def remove_from_ignore(request, pk):
#     food = Food.objects.get(pk=pk)
#     user = request.user
#     if user in food.ignored_by.all():
#         food.ignored_by.remove(user)
#     return HttpResponse('')
