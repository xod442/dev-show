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

class Disk_Hardware(db.Document):
    serialNumber = db.StringField(db_field="s", required=True)
    model = db.StringField(db_field="m", required=True)
    authentic = db.StringField(db_field="a", required=True)
    driveMedia = db.StringField(db_field="dm", required=True)
    status = db.StringField(db_field="st", required=True)
    deviceInterface = db.StringField(db_field="di", required=True)
    state = db.StringField(db_field="sa", required=True)
    blockSize = db.StringField(db_field="b", required=True)
    temperature = db.StringField(db_field="t", required=True)
    capacity = db.StringField(db_field="c", required=True)
    firmwareVersion = db.StringField(db_field="f", required=True)
    drivePaths = db.StringField(db_field="p", required=True)
    rotationalRpms = db.StringField(db_field="r", required=True)
    cage = db.StringField(db_field="d", required=True)
