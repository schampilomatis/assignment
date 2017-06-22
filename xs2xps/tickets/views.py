from django.shortcuts import render
from django.http import JsonResponse
from django.core.cache import cache
import calendar


def get_ratings_data():
    monthly_ratings = reversed(cache.get("monthly_ratings"))
    res = []

    for monthly_rating in monthly_ratings:
        month = int(monthly_rating["period"].split("-")[1])
        month_abbr = calendar.month_abbr[month]
        res.append({
            "month": month,
            "month_abbr": month_abbr,
            "rating": float(monthly_rating["rating"]),
            "percentage": float(monthly_rating["rating"]) * 50
        })

    return {
        "monthly_ratings": res,
        "recent_ratings": cache.get("recent_ratings"),
    }


def ratings(request):
    return render(request, 'ratings.html',get_ratings_data())


def apiratings(request):
    return get_ratings_data()


def get_tickets_data():
    return {
        "ticket_summaries": cache.get("ticket_summaries"),
        "tickets": cache.get("tickets"),
        "motion": cache.get("motion_detected"),
    }


def tickets(request):
    return render(request, 'tickets.html', get_tickets_data())


def apitickets(request):
    return JsonResponse(get_tickets_data())


def set_motion_detected(request, value):
    if value == 'on':
        cache.set("motion_detected", True)
    elif value == 'off':
        cache.set("motion_detected", False)
    else:
        return JsonResponse({"error": "invalid"})
    return JsonResponse({})

