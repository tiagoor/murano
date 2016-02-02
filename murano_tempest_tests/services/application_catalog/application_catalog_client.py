# Copyright (c) 2015 Mirantis, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import json
import os

import requests
from tempest import config
from tempest_lib.common import rest_client

from murano_tempest_tests import utils

CONF = config.CONF


class ApplicationCatalogClient(rest_client.RestClient):
    """Tempest REST client for Murano Application Catalog"""

    def __init__(self, auth_provider):
        super(ApplicationCatalogClient, self).__init__(
            auth_provider,
            CONF.application_catalog.catalog_type,
            CONF.identity.region,
            endpoint_type=CONF.application_catalog.endpoint_type)
        self.build_interval = CONF.application_catalog.build_interval
        self.build_timeout = CONF.application_catalog.build_timeout

# -----------------------------Packages methods--------------------------------
    def upload_package(self, package_name, package_path, top_dir, body):
        """Upload a Murano package into Murano repository

        :param package_name: Package name
        :param package_path: Path with .zip relatively top_dir
        :param top_dir: Top directory with tests
        :param body: dict of tags, parameters, etc
        :return:
        """
        headers = {'X-Auth-Token': self.auth_provider.get_token()}
        files = open(os.path.join(top_dir, package_path), 'rb')
        uri = "/v1/catalog/packages"
        post_body = {'JsonString': json.dumps(body)}
        endpoint = self.base_url
        url = endpoint + uri
        resp = requests.post(url, files={package_name: files}, data=post_body,
                             headers=headers)
        self.expected_success(200, resp.status_code)
        return self._parse_resp(resp.text)

    def update_package(self, package_id, post_body):
        headers = {
            'content-type': 'application/murano-packages-json-patch'
        }

        uri = 'v1/catalog/packages/{0}'.format(package_id)
        resp, body = self.patch(uri, json.dumps(post_body), headers=headers)
        self.expected_success(200, resp.status)
        return self._parse_resp(body)

    def delete_package(self, package_id):
        """Removes a package from a repository

        :param package_id: Package ID
        """
        uri = 'v1/catalog/packages/{0}'.format(package_id)
        resp, body = self.delete(uri)
        self.expected_success(200, resp.status)

    def get_package(self, package_id):
        uri = 'v1/catalog/packages/{0}'.format(package_id)
        resp, body = self.get(uri)
        self.expected_success(200, resp.status)
        return self._parse_resp(body)

    def get_list_packages(self):
        uri = 'v1/catalog/packages'
        resp, body = self.get(uri)
        self.expected_success(200, resp.status)
        return self._parse_resp(body)

    def download_package(self, package_id):
        headers = {
            'content-type': 'application/octet-stream'
        }
        uri = 'v1/catalog/packages/{0}/download'.format(package_id)
        resp, body = self.get(uri, headers=headers)
        self.expected_success(200, resp.status)
        return self._parse_resp(body)

    def get_ui_definition(self, package_id):
        headers = {
            'content-type': 'application/octet-stream'
        }
        uri = 'v1/catalog/packages/{0}/ui'.format(package_id)
        resp, body = self.get(uri, headers=headers)
        self.expected_success(200, resp.status)
        return self._parse_resp(body)

    def get_logo(self, package_id):
        headers = {
            'content-type': 'application/octet-stream'
        }
        uri = 'v1/catalog/packages/{0}/ui'.format(package_id)
        resp, body = self.get(uri, headers=headers)
        self.expected_success(200, resp.status)
        return self._parse_resp(body)

# -----------------------Methods for environment CRUD--------------------------
    def get_environments_list(self):
        uri = 'v1/environments'
        resp, body = self.get(uri)
        self.expected_success(200, resp.status)

        return self._parse_resp(body)

    def create_environment(self, name):
        uri = 'v1/environments'
        post_body = {'name': name}
        resp, body = self.post(uri, json.dumps(post_body))
        self.expected_success(200, resp.status)
        return self._parse_resp(body)

    def delete_environment(self, environment_id):
        uri = 'v1/environments/{0}'.format(environment_id)
        resp, body = self.delete(uri)
        self.expected_success(200, resp.status)

    def abandon_environment(self, environment_id):
        uri = 'v1/environments/{0}?abandon=True'.format(environment_id)
        resp, body = self.delete(uri)
        self.expected_success(200, resp.status)

    def update_environment(self, environment_id):
        uri = 'v1/environments/{0}'.format(environment_id)
        name = utils.generate_name("updated_env")
        post_body = {"name": name}
        resp, body = self.put(uri, json.dumps(post_body))
        self.expected_success(200, resp.status)
        return self._parse_resp(body)

    def get_environment(self, environment_id):
        uri = 'v1/environments/{0}'.format(environment_id)
        resp, body = self.get(uri)
        self.expected_success(200, resp.status)
        return self._parse_resp(body)

# -----------------------Methods for session manage ---------------------------
    def create_session(self, environment_id):
        body = None
        uri = 'v1/environments/{0}/configure'.format(environment_id)
        resp, body = self.post(uri, body)
        self.expected_success(200, resp.status)
        return self._parse_resp(body)

    def delete_session(self, environment_id, session_id):
        uri = 'v1/environments/{0}/sessions/{1}'.format(environment_id,
                                                        session_id)
        resp, body = self.delete(uri)
        self.expected_success(200, resp.status)
        return self._parse_resp(body)

    def get_session(self, environment_id, session_id):
        uri = 'v1/environments/{0}/sessions/{1}'.format(environment_id,
                                                        session_id)
        resp, body = self.get(uri)
        self.expected_success(200, resp.status)
        return self._parse_resp(body)

    def deploy_session(self, environment_id, session_id):
        body = None
        url = 'v1/environments/{0}/sessions/{1}/deploy'.format(environment_id,
                                                               session_id)
        resp, body = self.post(url, body)
        self.expected_success(200, resp.status)
        return self._parse_resp(body)

# -----------------------------Service methods---------------------------------
    def create_service(self, environment_id, session_id, post_body):
        headers = self.get_headers()
        headers.update(
            {'X-Configuration-Session': session_id}
        )
        uri = 'v1/environments/{0}/services'.format(environment_id)
        resp, body = self.post(uri, json.dumps(post_body), headers)
        self.expected_success(200, resp.status)
        return self._parse_resp(body)

    def delete_service(self, environment_id, session_id, service_id):
        headers = self.get_headers()
        headers.update(
            {'X-Configuration-Session': session_id}
        )
        uri = 'v1/environments/{0}/services/{1}'.format(environment_id,
                                                        service_id)
        resp, body = self.delete(uri, headers)
        self.expected_success(200, resp.status)
        return self._parse_resp(body)

    def get_services_list(self, environment_id, session_id=None):
        headers = self.get_headers()
        if session_id:
            headers.update(
                {'X-Configuration-Session': session_id}
            )
        uri = 'v1/environments/{0}/services'.format(environment_id)
        resp, body = self.get(uri, headers)
        self.expected_success(200, resp.status)
        # TODO(freerunner): Need to replace json.loads() to _parse_resp
        # method, when fix for https://bugs.launchpad.net/tempest/+bug/1539927
        # will resolved and new version of tempest-lib released.
        return json.loads(body)

    def get_service(self, environment_id, service_id, session_id=None):
        headers = self.get_headers()
        if session_id:
            headers.update(
                {'X-Configuration-Session': session_id}
            )
        uri = 'v1/environments/{0}/services/{1}'.format(environment_id,
                                                        service_id)
        resp, body = self.get(uri, headers)
        self.expected_success(200, resp.status)
        return self._parse_resp(body)