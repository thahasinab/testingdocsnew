""" *******************************************************************************************************************
|
|  Name        :  __applications.py
|  Module      :  risksense_api
|  Description :  A class to be used for searching for and updating Applications on the RiskSense Platform.
|  Copyright   :  (c) RiskSense, Inc.
|  License     :  Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
******************************************************************************************************************* """

from ast import Delete
from cmath import e
import json

from risksense_api import SearchFilter
from ..__exports import ExportFileType
from ..__exports import ExportRowNumbers
from ...__subject import Subject
from ..._params import *
from ..._api_request_handler import *
from ..__exports import Exports
import csv
import zipfile
import sys
import pandas as pd


class Applications(Subject):

    """ Applications class """

    def __init__(self, profile):

        """
        Initialization of Applications object.

        :param profile:     Profile Object
        :type  profile:     _profile
        """

        self.subject_name = "application"
        Subject.__init__(self, profile, self.subject_name)

    def create(self, name:str,groupids:list,networkid:int,applicationurl:str,criticality:int,externality:bool=False,csvdump:bool=False, client_id=None):

        """
        Create an application

        :param name:  Name of the application .
        :type  name:  str

        :param groupids:  ids of the groups you want it to be assigned to
        :type  groupids:  list

        :param networkid:       network id. Id of network the application to be a part of
        :type  networkid:       int

        :param applicationurl:       url of the application.
        :type  applicationurl:       str

        :param criticality:  the application criticality
        :type  criticality:       int

        :param externality: the application whether external or internal. Externality is true if application is external , false if internal

        :type  criticality:       bool

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    Jsonified response.
        :rtype:     json

        :raises RequestFailed,Exception:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))

        body =  {"name":name,"groupIds":groupids,"networkId":networkid,"url":applicationurl,"criticality":criticality,"externality":externality}

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('Error in creating application')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        if csvdump==True:
            jobid={'applicationid':[jsonified_response['id']]}
            df=pd.DataFrame(jobid)
            df.to_csv('applicationid.csv')

        return jsonified_response

    def delete(self, filterrequest:list,csvdump:bool=False, client_id:int=None):

        """
        Deletes an application

        :param filterrequest:  Search filters .
        :type  filterrequest:  list

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :return:    Jsonified response.
        :rtype:     json

        :raises RequestFailed,Exception:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))+'/delete'

        body =  {"filterRequest":{"filters":filterrequest}}

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        if csvdump==True:
            self.downloadfilterinexport('deletedapplications',filterrequest)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('Error in creating application')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response



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
        except(RequestFailed,MaxRetryError,StatusCodeError, ValueError) as e:
                    print(e)
                    print()
                    print("Unable to retrieve file. Exiting.")
                    sys.exit(1)

    def list_application_filter_fields(self,client_id:int=None):

        """
        Lists application filter fields.

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

    def get_single_search_page(self, search_filters, page_num=0, page_size=150,
                               sort_field=SortField.ID, sort_dir=SortDirection.ASC, client_id=None):

        """
        Searches for and returns applications based on the provided filter(s) and other parameters for a single page.

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
        except (RequestFailed,Exception) as e:
            print('Error finding application data')
            print(e)
            exit()

        return response

    def get_groupby_application(self,client_id=None):

        """
        Get groupby keymetrics

        :param client_id:      The client id , if none, default client id is taken
        :type  client_id:       int

        :return:    The keymetrics of the groupby
        :rtype:     dict
        
        """

        if client_id is None:
                client_id = self._use_default_client_id()[0]

        url = url = self.api_base_url.format(str(client_id)) + "/group-by"

        try:
                raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('Error getting group by application data')
            print(e)
            exit()


        jsonified_response = json.loads(raw_response.text)

        applicationgroupbykeymetrics={}
        
        for i in range(len(jsonified_response['groupByFields'])):
            applicationgroupbykeymetrics[jsonified_response['groupByFields'][i]['key']]=[jsonified_response['groupByFields'][i]['groupMetrics'][j]['key'] for j in range(len(jsonified_response['groupByFields'][i]['groupMetrics']))]
            
        return applicationgroupbykeymetrics



    def groupby_application(self,filters:list=[],sortorder:str=None,csvdump:bool=False,client_id:bool=None,):

        """
        Get groupby values for applications

        :param filters:        The filters which will populate in groupby
        :type filters:         list

        :param sortorderfield: The order to sort the groupby values, please choose ASC for ascending and DESC for descending
        :type sortorderfield:  str

        :param csvdump:       csvdump is a boolean which you can make true if you want to dump the data from system filters in a csv. Keep it false if its not needed.
        :type  csvdump:       bool

        :param client_id:      The client id , if none, default client id is taken
        :type  client_id:       int

        :return:    The groupby values of the application findings.
        :rtype:     dict

        
        """

        if client_id is None:
                client_id = self._use_default_client_id()[0]

        url = url = self.api_base_url.format(str(client_id)) + "/group-by"

        applicationslist=self.get_groupby_application()

        applicationskeys=list(applicationslist.keys())

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()
        try:
            for i in range(len(applicationskeys)):
                print(f'Index-{i},Key:{applicationskeys[i]}')
            keymetric=applicationskeys[int(input('Please enter the key for group by parameter:'))]
        except IndexError as ex:
            print()
            print('There was an error fetching group by data')
            print(ex)
            print('Please enter an index number from the above list')
            exit()
        except (Exception) as e:
            print('There was an error fetching group by data')
            print(e)
            exit()

        
        if sortorder is None:
            sortorder=[{"field":keymetric,"direction":"ASC"}]

        body = {
                "key": keymetric,
                "metricFields": applicationslist[keymetric],
                "filters": filters,
                "sortOrder": sortorder
                }
        try:
                raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There was an error fetching group by data')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)
        try:
            if csvdump==True:
                field_names = []
                for item in jsonified_response['data'][0]:
                    field_names.append(item)
                try:
                    with open('applicationgroupby.csv', 'w') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=field_names)
                        writer.writeheader()
                        for item in jsonified_response['data']:
                            writer.writerow(item)
                except (FileNotFoundError,Exception) as fnfe:
                    print("An exception has occurred while attempting to write the .csv file.")
                    print()
                    print(fnfe)
                    exit()
                else:
                    return jsonified_response
        except (Exception,RequestFailed) as e:
            print('Error dumping data in csv')
            print()
            print(e)
            exit()

        return jsonified_response

    def apply_system_filters(self, csvdump=False,client_id=None,):

        """
        Get data from system filters for application findings.

        :param csvdump:       csvdump is a boolean which you can make true if you want to dump the data from system filters in a csv. Keep it false if its not needed.
        :type  csvdump:       bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The data of the application findings based on the system filter chosen.
        :rtype:     dict

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        
        url= self.profile.platform_url + "/api/v1/search/systemFilter"

        try:
            systemfilter = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('Error getting data')
            print()
            print(e)
            exit()
        
        systemfilter=json.loads(systemfilter.text)

        systemfilters={}

        for filter in systemfilter:
            for applicationsystemfilter in filter['subjectFilters']:
                if applicationsystemfilter['subject']=="application":
                    systemfilters[filter['name']]=applicationsystemfilter["filterRequest"]
    
        systemfilterkeys=list(systemfilters.keys())
        i=0
        try:
            for key in systemfilterkeys:
                print(f'Index-{i},Key:{key}')
                i=i+1
            actualfilter=systemfilters[ systemfilterkeys[int(input('Please enter the key for group by parameter:'))]]
        except (IndexError) as ex:
            print()
            print('There was an error fetching system filters data')
            print('Please enter an index number from the above list')
            print(ex)
            exit()
        except (Exception) as e:
            print('There was an error fetching system filters data')
            print(e)
            exit()

        if csvdump==True:
            self.downloadfilterinexport('applicationsystemfilterdata',actualfilter['filters'])

        response=self.search(actualfilter['filters'])

        return response

    def search(self, search_filters:list, page_size=150, sort_field=SortField.ID, sort_dir=SortDirection.ASC, csvdump:bool=False,client_id:int=None,):

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

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    A list containing all applications returned by the search using the filter provided.
        :rtype:     list

        :raises RequestFailed:
        :raises Exception:
        """

        func_args = locals()
        func_args.pop('self')
        func_args.pop('csvdump')
        all_results = []

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()


        if client_id is None:
            client_id, func_args['client_id'] = self._use_default_client_id()

        try:
            page_info = self._get_page_info(subject_name=self.subject_name, search_filters=search_filters,
                                            page_size=page_size, client_id=client_id)
            num_pages = page_info[1]
        except (RequestFailed,Exception) as e:
            print('Error fetching application data')
            print(e)
            exit()


        page_range = range(0, num_pages)

        try:
            all_results = self._search(self.subject_name, self.get_single_search_page, page_range, **func_args)
        except (RequestFailed,Exception) as e:
            print('Error fetching application data')
            print(e)
            exit()
        
        if csvdump==True:
            self.downloadfilterinexport('applcationsearch',search_filters)

        return all_results

    def get_count(self, search_filters, client_id=None):

        """
        Gets a count of applications identified using the provided filter(s).

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The number of applications identified using the filter(s).
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            response = self.get_single_search_page(search_filters, client_id=client_id)
        except (RequestFailed,Exception) as e:
            print('Error fetching application data')
            print(e)
            exit()


        count = response['page']['totalElements']

        return count

    def merge_application(self, searchfilters:list,application_id_to_merge_to:int, csvdump:bool=False,client_id:int=None):

        """
       Merges applications based on search filters to the application id provided.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param application_id_to_merge_to: Application id to merge to.
        :type  application_id_to_merge_to:          int

        :param csvdump:       csvdump is a boolean which you can make true if you want to dump the data from system filters in a csv. Keep it false if its not needed.
        :type  csvdump:       bool        

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The job ID is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        
        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        if csvdump==True:
            self.downloadfilterinexport('applicationsmerged',searchfilters)

        url = self.profile.platform_url+'/api/v1/client/{}/search/application/job/merge'.format(str(client_id))

        body = {"filterRequest":{"filters":searchfilters},"sourceId":application_id_to_merge_to}

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('Error in merging applications')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def set_asset_criticality(self, filter:list,assetcriticality:int, csvdump:bool=False,client_id:int=None):

        """
        Set asset criticality for the application.

        :param filter:  A list of dictionaries containing filter parameters.
        :type  filter:  list

        :param assetcriticality:  The asset criticality to set the filter specified applications to.
        :type  assetcriticality:   int

        :param csvdump:       csvdump is a boolean which you can make true if you want to dump the data from system filters in a csv. Keep it false if its not needed.
        :type  csvdump:       bool  

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The job ID is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/update"

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()


        body = {"filterRequest":{"filters":filter},"criticality":assetcriticality}

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('Error in setting asset criticality')
            print(e)
            exit()

        if csvdump==True:
            self.downloadfilterinexport('applicationssetassetcriticality',filter)

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def set_address_type(self, filter:list,addresstype:str, csvdump:bool=False,client_id:int=None):

        """
        Set address type fo the application.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param addresstype:    The address type whether external or internal, provide string external for external and internal for internal 
        :type  addresstype:    str

        :param csvdump:       csvdump is a boolean which you can make true if you want to dump the data from system filters in a csv. Keep it false if its not needed.
        :type  csvdump:       bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The job ID is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/update"

        if addresstype.lower()=='internal':
            addresstypes=False
        if addresstype.lower()=='external':
            addresstypes=True

        body = {"filterRequest":{"filters":filter},"isExternal":addresstypes}

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('Error in setting address type')
            print(e)
            exit()
        
        if csvdump==True:
            self.downloadfilterinexport('applicationssetaddresstype',filter)

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def edit_application(self,filter:list,name:str,url:str,csvdump=True,client_id:int=None):

        """
        Edits an application.

        :param filter:  A list of dictionaries containing filter parameters.
        :type  filter:  list

        :param name:    Name of the application
        :type  name:    str

        :param url:    Url of the application
        :type  url:    str

        :param csvdump:       csvdump is a boolean which you can make true if you want to dump the data from system filters in a csv. Keep it false if its not needed.
        :type  csvdump:       bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The job ID is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/update"

        body = {"filterRequest":{"filters":filter,"sort":[],"projection":"basic","page":0,"size":10},"name":name,"url":url}

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()


        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('Error in setting address type')
            print(e)
            exit()

        if csvdump==True:
            self.downloadfilterinexport('applicationupdates',filter)

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id


    def add_tag(self, search_filters:list, tag_id:int,csvdump:bool=False, client_id=None):

        """ 
        Add a tag to application(s).

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param tag_id:          The tag ID to add to the application(s).
        :type  tag_id:          int

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The job ID is returned.
        :rtype:     int

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/tag"

        body = {
            "tagId": tag_id,
            "isRemove": False,
            "filterRequest": {
                "filters": search_filters
            }
        }

        if type(csvdump)!=bool:
            print('Please provide either true or false')
            exit()
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('Error in adding tag')
            print(e)
            exit()

        if csvdump==True:
            self.downloadfilterinexport('appfindingtagadddata',search_filters)

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def remove_tag(self, search_filters:list, tag_id:int, csvdump:bool=False,client_id:int=None):

        """
        Remove a tag from application(s).

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param tag_id:          The tag ID to remove from the application(s).
        :type  tag_id:          int

        :param csvdump:       csvdump is a boolean which you can make true if you want to dump the data from system filters in a csv. Keep it false if its not needed.
        :type  csvdump:       bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The job ID is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/tag"

        body = {
            "tagId": tag_id,
            "isRemove": True,
            "filterRequest": {
                "filters": search_filters
            }
        }

        if type(csvdump)!=bool:
            print('Please provide either true or false')
            exit()

        if csvdump==True:
            self.downloadfilterinexport('applicationsremovetag',search_filters)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('Error in removing tag')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def getexporttemplate(self,client_id:int=None):
        
        """
        Gets configurable export template for application findings.

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
        Initiates an export job on the platform for application finding(s) based on the
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


    def network_move(self, search_filters:list, network_id:int, force_merge:bool=False,csvdump:bool=False, client_id:int=None):

        """
        Move an application to a different network.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param network_id:      The ID of the network the application should be moved to.
        :type  network_id:      int

        :param force_merge:     Boolean indicating whether or not a merge should be forced.
        :type  force_merge:     bool

        :param csvdump:       csvdump is a boolean which you can make true if you want to dump the data from system filters in a csv. Keep it false if its not needed.
        :type  csvdump:       bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The job ID is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/network/move"

        body = {
            "filterRequest": {
                "filters": search_filters
            },
            "targetNetworkId": network_id,
            "isForceMerge": force_merge
        }

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()


        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('Error in moving application across network')
            print(e)
            exit()
        
        if csvdump==True:
            self.downloadfilterinexport('applicationsnetworkmove',search_filters)


        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id
    

    def run_urba(self, search_filters:list,csvdump:bool=False, client_id:int=None):

        """
        Initiates the update of remediation by assessment for application(s) specified in filter(s).

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param csvdump:       csvdump is a boolean which you can make true if you want to dump the data from system filters in a csv. Keep it false if its not needed.
        :type  csvdump:       bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The job ID is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/update-remediation-by-assessment"

        body = {
            "filterRequest": {
                "filters": search_filters
            }
        }

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        if csvdump==True:
            self.downloadfilterinexport('applicationsrunurba',search_filters)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('Error in running urba')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id


    def add_note(self, search_filters:list, note:str,csvdump:bool=False, client_id:int=None):

        """
        Add a note to applications based on search filters.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param note:            A note to be added to the application(s).
        :type  note:            str

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The job ID is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/note"

        body = {
            "filterRequest": {
                "filters": search_filters
            },
            "note": note
        }

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()
        


        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('Error in adding note')
            print(e)
            exit()
        
        if csvdump==True:
            self.downloadfilterinexport('addnote',search_filters)

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def get_model(self, client_id:int=None):

        """
        Get available projections and models for Applications.

        :param client_id:   Client ID
        :type  client_id:   int

        :return:    Application projections and models are returned.
        :rtype:     dict

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            response = self._model(self.subject_name, client_id)
        except (RequestFailed,Exception) as e:
            print('Error in getting model')
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
            print('Error in suggesting value for filter fields')
            print(e)
            exit()

        return response

    def add_group(self, search_filter:list, group_ids:list,csvdump:bool=False, client_id=None):

        """
        Add application(s) to one or more groups.

        :param search_filter:   Search filter
        :type  search_filter:   list

        :param group_ids:       List of Group IDs to add to application(s).
        :type  group_ids:       list

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:       Client ID
        :type  client_id:       int

        :return:    Job ID of group add job
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        
        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()


        try:
            response = self._add_group(self.subject_name, search_filter, group_ids, client_id)
        except (RequestFailed,Exception) as e:
            print('Error in adding applications to group')
            print(e)
            exit()

                
        if csvdump==True:
            self.downloadfilterinexport('addgroup',search_filter)

        return response

    def remove_group(self, search_filter:list, group_ids:list,csvdump:bool=False,client_id=None):

        """
        Remove application(s) from one or more groups.

        :param search_filter:   Search filter
        :type  search_filter:   list

        :param group_ids:       List of Group IDs to add to application(s).
        :type  group_ids:       list

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:       Client ID
        :type  client_id:       int

        :return:    Job ID of group remove job
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        
        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        try:
            response = self._remove_group(self.subject_name, search_filter, group_ids, client_id)
        except (RequestFailed,Exception) as e:
            print('Error in removing from group')
            print(e)
            exit()

        if csvdump==True:
            self.downloadfilterinexport('removegroup',search_filter)

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
