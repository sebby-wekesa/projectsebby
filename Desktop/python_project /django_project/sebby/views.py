from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Flight, Passanger

# Create your views here.
def index(request):
	context = {
		"flights": Flight.objects.all()
	}
	return render (request, "flights/index.html", context)
	
	
def flight(request, flight_id):
	try:
		flight = Flight.objects.get(pk=flight_id) 
	except Flight.DoesNotExist:
		raise Http404("Flight does not exist.")
	context = {
		"flight": flight,
		"passanger": flight.passanger.all(),
		"non_passanger": Passanger.objects.exclude(flights=flight).all()
	}
	return render(request, "flights/flight.html", context)
	
	
def book(request, flight_id):
	try:
		passanger_id = int(request.POST["passanger"])
		passanger = Passanger.objects.get(pk=passanger_id)
		flight = Flight.objects.get(pk=flight_id)
	except KeyError:
		return render(request, "flights/error.html", {"message": "No selection."})
	except Flight.DoesNotExist:
		return render(request, "flights/error.html", {"message": "No flight."})
	except Passanger.DoesNotExist:
		return render(request, "flights/error.html", {"message": "No passanger."})
	passanger.flights.add(flight)
	return HttpResponseRedirect(reverse("flight", args=(flight_id,)))
	

	
	
