from celery import shared_task
from .xps_connection import XPSClient
from django.core.cache import cache
from ..notificare.notificare import NotificareManager

@shared_task()
def get_xps_data_from_ws():
    ticket_summaries = XPSClient.call_action('tck', 'client_summaries_pull')["data"]["summaries"][0]
    ticket_summaries["over_deadline"] = str(int(ticket_summaries["open"]) - int(ticket_summaries["deadline_open_resolved_within"]))

    recent_ratings = XPSClient.call_action('tck', 'client_ratings_recent_pull')["data"]["ratings"]
    monthly_ratings = XPSClient.call_action('tck', 'client_ratings_monthly_pull')["data"]["ratings"]
    tickets = XPSClient.call_action('tck', 'tickets_pull', params={'filter_status_translated': 'open'})['data']['tickets']

    notify(ticket_summaries)
    cache.set('tickets', tickets, timeout=None)
    cache.set('ticket_summaries', ticket_summaries, timeout=None)
    cache.set('recent_ratings', recent_ratings, timeout=None)
    cache.set('monthly_ratings', monthly_ratings, timeout=None)


def notify(new_ticket_summaries):

    existing_xps_data = cache.get("ticket_summaries") or {}

    if existing_xps_data.get("new", None) is not None and int(existing_xps_data["new"]) < int(new_ticket_summaries["new"]):
        print("SENDING NOTIFICATION FOR NEW TICKET")
        notify_new(int(new_ticket_summaries["new"]) - int(existing_xps_data["new"]))

    if existing_xps_data.get("over_deadline", None) is not None and int(existing_xps_data["over_deadline"]) < int(new_ticket_summaries["over_deadline"]):
        print("SENDING NOTIFICATION FOR OVER DEADLINE TICKET")
        notify_over_deadline(int(new_ticket_summaries["new"]) - int(existing_xps_data["new"]))


def notify_new(count):
    return NotificareManager.send_notification_to_all("You have {} new tickets".format(count))


def notify_over_deadline(count):
    return NotificareManager.send_notification_to_all("{} tickets went out of deadline".format(count))
