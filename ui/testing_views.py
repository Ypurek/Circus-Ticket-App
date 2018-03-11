from django.shortcuts import render
from core import processing, forms


def service_view(request):
    return render(request, 'testing/index.html')


def credit_card_view(request):
    form = forms.CreditCardForm()

    if request.method == 'POST':
        form = forms.CreditCardForm(request.POST)
        if form.is_valid():
            processing.generate_credit_cards(form.cleaned_data['amount'] or 1000)

    context = {'credit_cards': processing.get_credit_card_list(),
               'form': form}

    return render(request, 'testing/credit_cards.html', context)


def discount_view(request):
    form = forms.DiscountForm()

    if request.method == 'POST':
        form = forms.DiscountForm(request.POST)
        if form.is_valid():
            processing.generate_discount_code(percent=form.cleaned_data['percent'] or 5, code='')

    context = {'discounts': processing.get_discounts_list(),
               'form': form}

    return render(request, 'testing/discounts.html', context)


def ticket_history_view(request, number=1):
    if number < 1:
        number = 1
    LIM = 10
    records = processing.get_ticket_history()
    num = int(len(records) / LIM)
    if num == 0:
        context = {'history': records}
    else:
        context = {'history': records[(number-1)*LIM:number*LIM],
                   'pages': [x+1 for x in range(num+1)],
                   'current': number}

    return render(request, 'testing/ticket_history.html', context)