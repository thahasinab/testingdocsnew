""" *******************************************************************************************************************
|
|  Name        :  __host_findings.py
|  Module      :  risksense_api
|  Description :  A class to be used for searching for and updating HostFindings on the RiskSense Platform.
|  Copyright   :  (c) RiskSense, Inc.
|  License     :  Apache-2.0 (http://www.apache.org/licenses/LICENSE-2.0)
|
******************************************************************************************************************* """

from http import client
import json
import datetime
from pydoc import synopsis
from sre_constants import SUCCESS
from ..__exports import ExportFileType
from ..__exports import ExportRowNumbers
from ...__subject import Subject
from ..._params import *
from ..._api_request_handler import *
from ..__notifications import Notifications
from ..__exports import Exports
import sys
import zipfile
import pandas as pd

import csv


class HostFindings(Subject):

    """ HostFindings class """

    def __init__(self, profile):

        """
        Initialization of HostFindings object.

        :param profile:     Profile Object
        :type  profile:     _profile

        """

        self.subject_name = "hostFinding"
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
                self.exports.download_export(exportid,f"{filename}.zip")
                with zipfile.ZipFile(f"{filename}.zip","r") as zip_ref:
                    zip_ref.extractall(filename)
        except(RequestFailed,MaxRetryError,StatusCodeError, ValueError):
                    print(ex)
                    print()
                    print("Unable to retrieve file. Exiting.")
                    sys.exit(1)
  
    def create(self, host_id_list:list, assessment_id:int, severity:str, source_id:str, scanner_uuid:str,
               title:str, finding_type:str,synopsis:str, description:str,solution:str,service_name:str,service_portnumber:str,filters:list,csvdump:bool=False, client_id=None, **kwargs):
        """
        Manually create a new host finding.

        :param host_id_list:    List of Host IDs to associate with this finding
        :type  host_id_list:    list

        :param assessment_id:   Assessment ID
        :type  assessment_id:   int

        :param severity:        Severity
        :type  severity:        str

        :param source_id:       Source ID
        :type  source_id:       str

        :param scanner_uuid:    Scanner UUID
        :type  scanner_uuid:    str

        :param title:           Host Finding Title
        :type  title:           str

        :param finding_type:    Host Finding Type
        :type  finding_type:    str

        :param synopsis:        Synopsis
        :type  synopsis:        str

        :param description:     Description
        :type  description:     str

        :param solution:        Solution
        :type  solution:        str

        :param service_name:    Service name
        :type  service_name:    str

        :param service_portnumber:  Service portnumber
        :type  service_portnumber:  str

        :param solution:        Solution
        :type  solution:        str

        :param filters   :        A series of filters that make up a complete filter     
        :type filters   :       list   
        
        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :param csvdump: dumps id to csv
        :type csvdump: bool

        :return:               The job ID is returned.
        :rtype:     int

        :except RequestFailed,Exception:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))

        synopsis = kwargs.get("synopsis", None)
        service = kwargs.get("service", None)
        cve_ids = kwargs.get("cve_ids", None)

        body = {
            "hostId": host_id_list,
            "assessmentId": assessment_id,
            "severity": severity,
            "sourceId": source_id,
            "scannerUuid": scanner_uuid,
            "title": title,
            "type": finding_type,
            "description": description,
            "solution": solution,
            "synopsis": synopsis,
            "service": {
                'name': service_name,
                'portNumber': service_portnumber
            },
            "cveIds": cve_ids,
            "filterRequest": {
                "filters":filters
            }
        }

        body = self._strip_nones_from_dict(body)

        if type(csvdump)!=bool:
            print('Please provide either true or false')
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        jsonified_response = json.loads(raw_response.text)
        hostfinding_id = jsonified_response['id']

        if csvdump==True:
            hostfinding={'jobid':[hostfinding_id]}
            df = pd.DataFrame(hostfinding)
            df.to_csv('hostfindingcreated.csv',index=None)

        return hostfinding_id

    def update(self, hostfindingid:int, client_id:int=None,csvdump:bool=False, **kwargs):
        """
        Update a new host finding.

        :param hostfindingid:    Host finding id which you want to update
        :type  hostfindingid:    int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :param csvdump: dumps id to csv
        :type csvdump: bool

        :keyword title:   title
        :type  title:     str
       
        :keyword description:   description
        :type  description:     str

        :keyword synopsis:   synopsis
        :type  synopsis:     str

        :keyword solution:   solution
        :type  solution:     str

        :return:    The hostfinding ID is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))+'/{}'.format(hostfindingid)

        title = kwargs.get("title", None)
        description = kwargs.get("description", None)
        solution = kwargs.get("solution", None)
        synopsis = kwargs.get("synopsis", None)

        body = {
            "description": description,
            "solution": solution,
            "synopsis": synopsis,
            "title": title  
            }

        body = self._strip_nones_from_dict(body)

        if type(csvdump)!=bool:
            print('Please provide either true or false')
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        if type(csvdump)!=bool:
            print('Please provide either true or false')
            exit()
    
        if csvdump==True:
            hostfinding={'jobid':[hostfinding_id]}
            df = pd.DataFrame(hostfinding)
            df.to_csv('hostfindingupdated.csv',index=None)

        jsonified_response = json.loads(raw_response.text)
        hostfinding_id = jsonified_response['id']

        return hostfinding_id

    def delete_manage_observations(self,hostfindingid:int,asssessmentid:list,client_id:int=None,csvdump:bool=False):

        """
        Delete manage observations

        :param hostfindingid:    Host finding id
        :type  hostfindingid:       int

        :param assessmentid:     Assessment id
        :type  assessmentid:       lis

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:        Client id of user, if none gets default client id
        :type  client_id:        int

        :return jsonified_response:    The jsonified response
        :type  jsonified_response:       dict
        
        """

        if client_id is None:
                client_id = self._use_default_client_id()[0]

        url = url = self.api_base_url.format(str(client_id)) + "/{}/assessment/delete".format(hostfindingid)

        body={
                "assessmentIds": asssessmentid
                }

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()
        
        if csvdump==True:
            self.downloadfilterinexport('deletemanageobservations',[{"field":"id","exclusive":False,"operator":"IN","value":f"{hostfindingid}"}])

        try:
                raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url=url,body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        
        jsonified_response = json.loads(raw_response.text)
        
        
            
      
        


        return jsonified_response

    def get_hostfinding_history(self,vulnerableids:list,client_id:int=None,csvdump=True):

        """
        Get Host findings history

        :param vulnerableids:    List of vulnerable ids to get history of
        :type  vulnerableids:       int

        :param client_id:      The client id , if none, default client id is taken
        :type  client_id:       int

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool


        :return jsonified_response:    The jsonified response
        :type  jsonified_response:       dict
        
        """

        if client_id is None:
                client_id = self._use_default_client_id()[0]

        url = url = self.api_base_url.format(str(client_id)) + "/history"

        body={
                "vulnIds": vulnerableids
                }

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        try:
                raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url=url,body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        
      
        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def get_groupby_hostfinding(self,client_id:int=None):

        """
        Get groupby values for app finding

        :param client_id:      The client id , if none, default client id is taken
        :type  client_id:       int

        :return hostfindinggroupbykeymetrics:      The host finding group by key metrics
        :type  hostfindinggroupbykeymetrics:       list
        
        """

        if client_id is None:
                client_id = self._use_default_client_id()[0]

        url = url = self.api_base_url.format(str(client_id)) + "/group-by"

        try:
                raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            

        jsonified_response = json.loads(raw_response.text)

        hostfindinggroupbykeymetrics={}

        for i in range(len(jsonified_response['groupByFields'])):
            hostfindinggroupbykeymetrics[jsonified_response['groupByFields'][i]['key']]=[jsonified_response['groupByFields'][i]['groupMetrics'][j]['key'] for j in range(len(jsonified_response['groupByFields'][i]['groupMetrics']))]

            
        return hostfindinggroupbykeymetrics

    def groupby_hostfinding(self,filters:list=[],sortorder:str=None,client_id:int=None,csvdump:bool=False):

        """
        Get groupby values for app finding

        :param hostfindingkey: The main key where other metric fields depend on
        :type  hostfindingkey: Str

        :param metricfields:   The fields that will be populated,choose one or many of the following "App Finding Assessment Date","App Finding Apps Count","App Finding Open Count","App Finding Closed Count","App Finding VRR Critical Count","App Finding VRR High Count","App Finding VRR Medium Count","App Finding VRR Low Count","App Finding VRR Info Count","App Finding With Threat Count","App Finding Threat Count","App Finding CVE Count"
        :type  metricfields:   list
        
        :param filters:        The filters which will populate in groupby
        :type filters:         list

        :param sortorderfield: The order to sort the groupby values, please choose ASC for ascending and DESC for descending
        :type sortorderfield:  str

        :param client_id:      The client id , if none, default client id is taken
        :type  client_id:       int

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :return groupby:      Group by information
        :type  client_id:     list
        
        """

        if client_id is None:
                client_id = self._use_default_client_id()[0]

        url = url = self.api_base_url.format(str(client_id)) + "/group-by"

        hostfindingslist=self.get_groupby_hostfinding()

        hostfindingskeys=list(hostfindingslist.keys())

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        for i in range(len(hostfindingskeys)):
            print(f'Index-{i},Key:{hostfindingskeys[i]}')
        try:
            keymetric=hostfindingskeys[int(input('Please enter the key for group by parameter:'))]
        except IndexError as ex:
                print()
                print('There was an error fetching group by data')
                print('Please enter an index number from the above list')
                print(ex)
                exit()
        except (Exception) as e:
                print('There was an error fetching group by data')
                print(e)
                exit()


        if sortorder is None:
            sortorder=[{"field":keymetric,"direction":"ASC"}]

        body = {
                "key": keymetric,
                "metricFields": hostfindingslist[keymetric],
                "filters": filters,
                "sortOrder": sortorder
                }
        try:
                raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            

        jsonified_response = json.loads(raw_response.text)

        if csvdump==True:
            field_names = []
            for item in jsonified_response['data'][0]:
                field_names.append(item)
            try:
                with open('hostfindinggroupby.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    for item in jsonified_response['data']:
                        print(item)
                        writer.writerow(item)
            except (FileNotFoundError,Exception) as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)
        return jsonified_response

    def get_single_search_page(self, search_filters, projection=Projection.BASIC, page_num=0, page_size=150,
                               sort_field=SortField.ID, sort_dir=SortDirection.ASC, client_id=None,csvdump=False):

        """
        Searches for and returns hostfindings based on the provided filter(s) and other parameters.

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
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def search(self, search_filters:list, projection=Projection.BASIC, page_size=150,
               sort_field=SortField.ID, sort_dir=SortDirection.ASC, client_id:int=None,csvdump:bool=False):

        """
        Searches for and returns hostfindings based on the provided filter(s) and other parameters.  Rather
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

        :param csvdump:         dumps data in csv
        :type  csvdump:         bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    A list containing all host findings returned by the search using the filter provided.
        :rtype:     list

        :raises RequestFailed:
        """

        func_args = locals()
        func_args.pop('self')
        func_args.pop('csvdump')
        all_results = []

        if client_id is None:
            client_id, func_args['client_id'] = self._use_default_client_id()
        
        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

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
            self.downloadfilterinexport('hostfindingsearchdata',search_filters)

        return all_results

    def get_count(self, search_filters, client_id=None):

        """
        Gets a count of hostfindings identified using the provided filter(s).

        :param search_filters:   A list of dictionaries containing filter parameters.
        :type  search_filters:   list

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The number of hostfindings identified using the provided filter(s).
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            page_info = self._get_page_info(self.subject_name, search_filters=search_filters, client_id=client_id)
            count = page_info[0]
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        return count

    def add_tag(self, search_filters:list, tag_id:int,csvdump:bool=False,client_id:int=None):

        """
        Adds a tag to hostfinding(s).

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param tag_id:          ID of tag to tbe added to hostfinding(s).
        :type  tag_id:          int

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

        url = self.api_base_url.format(str(client_id)) + "/tag"

        if type(csvdump)!=bool:
            print('Please provide either true or false')
            exit()

        body = {
            "tagId": tag_id,
            "isRemove": False,
            "filterRequest": {
                "filters": search_filters
            }
        }

        if csvdump==True:
            self.downloadfilterinexport('hostfindingtagadddata',search_filters)
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        if csvdump==True:
            jobid={'add_tag_jobid':[job_id]}
            df = pd.DataFrame(jobid)
            df.to_csv('add_tag.csv',index=None)
        return job_id

    def remove_tag(self, search_filters:list, tag_id:int, client_id:int=None,csvdump:bool=False):

        """
        Removes a tag from hostfinding(s).

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param tag_id:          ID of tag to tbe removed from hostfinding(s).
        :type  tag_id:          int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

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
            self.downloadfilterinexport('hostfindingtagremovedata',search_filters)

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

    def assign(self, search_filters:list, users:list,csvdump:bool=True, client_id=None):

        """
        Assigns hostfinding(s) to a list of user IDs.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param users:           A list of user IDs to be assigned to hostfinding(s).
        :type  users:           list

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

        url = self.api_base_url.format(str(client_id)) + "/assign"

        body = {
            "filters": search_filters,
            "userIds": users
        }

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()
        
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        
        if csvdump==True:
            self.downloadfilterinexport('assign',search_filters)

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def unassign(self, search_filters:list, users:list,csvdump:bool=False, client_id:int=None):

        """
        Unassigns hostfinding(s) from a list of user IDs.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param users:           A list of user IDs to be unassigned from hostfinding(s).
        :type  users:           list

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

        url = self.api_base_url.format(str(client_id)) + "/unassign"

        body = {
            "filters": search_filters,
            "userIds": users
        }

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

 
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        
        if csvdump==True:
            self.downloadfilterinexport('unassign',search_filters)
        

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id
    
    def self_assign(self,filterfields:list,userid:list,csvdump:bool=False,client_id:int=None):

        """
        The host findings fetched are assigned to the current user

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param userid:           A list of user IDs to be assigned to hostfinding(s).
        :type  userid:           list

        :param client_id:       Client ID. If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The job ID in the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """

         
        

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/self-assign"
        
        body = {
                "filters": filterfields,
                "userIds": userid
        }

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        
        
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        
        if csvdump==True:
            self.downloadfilterinexport('selfassign',filterfields)

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id
    
    def self_unassign(self,filterfields:list,userids:list,client_id:int=None,csvdump:bool=False):

        """
        The host findings fetched are unassigned from the current user

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param userids: A list of integers of user ids
        :type userids: list

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:       Client ID. If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The job ID in the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """
        
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/self-unassign"

        body = {
                "filters": filterfields,
                "userIds":userids
        }

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        if csvdump==True:
            self.downloadfilterinexport('selfunassign',filterfields)
        

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def list_hostfinding_filter_fields(self,client_id:int=None):

        """
        List filter endpoints.

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

    def apply_system_filters(self, client_id=None,csvdump=False):

        """
        Adds a tag to applicationFinding(s).

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param tag_id:          ID of tag to tbe added to applicationFinding(s).
        :type  tag_id:          int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The job ID is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        
        url= self.profile.platform_url + "/api/v1/search/systemFilter"

        try:
            systemfilter = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        
        
        systemfilter=json.loads(systemfilter.text)

        systemfilters={}

        for filter in systemfilter:
            for applicationFindingsystemfilter in filter['subjectFilters']:
                if applicationFindingsystemfilter['subject']=="applicationFinding":
                    systemfilters[filter['name']]=applicationFindingsystemfilter["filterRequest"]
        try:
            systemfilterkeys=list(systemfilters.keys())
            i=0
            for key in systemfilterkeys:
                print(f'Index-{i},Key:{key}')
                i=i+1

            actualfilter=systemfilters[ systemfilterkeys[int(input('Please enter the key for system filter parameter:'))]]

            response=self.search(actualfilter['filters'])

            if csvdump==True:
                self.downloadfilterinexport('hostfindingdataofsystemfilter',actualfilter['filters'])
            print(response)
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()


    def getexporttemplate(self,client_id:int=None):
        
        """
        Gets configurable export template for host findings.

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

        :param exportable_filter:       Exportable filter
        :type  exportable_filter:       list
        :param file_type:               File type to export.  ExportFileType.CSV,ExportFileType.XLSX,ExportFileType.JSON
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
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        return export_id



    def update_due_date(self, search_filters:list, new_due_date:str,csvdump:bool=False, client_id:int=None):

        """
        Updates the due date assigned to hostfinding(s) based on the provided filter(s)

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param new_due_date:    The new due date in the "YYYY-MM-DD" format.
        :type  new_due_date:    str

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

        url = self.api_base_url.format(str(client_id)) + "/update-due-date"

        body = {
            "filterRequest": {
                "filters": search_filters
            },
            "dueDate": new_due_date
        }

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')


        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        
        if csvdump==True:
            self.downloadfilterinexport('update due date',search_filters)

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def add_note(self, search_filters:list, new_note:str,csvdump:bool=False, client_id:int=None):

        """
        Adds a note to hostfinding(s) based on the filter(s) provided.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param new_note:        The note to be added to the hostfinding(s).  String.
        :type  new_note:        str

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
            "note": new_note
        }

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()


        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        
        if csvdump==True:
            self.downloadfilterinexport('addnote',search_filters)

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id


    def delete(self, search_filters:list,csvdump:bool=False, client_id:int=None):

        """
        Deletes hostfinding(s) based on the provided filter(s)

        :param search_filters:   A list of dictionaries containing filter parameters.
        :type  search_filters:   list

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

        url = self.api_base_url.format(str(client_id)) + "/delete"

        body = {
            "filterRequest": {
                "filters": search_filters
            }
        }

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()
        
        if csvdump==True:
            self.downloadfilterinexport('deletedhostfindings',search_filters)

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

    def subscribe_new_open_ransomware_findings(self,client_id=None):

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

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()
        
        self.notifications=Notifications(self.profile)
        try:
            subscribe = self.notifications.subscribe_notifications(notificationtypeid=4,subscribe=True)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        return subscribe

    def unsubscribe_new_open_ransomware_findings(self,client_id=None):

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

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()
        self.notifications=Notifications(self.profile)
        try:
            print(client_id)
            subscribe = self.notifications.unsubscribe_notifications(notificationtypeid=4)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        return subscribe

    def subscribe_new_open_critical_findings_vrr(self,client_id=None):

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

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()
        
        self.notifications=Notifications(self.profile)
        try:
            subscribe = self.notifications.subscribe_notifications(notificationtypeid=5,subscribe=True)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        return subscribe

    def unsubscribe_new_open_critical_findings_vrr(self,client_id=None):

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

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()
        self.notifications=Notifications(self.profile)
        try:
            print(client_id)
            subscribe = self.notifications.unsubscribe_notifications(notificationtypeid=5)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        return subscribe

    def subscribe_new_open_critical_findings_severity(self,client_id=None):

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

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()
        
        self.notifications=Notifications(self.profile)
        try:
            subscribe = self.notifications.subscribe_notifications(self,notificationtypeid=6,subscribe=True)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        return subscribe

    def unsubscribe_new_open_critical_findings_severity(self,client_id=None):

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

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()
        self.notifications=Notifications(self.profile)
        try:
            print(client_id)
            subscribe = self.notifications.unsubscribe_notifications(notificationtypeid=6)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        return subscribe

    def subscribe_new_open_high_findings_vrr(self,client_id=None):

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

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()
        
        self.notifications=Notifications(self.profile)
        try:
            subscribe = self.notifications.subscribe_notifications(notificationtypeid=7,subscribe=True)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        return subscribe

    def unsubscribe_new_open_high_findings_vrr(self,client_id=None):

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

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()
        self.notifications=Notifications(self.profile)
        try:
            print(client_id)
            subscribe = self.notifications.unsubscribe_notifications(notificationtypeid=7)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        return subscribe

    def subscribe_new_open_high_findings_severity(self,client_id=None):

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

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()
        
        self.notifications=Notifications(self.profile)
        try:
            subscribe = self.notifications.subscribe_notifications(notificationtypeid=8,subscribe=True)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        return subscribe

    def unsubscribe_new_open_high_findings_severity(self,client_id=None):

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

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()
        self.notifications=Notifications(self.profile)
        try:
            print(client_id)
            subscribe = self.notifications.subscribe_notifications(self,notificationtypeid=8,subscribe=False)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        return subscribe

    def map_findings(self, filter_request:list,workflowtype:str,workflowuuid:str,csvdump:bool=False,client_id:int=None):

        """
        Map hostfindings to a workflow .

        :param filter_request:      A list of dictionaries containing filter parameters.
        :type  filter_request:      list

        :param workflowtype:      Type of workflow, either falsePositive,remediation,acceptance,severityChange. Please use the exact names as above for workflow type
        :type  workflowtype:      str

        :param workflowuuid:      workflow uuid
        :type  workflowuuid:      str

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The job ID is returned.
        :rtype:     int

        :raises RequestFailed:
        """


        if client_id is None:
            client_id = self._use_default_client_id()[0]

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        body = {"subject":"hostFinding","filterRequest":{"filters":filter_request}}

        try:
            url = self.profile.platform_url+'/api/v1/client/{}/workflowBatch/{}/{}/map'.format(str(client_id),workflowtype,workflowuuid)


        except Exception as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        if csvdump==True:
            self.downloadfilterinexport('mapfindings',filter_request)

        success=True
        return success

    def add_ticket_tag(self,search_filters,tag_id,client_id=None):
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+f'/api/v1/client/{client_id}/search/hostFinding/job/tag'
        print(url)

        body = {"tagId":tag_id,"isRemove":False,"filterRequest":{"filters":search_filters},"publishTicketStats":False}

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response



    def unmap_findings(self, filter_request:list,workflowtype:str,workflowuuid:str,csvdump:bool=False, client_id:int=None):

        """
        Unmap findings from workflow.

        :param filter_request:      A list of dictionaries containing filter parameters.
        :type  filter_request:      list

        :param workflowtype:      Type of workflow, either falsePositive,remediation,acceptance,severityChange. Please use the exact names as above for workflow type
        :type  workflowtype:      str

        :param workflowuuid:      workflow uuid
        :type  workflowuuid:      str

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The job ID is returned.
        :rtype:     int

        :raises RequestFailed:
        """


        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+'/api/v1/client/{}/workflowBatch/{}/{}/unmap'.format(str(client_id),workflowtype,workflowuuid)

        body = {"subject":"hostFinding","filterRequest":{"filters":filter_request}}

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()


        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        
        if csvdump==True:
            self.downloadfilterinexport('unmapfindings',filter_request)
        
        success=True

        return success

    def get_model(self,csvdump:bool=False, client_id:int=None):

        """
        Get available projections and models for Host Findings.

        :param client_id:   Client ID
        :type  client_id:   int

        :param csvdump:     Dumps data in csv
        :type csvdump:      bool    

        :return:    Host Finding projections and models are returned.
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

    def suggest(self, search_filter_1:list, search_filter_2:dict, client_id:int=None):

        """
        Suggest values for filter fields.

        :param search_filter_1:     Search Filter 1
        :type  search_filter_1:     list

        :param search_filter_2:     Search Filter 2
        :type  search_filter_2:     dict

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
