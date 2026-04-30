# Copyright 2025 Lenovo Corporation
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

import aiohmi.redfish.oem.generic as generic


class OEMHandler(generic.OEMHandler):
    @classmethod
    async def create(cls, sysinfo, sysurl, webclient, cache, gpool=None):
        self = await super().create(sysinfo, sysurl, webclient, cache,
                                         gpool)
        if sysurl is None:
            systems, status = await webclient.grab_json_response_with_status('/redfish/v1/Systems')
            if status == 200:
                for system in systems.get('Members', []):
                    if system.get('@odata.id', '').endswith('/Self') or system.get('@odata.id', '').endswith('/System_0'):
                        sysurl = system['@odata.id']
                        break
            self._varsysurl = sysurl
        return self
