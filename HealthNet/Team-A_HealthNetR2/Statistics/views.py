from django.shortcuts import render, HttpResponseRedirect, render_to_response
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
import time
import datetime

import logging

# Create your views here.

dlogger = logging.getLogger('debug')

def index(request):
    if not request.user.is_authenticated() or request.user.profile.role != "Admin":
        return HttpResponseRedirect(reverse('user:login'))
    else:
        return render(request, "Statistics/index.html")

def dates(request):
    if not request.user.is_authenticated() or request.user.profile.role != "Admin":
        return HttpResponseRedirect(reverse('user:login'))
    else:
        beg_date = beg_date=datetime.datetime.now() - datetime.timedelta(days=30 )
        beg_date = beg_date.strftime("%d/%b/%Y %H:%M:%S")
        end_date = datetime.datetime.now().strftime("%d/%b/%Y %H:%M:%S")
        return render(request, "Statistics/logs.html", {'beg_date':beg_date,
                                                        'end_date':end_date})


def display_logs(request, beg_date=datetime.datetime.now() - datetime.timedelta(days=30 ), end_date=datetime.datetime.now() ):
                    #beg_date=time.strptime("05/May/2015 12:00:00", "%d/%b/%Y %H:%M:%S"),
                          #end_date=time.strptime("25/May/2015 12:00:00", "%d/%b/%Y %H:%M:%S")):
    entries = []
    for line in open('Statistics/healthnet.log'):
        tokens = line.strip('[').replace(']', '').split()
        if len(tokens) > 5:
            user = tokens[4]
            date = tokens[0] + ' ' + tokens[1]
            description = date + ' ' + user + ' '
            for token in tokens[5:]:
                description += token + " "
            dlogger.debug(description)

            user = User.objects.get(username=user)
            date = datetime.datetime.strptime(date, "%d/%b/%Y %H:%M:%S")

            if date >= beg_date and date <= end_date:
                entries.append( description )

           # creation_time = time.strptime(creation_time, "%H:%M:%S")



    return render(request, "Statistics/results.html", {'entries':entries})
