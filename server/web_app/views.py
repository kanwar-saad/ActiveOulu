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
from django.template import RequestContext, loader
from utils import tx_msg_to_worker
from forms import *
# Create message for sending to PMB 
def create_PMB_msg():
    time = None
    device = BTDevice.objects.all()
    for dev in device:
        #print dev.scanTime
        time = dev.scanTime
        break
    if not time:
        return ''
    else:
        msg = 'http://admin:testi123@10.20.20.211/trigger/20?var='
        activity_data = BTActivity.objects.filter(activityTime__exact=time).order_by('devID')
        for act in activity_data:
            msg = msg + str(act.activity) + ','
        msg = msg[0:len(msg)-1]
        return msg

def btScan(request):
    if (request.method == 'GET'):
        user = request.GET.get('user','')
        if (user != 'activeoulu'):
            return HttpResponse('Unauthorized', content_type="text/plain", status=401)
        else:
            api_url = 'http://stats.ubioulu.fi/panoulubt/devices.php?group=1'
            result = requests.get(api_url, headers={'Content-Type': 'application/json'})
            curr_activity = {}
            if not result.json:
                return HttpResponse('PanOulu Server not responding', content_type="text/plain", status=200)
            for r in result.json['result']: curr_activity.update(r)
            print 'Total records fetched : ' + str(len(curr_activity))
            devices = BTDevice.objects.all()
            curr_timestamp = datetime.now()
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
            msg = create_PMB_msg()
            #if msg : tx_msg_to_worker( create_PMB_msg())
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

                now = datetime.now()
                check_date = now - delta
                #print "Check date ", check_date            
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
                    max_date = check_date + (step_delta * (iter))
                    min_date = check_date + (step_delta * (iter-1))
                    observations = (((max_date - min_date).days * 1440) + ((max_date - min_date).seconds/60))/3
                    #print observations
                    #print "min_date ", min_date, "max_date ", max_date
                    
                    if min_date >= now:
                        iter = -1
                        break
                    else:
                        iter = iter + 1

                    activity_data = BTActivity.objects.filter(activityTime__gt=min_date, activityTime__lt=max_date, devID=id)
                    activity_data_count = 0 
                    if activity_data:
                        data_count =  activity_data.count()
                    else:
                        data_count = 0
                    for act in activity_data:
                        activity_data_count += act.activity
                        #print "activities =", act.activity
                    #print activity_data_count
                    if data_count: 
                        act_data_count_avg = round(activity_data_count/float(data_count))
                    else:
                        act_data_count_avg = 0
                    # Create X-axis format
                    str = ''
                    #print unit, step_unit
                    if (unit == 'd') and (step_unit == 'h'): str = max_date.strftime("%I:%M/%d")
                    elif (unit == 'd'): str = max_date.strftime("%d/%m")
                    elif (unit == 'w'): str = max_date.strftime("%A")[0:3] + max_date.strftime("/%d") 
                    elif (unit == 'm'): str = max_date.strftime("%B")[0:3] + max_date.strftime("/%d") 
                    elif (unit == 'y'): str = max_date.strftime("%B")[0:3] + max_date.strftime("/%Y")
                    data_json = {}
                    data_json['label'] = str
                    data_json['value'] = act_data_count_avg
                    act_list.append(data_json)
                    #print str
                    #print activity_data_count, act_data_count_avg
                
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




""" Web App front page serving function """
def index(request):
    return render_to_response('index.html', context_instance=RequestContext(request))



""" feedback results """
def feedback_results(request):
    data = ''
    fb_entries = Feedback.objects.all()
    for f in fb_entries:
       data = data + '\r\n' + \
                        f.q1 + ',' +\
                        f.q2 + ',' + \
                        f.q3_city + ',' + \
                        f.q3_country + ',' + \
                        f.q4 + ',' + \
                        f.q5 + ',' + \
                        f.q5_other + ',' + \
                        f.q6 + ',' + \
                        f.q6_title + ',' + \
                        f.q7.ctime() + ',' + \
                        f.q8 + ',' + \
                        f.q9 + ',' + \
                        f.q10 + ',' + \
                        f.q11 + ',' + \
                        f.q11_why + ',' + \
                        f.q12 + ',' + \
                        f.q12_how + ',' + \
                        f.q13 + ',' + \
                        f.q13_why + ',' + \
                        f.q14 + ',' + \
                        f.q14_which + ',' + \
                        f.q14_how + ',' + \
                        f.q15 + ',' + \
                        f.name + ',' + \
                        f.email + ',' + \
                        f.datetime.ctime()

    fb_entries = Feedback_fi.objects.all()
    for f in fb_entries:
        data = data + '\r\n' + \
                        f.q1 + ',' +\
                        f.q2 + ',' + \
                        f.q3_city + ',' + \
                        f.q3_country + ',' + \
                        f.q4 + ',' + \
                        f.q5 + ',' + \
                        f.q5_other + ',' + \
                        f.q6 + ',' + \
                        f.q6_title + ',' + \
                        f.q7.ctime() + ',' + \
                        f.q8 + ',' + \
                        f.q9 + ',' + \
                        f.q10 + ',' + \
                        f.q11 + ',' + \
                        f.q11_why + ',' + \
                        f.q12 + ',' + \
                        f.q12_how + ',' + \
                        f.q13 + ',' + \
                        f.q13_why + ',' + \
                        f.q14 + ',' + \
                        f.q14_which + ',' + \
                        f.q14_how + ',' + \
                        f.q15 + ',' + \
                        f.name + ',' + \
                        f.email + ',' + \
                        f.datetime.ctime()
                         
    response = HttpResponse(data, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="feedback_results.csv"'
    return response

""" Feedback form - english """
def feedback(request):
    ctx = {}
    if request.method == 'POST':
        
        form = ctx['form'] = FeedbackForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            f = Feedback()
            #test_field = form.cleaned_data['test_field']
            f.q1 = form.cleaned_data['q1']
            f.q2 = form.cleaned_data['q2']
            f.q3_city = form.cleaned_data['q3_city']
            f.q3_country = form.cleaned_data['q3_country']
            f.q4 = form.cleaned_data['q4']
            f.q5 = form.cleaned_data['q5']
            f.q5_other = form.cleaned_data['q5_other']
            f.q6 = form.cleaned_data['q6']
            f.q6_title = form.cleaned_data['q6_title']
            f.q7 = form.cleaned_data['q7']
            f.q8 = form.cleaned_data['q8']
            f.q9 = form.cleaned_data['q9']
            f.q10 = form.cleaned_data['q10']
            f.q11 = form.cleaned_data['q11']
            f.q11_why = form.cleaned_data['q11_why']
            f.q12 = form.cleaned_data['q12']
            f.q12_how = form.cleaned_data['q12_how']
            f.q13 = form.cleaned_data['q13']
            f.q13_why = form.cleaned_data['q13_why']
            f.q14 = form.cleaned_data['q14']
            f.q14_which = form.cleaned_data['q14_which']
            f.q14_how = form.cleaned_data['q14_how']
            f.q15 = form.cleaned_data['q15']
            f.name = form.cleaned_data['name']
            f.email = form.cleaned_data['email']
            f.datetime = datetime.now()
            """
            
            """
            print form.cleaned_data
            f.save()
            return HttpResponseRedirect('/static/thankyou.html') # Redirect after POST
        else:
            print 'form is not valid'
            ctx['error'] = 'Invalid Form Data'
    else:
        ctx['form'] = FeedbackForm() # An unbound form
   
    return render_to_response('feedback.html', ctx,  context_instance=RequestContext(request))


""" Feedback form - Finnish """
def feedback_fi(request):
    ctx = {}
    if request.method == 'POST':
        
        form = ctx['form'] = FeedbackForm_fi(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            f = Feedback_fi()
            #test_field = form.cleaned_data['test_field']
            f.q1 = form.cleaned_data['q1']
            f.q2 = form.cleaned_data['q2']
            f.q3_city = form.cleaned_data['q3_city']
            f.q3_country = form.cleaned_data['q3_country']
            f.q4 = form.cleaned_data['q4']
            f.q5 = form.cleaned_data['q5']
            f.q5_other = form.cleaned_data['q5_other']
            f.q6 = form.cleaned_data['q6']
            f.q6_title = form.cleaned_data['q6_title']
            f.q7 = form.cleaned_data['q7']
            f.q8 = form.cleaned_data['q8']
            f.q9 = form.cleaned_data['q9']
            f.q10 = form.cleaned_data['q10']
            f.q11 = form.cleaned_data['q11']
            f.q11_why = form.cleaned_data['q11_why']
            f.q12 = form.cleaned_data['q12']
            f.q12_how = form.cleaned_data['q12_how']
            f.q13 = form.cleaned_data['q13']
            f.q13_why = form.cleaned_data['q13_why']
            f.q14 = form.cleaned_data['q14']
            f.q14_which = form.cleaned_data['q14_which']
            f.q14_how = form.cleaned_data['q14_how']
            f.q15 = form.cleaned_data['q15']
            f.name = form.cleaned_data['name']
            f.email = form.cleaned_data['email']
            f.datetime = datetime.now()
            #print form.cleaned_data
            f.save()
            return HttpResponseRedirect('/static/thankyou.html') # Redirect after POST
        else:
            print 'form is not valid'
            ctx['error'] = 'Invalid Form Data'
    else:
        ctx['form'] = FeedbackForm_fi() # An unbound form
   
    return render_to_response('feedback_fi.html', ctx,  context_instance=RequestContext(request))
