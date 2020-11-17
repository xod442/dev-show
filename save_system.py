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
from database.system import System
import time
from collections import OrderedDict
# from qumulo.rest_client import RestClient
requests.packages.urllib3.disable_warnings()

def save_system(uuid,family,serno,model,software,build):

    # Clear switches database on new session.
    System.objects().delete()


    # Build database entry to save creds
    sys = System(uuid=uuid,family=family,serno=serno,model=model,software=software,build=build)
    # Save the record
    try:
        sys.save()
    except:
        error="SUB-system_save-ERR001 - Failed to save System Information"
        return render_template('main/dberror.html', error=error)

    return
