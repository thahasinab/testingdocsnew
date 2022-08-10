"""
Networks
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
from ...__subject import Subject
from ..._params import *
from ..._api_request_handler import *
import csv


class Networks(Subject):

    """ Networks class """

    def __init__(self, profile):

        """
        Initialization of Networks object.

        :param profile:     Profile Object
        :type  profile:     _profile

        """

        self.subject_name = "network"
        Subject.__init__(self, profile, self.subject_name)

    def list_network_filter_fields(self,client_id=None):

        """
        List filter endpoints.

        :param filter_subject:  Supported Subjects are: 
       
        :type filter_subject:   FilterSubject attribute

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON output from the platform is returned, listing the available filters.
        :rtype:     dict

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))+'/filter'
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)

        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response



    def create(self, name, network_type, client_id=None):

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

        url = self.api_base_url.format(str(client_id))

        body = {
            "name": name,
            "type": network_type
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        jsonified_response = json.loads(raw_response.text)
        network_id = jsonified_response['id']

        return network_id

    def create_ip_network(self, name, client_id=None):

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

        url = self.api_base_url.format(str(client_id))

        body = {
            "name": name,
            "type": "IP"
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        jsonified_response = json.loads(raw_response.text)
        network_id = jsonified_response['id']

        return network_id

    def create_hostname_network(self, name, client_id=None):

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

        url = self.api_base_url.format(str(client_id))

        body = {
            "name": name,
            "type": "HOSTNAME"
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        jsonified_response = json.loads(raw_response.text)
        network_id = jsonified_response['id']

        return network_id

    def create_mixed_network(self, name, client_id=None):

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

        url = self.api_base_url.format(str(client_id))

        body = {
            "name": name,
            "type": "MIXED"
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        jsonified_response = json.loads(raw_response.text)
        network_id = jsonified_response['id']

        return network_id

    def update(self, network_id,name, client_id=None):

        """
        Update an existing network.

        :param network_id:  The network ID.
        :type  network_id:  int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :keyword name:          A new name for the network.             (str)
        :keyword network_type:  The network type. "IP" or "hostname".   (str)

        :return:    The network ID
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}".format(str(network_id))

        print(url)
        body = {
            "name": name
        }
        print(body)

        body = self._strip_nones_from_dict(body)

        if body == {}:
            raise ValueError("Body is empty. Name and/or network_type not provided.")

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        
        
        print(raw_response)
        jsonified_response = json.loads(raw_response.text)
        returned_id = jsonified_response['id']

        return returned_id

    def delete(self, network_id, client_id=None,csvdump=False):

        """
        Deletes a network.

        :param network_id:  The network ID to be deleted.
        :type  network_id:  str

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    True/False indicating whether or not the operation was successful.
        :rtype:     bool

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}".format(str(network_id))

        if csvdump==True:
            jsonified_response=self.get_single_search_page([{"field":"id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":f"{network_id}"}])
            print(jsonified_response)
            field_names = []
            for item in jsonified_response['_embedded']['networks'][0]:
                field_names.append(item)
            try:
                with open('get_networks.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    for item in jsonified_response['_embedded']['networks']:
                        writer.writerow(item)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)
        try:
            self.request_handler.make_request(ApiRequestHandler.DELETE, url)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        success = True

        return success

    def get_single_search_page(self, search_filters, page_num=0, page_size=150,
                               sort_field=SortField.ID, sort_dir=SortDirection.ASC, client_id=None):

        """
        Searches for and returns networks based on the provided filter(s) and other parameters.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param page_num:        Page number of results to be returned.
        :type  page_num:        int

        :param page_size:       Number of results to be returned per page.
        :type  page_size:       int

        :param sort_field:      Name of field to sort results on.
        :type  sort_field:      SortField attribute

        :param sort_dir:        Direction to sort. SortDirection.ASC or SortDirection.DESC
        :type  sort_dir:        SortDirection attribute

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    A paginated JSON response from the platform is returned.
        :rtype:     dict

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/search"

        body = {
            "filters": search_filters,
            "projection": Projection.BASIC,
            "sort": [
                {
                    "field": sort_field,
                    "direction": sort_dir
                }
            ],
            "page": page_num,
            "size": page_size
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

    def search(self, search_filters, page_size=150, sort_field=SortField.ID, sort_dir=SortDirection.ASC, client_id=None,csvdump=False):

        """
        Searches for and returns networks based on the provided filter(s) and other parameters.  Rather
        than returning paginated results, this function cycles through all pages of results and returns
        them all in a single list.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param page_size:       The number of results per page to be returned.
        :type  page_size:       int

        :param sort_field:      Name of field to sort results on.
        :type  sort_field:      SortField attribute

        :param sort_dir:        Direction to sort. SortDirection.ASC or SortDirection.DESC
        :type  sort_dir:        SortDirection attribute

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    A list containing all hosts returned by the search using the filter provided.
        :rtype:     list

        :raises RequestFailed:
        """

        func_args = locals()
        func_args.pop('self')
        func_args.pop('csvdump')
        all_results = []

        if client_id is None:
            client_id, func_args['client_id'] = self._use_default_client_id()

        try:
            page_info = self._get_page_info(self.subject_name, search_filters, page_size=page_size, client_id=client_id)
            num_pages = page_info[1]
        except (RequestFailed, StatusCodeError, MaxRetryError, PageSizeError):
            print("There was a problem with the networks search.")
        

        page_range = range(0, num_pages)

        try:
            all_results = self._search(self.subject_name, self.get_single_search_page, page_range, **func_args)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        if csvdump==True:
            field_names = []
            for item in all_results[0]:
                field_names.append(item)
            try:
                with open('get_networks.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    for item in all_results:
                        writer.writerow(item)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)
        

        return all_results

    def get_model(self, client_id=None):

        """
        Get available projections and models for Networks.

        :param client_id:   Client ID
        :type  client_id:   int

        :return:    Networks projections and models are returned.
        :rtype:     dict

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            response = self._model(self.subject_name, client_id)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        return response

    def suggest(self, search_filter_1, search_filter_2, client_id=None):

        """
        Suggest values for filter fields.

        :param search_filter_1:     Search Filter 1
        :type  search_filter_1:     list

        :param search_filter_2:     Search Filter 2
        :type  search_filter_2:     list

        :param client_id:           Client ID
        :type  client_id:           int

        :return:    Value suggestions
        :rtype:     list

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            response = self._suggest(self.subject_name, search_filter_1, search_filter_2, client_id)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        return response

    def filter_network(self,client_id=None):
        """
        Lists fields that can be filtered by in the filter network endpoint

        :param client_id:   Client ID
        :type  client_id:   int

        :raises RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/filter"

        try:
            raw_response=self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        
        
        jsonified_response = json.loads(raw_response.text)

        return jsonified_response
        
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
