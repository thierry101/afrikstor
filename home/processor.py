import json
import socket
import datetime
from django.utils import timezone
from django.http import JsonResponse
from settingSite.models import Visitor_Infos
# from django.conf import settings


# import random

def save_visitor_infos(request):
    try:
        #----- get visitor ip -----#
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        #----- check if ip adress is valid -----#
        try:
            socket.inet_aton(ip)
            ip_valid = True
        except socket.error:
            ip_valid = False
        #----- check if ip adress is valid -----#
        if ip_valid:

            present_date = timezone.now()
            ref_date_1 = present_date - datetime.timedelta(days=1)
            ref_date_month = present_date - datetime.timedelta(minutes=43200)
            ref_date_year = present_date - datetime.timedelta(minutes=518400)

            if Visitor_Infos.objects.filter(ip_address=ip, page_visited=request.path, event_date__gte=ref_date_1).count() == 0:
                new_visitor_infos = Visitor_Infos(
                    ip_address=ip,
                    page_visited=request.path,
                    event_date=present_date)
                new_visitor_infos.save()

            if Visitor_Infos.objects.filter(ip_address=ip, page_visited=request.path, event_date__gte=ref_date_1).count() == 1:
                visitor_infos_obj = Visitor_Infos.objects.get(
                    ip_address=ip, page_visited=request.path, event_date__gte=ref_date_1)
                visitor_infos_obj.event_date = present_date
                visitor_infos_obj.save()
    except:
        pass

    context_nb_vistors = 0
    context_nb_vistors_all = 0
    ref_date = present_date - datetime.timedelta(minutes=1440)
    context_nb_vistors = Visitor_Infos.objects.filter(
        event_date__gte=ref_date).values_list('ip_address', flat=True).distinct().count()
    cont_nb_vistors_month = Visitor_Infos.objects.filter(
        event_date__gte=ref_date_month).values_list('ip_address', flat=True).distinct().count()
    cont_nb_vistors_year = Visitor_Infos.objects.filter(
        event_date__gte=ref_date_year).values_list('ip_address', flat=True).distinct().count()
    context_nb_vistors_all += context_nb_vistors
    data = {
        "day_visitor": context_nb_vistors,
        "month_visitors": cont_nb_vistors_month,
        "year_visitors": cont_nb_vistors_year,
        "all_visitors": context_nb_vistors_all,
    },
    return ''
    # return JsonResponse(data, safe=False)
