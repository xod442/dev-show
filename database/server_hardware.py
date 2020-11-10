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


from application import db

class Server_Hardware(db.Document):
    serno = db.StringField(db_field="s", required=True)
    proctype = db.StringField(db_field="p", required=True)
    form = db.StringField(db_field="f", required=True)
    hostname = db.StringField(db_field="h", required=True)
    ipaddress = db.StringField(db_field="i", required=True)
    asset = db.StringField(db_field="a", required=True)
    license = db.StringField(db_field="l", required=True)
    sname = db.StringField(db_field="sn", required=True)
    mem = db.StringField(db_field="m", required=True)
    hostos = db.StringField(db_field="ho", required=True)
    mpmodel = db.StringField(db_field="mpm", required=True)
    type = db.StringField(db_field="t", required=True)
    description = db.StringField(db_field="d", required=True)
    firmver = db.StringField(db_field="fv", required=True)
    vserno = db.StringField(db_field="v", required=True)
    etag = db.StringField(db_field="e", required=True)
    smodel = db.StringField(db_field="sm", required=True)
    power = db.StringField(db_field="po", required=True)
    name = db.StringField(db_field="n", required=True)
    cores = db.StringField(db_field="c", required=True)
    romv = db.StringField(db_field="r", required=True)
    position = db.StringField(db_field="pos", required=True)
    model = db.StringField(db_field="mo", required=True)
