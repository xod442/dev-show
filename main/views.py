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
from utilities.populate import servers
from utilities.populate import disks
from utilities.populate import sanmanagers
from database.server_hardware import Server_Hardware
from database.disk_hardware import Disk_Hardware
from database.san_managers import San_Managers
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

@main_app.route('/main_load', methods=('GET', 'POST'))
def main_load():
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
    try:
        client = OneViewClient(authx)
    except:
        error="ERR00X - Wrong host, user or password, please try again!"
        return render_template('main/dberror.html', error=error)

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


    # Clear switches database on new session.
    Alerts.objects().delete()

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

    # Populate the rest of the mongo collections
    #------------------------------------------------SERVERS------------------
    # Get and Save Server Hardware
    ov_servers = client.server_hardware.get_all()
    try:
        load_servers = servers(ov_servers)
    except:
        error="ERR004 - Failed to save server hardware information to mongo"
        return render_template('main/dberror.html', error=error)
    #-----------------------------------------------DISKS-----------------
    # Get and Save D3940 Hardware
    ov_disks = client.drive_enclosures.get_all()
    try:
        load_disks = disks(ov_disks)
    except:
        error="ERR005 - Failed to save disk hardware information to mongo"
        return render_template('main/dberror.html', error=error)
    #-----------------------------------------------SAN MANAGERS---------------

    # Get and Save San Managers
    ov_san_managers = client.san_managers.get_all()

    # Clear San Managers database on new session.
    San_Managers.objects().delete()
    count = 0
    for sm in ov_san_managers:
        status=sm['status'].encode('utf-8')
        display=sm['connectionInfo'][count]['displayName'].encode('utf-8')
        name=sm['connectionInfo'][count]['name'].encode('utf-8')
        ipaddress=sm['connectionInfo'][count]['value'].encode('utf-8')
        description=sm['description'].encode('utf-8')
        state=sm['state'].encode('utf-8')
        refresh=sm['refreshState'].encode('utf-8')
        inside=sm['isInternal']

        inside = str("{}").format(sm['isInternal'])

        # Build database entry to save creds
        manager = San_Managers(status=sm['status'].encode('utf-8'),
                              display=sm['connectionInfo'][count]['displayName'].encode('utf-8'),
                              name=sm['connectionInfo'][count]['name'].encode('utf-8'),
                              ipaddress=sm['connectionInfo'][count]['value'].encode('utf-8'),
                              description=sm['description'].encode('utf-8'),
                              state=sm['state'].encode('utf-8'),
                              refresh=sm['refreshState'].encode('utf-8'),
                              inside=inside)


        # out=[status,display,name,ipaddress,description,state,refresh,inside]

        try:
            manager.save()
        except:
            error="SUB-SUB routine- ERR00777 - Failed to save san manager"
            return render_template('main/dberror.html', error=error)

    '''
    try:
        load_san_manager = sanmanagers(ov_sanmanagers)
    except:
        error="ERR005 - Failed to save san manager information to mongo"
        return render_template('main/dberror.html', error=error)
    '''
    #-----------------------------------------------RENDER-----------------
    return render_template('main/index.html', uuid=uuid,
                                               family=family,
                                               serno=serno,
                                               model=model,
                                               software=software,
                                               build=build,
                                               out_alerts=out_alerts,
                                               pad=pad)













@main_app.route('/main_select', methods=('GET', 'POST'))
def main_select():
    '''
    return to the main screen
    '''
    # get system information
    system = System.objects()
    for s in system:
        uuid = s.uuid.encode('utf8')
        family=s.family.encode('utf8')
        serno=s.serno.encode('utf8')
        model=s.model.encode('utf8')
        software=s.software.encode('utf8')
        build=s.build.encode('utf8')

    # Get alerts
    alerts = Alerts.objects()
    out_alerts = []
    for alert in alerts:
        out = [alert.severity,alert.description,alert.modified]
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

@main_app.route('/diskhardware', methods=('GET', 'POST'))
def diskhardware():
    '''
    Display table of the disk hardware
    '''
    disks = Disk_Hardware.objects()

    out_disks = []

    for disk in disks:
        out = [disk.cage,
              disk.serialNumber,
              disk.model,
              disk.rotationalRpms,
              disk.drivePaths,
              disk.firmwareVersion,
              disk.capacity,
              disk.temperature,
              disk.blockSize,
              disk.deviceInterface,
              disk.status,
              disk.driveMedia,
              disk.authentic,
             ]

        out_disks.append(out)

    return render_template('main/diskhardware.html', out_disks=out_disks)

@main_app.route('/serverhardware', methods=('GET', 'POST'))
def serverhardware():
    '''
    Display table of the server hardware
    '''
    servers = Server_Hardware.objects()

    out_servers = []

    for server in servers:
        out = [server.model,
              server.serno,
              server.smodel,
              server.proctype,
              server.name,
              server.sname,
              server.mem,
              server.firmver,
              server.romv]

        out_servers.append(out)

    return render_template('main/serverhardware.html', out_servers=out_servers)

@main_app.route('/sanmanagers', methods=('GET', 'POST'))
def sanmanagers():
    '''
    Display table of the server hardware
    '''
    sanmanagers = San_Managers.objects()

    out_managers = []

    for man in sanmanagers:
        out = [man.status,
              man.display,
              man.name,
              man.ipaddress,
              man.description,
              man.state,
              man.refresh,
              man.inside]

        out_managers.append(out)

    return render_template('main/sanmanagers.html', out_managers=out_managers)


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
