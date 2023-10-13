from django.shortcuts import render
from django.http import HttpResponseRedirect
from food.models import Food
from .models import Plan, Meal, Meal_has_Food
from random import randint
import ast
from numpy import array
from scipy.optimize import lsq_linear


def serving_master(prots, fats, carbs, calories, healthscore,
                   Main, Side, Veg, Other=None):
    # Measures to make nutrients non-negative
    if prots < 0: prots = 0
    if fats < 0: fats = 0
    if carbs < 0: carbs = 0
    if calories < 0: calories = 0
    if healthscore < 0: healthscore = 0

    # Making sure certain percentage of nutritional value comes from
    # the right source, and calibrating nutrients after each assignment
    Veg_s = 0.6 * healthscore / Veg.healthscore
    prots -= Veg.protein * Veg_s
    carbs -= Veg.carbs * Veg_s
    fats -= Veg.fat * Veg_s
    healthscore -= Veg.healthscore * Veg_s

    Main_s = 0.6 * prots / Main.protein + 0.05 * fats / Main.fat
    prots -= Main.protein * Main_s
    carbs -= Main.carbs * Main_s
    fats -= Main.fat * Main_s
    healthscore -= Main.healthscore * Main_s

    Side_s = 0.7 * carbs / Side.carbs
    prots -= Side.protein * Side_s
    carbs -= Side.carbs * Side_s
    fats -= Side.fat * Side_s
    healthscore -= Side.healthscore * Side_s

    # calibrating calories
    calories -= Main.calories * Main_s +\
        Side.calories * Side_s + Veg.calories * Veg_s

    if Other:  # Other may not be in the meal
        Other_s = 0.05 * calories / Other.calories
        prots -= Other.protein * Other_s
        carbs -= Other.carbs * Other_s
        fats -= Other.fat * Other_s
        healthscore -= Other.healthscore * Other_s
        calories -= Other.calories * Other_s
    else:
        Other_s = 0

    # print(prots,"|", fats, "|", carbs, "|", calories, "|", healthscore)
    if calories > 200 or prots > 10 or carbs > 10 or fats > 25:
        # if actual macronutrients values are not close enough
        # to the expected values, another iteration is executed
        #  print("ONE MORE ITERATION!")
        extra_servings = serving_master(
            prots, fats, carbs,
            calories, healthscore,
            Main, Side, Veg, Other,
        )
        Main_s += extra_servings[0]
        Side_s += extra_servings[1]
        Veg_s += extra_servings[2]
        Other_s += extra_servings[3]
    return Main_s, Side_s, Veg_s, Other_s  # servings of each category

def create_new_plan(request):
    new_plan = Plan(  # creating plan with name provided by user
        owner=request.user,
        name=request.POST.get('plan_name'),  # user input
    )
    new_plan.save()
    #  nested looping for, there meal number and food "indecies", m and f, start with 1, not 0
    for m in range(1, int(request.POST.get('meal_num')) + 1):
        meal = Meal(plan=new_plan, index=m)  # creating m-th meal
        meal.save()
        for f in range(1, int(request.POST.get('three_or_four')) + 1):
            food_name = request.POST.get('food_{}{}'.format(m, f))  # finding
            serving = int(request.POST.get('serving_{}{}'.format(m, f)))
            Meal_has_Food(  # linking f-th food to m-th meal
                meal=meal,
                food=Food.objects.get(name=food_name),
                portion_size=serving,
            ).save()

def categories_of_food(request):
    ignored = list(request.user.ignored_food.all())  # ignored food
    choices = Food.objects.all().exclude(name__in=ignored)
    return choices.filter(type="Main"), choices.filter(type="Side"),\
           choices.filter(type="Vegetables"), choices.filter(type="Other")

def meal_planner(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/accounts/login')
    enough_favourites = True
    reasons = ""  # reason why not enough favourites, message for user
    plan = []  # list, where all meals lists would go
    meal_num = 0  # some context vars
    if request.method == 'POST' and 'create' in request.POST:  # "create" button was clicked

        weight = float(request.POST.get('weight'))
        calories = float(request.POST.get('calories'))
        diet = ast.literal_eval(request.POST.get('diet'))  # string representation of a list --> list
        meal_num = int(request.POST.get('meal_num'))

        # Calculating daily macronutrients
        prots = diet[0] * weight
        fats = diet[1] * weight
        carbs = diet[2] * weight
        if not fats:  # one of the macros is always not fixed
            fats = (calories - prots * 4 - carbs * 4) / 9
        elif not carbs:
            carbs = (calories - prots * 4 - fats * 9) / 4

        Main_choices, Side_choices, Veg_choices, Other_choices = categories_of_food(request)

        # Narrowing choices of some categories depending on the diet.
        use_least_squares = False
        if carbs / weight < 3:  # measure for low carb diets
            Side_choices = Side_choices.filter(carbs__lt=25)  # lt --> less than
        else:
            Side_choices = Side_choices.filter(carbs__gte=25)  # gte --> more or equal
        if fats / weight >= 2:  # measure for fat-rich diets
            Main_choices = Main_choices.filter(fat__gte=30)
            Veg_choices = Veg_choices.filter(fat__gte=8)
            use_least_squares = True  # recursion cannot solve this type of diet
        else:
            Main_choices = Main_choices.filter(fat__lt=30)
            Veg_choices = Veg_choices.filter(fat__lt=8)

        # if "favourite food only" was checked only favourite foods are taken
        if request.POST.get('fav_checkbox'):  # but there are some requirements
            favourites = list(request.user.favourite_food.all())
            Main_choices = Main_choices.filter(name__in=favourites)
            Side_choices = Side_choices.filter(name__in=favourites)
            Veg_choices = Veg_choices.filter(name__in=favourites)
            Other_choices = Other_choices.filter(name__in=favourites)
            # checking if all requirements are satisfied
            if len(Main_choices) < 2:  # two or more Mains required
                reasons += "Not enough main course options. "
            if len(Side_choices) < 2:  # two or more Sides required
                reasons += "Not enough side dish (garnish) options. "
            if not Veg_choices:  # at least one source of vegetables required
                reasons += "There's no vegetable or leafy greens options. "
            if reasons:
                enough_favourites = False

        if enough_favourites:  # unless user checked the checkbox AND his favourites are insufficient

            prots = prots / meal_num
            fats = fats / meal_num
            carbs = carbs / meal_num
            calories = calories / meal_num  # energy per meal
            healthscore = 40 / meal_num

            # main for loop, where servings of each meal are
            for i in range(meal_num):
                # taking random item from each category
                Main = Main_choices[randint(0, len(Main_choices) - 1)]
                Side = Side_choices[randint(0, len(Side_choices) - 1)]
                Veg = Veg_choices[randint(0, len(Veg_choices) - 1)]
                if Other_choices:  # Other is different, it doesn't have to be in a plan
                    Other = Other_choices[randint(0, len(Other_choices) - 1)]
                else:
                    Other = 0

                #  trying to use recursion
                recursion_has_failed = False
                if not use_least_squares:
                    # try:
                    servings = serving_master(prots, fats, carbs, calories,
                                              healthscore, Main, Side, Veg, Other,)
                    # except RecursionError:
                    #     recursion_has_failed = True
                    # except:  # UBERI ETO POTOM !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    #     recursion_has_failed = True

                # if use_least_squares or recursion_has_failed:
                #     if Other != 0:
                #         Other_p, Other_f, Other_c, = Other.protein, Other.fat, Other.carbs
                #         Other_h, Other_kcal = Other.healthscore, Other.calories
                #     else:
                #         Other = Other_p = Other_f = Other_c = Other_h = Other_kcal = 0
                #     A = array([  # content of nutrients in food
                #         [Main.protein,     Side.protein,     Veg.protein,     Other_p],
                #         [Main.carbs,       Side.carbs,       Veg.carbs,       Other_c],
                #         [Main.fat,         Side.fat,         Veg.fat,         Other_f],
                #         [Main.healthscore, Side.healthscore, Veg.healthscore, Other_h],
                #         [Main.calories,    Side.calories,    Veg.calories,    Other_kcal],
                #     ])
                #     b = array([  # requirements column vector
                #         prots,
                #         carbs,
                #         fats,
                #         healthscore,
                #         calories,
                #     ])
                #     servings = lsq_linear(A, b, bounds=(0.17, 4)).x.tolist()
                #     # print("r =", servings)

                display_error_in_macronutrients(Main, Side, Veg, Other, servings,
                                                calories, prots, fats, carbs, healthscore)

                Main_s = int(servings[0] * 100)  # servings converted to grams or ml
                Side_s = int(servings[1] * 100)  # and rounded to the integer
                Veg_s = int(servings[2] * 100)
                Other_s = int(servings[3] * 100)
                # Organising food choices, servings and units in a list
                meal = [
                    [Main, Main_s, Main.unit],
                    [Side, Side_s, Side.unit],
                    [Veg, Veg_s, Veg.unit]
                ]
                if Other_s and Other:
                    meal.append([Other, Other_s, Other.unit])
                plan.append(meal)  # appending meal list to the plan list

    if request.method == 'POST' and 'save' in request.POST:  # "save" button was clicked
        create_new_plan(request)

    context = {
        "enough_favourites": enough_favourites,
        "reasons": reasons,
        "plan": plan,
        "meal_num": meal_num,
    }
    return render(request, 'planner/mealplanner.html', context)


def display_error_in_macronutrients(Main, Side, Veg, Other, servings,
                                    calories, prots, fats, carbs, healthscore):
    # Calculating the difference between the expected and actual values
    cal_err = Main.calories * servings[0] + Side.calories * servings[1] + \
              Veg.calories * servings[2] - calories

    pro_err = Main.protein * servings[0] + Side.protein * servings[1] + \
              Veg.protein * servings[2] - prots

    fat_err = Main.fat * servings[0] + Side.fat * servings[1] + \
              Veg.fat * servings[2] - fats

    car_err = Main.carbs * servings[0] + Side.carbs * servings[1] + \
              Veg.carbs * servings[2] - carbs

    hls_err = Main.healthscore * servings[0] + Side.healthscore * servings[1] + \
              Veg.healthscore * servings[2] - healthscore
    try:
        cal_err -= Other.calories * servings[3]
        pro_err -= Other.protein * servings[3]
        fat_err -= Other.fat * servings[3]
        car_err -= Other.carbs * servings[3]
        hls_err -= Other.healthscore * servings[3]
    except:
        print("no other")
    print("cal_err --->", cal_err)
    print("pro_err --->", pro_err)
    print("fat_err --->", fat_err)
    print("car_err --->", car_err)
    print("hls_err --->", hls_err)
    print(" ")


