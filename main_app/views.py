from shutil import unregister_archive_format
from unicodedata import name
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from .models import Coins, Owner, Category, Category
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.

class Home(TemplateView):
    template_name = "home.html"
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context

class About(TemplateView):
    template_name = "about.html"

# class Coin:
#     def __init__(self, name, image, material, origin, weight, year, history):
#         self.name = name
#         self.image = image
#         self.material = material
#         self.origin = origin
#         self.weight = weight
#         self.year = year
#         self.history = history

# coins = [
#     Coin(
#         "Ancient Lydia",
#         "https://www.austincoins.com/media/catalog/product/cache/e3c3418b62b13e389702728a1749ff72/l/y/lydia-croesus-half-stater-au-5-3-obv_1.png",
#         "Silver",
#         "Lydia (Croesus or later)",
#         "4.98g",
#         "561 B.C.",
#         "Over 2,500 years ago, King Croesus of the Lydian Empire was responsible for pushing the evolution of coinage into a new era. Until this point in history, electrum, a naturally occurring alloy of gold and silver, was used for currency. Croesus' genius came in the creation of “a complex interrelated, bimetallic monetary system” using the first ever pure gold and pure silver coins. This system established a silver to gold ratio of 13:1 meaning that thirteen Silver Staters was worth one Gold Stater. The large Staters were complimented by fractional denominations as small as a 1/24th Stater - an expansive, but popular project for set-builders."
#     ),
#     Coin(
#         "St. Gaudens",
#         "https://www.austincoins.com/media/catalog/product/cache/e3c3418b62b13e389702728a1749ff72/1/9/1908_stgaudens_20_ms66_case_2.jpg",
#         "Gold",
#         "United Sates of America",
#         "1oz",
#         "1908",
#         "Augustus Saint-Gaudens sculpted such a beautiful design for the coin that took his name that the U.S. Mint chose to celebrate it with today's Gold American Eagle program. Similarly, today’s Eagle (and other bullion) buyers are still attracted to the $20 Saints due to their familiar design, near one-ounce gold content and 100-year legacy."
#     ),
#     Coin(
#         "Austrian Philharmonics",
#         "https://www.austincoins.com/media/catalog/product/cache/e3c3418b62b13e389702728a1749ff72/1/o/1ozplatphil_2019_front.jpg",
#         "Platinum",
#         "Austria",
#         "1oz",
#         "2019",
#         "The Austrian Mint has long been a standard-bearer in gold and silver bullion coins with their highly popular Philharmonics. In 2016, they finally expanded their line-up with the Platinum Philharmonics. This attractive one-ounce platinum coin features the same award-winning design as seen on the gold and silver Philharmonics with the Great Pipe Organ of Vienna's Golden Concert Hall on the obverse and musical instruments of the famous orchestra on the reverse."
#     ),
#     Coin(
#         "8 Escudo",
#         "https://www.austincoins.com/media/catalog/product/cache/e3c3418b62b13e389702728a1749ff72/1/7/1770-lm-jm-peru-8-esc-au58-holder.png",
#         "Gold",
#         "Peru",
#         "?",
#         "1770",
#         "Outright finest known out of seven total graded for the issue, this gorgeous Peruvian gold 8 Escudo has been certified in NGC About Unc. 58 condition. The overall strike and detail is remarkable for these early Colonial issues and we love the value to be had in these truly rare gold coins. Collectors and investors alike are discovering the value to be had in these Pre-1800 dated gold escudos in high grades, and this finest known example is no exception. Coin shown is the exact coin you will receive."
#     ),
# ]

@method_decorator(login_required, name='dispatch')
class CoinList(TemplateView):
    template_name = "coin_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name")
        if name != None:
            context["coins"] = Coins.objects.filter(name__icontains=name)
            context["header"] = f"Searching for {name}"
        else:
            context["coins"] = Coins.objects.filter(user=self.request.user)
            context["header"] = "Trending Coins"
        return context

class CoinCreate(CreateView):
    model = Coins
    fields = ['name', 'image', 'material', 'origin', 'weight', 'year', 'history']
    template_name = "coin_create.html"
    def form_valid(self,form):
        form.instance.user = self.request.user
        return super(CoinCreate, self).form_valid(form)
    success_url = "/coins/"

class CoinDetail(DetailView):
    model = Coins
    template_name = "coin_detail.html"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context

class CoinUpdate(UpdateView):
    model = Coins
    fields = ['name', 'image', 'material', 'origin', 'weight', 'year', 'history']
    template_name = "coin_update.html"
    success_url = "/coins/"

class CoinDelete(DeleteView):
    model = Coins
    template_name = "coin_delete_confirmation.html"
    success_url = "/coins/"

class OwnerCreate(View):
    def post(self, request, pk):
        name = request.POST.get("name")
        location = request.POST.get("location")
        asking_price = request.POST.get("asking_price")
        coins = Coins.objects.get(pk=pk)
        Owner.objects.create(name=name, location=location, asking_price=asking_price, coins=coins)
        return redirect('coin_detail', pk=pk)

class CategoryCoinAssoc(View):
    def get(self, request, pk, coins_pk):
        assoc = request.GET.get("assoc")
        if assoc == "remove":
            Category.objects.get(pk=pk).coins.remove(coins_pk)
        return redirect('home')
class Signup(View):
    def get(self, request):
        form = UserCreationForm()
        context = {"form": form}
        return render(request, "registration/signup.html", context)
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("coin_list")
        else: 
            context = {"form": form}
            return render(request, "registration/signup.html", context)

