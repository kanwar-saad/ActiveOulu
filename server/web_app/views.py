import os, sys, time, pprint
from datetime import *
from time import gmtime, strftime
from web_app.models import *
import json, requests
from django.http import *
import uuid
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.db.models import *




resp = '<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><soapenv:Body><notifications xmlns="http://soap.sforce.com/2005/09/outbound"><Ack>true</Ack></notifications></soapenv:Body></soapenv:Envelope>'


@csrf_exempt
def outbound_message_handler(request, tenantName):

	msg = request.read()
	print msg

	return HttpResponse(resp)	








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
        devices = BTDevice.objects.all().order_by('devID')

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

        activity_data = BTActivity.objects.filter(activityTime__exact=time).order_by('devID')

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


def btActivityHistory(request):
    result = {}
    if (request.method == 'GET'):
        # Get parameters
        id = request.GET.get('id', '')
        time = request.GET.get('t', '')
        step_str = request.GET.get('step', '')

        if (id and time and step_str):
            device = BTDevice.objects.filter(devID=id)
            t = time[0:len(time)-1]
            unit = time[len(time)-1]
            step = int(step_str[0:len(step_str)-1])
            step_unit = step_str[len(step_str)-1]
            time = int(t)

            step_delta = ''
            delta = ''
            if (not step or not time or not unit or not step_unit):
                print "Error in parsing input time parameters"
            else:
                if (step_unit == 'h'): step_delta = timedelta(hours=step)
                if (step_unit == 'd'): step_delta = timedelta(days=step)
                if (step_unit == 'w'): step_delta = timedelta(weeks=step)
                if (step_unit == 'm'): step_delta = timedelta(days=step*30)
                
                if (unit == 'd'): delta = timedelta(days=time) 
                if (unit == 'w'): delta = timedelta(weeks=time) 
                if (unit == 'm'): delta = timedelta(days=time*30) 
                if (unit == 'y'): delta = timedelta(days=time*365)

                now = datetime.datetime.now()
                check_date = now - delta
                print "Check date ", check_date            
            if (not delta or not step_delta):
                result['error'] = 'Error in Time Bound Calculation'
                print 'Error in Time Bound Calculation'
            elif (len(device) == 0):
                result['error']  = 'No device Found'
            else:
                result['device_id'] = device[0].devID
                result['device_name'] = device[0].devName
                
                iter = 0
                act_list = []
                while (iter != -1):
                    max_date = check_date + (step_delta * (iter+1))
                    min_date = check_date + (step_delta * iter)
                    print "min_date ", min_date, "max_date ", max_date
                    
                    if min_date >= now:
                        iter = -1
                        break
                    else:
                        iter = iter + 1

                    activity_data_count = BTActivity.objects.filter(activityTime__gt=min_date, activityTime__lt=max_date, devID=id).count()

                    # Create X-axis format
                    str = ''
                    print unit, step_unit
                    if (unit == 'd') and (step_unit == 'h'): str = max_date.strftime("%I:%M/%d")
                    if (unit == 'd'): str = max_date.strftime("%d/%m")
                    if (unit == 'w'): str = max_date.strftime("%A")[0:3] + max_date.strftime("/%d") 
                    if (unit == 'm'): str = max_date.strftime("%B/%d") 
                    if (unit == 'y'): str = max_date.strftime("%B/%Y")
                    data_json = {}
                    data_json['label'] = str
                    data_json['value'] = activity_data_count
                    act_list.append(data_json)
                    print str
                    print activity_data_count
                
                result['history'] = act_list
                result_json = json.dumps(result)
                return HttpResponse(result_json, content_type='application/json', status=200)

 
                #activity_data = BTActivity.objects.filter(activityTime__exact=time)               

        else:   # return cumulative result
           result['error'] =  'no args' 

        result_json = json.dumps(result)        
        return HttpResponse(result_json, content_type='application/json', status=200) 
         
    else:
        result['error'] = 'Invalid Request'
        result_json = json.dumps(result)
        return HttpResponse(result_json, content_type='application/json', status=400)


	
