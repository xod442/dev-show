# -*- coding: utf-8 -*-
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
# __maintainer__ = "Rick Kauffman"
# __email__ = "rick.a.kauffman@hpe.com".


from flask import Blueprint, render_template, request, redirect, session, url_for, abort
import os
# from werkzeug import secure_filename
from mongoengine import Q
import json
import requests
# Add additional mongo collections here
from database.server_hardware import Server_Hardware
# import time
# from collections import OrderedDict
# from qumulo.rest_client import RestClient
requests.packages.urllib3.disable_warnings()

def servers(ov_servers):

    # Clear switches database on new session.
    Server_Hardware.objects().delete()

    # Load server into mongo database
    for server in ov_servers:
        # Mongo collection will not allow blank fields
        if server['processorType'] == None:
            server['processorType'] = '-'
        if server['formFactor'] == None:
            server['formFactor'] = '-'
        if server['assetTag'] == None:
            server['assetTag'] = '-'
        if server['serverName'] == None:
            server['serverName'] = '-'
        if server['memoryMb'] == None:
            server['memoryMb'] = '-'
        if server['description'] == None:
            server['description'] = '-'
        if server['virtualSerialNumber'] == None:
            server['virtualSerialNumber'] = '-'
        if server['romVersion'] == None:
            server['romVersion'] = '-'

        # Build database entry to save creds
        serve = Server_Hardware(serno=server['serialNumber'].encode('utf-8'),
                                proctype = server['processorType'],
                                form = server['formFactor'],
                                hostname = server['mpHostInfo']['mpHostName'].encode('utf-8'),
                                ipaddress = server['mpHostInfo']['mpIpAddresses'][0]['address'].encode('utf-8'),
                                asset = server['assetTag'],
                                license = server['licensingIntent'].encode('utf-8'),
                                sname = server['serverName'],
                                mem = server['memoryMb'],
                                hostos = str(server['hostOsType']),
                                mpmodel = server['mpModel'].encode('utf-8'),
                                type = server['type'].encode('utf-8'),
                                description = server['description'],
                                firmver = server['mpFirmwareVersion'].encode('utf-8'),
                                vserno = server['virtualSerialNumber'],
                                etag = server['eTag'].encode('utf-8'),
                                smodel = server['shortModel'].encode('utf-8'),
                                power = server['powerState'].encode('utf-8'),
                                name = server['name'].encode('utf-8'),
                                cores = str(server['processorCoreCount']),
                                romv = server['romVersion'],
                                position = str(server['position']),
                                model = server['model'].encode('utf-8'))

        # Save the record
        try:
            serve.save()
        except:
            error="SUB-SUB routine- ERR00100 - Failed to save server_harware"
            return render_template('main/dberror.html', error=error, serve=serve)
    return
