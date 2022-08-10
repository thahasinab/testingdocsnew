"""
Role
"""
""" *******************************************************************************************************************
|
|  Name        :  __networks.py
|  Module      :  risksense_api
|  Description :  A class to be used for interacting with RiskSense platform networks.
|  Copyright   :  (c) RiskSense, Inc.
|  License     :  Apache-2.0
|
******************************************************************************************************************* """

import json
from sre_constants import SUCCESS
from .. import Subject
from ..._params import *
from ..._api_request_handler import *


class Role(Subject):

    """ Networks class """

    def __init__(self, profile):

        """
        Initialization of Networks object.

        :param profile:     Profile Object
        :type  profile:     _profile

        """

        self.subject_name = "role"
        Subject.__init__(self, profile, self.subject_name)
        self.alt_api_base_url=self.profile.platform_url+"/api/v1/client/{}/"

    def create(self, name=None, description=None, client_id=None):

        """
        Create a new role.

        :param name:            The name for the new network.
        :type  name:            str

        :param decription:      The description of the role.
        :type  decription:    str.

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The new role ID.
        :rtype:     int

        :raises RequestFailed:
        """
        print(name,description)

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))

        #if name or description is None:
        #   raise ValueError('Name or description is not provided please provide them')

        body = {
            "name": name,
            "description": description
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)


        return jsonified_response

    def allow_privileges(self, roleid=None, client_id=None):

        """
        Create a new network.

        :param name:            The name for the new network.
        :type  name:            str

        :param network_type:    The network type.  The options are "IP" or "hostname"
        :type  network_type:    str.

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The new network ID.
        :rtype:     int

        :raises RequestFailed:
        """

        privlegesids,privilegesnames=self.get_privileges()

        for i in range(len(privilegesnames)):
            print(i,privilegesnames[i])
        
        try:
            inputsofrolestoallow=[privlegesids[int(i)] for i in input('Please enter the privileges ids that you want to allow to the role seperated by comma:').split(',')]
        except (IndexError, Exception) as e:
                        print()
                        print('There seems to be an exception,please provide an index from the list')
                        print(e)
                        exit()       

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        body = {
            "negate":False
        }
        for i in inputsofrolestoallow:
            url = url = self.api_base_url.format(str(client_id))+'/{}/privilege/{}'.format(roleid,i)
            print(url)
            try:
                raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
                print(raw_response.status_code)
            except (RequestFailed,Exception) as e:
                 print()
                 print('There seems to be an exception')
                 print(e)
                 exit()
        success=True
        return success
    
    def deny_privileges(self, roleid=None, client_id=None):

        """
        Create a new network.

        :param name:            The name for the new network.
        :type  name:            str

        :param network_type:    The network type.  The options are "IP" or "hostname"
        :type  network_type:    str.

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The new network ID.
        :rtype:     int

        :raises RequestFailed:
        """

        privlegesids,privilegesnames=self.get_privileges()

        for i in range(len(privilegesnames)):
            print(i,privilegesnames[i])
        try:
            inputsofrolestodeny=[privlegesids[int(i)] for i in input('Please enter the privileges ids that you want to deny to the role seperated by comma:').split(',')]        
        except (IndexError, Exception) as e:
                        print()
                        print('There seems to be an exception,please provide an index from the list')
                        print(e)
                        exit()
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        body = {
            "negate":True
        }
        for i in inputsofrolestodeny:
            url = url = self.api_base_url.format(str(client_id))+'/{}/privilege/{}'.format(roleid,i)
            print(url)
            try:
                raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
                print(raw_response.status_code)
            except (RequestFailed,Exception) as e:
                 print()
                 print('There seems to be an exception')
                 print(e)
                 exit()
        success=True
        return success

    def delete_privileges(self, roleid=None, client_id=None):

        """
        Create a new network.

        :param name:            The name for the new network.
        :type  name:            str

        :param network_type:    The network type.  The options are "IP" or "hostname"
        :type  network_type:    str.

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The new network ID.
        :rtype:     int

        :raises RequestFailed:
        """

        privlegesids,privilegesnames=self.get_privileges()

        for i in range(len(privilegesnames)):
            print(i,privilegesnames[i])
        
        try:
            inputsofrolestodeny=[privlegesids[int(i)] for i in input('Please enter the privileges ids that you want to remove to the role seperated by comma:').split(',')]        
        except (IndexError, Exception) as e:
                        print()
                        print('There seems to be an exception,please provide an index from the list')
                        print(e)
                        exit()   
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        for i in inputsofrolestodeny:
            url = url = self.api_base_url.format(str(client_id))+'/{}/privilege/{}'.format(roleid,i)
            print(url)
            try:
                raw_response = self.request_handler.make_request(ApiRequestHandler.DELETE, url)
                print(raw_response.status_code)
            except (RequestFailed,Exception) as e:
                 print()
                 print('There seems to be an exception')
                 print(e)
        sucess=True
        return sucess
    def get_privileges(self, client_id=None):

        """
        Create a new network.

        :param name:            The name for the new network.
        :type  name:            str

        :param network_type:    The network type.  The options are "IP" or "hostname"
        :type  network_type:    str.

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The new network ID.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.alt_api_base_url.format(client_id)+'privilege?page=0&size=500'

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        
        if raw_response.status_code==200:
            jsonified_response = json.loads(raw_response.text)
            privilegesid=[jsonified_response["_embedded"]["privileges"][i]['id'] for i in range(len(jsonified_response["_embedded"]["privileges"]))]
            privilegesname=[jsonified_response["_embedded"]["privileges"][i]['name'] for i in range(len(jsonified_response["_embedded"]["privileges"]))]
            return privilegesid,privilegesname
        else:
            print(raw_response)
        


    def update(self, roleid,name=None, description=None, client_id=None):

        """
        Create a new role.

        :param name:            The name for the new network.
        :type  name:            str

        :param decription:      The description of the role.
        :type  decription:    str.

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The new role ID.
        :rtype:     int

        :raises RequestFailed:
        """
        print(name,description)

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))+'/{}'.format(roleid)

        #if name or description is None:
        #   raise ValueError('Name or description is not provided please provide them')

        body = {
            "name": name,
            "description": description
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)
        role_id = jsonified_response['id']
        role_name=jsonified_response['name']


        return role_id,role_name


"""
   Copyright 2021 RiskSense, Inc.
   
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at:
   
   http://www.apache.org/licenses/LICENSE-2.0
   
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
