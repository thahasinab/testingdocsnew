""" *******************************************************************************************************************
|
|  Name        :  __patch.py
|  Description :  Patch
|  Project     :  risksense_api
|  Copyright   :  2022 RiskSense, Inc.
|  License     :  Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
******************************************************************************************************************* """

import json
import sys
import time
import concurrent.futures
from .. import Subject
from ..__exports import ExportFileType
from ..__exports import ExportRowNumbers
from ..__exports import Exports
from ..._params import *
from ..._api_request_handler import *
import sys
import csv
import zipfile

class Patch(Subject):

    """ Playbooks class """

    def downloadfilterinexport(self,filename,filters,client_id=None):

        """
        Export files based on filter.

        :param filename:   Name of the file to export
        :type  filename:   str

        :param filter:   List of filters
        :type  filter:   list

        :param client_id:   Client ID
        :type  client_id:   int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id= self._use_default_client_id()
        exportid=self.export(filters,file_name=filename)
        self.exports=Exports(self.profile)
        while(True):
                try:
                    exportstatus=self.exports.check_status(exportid)
                    if exportstatus=='COMPLETE':
                        print('Export Complete')
                        break
                    elif exportstatus=='ERROR':
                        print('error getting zip file please check ')
                        exit()
                except (RequestFailed,MaxRetryError,StatusCodeError, ValueError) as ex:       
                    print(ex)
                    print()
                    print("Unable to export the file.")
                    sys.exit("Exiting")
        try:   
            self.exports.download_export(exportid,f"{filename}.zip")
            with zipfile.ZipFile(f"{filename}.zip","r") as zip_ref:
                zip_ref.extractall(filename)
        except(RequestFailed,MaxRetryError,StatusCodeError, ValueError) as ex:
                    print(ex)
                    print()
                    print("Unable to retrieve file. Exiting.")
                    sys.exit(1)

    def __init__(self, profile):

        """
        Initialization of Patch object.

        :param profile:     Profile Object
        :type  profile:     _profile

        """
        self.subject_name = "patch"
        Subject.__init__(self, profile, self.subject_name)
    
    def getexporttemplate(self,client_id:int=None):
        
        """
        Gets configurable export template for patches.

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The Exportable fields
        :rtype:     list

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/export/template"

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('Error in getting export template')
            print(e)
            exit()

        exportablefilter = json.loads(raw_response.text)

        for i in range(len(exportablefilter['exportableFields'])):
            for j in range(len(exportablefilter['exportableFields'][i]['fields'])):
                if exportablefilter['exportableFields'][i]['fields'][j]['selected']==False:
                    exportablefilter['exportableFields'][i]['fields'][j]['selected']=True

        return exportablefilter['exportableFields']
    
    def export(self, search_filters:list, file_name:str, row_count=ExportRowNumbers.ROW_ALL,file_type=ExportFileType.CSV, client_id=None):

        """
        Initiates an export job on the platform for patche(s) based on the
        provided filter(s).

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param file_name:       The name to be used for the exported file.
        :type  file_name:       str

        :param row_count:       No of rows to be exported. Possible options : (ExportRowNumbers.ROW_5000,ExportRowNumbers.ROW_10000,ExportRowNumbers.ROW_25000,ExportRowNumbers.ROW_50000",ExportRowNumbers.ROW_100000",ExportRowNumbers.ROW_ALL)
        :type  row_count:       str
        
        :param file_type:       File type to export.  ExportFileType.CSV, ExportFileType.JSON, or ExportFileType.XLSX
        :type  file_type:       str

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The job ID in the platform from is returned.
        :rtype:     int

        :raises RequestFailed:
        """
        func_args = locals()
        func_args['exportable_filter']=self.getexporttemplate()
        func_args.pop('self')
        if client_id is None:
            func_args['client_id'] = self._use_default_client_id()[1]
        try:
            export_id = self._export(self.subject_name, **func_args)
        except (RequestFailed,Exception) as e:
            print('Error in exporting application data')
            print(e)
            exit()

        return export_id

    def get_filter(self, client_id:int=None):

        """
        Get a list of supported patch filters.

        :param client_id:   Client ID
        :type  client_id:   int

        :return:    Filter information
        :rtype:     list

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/filter"

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
            filters = json.loads(raw_response.text)
            return filters
        except RequestFailed as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        


    def get_single_search_page(self, search_filters:list, projection=Projection.BASIC, page_num=0, page_size=150,
                               sort_field=SortField.ID, sort_dir=SortDirection.ASC, client_id=None):

        """
        Searches for and returns hosts based on the provided filter(s) and other parameters.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param projection:      Projection to be used in API request.  Projection.BASIC or Projection.DETAIL
        :type  projection:      Projection attribute

        :param page_num:        The page number of results to be returned.
        :type  page_num:        int

        :param page_size:       The number of results per page to be returned.
        :type  page_size:       int

        :param sort_field:      The field to be used for sorting results returned.
        :type  sort_field:      SortField attribute

        :param sort_dir:        The direction of sorting to be used. SortDirection.ASC or SortDirection.DESC
        :type  sort_dir:        SortDirection attribute

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON response from the platform is returned.
        :rtype:     dict

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/search"

        body = {
            "filters": search_filters,
            "projection": projection,
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
            jsonified_response = json.loads(raw_response.text)
        except RequestFailed as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        return jsonified_response


    def search(self, search_filters:list, projection=Projection.BASIC, page_size=150,
               sort_field=SortField.ID, sort_dir=SortDirection.ASC,csvdump:bool=False, client_id:int=None):

        """
        Searches for and returns patch data based on the provided filter(s) and other parameters.  Rather
        than returning paginated results, this function cycles through all pages of results and returns
        them all in a single list.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param projection:      Projection to be used in API request.  Projection.BASIC or Projection.DETAIL
        :type  projection:      Projection attribute

        :param page_size:       The number of results per page to be returned.
        :type  page_size:       int

        :param sort_field:      The field to be used for sorting results returned.
        :type  sort_field:      SortField attribute

        :param sort_dir:        The direction of sorting to be used. SortDirection.ASC or SortDirection.DESC
        :type  sort_dir:        SortDirection attribute
    
        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    A list containing all hosts returned by the search using the filter provided.
        :rtype:     list

        :raises RequestFailed:
        :raises Exception:
        """

        func_args = locals()
        func_args.pop('self')
        func_args.pop('csvdump')

        if client_id is None:
            client_id, func_args['client_id'] = self._use_default_client_id()
        
        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        try:
            page_info = self._get_page_info(self.subject_name, search_filters, page_size=page_size, client_id=client_id)
            num_pages = page_info[1]
        except RequestFailed as e:
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

        if csvdump==True:
            self.downloadfilterinexport('patchsearch',search_filters)

        return all_results
    
    def suggest(self, search_filter_1:list, search_filter_2:dict, client_id:int=None):

        """
        Suggest values for filter fields.

        :param search_filter_1:     Search Filter 1
        :type  search_filter_1:     list

        :param search_filter_2:     Search Filter 2
        :type  search_filter_2:     dict

        :param client_id:           Client ID
        :type  client_id:           int

        :return:    suggestions
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
