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

pci_fields = (
    inventory.EntryField("index", "B"),
    inventory.EntryField("PCIType", "B", mapper={
        0x0: "On board slot",
        0x1: "Riser Type 1",
        0x2: "Riser Type 2",
        0x3: "Riser Type 3",
        0x4: "Riser Type 4",
        0x5: "Riser Type 5",
        0x6: "Riser Type 6a",
        0x7: "Riser Type 6b",
        0x8: "ROC",
        0x9: "Mezz"
    }),
    inventory.EntryField("BusNumber", "B"),
    inventory.EntryField("DeviceFunction", "B"),
    inventory.EntryField("VendorID", "<H", presence=True),
    inventory.EntryField("DeviceID", "<H"),
    inventory.EntryField("SubSystemVendorID", "<H"),
    inventory.EntryField("SubSystemID", "<H"),
    inventory.EntryField("InterfaceType", "B"),
    inventory.EntryField("SubClassCode", "B"),
    inventory.EntryField("BaseClassCode", "B"),
    inventory.EntryField("LinkSpeed", "B"),
    inventory.EntryField("LinkWidth", "B"),
    inventory.EntryField("Reserved", "h")
)


def parse_pci_info(raw):
    return inventory.parse_inventory_category_entry(raw, pci_fields)


def get_categories():
    return {
        "pci": {
            "idstr": "PCI {0}",
            "parser": parse_pci_info,
            "command": {
                "netfn": 0x06,
                "command": 0x59,
                "data": (0x00, 0xc1, 0x03, 0x00)
            },
            "workaround_bmc_bug": lambda t: t == "ami"
        }
    }
