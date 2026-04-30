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


dimm_fields = (
    inventory.EntryField("index", "B"),
    inventory.EntryField("manufacture_location", "B"),
    inventory.EntryField("channel_number", "B"),
    inventory.EntryField("module_type", "10s"),
    inventory.EntryField("ddr_voltage", "10s"),
    inventory.EntryField("speed", "<h",
                         valuefunc=lambda v: str(v) + " MHz"),
    inventory.EntryField("capacity_mb", "<h",
                         valuefunc=lambda v: v * 1024),
    inventory.EntryField("manufacturer", "30s"),
    inventory.EntryField("serial", ">I",
                         valuefunc=lambda v: hex(v)[2:]),
    inventory.EntryField("model", "21s"),
    inventory.EntryField("reserved", "h", include=False)
)

dimm_cmd = {
    "lenovo": {
        "netfn": 0x06,
        "command": 0x59,
        "data": (0x00, 0xc1, 0x02, 0x00)},
    "asrock": {
        "netfn": 0x3a,
        "command": 0x50,
        "data": (0x01, 0x02, 0x01)},
}


def parse_dimm_info(raw):
    return inventory.parse_inventory_category_entry(raw, dimm_fields)


def get_categories():
    return {
        "dimm": {
            "idstr": "DIMM {0}",
            "parser": parse_dimm_info,
            "command": dimm_cmd,
            "workaround_bmc_bug": lambda t: True
        }
    }
