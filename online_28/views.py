from django.shortcuts import render

# Create your views here.


def index(request):
    context={
        "amit":"good",
        "adi":"bad",
        "abhi":"soosso"
    }
    return render(request,'dashboard.html',context)