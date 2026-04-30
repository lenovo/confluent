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


raid_controller_fields = (
    inventory.EntryField("ControllerID", "I"),
    inventory.EntryField("AdapterType", "B", mapper={
        0x00: "Unknown",
        0x01: "RAIDController"
    }),
    inventory.EntryField("SupercapPresence", "B", mapper={
        0x00: "Absent",
        0x01: "Present"
    }),
    inventory.EntryField("FlashComponent1Name", "16s"),
    inventory.EntryField("FlashComponent1Version", "64s"),
    inventory.EntryField("FlashComponent2Name", "16s"),
    inventory.EntryField("FlashComponent2Version", "64s"),
    inventory.EntryField("FlashComponent3Name", "16s"),
    inventory.EntryField("FlashComponent3Version", "64s"),
    inventory.EntryField("FlashComponent4Name", "16s"),
    inventory.EntryField("FlashComponent4Version", "64s"),
    inventory.EntryField("FlashComponent5Name", "16s"),
    inventory.EntryField("FlashComponent5Version", "64s"),
    inventory.EntryField("FlashComponent6Name", "16s"),
    inventory.EntryField("FlashComponent6Version", "64s"),
    inventory.EntryField("FlashComponent7Name", "16s"),
    inventory.EntryField("FlashComponent7Version", "64s"),
    inventory.EntryField("FlashComponent8Name", "16s"),
    inventory.EntryField("FlashComponent8Version", "64s")
)


def parse_raid_controller_info(raw):
    return inventory.parse_inventory_category_entry(
        raw, raid_controller_fields)


def get_categories():
    return {
        "raid_controller": {
            "idstr": "RAID Controller {0}",
            "parser": parse_raid_controller_info,
            "countable": False,
            "command": {
                "netfn": 0x06,
                "command": 0x59,
                "data": (0x00, 0xc4, 0x00, 0x00)
            }
        }
    }
