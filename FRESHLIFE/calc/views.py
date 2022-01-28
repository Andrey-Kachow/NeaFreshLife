from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Activity, Latest_inputs
from django.core.exceptions import ObjectDoesNotExist


def calculator(request, user_came_from_planner=0):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/accounts/login')
    activities_list = Activity.objects.all().order_by("name")  # taking activities from db
    calories = prots = fats = carbs = 0  # context vars
    if request.method == "POST":
        weight = float(request.POST.get('weight'))
        bodyfat = float(request.POST.get('bodyfat'))
        activity_choice = int(request.POST.get('activity'))
        goal = float(request.POST.get('goal'))
        advanced_checkbox = request.POST.get('adCalc')

        bmr = 370 + 21.6 * weight * (100 - bodyfat) / 100
        if advanced_checkbox:
            eat_per_kg = float(request.POST.get('sneaky'))  # hidden input in calculator.html
            calories += int(eat_per_kg * weight / 7)  # Exercise Energy Expenditure is added here
            common_difference = 0.05  # (1.15, 1.20. 1.25, ...)
        else:
            common_difference = 0.15  # (1.15, 1.30, 1.45, ...)
        # arithmetic sequence instead of "if" clause for determining activity coeficient
        activity_coef = 1.15 + common_difference * (activity_choice - 1)

        calories += int(bmr * activity_coef * goal)
        prots = int(weight * 1.5)  # Proteins
        fats = int(weight * 0.9)
        carbs = int((calories - prots * 4 - fats * 9) / 4)  # Carbohydrates
        # ---------------------------------------------------------------------
        # Updating User's Latest_inputs
        user = request.user
        try:  # plan a, if everything is OK
            if user.latest_inputs:
                user.latest_inputs.weight = weight
                user.latest_inputs.calories = calories
                user.save()
        except ObjectDoesNotExist:  # plan b, if User "lost" his latest_inputs
            Latest_inputs(user=user, weight=weight, calories=calories).save()
        # ---------------------------------------------------------------------
        if user_came_from_planner:  # coming back to meal planner
            return redirect('planner:meal_planner')
    context = {
        'calories': calories,
        'prots': prots,
        'fats': fats,
        'carbs': carbs,
        'activities': activities_list,
    }
    return render(request, 'calc/calculator.html', context)

# if request.GET.get('weight'):  # assigning weight
    # print(weight + 5)
