from django.db import models
from django.contrib.auth.models import User
from food.models import Food
from datetime import datetime


class Plan(models.Model):
    name = models.CharField(max_length=45)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now)  # when created

    def __str__(self):
        return self.name


class Meal(models.Model):
    index = models.IntegerField(null=True)  # order number in the plan
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    food = models.ManyToManyField(Food, through='Meal_has_food')

    def __str__(self):
        return "{}--{}".format(self.plan, self.index)


class Meal_has_Food(models.Model):  # intermediary model (junction table)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    portion_size = models.IntegerField()

    def __str__(self):  # str help work with normalized data
        if self.food.unit == "null":
            unit = ""
        else:
            unit = self.food.unit
        return "{}--{} {}{}".format(self.meal, self.food,
                                    self.portion_size, unit)
        # example str: "TESTPLAN--3--Tomato sauce 30g"

