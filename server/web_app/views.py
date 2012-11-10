import os, sys, time, pprint
from datetime import *
from time import gmtime, strftime
from web_app.models import *
import json, requests
from django.http import *
import uuid
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt


def btScan(request):
    if (request.method == 'GET'):
        user = request.GET.get('user','')
        if (user != 'activeoulu'):
            return HttpResponse('Unauthorized', content_type="text/plain", status=401)
        else:
            api_url = 'http://stats.ubioulu.fi/panoulubt/devices.php?group=1'
            result = requests.get(api_url, headers={'Content-Type': 'application/json'})
            curr_activity = {}
            for r in result.json['result']: curr_activity.update(r)
            print 'Total records fetched : ' + str(len(curr_activity))
            devices = BTDevice.objects.all()
            curr_timestamp = datetime.datetime.now()
            for dev in devices:
                users = 0
                if (curr_activity.get(str(dev.devID),'') != ''):
                    print "Data Received for " + str(dev.devID)
                    users = curr_activity.get(str(dev.devID),'')

                # Create Activity History Record
                bta = BTActivity(devID=dev.devID, activityTime=curr_timestamp, activity=users)
                bta.save()
                # Update last scantime field in device info
                dev.scanTime = curr_timestamp
                dev.save()
            return HttpResponse(result.text, content_type="text/plain", status=200)
    else:
        result = {}
        result['error'] = 'Invalid Request'
        result_json = json.dumps(result)
        return HttpResponse(result_json, content_type='application/json', status=400)




def btDevices(request):
    result = {}
    if (request.method == 'GET'):
        devices = BTDevice.objects.all()

        dev_list = []
        for dev in devices:
            dev_json = {}
            dev_json['id'] = dev.devID
            dev_json['name'] = dev.devName
            dev_json['longitude'] = dev.devLocLong
            dev_json['latitude'] = dev.devLocLat
            dev_list.append(dev_json)
        
        result['devices'] = dev_list
         
        result_json = json.dumps(result)
        return HttpResponse(result_json, content_type='application/json', status=200) 
    else:
        result['error'] = 'Invalid Request'
        result_json = json.dumps(result)
        return HttpResponse(result_json, content_type='application/json', status=400)



def btActivity(request):
    result = {}
    if (request.method == 'GET'):
        # Get a single device only to fetch the last scan timestamp
        device = BTDevice.objects.all()
        for dev in device:
            #print dev.scanTime
            time = dev.scanTime
            break

        activity_data = BTActivity.objects.filter(activityTime__exact=time)

        act_list = []
        for act in activity_data:
            #print str(act.devID) + " " + str(act.activity)
            act_json = {}
            act_json['id'] = act.devID
            act_json['count'] = act.activity
            act_list.append(act_json)
        
        result['activity'] = act_list
        result['scan_time'] = str(time)
        result_json = json.dumps(result)
        return HttpResponse(result_json, content_type='application/json', status=200) 
    else:
        result['error'] = 'Invalid Request'
        result_json = json.dumps(result)
        return HttpResponse(result_json, content_type='application/json', status=400)

