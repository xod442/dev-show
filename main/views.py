# (C) Copyright 2019 Hewlett Packard Enterprise Development LP.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#  http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# __author__ = "@netwookie"
# __credits__ = ["Rick Kauffman"]
# __license__ = "Apache2.0"
# __version__ = "1.0.0"
# __maintainer__ = "Rick Kauffman"
# __email__ = "rick.a.kauffman@hpe.com"

from flask import Blueprint, render_template, request, redirect, session, url_for, abort
import os
# from werkzeug import secure_filename
from mongoengine import Q
import json
import requests
from database.system import System
from database.creds import Creds
from database.alerts import Alerts
from utilities.get_creds import get
from utilities.save_creds import save
from utilities.save_system import save_system
from utilities.get_system import get_system
from utilities.save_alerts import save_alerts
from utilities.get_alerts import get_alerts
import time
from collections import OrderedDict
from hpOneView.oneview_client import OneViewClient
# from qumulo.rest_client import RestClient
requests.packages.urllib3.disable_warnings()



main_app = Blueprint('main_app', __name__)

@main_app.route('/main', methods=('GET', 'POST'))
@main_app.route('/', methods=('GET', 'POST'))
@main_app.route('/index', methods=('GET', 'POST'))
def main():
    ''' Display login screen
    '''
    # Clear credential database on new session.
    Creds.objects().delete()

    return render_template('main/login.html')

@main_app.route('/help', methods=('GET', 'POST'))
def help():

    return render_template('main/help.html')

@main_app.route('/main_select', methods=('GET', 'POST'))
def main_select():
    '''
    read creds
    '''

    # If this is a POSt it is from the login screen capture creds and save
    if request.method == 'POST':

        #Get creds from login
        ipaddress = request.form['ipaddress'].encode('utf-8')
        user = request.form['user'].encode('utf-8')
        password = request.form['password'].encode('utf-8')


        # Save the record
        try:
            savecreds=save(ipaddress,user,password)
        except:
            error="ERR001 - Failed to save login credentials"
            return render_template('main/dberror.html', error=error)


    # Returning to the main page if HTTP GET pull creds from DB
    creds=get()

    authx = {
        "ip" : creds[0],
        "credentials" : {
            "userName" : creds[1],
            "password" : creds[2]
        }
    }
    # Create client connector
    client = OneViewClient(authx)

    # Get system information
    ov = client.appliance_node_information.get_version()
    #
    uuid=ov['uuid'].encode('utf-8')
    family=ov['family'].encode('utf-8')
    serno=ov['serialNumber'].encode('utf-8')
    model=ov['modelNumber'].encode('utf-8')
    software=ov['softwareVersion'].encode('utf-8')
    build=ov['build'].encode('utf-8')

    # Save the system to mongo
    try:
        savesys=save_system(uuid,family,serno,model,software,build)
    except:
        error="ERR002 - Failed to save system information to mongo"
        return render_template('main/dberror.html', error=error)

    # Get alerts
    out_alerts = []
    ov = client.alerts.get_all()
    for alert in ov:
        severity=alert['severity'].encode('utf-8')
        description=alert['description'].encode('utf-8')
        modified=alert['modified'].encode('utf-8')

        # Save the alerts to mongo
        try:
            savealert=save_alerts(severity,description,modified)
        except:
            error="ERR003 - Failed to save alarm information to mongo"
            return render_template('main/dberror.html', error=error)

        out = [severity,description,modified]
        out_alerts.append(out)

        pad='104.55.322'



    return render_template('main/index.html', uuid=uuid,
                                               family=family,
                                               serno=serno,
                                               model=model,
                                               software=software,
                                               build=build,
                                               out_alerts=out_alerts,
                                               pad=pad)


@main_app.route('/charts', methods=('GET', 'POST'))
def charts():
    '''
    Display Charts
    '''
    return render_template('main/charts.html')

@main_app.route('/maps', methods=('GET', 'POST'))
def maps():
    '''
    Display Maps
    '''
    return render_template('main/maps.html')

@main_app.route('/users', methods=('GET', 'POST'))
def users():
    '''
    Manage Users
    '''
    return render_template('main/manage-users.html')

@main_app.route('/preferences', methods=('GET', 'POST'))
def preferences():
    '''
    Manage Preferences
    '''
    return render_template('main/preferences.html')

@main_app.route('/logout', methods=('GET', 'POST'))
def logout():
    '''
    Logout of system
    '''
    return render_template('main/logout.html')

@main_app.route('/timestamps', methods=('GET', 'POST'))
def timestamps():
    '''
    Get Qumulo Timestamps
    '''

    # Get user informaation
    creds = Creds.objects.first()
    user = creds.user
    password = creds.password
    ipaddress= creds.ipaddress

    columns = ["iops.read.rate", "iops.write.rate",
               "throughput.read.rate", "throughput.write.rate",
               "reclaim.deferred.rate", "reclaim.snapshot.rate"]

    #
    feed = []
    rc = RestClient(ipaddress,8000)
    rc.login(user,password)
    #
    begin_time = int(time.time()) - 60 * 60 * 24
    results = rc.analytics.time_series_get(begin_time = begin_time)
    data = {}
    #
    for i in range(0,len(results[0]['times'])-1):
        ts = results[0]['times'][i]
        data[ts] = [None] * len(columns)

    for series in results:
        if series['id'] not in columns:
            continue
        for i in range(0,len(series['values'])):
            ts = series['times'][i]
            data[ts][columns.index(series['id'])] = series['values'][i]

    for key in data.items():
        tmp=[key[0],key[1][0],key[1][1],key[1][2],key[1][3],key[1][4],key[1][5]]
        if key[1][0] == 0.0 and key[1][1] == 0.0 and key[1][2] == 0.0 and key[1][3] == 0.0 and key[1][4] == 0.0 and key[1][5] == 0.0:
            continue
        feed.append(tmp)



    return render_template('main/index.sm.html', feed=feed)
