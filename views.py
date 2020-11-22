from django.shortcuts import render, redirect
from .models import Category
import requests
from .models import Profile, life, Category, FoodAnalysis
from django.contrib import messages
from datetime import date

# Create your views here.
def index(request):
    b11 = Profile.objects.filter(user=request.user)
    for k in b11:
        if date.today() > k.date:
            FoodAnalysis.objects.filter(user=request.user).delete()
            k.date = date.today()
            k.save(update_fields=["date"])
    if request.method == "POST":
        foods = request.POST.get("food")
        quan = request.POST.get("quantity")
        url = "https://api.nutritionix.com/v1_1/search/{}?results=0:20&fields=item_name,nf_calories&appId=7303c6c9&appKey=1cc35120ce7c46e633cf2e8a320e9f3e"
        r = requests.get(url.format(foods)).json()
        if len(r["hits"]) == 0:
            messages.success(request, f"This type of food does not Exist")
            return render(request, "calorie/index.html")
        else:
            cal = r["hits"][0]["fields"]["nf_calories"] * float(quan)
            a = Profile.objects.filter(user=request.user)
            b = a[0].age
            c = a[0].sex
            d = a[0].lifestyle
            e = a[0].category
            g = a[0].Height
            h = a[0].target
            if str(c) == "male":
                bmr = 655 + (9.6 * h) + (1.8 * g) - (4.7 * b)
                if str(d) == "Sedentary":
                    intake = bmr * (1.2)
                elif str(d) == "Somewhat-active":
                    intake = bmr * (1.55)
                else:
                    intake = bmr * (1.9)
            else:
                bmr = 66 + (13.7 * h) + (5 * g) - (6.8 * b)
                if str(d) == "Sedentary":
                    intake = bmr * (1.2)
                elif str(d) == "Somewhat-active":
                    intake = bmr * (1.55)
                else:
                    intake = bmr * (1.9)
            if str(e) == "strength":
                intake = intake + 60
            elif str(e) == "weightloss":
                intake = intake + 100
            elif str(e) == "leanbody":
                intake = intake + 70
            elif str(e) == "musclebuilding":
                intake = intake + 80
            elif str(e) == "ketodiet":
                intake = intake + 90
            else:
                intake = intake + 50
            a = FoodAnalysis(Name=foods, Quantity=quan, user=request.user, calorie=cal)
            a.save()
            example = FoodAnalysis.objects.filter(user=request.user)
            sums = 0
            for i in example:
                sums = sums + i.calorie
            intakes = intake - sums
            if intakes < 0:
                intakes = 0
        return render(request, "calorie/index.html", {"sums": sums, "intakes": intakes})
    else:
        a = Profile.objects.filter(user=request.user)
        b = a[0].age
        c = a[0].sex
        d = a[0].lifestyle
        e = a[0].category
        g = a[0].Height
        h = a[0].target
        if str(c) == "male":
            bmr = 655 + (9.6 * h) + (1.8 * g) - (4.7 * b)
            if str(d) == "Sedentary":
                intake = bmr * (1.2)
            elif str(d) == "Somewhat-active":
                intake = bmr * (1.55)
            else:
                intake = bmr * (1.9)
        else:
            bmr = 66 + (13.7 * h) + (5 * g) - (6.8 * b)
            if str(d) == "Sedentary":
                intake = bmr * (1.2)
            elif str(d) == "Somewhat-active":
                intake = bmr * (1.55)
            else:
                intake = bmr * (1.9)
        if str(e) == "strength":
            intake = intake + 60
        elif str(e) == "weightloss":
            intake = intake + 100
        elif str(e) == "leanbody":
            intake = intake + 70
        elif str(e) == "musclebuilding":
            intake = intake + 80
        elif str(e) == "ketodiet":
            intake = intake + 90
        else:
            intake = intake + 50
        example = FoodAnalysis.objects.filter(user=request.user)
        sums = 0
        for i in example:
            sums = sums + i.calorie
        intakes = intake - sums
        if intakes < 0:
            intakes = 0
        return render(request, "calorie/index.html", {"sums": sums, "intakes": intakes})
    return render(request, "calorie/index.html")


def profile(request):
    name = request.user
    h = Profile.objects.filter(user=name)
    e = h[0]
    a=e.Height
    b=e.Weight
    bmi=(b/(a*a))*(10000)
    ideal=((2.2)*bmi+((3.5*bmi)*((a/100)-1.5)))
    if request.method == "POST":
        ee = request.POST.get("tweight")
        if(int(ee)-int(ideal)>10 or int(ee)-int(ideal)<-10):
            messages.success(request,f'No to be healthy your target weight should not be this much.')
            return render(request,'calorie/profile.html')
        else:
            e.target = ee
            e.save(update_fields=["target"])
            return redirect("index")
    return render(request, "calorie/profile.html",{'ideal':ideal})

def loginfinal(request):
    a = Profile.objects.filter(user=request.user)
    g = len(a)
    if g == 0:
        return redirect("plans")
    else:
        return redirect("index")


def plans(request):
    a = Category.objects.all()
    return render(request, "calorie/plans.html", {"a": a})


def firstprofile(request, pd):
    a = Category.objects.all()
    a1 = life.objects.all()
    name = request.user
    plan = a[pd - 1]
    h = Profile.objects.filter(user=name)
    g = len(h)
    if request.method == "POST":
        b = request.POST.get("username")
        c = request.POST.get("weight")
        d = request.POST.get("height")
        e = request.POST.get("plans")
        gg = request.POST.get("gender")
        gg1 = request.POST.get("age")
        gg2 = request.POST.get("brow")
        if int(c) < 20 or int(c) > 200:
            messages.success(request, f"Invalid Height")
            return render(request, "calorie/plans.html")
        elif int(d) < 80 or int(d) > 250:
            messages.success(request, f"Invalid Weight")
            return render(request, "calorie/plans.html")
        elif int(gg1) < 4 or int(gg1) > 100:
            messages.success(request, f"Below 4 Years of age member not allowed")
            return render(request, "calorie/plans.html")
        else:
            f = Profile(
                Height=d, Weight=c, category=e, user=b, sex=gg, age=gg1, lifestyle=gg2
            )
            f.save()
        return redirect("profile")
    return render(
        request,
        "calorie/firstprofile.html",
        {"name": name, "plan": plan, "g": g, "a1": a1})