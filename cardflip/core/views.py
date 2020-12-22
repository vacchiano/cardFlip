from django.shortcuts import render
from django.http import HttpResponse
from .script import webScrape

# Create your views here.
def index(request):
    context = {}
    return render(request, 'core/index.html', context)

def about(request):
    context = {}
    return render(request, 'core/about.html', context)

def results(request):
    if request.method == "POST":
        query = ""
        request.session['player_name'] = request.POST['player_name']
        query += " " + request.POST['player_name']

        query += " " + request.POST['card_keyword']
        request.session['keyword'] = request.POST['card_keyword']

        query += " " + request.POST['card_brand']
        request.session['brand'] = request.POST['card_brand']

        query += " " + request.POST['card_year']
        request.session['year'] = request.POST['card_year']

        request.session['card_psa'] = request.POST.get('card_psa', '')
        psa = request.POST.get('card_psa', '')
        if (psa != ''):
            query += " PSA" + psa
        
        query = query.replace("  ", " ")
        query = query.replace(" ", "+")
        data = webScrape(query)
        request.session['img_url'] = data[0]
        request.session['avg_price'] = data[1]

    context = {}
    return render(request, 'core/results.html', context)