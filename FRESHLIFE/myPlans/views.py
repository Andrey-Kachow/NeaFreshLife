from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from planner.models import Plan


def user_plans(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/accounts/login')
    # user plans from latest to oldest
    plans = request.user.plan_set.all().order_by("-date")
    context = {
        'plans': plans,
    }
    return render(request, "myPlans/plans.html", context)


def user_plan(request, index):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/accounts/login')
    # taking one element from user plans (from latest to oldest)
    # 1 is subtracted from index, because it starts from 0, while
    # forloop counter starts from 1
    plan = request.user.plan_set.all().order_by("-date")[index - 1]
    context = {
        "plan": plan,
        "meals": plan.meal_set.all().order_by("index")
    }
    return render(request, "myPlans/plan.html", context)


def delete_plan(request, pk):
    Plan.objects.get(pk=pk).delete()  # finding plan by pk and deleting it
    return redirect("myPlans:plans")
    # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

