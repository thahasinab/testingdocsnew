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

from requests import head
from .. import Subject
from ..._params import *
from ..._api_request_handler import *


class Scanner(Subject):

    """ Networks class """

    def __init__(self, profile):

        """
        Initialization of Networks object.

        :param profile:     Profile Object
        :type  profile:     _profile

        """

        self.subject_name = "scanner"
        Subject.__init__(self, profile, self.subject_name)
        self.alt_api_base_url=self.profile.platform_url+ "/api/v1/client/{}/csvUpload/scanner/{}"
        self.alt_api_base_url1=self.profile.platform_url+ "/api/v1/client/{}/csvUpload"

    def updatemapping(self,uuid,mappinguuid,mappings,uploadid,fileuuid,findingType,isAssetOnly=True,header=True,client_id=None):
        
        if client_id is None:
            client_id = self._use_default_client_id()[0]
        
        url=self.alt_api_base_url.format(str(client_id),str(uuid))+'/mapping/{}'.format(mappinguuid)

        body={"header":header,"isAssetOnly":isAssetOnly,"mappings":mappings,"csvFileDetails":{"uploadId":uploadid,"fileUuid":f"{fileuuid}"},"findingType":findingType}

        try:
            raw_response=self.request_handler.make_request(ApiRequestHandler.PUT, url,body=body)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        
        jsonified_response = json.loads(raw_response.text)

        return jsonified_response
    
    def createmapping(self,uuid,mappingname,description,version,findingType,mappings,uploadid,fileuuid,header=True,client_id=None):
        
        if client_id is None:
            client_id = self._use_default_client_id()[0]
        
        url=self.alt_api_base_url.format(str(client_id),str(uuid))+'/mapping'

        body={"name":f"{mappingname}","description":description,"version":str(version),"header":header,"findingType":findingType,"mappings":mappings,"csvFileDetails":{"uploadId":uploadid,"fileUuid":fileuuid}}

        try:
            raw_response=self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        if raw_response.status_code==500:
            print('Mapping locked and already exists, please enter a new name')
            exit()
        else:
            jsonified_response = json.loads(raw_response.text)
        
        

        return jsonified_response

    def validatemapping(self,uuid,mappinguuid,uploadid,fileid,isfullscan=False,isAssetOnly=True,client_id=None):
        
        if client_id is None:
            client_id = self._use_default_client_id()[0]
        
        url=self.alt_api_base_url.format(str(client_id),str(uuid))+'/mapping/{}/validate'.format(mappinguuid)

        body={"csvFileDetails":{"uploadId":uploadid,"fileId":fileid},"isFullScan":isfullscan,"isAssetOnly":isAssetOnly}

        try:
            raw_response=self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        
        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def validatemappingresult(self,uuid,mappinguuid,uploadid,fileid,isAssetOnly=True,client_id=None):
        
        if client_id is None:
            client_id = self._use_default_client_id()[0]
        
        url=self.alt_api_base_url.format(str(client_id),str(uuid))+'/mapping/{}/validate/results'.format(mappinguuid)

        validatemappingresultsdata={"csvFileDetails":{"uploadId":uploadid,"fileId":fileid},"isAssetOnly":isAssetOnly}

        try:
            raw_response=self.request_handler.make_request(ApiRequestHandler.POST, url,body=validatemappingresultsdata)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        
        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def lockmapping(self,uuid,mappinguuid,uploadid,fileid,isAssetOnly=True,client_id=None):
        
        if client_id is None:
            client_id = self._use_default_client_id()[0]
        
        url=self.alt_api_base_url.format(str(client_id),str(uuid))+'/mapping/{}/lock'.format(mappinguuid)

        validatemappingresultsdata={"csvFileDetails":{"uploadId":uploadid,"fileId":fileid},"isAssetOnly":isAssetOnly}

        try:
            raw_response=self.request_handler.make_request(ApiRequestHandler.POST, url,body=validatemappingresultsdata)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        
        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def uploadassetfindings(self,client_id=None):
        
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.alt_api_base_url1.format(str(client_id)) + "/assetFindings"

        try:
            raw_response=self.request_handler.make_request(ApiRequestHandler.GET, url)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        
        jsonified_response = json.loads(raw_response.text)

        return jsonified_response
        

    def searchmapping(self,uuid,client_id=None):
        
        if client_id is None:
            client_id = self._use_default_client_id()[0]
        
        url=self.alt_api_base_url.format(str(client_id),str(uuid))+'/mapping'

        try:
            raw_response=self.request_handler.make_request(ApiRequestHandler.GET, url)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        
        jsonified_response = json.loads(raw_response.text)

        return jsonified_response



    def scannercreate(self,body,client_id=None):

        """
        Create a new scanner.

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

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def update(self, network_id, client_id=None, **kwargs):

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

        name = kwargs.get('name', None)
        network_type = kwargs.get('network_type', None)

        body = {
            "name": name,
            "type": network_type
        }

        body = self._strip_nones_from_dict(body)

        if body == {}:
            raise ValueError("Body is empty. Name and/or new_asset_criticality not provided.")

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        
        print(raw_response)
        jsonified_response = json.loads(raw_response.text)
        returned_id = jsonified_response['id']

        return returned_id

    def delete(self, network_id, client_id=None):

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

        try:
            self.request_handler.make_request(ApiRequestHandler.DELETE, url)
        except RequestFailed as e:
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
        print(url)
        body = {
            "filters": search_filters,
            "projection": "internal",
            "sort": [
                {
                    "field": "name",
                    "direction": sort_dir
                }
            ],
            "page": page_num,
            "size": page_size
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def search(self, search_filters, page_size=150, sort_field=SortField.ID, sort_dir=SortDirection.ASC, client_id=None):

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
        all_results = []

        if client_id is None:
            client_id, func_args['client_id'] = self._use_default_client_id()

        try:
            page_info = self._get_page_info(self.subject_name, search_filters, page_size=page_size, client_id=client_id)
            num_pages = page_info[1]
        except (RequestFailed, StatusCodeError, MaxRetryError, PageSizeError) as e:
            print("There was a problem with the networks search.")
            print(e)
            exit()

        page_range = range(0, num_pages)

        try:
            all_results = self._search(self.subject_name, self.get_single_search_page, page_range, **func_args)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

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
        except RequestFailed as e:
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
        except RequestFailed as e:
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
        except RequestFailed as e:
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
