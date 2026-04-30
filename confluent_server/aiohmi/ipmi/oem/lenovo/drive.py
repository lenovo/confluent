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

drive_fields = (
    inventory.EntryField("index", "B"),
    inventory.EntryField("VendorID", "64s"),
    inventory.EntryField("Size", "I",
                         valuefunc=lambda v: str(v) + " MB"),
    inventory.EntryField("MediaType", "B", mapper={
        0x00: "HDD",
        0x01: "SSD"
    }),
    inventory.EntryField("InterfaceType", "B", mapper={
        0x00: "Unknown",
        0x01: "ParallelSCSI",
        0x02: "SAS",
        0x03: "SATA",
        0x04: "FC"
    }),
    inventory.EntryField("FormFactor", "B", mapper={
        0x00: "Unknown",
        0x01: "2.5in",
        0x02: "3.5in"
    }),
    inventory.EntryField("LinkSpeed", "B", mapper={
        0x00: "Unknown",
        0x01: "1.5 Gb/s",
        0x02: "3.0 Gb/s",
        0x03: "6.0 Gb/s",
        0x04: "12.0 Gb/s"
    }),
    inventory.EntryField("SlotNumber", "B"),
    inventory.EntryField("ControllerIndex", "B"),
    inventory.EntryField("DeviceState", "B", mapper={
        0x00: "active",
        0x01: "stopped",
        0xff: "transitioning"
    }))


def parse_drive_info(raw):
    return inventory.parse_inventory_category_entry(raw, drive_fields)


def get_categories():
    return {
        "drive": {
            "idstr": "Drive {0}",
            "parser": parse_drive_info,
            "command": {
                "netfn": 0x06,
                "command": 0x59,
                "data": (0x00, 0xc1, 0x04, 0x00)
            }
        }
    }
