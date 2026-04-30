# Copyright 2015 Lenovo
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from aiohmi.ipmi.oem.lenovo import inventory

cpu_fields = (
    inventory.EntryField("index", "B"),
    inventory.EntryField("Cores", "B"),
    inventory.EntryField("Threads", "B"),
    inventory.EntryField("Manufacturer", "13s"),
    inventory.EntryField("Family", "30s"),
    inventory.EntryField("Model", "30s"),
    inventory.EntryField("Stepping", "3s"),
    inventory.EntryField("Maximum Frequency", "<I",
                         valuefunc=lambda v: str(v) + " MHz"),
    inventory.EntryField("Reserved", "h", include=False))

cpu_cmd = {
    "lenovo": {
        "netfn": 0x06,
        "command": 0x59,
        "data": (0x00, 0xc1, 0x01, 0x00)},
    "asrock": {
        "netfn": 0x3a,
        "command": 0x50,
        "data": (0x01, 0x01, 0x00)},
}


def parse_cpu_info(raw):
    return inventory.parse_inventory_category_entry(raw, cpu_fields)


def get_categories():
    return {
        "cpu": {
            "idstr": "CPU {0}",
            "parser": parse_cpu_info,
            "command": cpu_cmd,
            "workaround_bmc_bug": lambda t: t == "ami"
        }
    }
