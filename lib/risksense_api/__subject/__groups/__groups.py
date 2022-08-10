"""
Groups
"""


""" *******************************************************************************************************************
|
|  Name        :  __groups.py
|  Module      :  risksense_api
|  Description :  A class to be used for searching for and updating groups on the RiskSense Platform.
|  Copyright   : (c) RiskSense, Inc.
|  License     : Apache-2.0 (http://www.apache.org/licenses/LICENSE-2.0)
|
******************************************************************************************************************* """

from cProfile import Profile
from http import client
import json
import profile
from ...__subject import Subject
from ..__exports import ExportFileType
from ..__exports import ExportRowNumbers
from ..__notifications import Notifications
from ..._params import *
from ..._api_request_handler import *
from ..__exports import Exports
import zipfile
import sys
import csv


class Groups(Subject):

    """ Groups Class """

    def __init__(self, profile):

        """
        Initialization of Groups object.

        :param profile:     Profile Object
        :type  profile:     _profile

        """
        self.profile=profile
        self.subject_name = "group"
        Subject.__init__(self, profile, self.subject_name)

    def downloadfilterinexport(self,filename,filters,client_id=None):
        if client_id is None:
            client_id= self._use_default_client_id()
        exportid=self.export(filters,file_name=filename)
        self.exports=Exports(self.profile)
        while(True):
                try:
                    exportstatus=self.exports.check_status(exportid)
                    print(exportstatus)
                    if exportstatus=='COMPLETE':
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
                self.exports.download_export(exportid,f"{filename}.csv")
        except(RequestFailed,MaxRetryError,StatusCodeError, ValueError) as ex:
                    print(ex)
                    print()
                    print("Unable to retrieve file. Exiting.")
                    sys.exit(1)

    def list_group_filter_fields(self,client_id=None):

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



    def get_single_search_page(self, search_filters, projection=Projection.BASIC, page_num=0, page_size=150,
                               sort_field=SortField.ID, sort_dir=SortDirection.ASC, client_id=None):

        """
        Searches for and returns groups based on the provided filter(s) and other parameters.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param projection:      Projection to use
        :type  projection:      str

        :param page_num:        The page number of results to be returned.
        :type  page_num:        int

        :param page_size:       The number of results per page to be returned.
        :type  page_size:       int

        :param sort_field:      The field to be used for sorting the results returned.
        :type  sort_field       SortField attribute

        :param sort_dir:        The direction of sorting to be used. (SortDirection.ASC or SortDirection.DESC)
        :type  sort_dir:        SortDirection attribute

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON response from the platform is returned.
        :rtype:     dict

        :s RequestFailed:
        """

        func_args = locals()
        func_args.pop('self')

        if client_id is None:
            client_id, func_args['client_id'] = self._use_default_client_id()

        try:
            response = self._get_single_search_page(self.subject_name, **func_args)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit() 
        return response

    def get_group_by_id(self, group_id, projection=Projection.BASIC, page_num=0, page_size=150,
                               sort_field=SortField.ID, sort_dir=SortDirection.ASC, client_id=None,csvdump=False):

        """
        Searches for and returns groups based on the provided filter(s) and other parameters.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param projection:      Projection to use
        :type  projection:      str

        :param page_num:        The page number of results to be returned.
        :type  page_num:        int

        :param page_size:       The number of results per page to be returned.
        :type  page_size:       int

        :param sort_field:      The field to be used for sorting the results returned.
        :type  sort_field       SortField attribute

        :param sort_dir:        The direction of sorting to be used. (SortDirection.ASC or SortDirection.DESC)
        :type  sort_dir:        SortDirection attribute

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON response from the platform is returned.
        :rtype:     dict

        :s RequestFailed:
        """
        try:
            search_filters=[{"field":"id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":f"{','.join(group_id)}"}]
            func_args = locals()
            func_args.pop('self')
            func_args['search_filters']=search_filters
            if client_id is None:
                client_id, func_args['client_id'] = self._use_default_client_id()
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        try:
            response = self._get_single_search_page(self.subject_name, **func_args)
            print(response)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        try:

            if csvdump==True:
                self.downloadfilterinexport('groupexport',search_filters)    

            return response
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

    def edit_custom_group_properties(self, group_ids, properties, client_id=None):

        """
        Searches for and returns groups based on the provided filter(s) and other parameters.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param projection:      Projection to use
        :type  projection:      str

        :param page_num:        The page number of results to be returned.
        :type  page_num:        int

        :param page_size:       The number of results per page to be returned.
        :type  page_size:       int

        :param sort_field:      The field to be used for sorting the results returned.
        :type  sort_field       SortField attribute

        :param sort_dir:        The direction of sorting to be used. (SortDirection.ASC or SortDirection.DESC)
        :type  sort_dir:        SortDirection attribute

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON response from the platform is returned.
        :rtype:     dict

        :s RequestFailed:
        """

        


        if client_id is None:
            client_id = self._use_default_client_id()[0]
        
        url = self.api_base_url.format(str(client_id))+'/properties'


        body={"groupIds":group_ids,"properties":properties}

        print(body)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
            print(raw_response.text)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        
        if raw_response.status_code==200:
            return 'works'


    def search(self, search_filters, projection=Projection.DETAIL, page_size=150,
               sort_field=SortField.ID, sort_dir=SortDirection.ASC, client_id=None,csvdump=False):

        """
        Searches for and returns groups based on the provided filter(s) and other parameters.  Rather
        than returning paginated results, this function cycles through all pages of results and returns
        them all in a single list.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param projection:      Projection to use
        :type  projection:      str

        :param page_size:       The number of results per page to be returned.
        :type  page_size:       int

        :param sort_field:      The field to be used for sorting the results returned.
        :type  sort_field       SortField attribute

        :param sort_dir:        The direction of sorting to be used. (SortDirection.ASC or SortDirection.DESC)
        :type  sort_dir:        SortDirection attribute

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    A list containing all host findings returned by the search using the filter provided.
        :rtype:     list

        :s RequestFailed:
        """

        func_args = locals()
        func_args.pop('self')
        all_results = []
        func_args.pop('csvdump')

        if client_id is None:
            client_id, func_args['client_id'] = self._use_default_client_id()

        try:
            page_info = self._get_page_info(self.subject_name, search_filters, page_size=page_size, client_id=client_id)
            num_pages = page_info[1]
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            

        page_range = range(0, num_pages)

        try:
            all_results = self._search(self.subject_name, self.get_single_search_page, page_range, **func_args)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        if csvdump==True:
            self.downloadfilterinexport('groupsearchdata',search_filters)      

        return all_results


    def subscribe_change_in_grouprs3(self,client_id=None):

        """
        Searches for and returns groups based on the provided filter(s) and other parameters.  Rather
        than returning paginated results, this function cycles through all pages of results and returns
        them all in a single list.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param projection:      Projection to use
        :type  projection:      str

        :param page_size:       The number of results per page to be returned.
        :type  page_size:       int

        :param sort_field:      The field to be used for sorting the results returned.
        :type  sort_field       SortField attribute

        :param sort_dir:        The direction of sorting to be used. (SortDirection.ASC or SortDirection.DESC)
        :type  sort_dir:        SortDirection attribute

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    A list containing all host findings returned by the search using the filter provided.
        :rtype:     list

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()
        
        self.notifications=Notifications(self.profile)
        try:
            subscribe = self.notifications.subscribe_notifications(notificationtypeid=3,subscribe=True)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            

        return subscribe

    def unsubscribe_change_in_grouprs3(self,client_id=None):

        """
        Searches for and returns groups based on the provided filter(s) and other parameters.  Rather
        than returning paginated results, this function cycles through all pages of results and returns
        them all in a single list.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param projection:      Projection to use
        :type  projection:      str

        :param page_size:       The number of results per page to be returned.
        :type  page_size:       int

        :param sort_field:      The field to be used for sorting the results returned.
        :type  sort_field       SortField attribute

        :param sort_dir:        The direction of sorting to be used. (SortDirection.ASC or SortDirection.DESC)
        :type  sort_dir:        SortDirection attribute

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    A list containing all host findings returned by the search using the filter provided.
        :rtype:     list

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()

        try:
            print(client_id)
            subscribe = self.notifications.subscribe_notifications(self,notificationtypeid=3,subscribe=False)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            

        return subscribe


    def create(self, name,description, client_id=None):

        """
        Creates a new group.

        :param name:                The name to be used for the new group.
        :type  name:                str

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The new group ID is returned.
        :rtype:     int

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))

        body = {
            "name": name,
            "description":description
        }
        

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        
        jsonified_response = json.loads(raw_response.text)
        new_group_id = jsonified_response['id']

        return new_group_id

    def history(self, groupid, client_id=None,csvdump=False):

        """
        Get group history.

        :param groupid:             The id to be used to fetch group history.
        :type  groupid:             int

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The history of group id.
        :rtype:     str

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))+f'/{groupid}/history'

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        jsonified_response = json.loads(raw_response.text)
        
        if csvdump==True:
            field_names = []
            for item in jsonified_response[0]:
                field_names.append(item)
            try:
                with open('grouphistory.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    for item in jsonified_response:
                        writer.writerow(item)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)
        return jsonified_response

    def deletebygroupids(self, groupids, client_id=None,csvdump=False):

        """
        Deletes groups as specified in search_filters.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    A list of dicts containing name/assetCriticality of deleted groups is returned.
        :rtype:     list

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/delete"

        body = {
            "filterRequest": {
                "filters": [{"field":"id","exclusive":False,"operator":"IN","value":f"{','.join([str(i) for i in groupids])}"}]}
        }

        if csvdump==True:
            self.downloadfilterinexport('groupexport',[{"field":"id","exclusive":False,"operator":"IN","value":f"{','.join([str(i) for i in groupids])}"}])
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            

        if raw_response.status_code == 200:   
            jsonified_response = json.loads(raw_response.text)
            deleted_groups = jsonified_response['id']

        return deleted_groups
 
    def delete(self, search_filters, client_id=None,csvdump=False):

        """
        Deletes groups as specified in search_filters.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    A list of dicts containing name/assetCriticality of deleted groups is returned.
        :rtype:     list

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/delete"

        body = {
            "filterRequest": {
                "filters": search_filters
            }
        }


        if csvdump==True:
            self.downloadfilterinexport('groupexportbeforedeleting',search_filters)
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            

        if raw_response.status_code == 200:   
            jsonified_response = json.loads(raw_response.text)
            deleted_groups = jsonified_response['id']

        return deleted_groups

    def update_single_group(self, group_id, client_id=None, **kwargs):

        """
        Updates a group name and/or asset criticality.

        :param group_id:    The group ID.
        :type  group_id:    int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :keyword name:                  The new name.  (str)
        :keyword asset_criticality:     The new asset criticality.  (int)

        :return:    The job ID is returned.
        :rtype:     int

        :s RequestFailed:
        :s ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        name = kwargs.get('name', None)
        description = kwargs.get('description', None)

        url = self.api_base_url.format(str(client_id)) + "/" + str(group_id)

        body = {}

        if name is not None:
            body.update(name=name)

        if description is not None:
            body.update(description=description)

        if body == {}:
             ValueError("Body is empty. Please provide name and/or description")

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def update_multiple_groups(self, search_filters, new_asset_criticality, client_id=None):

        """
        Updates the default asset criticality of multiple groups, based on the specified filter(s).

        :param search_filters:          A list of dictionaries containing filter parameters.
        :type  search_filters:          list

        :param new_asset_criticality:   Reflects the default criticality of Hosts in the groups.
        :type  new_asset_criticality:   integer

        :param client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:               int

        :return:    The job ID is returned
        :rtype:     int

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        body = {
            "assetCriticality": new_asset_criticality,
            "filterRequest": {
                "filters": search_filters
            }
        }

        url = self.api_base_url.format(str(client_id)) + "/update"

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def assign(self, search_filters, user_ids, client_id=None):

        """
        Assign group(s) to user IDs, based on specified filter(s)

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param user_ids:        A list of user IDs.
        :type  user_ids:        list

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The job ID is returned.
        :rtype:     int

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/assign"

        body = {
            "filters": search_filters,
            "userIds": user_ids
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def unassign(self, search_filters, user_ids, client_id=None,csvdump=False):

        """
        Unassign group(s) from user IDs, based on specified filter(s)

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param user_ids:        A list of user IDs.
        :type  user_ids:        list

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The job ID is returned.
        :rtype:     int

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/unassign"

        if csvdump==True:
            self.downloadfilterinexport('groupexportbeforeunassigning',search_filters)

        body = {
            "filters": search_filters,
            "userIds": user_ids
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def get_model(self, client_id=None):

        """
        Get available projections and models for Groups.

        :param client_id:   Client ID
        :type  client_id:   int

        :return:    Group projections and models are returned.
        :rtype:     dict

        :s RequestFailed:
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

        :s RequestFailed:
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
    
    def getexporttemplate(self,client_id=None):
        
        """
        Gets configurable export template for application findings.

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The Exportable fields
        :rtype:     list

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/export/template"

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        exportablefilter = json.loads(raw_response.text)

        for i in range(len(exportablefilter['exportableFields'])):
            for j in range(len(exportablefilter['exportableFields'][i]['fields'])):
                if exportablefilter['exportableFields'][i]['fields'][j]['selected']==False:
                    exportablefilter['exportableFields'][i]['fields'][j]['selected']=True

        return exportablefilter['exportableFields']

    def export(self, search_filters, file_name, row_count=ExportRowNumbers.ROW_ALL,file_type=ExportFileType.CSV, client_id=None):

        """
        Initiates an export job on the platform for group(s) based on the
        provided filter(s).

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param file_name:       The name to be used for the exported file.
        :type  file_name:       str

        :param row_count:       No of rows to be exported. Possible options : (ExportRowNumbers.ROW_5000,ExportRowNumbers.ROW_10000,ExportRowNumbers.ROW_25000,ExportRowNumbers.ROW_50000",ExportRowNumbers.ROW_100000",ExportRowNumbers.ROW_ALL)
        :type  row_count:       str

        :param exportable_filter:       Exportable filter
        :type  exportable_filter:       list

        :param file_type:       File type to export.  ExportFileType.CSV, ExportFileType.XML, or ExportFileType.XLSX
        :type  file_type:       str

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The job ID in the platform from is returned.
        :rtype:     int

        :s RequestFailed:
        """
        func_args = locals()
        func_args['exportable_filter']=self.getexporttemplate()
        func_args.pop('self')

        if client_id is None:
            func_args['client_id'] = self._use_default_client_id()[1]

        try:
            export_id = self._export(self.subject_name, **func_args)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        
        return export_id

    def exportselectedgroups(self,groupid, file_name, row_count=ExportRowNumbers.ROW_ALL,file_type=ExportFileType.CSV, client_id=None):

        """
        Initiates an export job on the platform for group(s) based on the
        provided filter(s).

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param file_name:       The name to be used for the exported file.
        :type  file_name:       str

        :param row_count:       No of rows to be exported. Possible options : (ExportRowNumbers.ROW_5000,ExportRowNumbers.ROW_10000,ExportRowNumbers.ROW_25000,ExportRowNumbers.ROW_50000",ExportRowNumbers.ROW_100000",ExportRowNumbers.ROW_ALL)
        :type  row_count:       str

        :param exportable_filter:       Exportable filter
        :type  exportable_filter:       list

        :param file_type:       File type to export.  ExportFileType.CSV, ExportFileType.XML, or ExportFileType.XLSX
        :type  file_type:       str

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The job ID in the platform from is returned.
        :rtype:     int

        :s RequestFailed:
        """
        func_args = locals()
        func_args['exportable_filter']=self.getexporttemplate()
        func_args.pop('self')

        func_args['search_filters']=[{"field":"id","exclusive":False,"operator":"IN","value":f"{','.join(groupid)}"}]

        if client_id is None:
            func_args['client_id'] = self._use_default_client_id()[1]

        try:
            export_id = self._export(self.subject_name, **func_args)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
        
        return export_id


    def group_filter_fields(self,clientid=None):
        """
        List fields that can be filtered by in the search endpoint

        :param client_id:  The client id , if none, takes default client id
        :return client_id: int
        
        """
        
        if clientid is None:
            clientid = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(clientid)) + "/filter"

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

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