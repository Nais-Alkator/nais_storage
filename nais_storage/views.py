from django.shortcuts import render


def view_main_page(request):
	return render(request, "base.html")


def get_order_details(request):
	return render(request, "order_details.html")
