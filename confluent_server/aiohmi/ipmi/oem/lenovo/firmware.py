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


firmware_fields = (
    inventory.EntryField("Revision", "B"),
    inventory.EntryField("Bios", "16s"),
    inventory.EntryField("Operational ME", "10s"),
    inventory.EntryField("Recovery ME", "10s"),
    inventory.EntryField("RAID 1", "16s"),
    inventory.EntryField("RAID 2", "16s"),
    inventory.EntryField("Mezz 1", "16s"),
    inventory.EntryField("Mezz 2", "16s"),
    inventory.EntryField("BMC", "16s"),
    inventory.EntryField("LEPT", "16s"),
    inventory.EntryField("PSU 1", "16s"),
    inventory.EntryField("PSU 2", "16s"),
    inventory.EntryField("CPLD", "16s"),
    inventory.EntryField("LIND", "16s"),
    inventory.EntryField("WIND", "16s"),
    inventory.EntryField("DIAG", "16s"))

asrock_firmware_fields = (
    inventory.EntryField("Major Firmware Revision", "B"),
    inventory.EntryField("Minor Firmware Revision", "B"),
    inventory.EntryField("Auxiliary Firmware Revision", "4s"))

firmware_cmd = {
    "lenovo": {
        "netfn": 0x06,
        "command": 0x59,
        "data": (0x00, 0xc7, 0x00, 0x00)},
    "asrock": {
        "netfn": 0x3a,
        "command": 0x50,
        "data": (0x02, 0x00, 0x01)},
}

bios_cmd = {
    "lenovo": {
        "netfn": 0x32,
        "command": 0xE8,
        "data": (0x01, 0x01, 0x02)},
    "asrock": {
        "netfn": 0x3a,
        "command": 0x50,
        "data": (0x02, 0x01, 0x01)},
}


def parse_firmware_info(raw, bios_versions=None, asrock=False):
    fields = firmware_fields

    if asrock:
        fields = asrock_firmware_fields

    bytes_read, data = inventory.parse_inventory_category_entry(raw, fields)
    if asrock:
        major_version = data['Major Firmware Revision']
        minor_version = data['Minor Firmware Revision']
        # Asrock RS160 the minor version is Binary Coded Decimal,
        # convert it to Decimal
        minor_version = (0xff & (minor_version >> 4)) * 10 + \
                        (0xf & minor_version)
        aux_reversion = 0
        if str(data['Auxiliary Firmware Revision']) != '':
            aux_reversion = ord(data['Auxiliary Firmware Revision'])

        bmc_version = "%s.%s.%s" % (
            str(major_version),
            str(minor_version),
            str(aux_reversion))

        yield ("BMC", {'version': bmc_version})
        if bios_versions is not None:
            yield ("Bios", {'version': bios_versions[0:]})
    else:
        del data["Revision"]
        for key in data:
            yield (key, {'version': data[key]})
        if bios_versions is not None:
            yield ("Bios_bundle_ver",
                   {'version': bios_versions['new_img_version']})
            yield ("Bios_current_ver",
                   {'version': bios_versions['cur_img_version']})


def parse_bios_number(raw):
    return inventory.parse_bios_number_entry(raw)


def get_categories():
    return {
        "firmware": {
            "idstr": "FW Version",
            "parser": parse_firmware_info,
            "command": firmware_cmd
        },
        "bios_version": {
            "idstr": "Bios Version",
            "parser": parse_bios_number,
            "command": bios_cmd
        }
    }
