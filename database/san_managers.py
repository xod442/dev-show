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

class San_Managers(db.Document):
    status = db.StringField(db_field="s", required=True)
    display = db.StringField(db_field="d", required=True)
    name = db.StringField(db_field="n", required=True)
    ipaddress = db.StringField(db_field="i", required=True)
    description = db.StringField(db_field="de", required=True)
    state = db.StringField(db_field="st", required=True)
    refresh = db.StringField(db_field="r", required=True)
    inside = db.StringField(db_field="in", required=True)
