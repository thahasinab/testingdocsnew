""" *******************************************************************************************************************
|
|  Name        :  __application_urls.py
|  Description :  ApplicationUrls
|  Project     :  risksense_api
|  Copyright   :  2022 RiskSense, Inc.
|  License     :  Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
******************************************************************************************************************* """


from ...__subject import Subject
from ..._params import *
from ..._api_request_handler import *
import json
import csv

class ApplicationUrls(Subject):

    """ ApplicationUrl class """

    def __init__(self, profile):

        """
        Initialization of ApplicationUrl object.

        :param profile:     Profile Object
        :type  profile:     _profile
        """

        self.subject_name = 'applicationUrl'
        Subject.__init__(self, profile, self.subject_name)

    def get_model(self, client_id:int=None):

        """
        Get available projections and models for ApplicationUrl.

        :param client_id:   Client ID
        :type  client_id:   int

        :return:    ApplicationUrl projections and models are returned.
        :rtype:     dict

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            response = self._model(self.subject_name, client_id)
        except (RequestFailed, Exception) as e:
            print()
            print('There seems to be an exception')
            print(e)
            exit()

        return response

    def list_applicationurl_filter_fields(self,client_id:int=None):

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
        except (RequestFailed, Exception) as e:
            print()
            print('There seems to be an exception')
            print(e)
            exit()

        return response

    def get_single_search_page(self, search_filters, page_num=0, page_size=150,
                               sort_field=SortField.ID, sort_dir=SortDirection.ASC, client_id=None):

        """
        Searches for and returns applications based on the provided filter(s) and other parameters.

        :param search_filters:  List of dictionaries containing filter parameters.
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

        :return:    The paginated JSON response from the platform is returned.
        :rtype:     dict

        :raises RequestFailed:
        """

        func_args = locals()
        func_args.pop('self')

        if client_id is None:
            client_id, func_args['client_id'] = self._use_default_client_id()

        try:
            response = self._get_single_search_page(self.subject_name, **func_args)
        except (RequestFailed, Exception) as e:
            print()
            print('There seems to be an exception')
            print(e)
            exit()

        return response

    def search(self, search_filters, page_size=150, sort_field=SortField.ID, sort_dir=SortDirection.ASC,csvdump=False, client_id=None):

        """
        Searches for and returns applications based on the provided filter(s) and other parameters.  Rather
        than returning paginated results, this function cycles through all pages of results and returns
        them all in a single list.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param page_size:       The number of results per page to be returned.
        :type  page_size:       int

        :param sort_field:      The field to be used for sorting results returned.
        :type  sort_field:      SortField attribute

        :param sort_dir:        The direction of sorting to be used. SortDirection.ASC or SortDirection.DESC
        :type  sort_dir:        SortDirection attribute

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    A list containing all applications returned by the search using the filter provided.
        :rtype:     list

        :raises RequestFailed:
        :raises Exception:
        """

        func_args = locals()
        func_args.pop('self')
        csvdumpval=csvdump
        func_args.pop('csvdump')
        all_results = []
        if client_id is None:
            client_id, func_args['client_id'] = self._use_default_client_id()

        try:
            page_info = self._get_page_info(subject_name=self.subject_name, search_filters=search_filters,
                                            page_size=page_size, client_id=client_id)
            num_pages = page_info[1]
        except (RequestFailed, Exception) as e:
            print()
            print('There seems to be an exception')
            print(e)
            exit()

        page_range = range(0, num_pages)

        try:
            all_results = self._search(self.subject_name, self.get_single_search_page, page_range, **func_args)
        except (RequestFailed, Exception) as e:
            print()
            print('There seems to be an exception')
            print(e)
            exit()
        print(csvdump)
        if csvdump==True:
                print('Printing application urls data in a csv called applicationurls.csv')
                newdump=[]
                for i in all_results:
                    temp={}
                    for key,value in i.items():
                        print(temp)
                        temp[key]=value
                        if key=="groupIds":
                            temp[key]=','.join(str(i) for i in value)
                    newdump.append(temp)
                field_names=[]
                for item in newdump[0]:
                    field_names.append(item)
                with open('applicationurls.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    for item in newdump:
                        writer.writerow(item)
                

        return all_results
        

"""
   Copyright 2022 RiskSense, Inc.

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
