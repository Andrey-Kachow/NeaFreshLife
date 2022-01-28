from django.db import models
from django.contrib.auth.models import User
import pickle


class Food(models.Model):
    TYPE_CHOICES = (
        ("M", "Main"),
        ("S", "Side"),
        ("V", "Vegetables"),
        ("O", "Other")
    )
    name = models.CharField(max_length=45)
    calories = models.IntegerField()

    fat = models.DecimalField(max_digits=3, decimal_places=1)
    saturated_fat = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    cholesterol = models.DecimalField(max_digits=4, decimal_places=2, null=True)  # in grams
    monounsaturated = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    polyunsaturated = models.DecimalField(max_digits=3, decimal_places=1, null=True)

    carbs = models.DecimalField(max_digits=3, decimal_places=1)
    sugars = models.DecimalField(max_digits=3, decimal_places=1)
    fibre = models.DecimalField(max_digits=3, decimal_places=1)

    protein = models.DecimalField(max_digits=3, decimal_places=1)
    protein_quality = models.IntegerField(null=True)  # protein efficiency

    gi = models.IntegerField()
    healthscore = models.IntegerField()
    type = models.CharField(max_length=45, choices=TYPE_CHOICES)
    unit = models.CharField(max_length=45, default="g")

    image = models.ImageField(blank=True, upload_to="images/food/")

    loved_by = models.ManyToManyField(User,
                                      blank=True,
                                      related_name="favourite_food")
    ignored_by = models.ManyToManyField(User,
                                        blank=True,
                                        related_name="ignored_food")
    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    @property  # energy in joules
    def joules(self): return int(self.calories * 4.2)

    @property  # the value of protein which has proper amino acid content
    def prot(self):
        try:
            return self.protein * self.protein_quality / 100
        except TypeError:
            return None

    @property
    def protein_efficiency(self):
        return str(self.protein_quality) + "%"

    @property
    def cholesterol_mg(self):
        try:
            return int(self.cholesterol * 1000)
        except TypeError:
            return None



# ----------------------------------
def fix_calories():  # Makes sure that the calories value fits the macronutrient content
    for item in Food.objects.all():
        old = item.calories
        item.calories = item.protein * 4 + item.carbs * 4 + item.fat * 9
        item.save()
        print(item, old, "-->", item.calories)


# Not longer 100% legit
def Save_as_text_file():
    print("JOPA")
    f = open("food.txt", "w")
    f.write("__________________________________________\n")
    for food in Food.objects.all():
        f.write("\n")
        f.write("{}:\n".format(food.name))
        f.write("Energy ---------- {}\n".format(food.calories))
        f.write("Fat ------------- {}\n".format(food.fat))
        f.write("Carbs ----------- {}\n".format(food.carbs))
        f.write("Sugar ----------- {}\n".format(food.sugars))
        f.write("Fiber ----------- {}\n".format(food.fibre))
        f.write("Protein --------- {}\n".format(food.protein))
        f.write("\n")
        f.write("Gi -------------- {}\n".format(food.gi))
        f.write("Healthscore ----- {}\n".format(food.healthscore))
        f.write("Type ------------ {}\n".format(food.type))
        f.write("Unit ------------ {}\n".format(food.unit))
        f.write("\n")
        f.write("__________________________________________\n")
        print("Added {} to food.txt".format(food.name))
    f.close()
    print("Done")

def Save_as_binary_file():
    f = open("food" + ".gme", "wb")
    save = pickle.Pickler(f).dump  # writing long code as save
    for food in Food.objects.all():
        save(food.name)
        save(food.calories)
        save(food.fat)
        save(food.carbs)
        save(food.sugars)
        save(food.fibre)
        save(food.protein)
        save(food.gi)
        save(food.healthscore)
        save(food.type)
        save(food.unit)
        save(food.image)
        print("Added {} to food.gme".format(food.name))
    f.close()

