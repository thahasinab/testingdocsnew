""" *******************************************************************************************************************
|
|  Name        :  __application_findings.py
|  Module      :  risksense_api
|  Description :  A class to be used for searching for and updating Application Findings on the RiskSense Platform.
|  Copyright   :  (c) RiskSense, Inc.
|  License     :  Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
******************************************************************************************************************* """

from cmath import e
import json
import datetime
from ..__exports import ExportFileType
from ..__exports import ExportRowNumbers
from ...__subject import Subject
from ..._params import *
from ..._api_request_handler import *
from ..__notifications import Notifications
from ..__exports import Exports
import csv
import zipfile
import sys
import pandas as pd


class ApplicationFindings(Subject):

    """ ApplicationFindings Class """

    def __init__(self, profile):

        """
        Initialization of ApplicationFindings object.

        :param profile:     Profile Object
        :type  profile:     _profile
        """
        self.subject_name = 'applicationFinding'
        Subject.__init__(self, profile, self.subject_name)
        self.alt_base_api_url=self.profile.platform_url + "/api/v1/client/{}/search/{}"

    def create(self,applicationids:list,assessmentid:int, synopsis:str,description:str,severity:str,sourceid:str,scanneruuid:str,title:str,solution:str,parameter:str,payload:str,request:str,response:str,filterrequests:list,cweids:list,applicationurl:str,isSelectedAll:bool=False,csvdump:bool=False,client_id:int=None)->json:

        """
        Creates application finding.

        :param applicationids:  A list containing application ids the findings are part of
        :type  applicationids:  list

        :param assessmentid:    Assessment id of the finding
        :type  assessmentid:    int

        :param synopsis:       Synopsis for the application finding
        :type  synopsis:       str

        :param description:       description for the application finding
        :type  description:       str

        :param severity:       Application severity 
        :type  description:       str

        :param sourceid:       Sourceid of the application
        :type  sourceid:       str

        :param scanneruuid:      scanneruuid of the application
        :type  scanneruuid:      str

        :param title:      title for the application
        :type  title:      str

        :param solution:      solution for the application
        :type  solution:      str

        :param parameter:      parameter for the application
        :type  parameter:      str

        :param payload:      payload for the application
        :type  payload:      str

        :param request:      request for the application
        :type  request:      str

        :param response:      request for the application
        :type  response:      str


        :param filterrequests:      filterrequests for the application as a list
        :type  filterrequests:      list

        :param cweids:      cwe ids  for the application as a list
        :type  cweids:      list

        :param applicationurl:      applicationurl  for the application as a list
        :type  applicationurl:      applicationurl

        :param isSelectedAll:      whether isselectedall
        :type  isSelectedAll:      bool
       
        :param csvdump: dumps id to csv
        :type csvdump: bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    Jsonified response.
        :rtype:     json

        :Exception RequestFailed,Exception :
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))

        body = {
            "applicationIds":applicationids,"assessmentId":assessmentid,
            "synopsis":synopsis,"description":description,
            "severity":severity,
            "sourceId":sourceid,"scannerUuid":scanneruuid,
            "title":title,
            "solution":solution,
            "parameter":parameter,
            "payload":payload,
            "request":request,
            "response":response,
            "isSelectedAll":isSelectedAll,
            "filterRequest":{"filters":filterrequests},
            "cweIds":cweids,
            "applicationUrl":applicationurl}

        if type(csvdump)!=bool:
            print('Error in csvdumpvalue,Please provide either true or false')
            exit()
        
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
            jsonified_response = json.loads(raw_response.text)

        except (RequestFailed,Exception) as e:
            print('There was an error creating application finding')
            print(e)
            exit()
       
        if csvdump==True:
            applicationfinding={'jobid':[jsonified_response['id']]}
            df = pd.DataFrame(applicationfinding)
            df.to_csv('applicationfindingcreated.csv',index=False)
        return jsonified_response

    def update(self,applicationfindingid:int,applicationids:int,assessmentid:int,applicationurl:str,severity:int,sourceid:int,title:str,description:str,solution:str,synopsis:str,notes:str,cweids:int,request:str,response:str,parameter:str,payload:str,vulnrequestid:int,csvdump:bool=False,client_id:int=None)->json:

        """
        Update application finding.

        :param applicationfindingid:  An id of the application finding to update
        :type  applicationfindingid:  int

        :param applicationids:  A list containing application ids the findings are part of
        :type  search_filters:  list

        :param assessmentid:    Assessment id of the finding
        :type  assessmentid:    int

        :param applicationurl:  Url of the application
        :type  search_filters:  str

        :param severity:       Application severity 
        :type  severity:        int

        :param sourceid:       Sourceid of the application
        :type  sourceid:       int

        
        :param title:      title for the application
        :type  title:      str

        :param description:       description for the application finding
        :type  description:       str

        :param solution:      solution for the application
        :type  solution:      str

        :param synopsis:       Synopsis for the application finding
        :type  synopsis:       str

        :param notes:       notes for application finding
        :type  notes:       str

        :param cweids:       cwe id
        :type  cweids:       int

        
        :param request:      request for the application
        :type  request:      str

        :param response:      request for the application
        :type  response:      str

        :param parameter:      parameter for the application
        :type  parameter:      str

        :param payload:      payload for the application
        :type  payload:      str

        :param vulnrequestid:      payload for the application
        :type  vulnrequestid:      str        

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    Jsonified response.
        :rtype:     json

        :Exception RequestFailed,Exception :
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))+'/{}'.format(str(applicationfindingid))
        body = {
                "applicationId": applicationids,
                "assessmentId": assessmentid,
                "applicationUrl": applicationurl,
                "severity": severity,
                "sourceId": sourceid,
                "title": title,
                "description": description,
                "solution": solution,
                "synopsis": synopsis,
                "notes":    notes,
                "cweId": cweids,
                "request": request,
                "response": response,
                "parameter": parameter,
                "payload": payload,
                "vulnRequestId": vulnrequestid
                }
        
        if type(csvdump)!=bool:
            print('Please provide either true or false')
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
            jsonified_response = json.loads(raw_response.text)
            
        except (RequestFailed,Exception) as e:
            print('There was an error creating application finding')
            print(e)
            exit()
    
        if csvdump==True:
            hostfinding={'jobid':[jsonified_response['id']]}
            df = pd.DataFrame(hostfinding)
            df.to_csv('applicationfindingupdates.csv',index=None)
        
        return jsonified_response
        

    def get_model(self, client_id:int=None):

        """
        Get available projections and models for Application Findings.

        :param client_id:   Client ID
        :type  client_id:   int

        :return:    Application Finding projections and models are returned.
        :rtype:     dict

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            response = self._model(self.subject_name, client_id)
            
        except (RequestFailed,Exception) as e:
            print('There was an error getting available projection models for application findings')
            print(e)
            exit()

        return response
    def list_applicationfinding_filter_fields(self,client_id:int=None):

        """
        Lists application finding filter fields.

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON output from the platform is returned, listing the available filter fields.
        :rtype:     dict

        :s RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))+'/filter'
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url) 
            jsonified_response = json.loads(raw_response.text)
            return jsonified_response

        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()


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
            print('There was an error getting suggest values for filter fields')
            print(e)
            exit()
        return response
        

    def search(self, search_filters:list, projection:str=Projection.BASIC, page_size=150,
               sort_field=SortField.ID, sort_dir=SortDirection.ASC,csvdump:bool=False, client_id:int=None):

        """
        Searches for and returns application findings based on the provided filter(s) and other parameters.
        Rather than returning paginated results, this function cycles through all pages of results and returns
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

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :param csvdump:       csvdump is a boolean which you can make true if you want to dump the data from system filters in a csv. Keep it false if its not needed.
        :type  csvdump:       bool

        :return:    A list containing all application findings returned by the search using the filter provided.
        :rtype:     list

        :raises RequestFailed:
        """

        func_args = locals()
        func_args.pop('self')
        all_results = []
        func_args.pop('csvdump')
        if client_id is None:
            client_id, func_args['client_id'] = self._use_default_client_id()

        try:
            page_info = self._get_page_info(subject_name=self.subject_name, search_filters=search_filters,
            page_size=page_size, client_id=client_id)
            num_pages = page_info[1]
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print(e)
            exit()

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()
        
        
        page_range = range(0, num_pages)

        try:
            all_results = self._search(self.subject_name, self.get_single_search_page, page_range, **func_args)
        except (RequestFailed,Exception) as e:
            print('There was an error searching application finding data')
            print(e)
            exit()

        if csvdump==True:
            self.downloadfilterinexport('applicationfindingdatasearch',search_filters)
        return all_results


    def downloadfilterinexport(self,filename:str,filters:list,client_id:int=None):
        
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


    def get_single_search_page(self, search_filters, projection=Projection.BASIC, page_num=0, page_size=150,
                               sort_field=SortField.ID, sort_dir=SortDirection.ASC, client_id:int=None,csvdump=False):

        """
        Searches for and returns application findings based on the provided filter(s) and other parameters.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param projection:      The projection to use for API call.  Projection.BASIC or Projection.DETAIL
        :type  projection:      Projection attribute

        :param page_num:        Page number of results to be returned.
        :type  page_num:        int

        :param page_size:       Number of results to be returned per page.
        :type  page_size:       int

        :param sort_field:      Name of field to sort results on.
        :type  sort_field:      SortField attribute

        :param sort_dir:        Direction to sort. SortDirection.ASC or SortDirection.DESC.
        :type  sort_dir:        SortDirection attribute

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The paginated JSON response from the platform is returned.
        :rtype:     dict

        :raises RequestFailed:
        """
        try:
            func_args = locals()
            func_args.pop('self')

            if client_id is None:
                client_id, func_args['client_id'] = self._use_default_client_id()

            try:
                response = self._get_single_search_page(self.subject_name, **func_args)
            except (RequestFailed,Exception) as e:
                print('Error finding application findings data')
                print()
                print(e)

            return response
        except (Exception) as e:
                print('There was an error in getting single search page')
                print(e)
                exit()
    def apply_system_filters(self, csvdump:bool=False,client_id:int=None,):

        """
        Get data from system filters for application findings.

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :param csvdump:       csvdump is a boolean which you can make true if you want to dump the data from system filters in a csv. Keep it false if its not needed.
        :type  csvdump:       bool

        :raises RequestFailed:
        """
        try:
            if client_id is None:
                client_id = self._use_default_client_id()[0]
            
            url= self.profile.platform_url + "/api/v1/search/systemFilter"

            try:
                systemfilter = self.request_handler.make_request(ApiRequestHandler.GET, url)
            except (RequestFailed,Exception) as e:
                print('There was an error fetching system filters data')
                print(e)
                exit()
            
            systemfilter=json.loads(systemfilter.text)

            systemfilters={}

            for filter in systemfilter:
                for applicationFindingsystemfilter in filter['subjectFilters']:
                    if applicationFindingsystemfilter['subject']=="applicationFinding":
                        systemfilters[filter['name']]=applicationFindingsystemfilter["filterRequest"]
        
            systemfilterkeys=list(systemfilters.keys())
            i=0
            try:
                for key in systemfilterkeys:
                    print(f'Index-{i},Key:{key}')
                    i=i+1
                actualfilter=systemfilters[ systemfilterkeys[int(input('Please enter the key for the system filter to add:'))]]
            except IndexError as ex:
                print()
                print('There was an error fetching system filters data')
                print('Please enter an index number from the above list')
                exit()
            except (Exception) as e:
                print('There was an error fetching system filters data')
                print(e)
                exit()

            try:
                response=self.search(actualfilter['filters'])
            except (Exception) as e:
                print('There was an error fetching search data')
                print(e)
                exit()
            

            if csvdump==True:
                self.downloadfilterinexport('applicationfindingdataofsystemfilter',actualfilter['filters'])
            return response
        except (Exception) as e:
                print('There was an error in apply system filters function')
                print(e)
                exit()


    def get_groupby_appfinding(self,client_id:int=None):

        """
        Returns groupby data especially key metrics 

        :param client_id:      The client id , if none, default client id is taken
        :type  client_id:       int

        :return appfindinggroupbykeymetrics: Returns the key metrics of the group by data
        :type return: dict  
        
        """
        try:
            if client_id is None:
                    client_id = self._use_default_client_id()[0]

            url = url = self.api_base_url.format(str(client_id)) + "/group-by"

            try:
                    raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
            except (RequestFailed,Exception) as e:
                print('There was an error fetching groupby fields data')
                print(e)
                exit()

            jsonified_response = json.loads(raw_response.text)

            appfindinggroupbykeymetrics={}

            for i in range(len(jsonified_response['groupByFields'])):
                appfindinggroupbykeymetrics[jsonified_response['groupByFields'][i]['key']]=[jsonified_response['groupByFields'][i]['groupMetrics'][j]['key'] for j in range(len(jsonified_response['groupByFields'][i]['groupMetrics']))]

                
            return appfindinggroupbykeymetrics
        except (Exception) as e:
                print('There was an error in returning group by key metrics function')
                print(e)
                exit()
        

    def groupby_appfinding(self,filters:list=[],sortorder:str=None,csvdump:bool=False,client_id:int=None):

        """
        Gets groupby data for all application finding
        
        :param filters:        The filters which will be used for groupby
        :type filters:         list

        :param sortorderfield: The order to sort the groupby values, please choose ASC for ascending and DESC for descending
        :type sortorderfield:  str

        :param csvdump:      Whether to export the data populated, if false will not export
        :type  csvdump:       bool

        :param client_id:      The client id , if none, default client id is taken
        :type  client_id:       int

        :return jsonified response
        :return type : dict


        
        """
        try:
            if client_id is None:
                    client_id = self._use_default_client_id()[0]

            url = url = self.api_base_url.format(str(client_id)) + "/group-by"

            appfindingslist=self.get_groupby_appfinding()

            appfindingskeys=list(appfindingslist.keys())

            try:
                for i in range(len(appfindingskeys)):
                    print(f'Index-{i},Key:{appfindingskeys[i]}')
                keymetric=appfindingskeys[int(input('Please enter the key for group by parameter:'))]
            except IndexError as ex:
                print()
                print('There was an error fetching group by data')
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
                    "metricFields": appfindingslist[keymetric],
                    "filters": filters,
                    "sortOrder": sortorder
                    }
            try:
                    raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
                    jsonified_response = json.loads(raw_response.text)
            except (RequestFailed,Exception) as e:
                print('There was an error fetching groupby data')
                print(e)
                exit()
            try:
                if csvdump==True:
                    field_names = []
                    for item in jsonified_response['data'][0]:
                        field_names.append(item)

                    try:
                        with open('applicationfindinggroupby.csv', 'w') as csvfile:
                            writer = csv.DictWriter(csvfile, fieldnames=field_names)
                            writer.writeheader()
                            for item in jsonified_response['data']:
                                writer.writerow(item)
                    except FileNotFoundError as fnfe:
                        print("An exception has occurred while attempting to write the .csv file.")
                        print()
                        print(fnfe)
            except Exception as e:
                    print('There seems to be an exception')
                    print(e)
                    exit()
            return jsonified_response
        except (Exception) as e:
                print('There was an error getting all group by data')
                print(e)
                exit()

    def get_count(self, search_filters:list, client_id:int=None):

        """
        Gets a count of application findings identified using the provided filter(s).

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The number of application findings identified is returned.

        :raises RequestFailed:
        """
        try:
            if client_id is None:
                client_id = self._use_default_client_id()[0]

            try:
                page_info = self._get_page_info(self.subject_name, search_filters, client_id=client_id)
                count = page_info[0]
            except (RequestFailed,Exception) as e:
                print('There was an error getting count data')
                print(e)
                exit()

            return count
        except (Exception) as e:
                print('There was an error completing the get count function')
                print(e)
                exit()

    def add_tag(self, search_filters:list, tag_id:int, csvdump:bool=False,client_id:int=None):

        """
        Add a tag to application findings.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param tag_id:          The tag ID to apply.
        :type  tag_id:          int

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The job ID is returned.
        :rtype:     int

        :raises RequestFailed:
        """
        try:
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
                print('There was an error adding tag')
                print(e)
                exit()
            
            if csvdump==True:
                self.downloadfilterinexport('applicationfindingtagadd',search_filters)

            jsonified_response = json.loads(raw_response.text)
            job_id = jsonified_response['id']

            return job_id
        except (Exception) as e:
                print('There was an error completing the tag addition function')
                print(e)
                exit()
        

    def remove_tag(self, search_filters:list, tag_id:int,csvdump:bool=False, client_id:int=None):

        """
        Remove a tag to application findings.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param tag_id:          The tag ID to remove.
        :type  tag_id:          int

        :param csvdump:       csvdump is a boolean which you can make true if you want to dump the data from system filters in a csv. Keep it false if its not needed.
        :type  csvdump:       bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The job ID in the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """
        try:
            if client_id is None:
                client_id = self._use_default_client_id()[0]
            
            if csvdump==True:
                self.downloadfilterinexport('applicationfindingtowhichtagisremoved',search_filters)

            url = self.api_base_url.format(str(client_id)) + "/tag"
            
            body = {"tagId":tag_id,"isRemove":True,"filterRequest":{"filters":search_filters},"publishTicketStats":False}

            try:
                raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url=url, body=body)
            except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            
            jsonified_response = json.loads(raw_response.text)
            job_id = jsonified_response['id']

            return job_id
        except (Exception) as e:
                print('There was an error completing the tag removal function')
                print(e)
                exit()
        

    def assign(self, search_filters:list, user_ids:list,csvdump:bool=False, client_id:int=None):

        """
        Assign user(s) to application findings.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param user_ids:        A list of user IDs.
        :type  user_ids:        list

        :param csvdump:       Dumps data in csv  
        :type  csvdump:       bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The job ID in the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/assign"

        body = {
            "filters": search_filters,
            "userIds": user_ids
        }


        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        if csvdump==True:
            self.downloadfilterinexport('applicationfindingtagisassigned',search_filters)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There was an error assigning tag')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def unassign(self, search_filters:list, user_ids:list,csvdump:bool=False, client_id:int=None):

        """
        Unassigns user(s) from application findings.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param user_ids:        A list of user IDs.
        :type  user_ids:        list


        :param csvdump:       csvdump is a boolean which you can make true if you want to dump the data from system filters in a csv. Keep it false if its not needed.
        :type  csvdump:       bool

        
        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The job ID in the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/unassign"

        body = {
            "filters": search_filters,
            "userIds": user_ids
        }
        
        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()


        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There was an error unassigning tag')
            print(e)
            exit()
        
        if csvdump==True:
            self.downloadfilterinexport(f'applicationfindingtagisunassigned',search_filters)

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def getdynamiccolumns(self,client_id:int=None):
        
        """
        Gets Dynamic columns for the application findings.

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The Dynamic columns
        :rtype:     list

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.alt_base_api_url.format(str(client_id),self.subject_name) + "/dynamic-columns"

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('There was an error in getting dynamic columns')
            print(e)
            exit()
        jsonified_response = json.loads(raw_response.text)
        return jsonified_response
        
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
            print('There was an error getting export template')
            print(e)
            exit()
        
        exportablefilter = json.loads(raw_response.text)

        for i in range(len(exportablefilter['exportableFields'])):
            for j in range(len(exportablefilter['exportableFields'][i]['fields'])):
                if exportablefilter['exportableFields'][i]['fields'][j]['selected']==False:
                    exportablefilter['exportableFields'][i]['fields'][j]['selected']=True

        return exportablefilter['exportableFields']

    def export(self, search_filters:list, file_name:str, row_count:str=ExportRowNumbers.ROW_ALL,file_type:str=ExportFileType.CSV, client_id:int=None):

        """
        Initiates an export job on the platform for application finding(s) based on the
        provided filter(s), by default fetches all the columns data.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param file_name:       The name to be used for the exported file.
        :type  file_name:       str

        :param row_count:       No of rows to be exported. Possible options : (ExportRowNumbers.ROW_5000,ExportRowNumbers.ROW_10000,ExportRowNumbers.ROW_25000,ExportRowNumbers.ROW_50000",ExportRowNumbers.ROW_100000",ExportRowNumbers.ROW_ALL)
        :type  row_count:       str

        :param file_type:       File type to export.  ExportFileType.CSV, or ExportFileType.JSON
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
            print('There was an error performing export job')
            print(e)
            exit()
        return export_id
  
    def subscribe_new_open_ransomware_findings(self,client_id:int=None):

        """
        Subscribes the user to new open ransomware findings

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The response to the subscription that was performed
        :rtype:     dict

        """

        if client_id is None:
            client_id = self._use_default_client_id()
        
        self.notifications=Notifications(self.profile)
        try:
            subscribe = self.notifications.subscribe_notifications(notificationtypeid=4,subscribe=True)
        except (RequestFailed,Exception) as e:
            print('There was an error subscribing new open ransomware findings')
            print(e)
            exit()

        return subscribe

    def unsubscribe_new_open_ransomware_findings(self,client_id:int=None):

        """
        Unsubscribes the user from new open ransomware findings

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The response to the subscription that was performed
        :rtype:     dict

        """

        if client_id is None:
            client_id = self._use_default_client_id()
        self.notifications=Notifications(self.profile)
        try:
            print(client_id)
            subscribe = self.notifications.unsubscribe_notifications(notificationtypeid=4)
        except (RequestFailed,Exception) as e:
            print('There was an error unsubscribing new open ransomware findings')
            print(e)
            exit()

        return subscribe

    def subscribe_new_open_critical_findings_vrr(self,client_id:int=None):

        """
        Subscribes the user to new open critical findings

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The response to the subscription that was performed
        :rtype:     dict

        """

        if client_id is None:
            client_id = self._use_default_client_id()
        
        self.notifications=Notifications(self.profile)
        try:
            subscribe = self.notifications.subscribe_notifications(notificationtypeid=5,subscribe=True)
        except (RequestFailed,Exception) as e:
            print('There was an error subscribing new open critical findings vrr')
            print(e)
            exit()

        return subscribe

    def unsubscribe_new_open_critical_findings_vrr(self,client_id:int=None):

        """
        Unsubscribes the user from new open critical findings

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The response to the subscription that was performed
        :rtype:     dict

        """

        if client_id is None:
            client_id = self._use_default_client_id()
        
        self.notifications=Notifications(self.profile)
        try:
            subscribe = self.notifications.subscribe_notifications(notificationtypeid=6,subscribe=True)
        except (RequestFailed,Exception) as e:
            print('There was an error unsubscribing new open critical findings severity')
            print(e)
            exit()

        return subscribe

    def subscribe_new_open_critical_findings_severity(self,client_id:int=None):

        """
        Subscribes the user to new open critical findings based on severity

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The response to the subscription that was performed
        :rtype:     dict

        """

        if client_id is None:
            client_id = self._use_default_client_id()
        self.notifications=Notifications(self.profile)
        try:
            print(client_id)
            subscribe = self.notifications.subscribe_notifications(notificationtypeid=6)
        except (RequestFailed,Exception) as e:
            print('There was an error unsubscribing new open critical findings severity')
            print(e)
            exit()

        return subscribe

    def unsubscribe_new_open_critical_findings_severity(self,client_id:int=None):

        """
        Unsubscribes the user to new open critical findings based on severity

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The response to the subscription that was performed
        :rtype:     dict

        """

        if client_id is None:
            client_id = self._use_default_client_id()
        self.notifications=Notifications(self.profile)
        try:
            print(client_id)
            subscribe = self.notifications.unsubscribe_notifications(notificationtypeid=6)
        except (RequestFailed,Exception) as e:
            print('There was an error unsubscribing new open critical findings severity')
            print(e)
            exit()

        return subscribe

    def subscribe_new_open_high_findings_vrr(self,client_id:int=None):

        """
        Subscribes the user to new open high findings based on vrr

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The response to the subscription that was performed
        :rtype:     dict

        """

        if client_id is None:
            client_id = self._use_default_client_id()
        
        self.notifications=Notifications(self.profile)
        try:
            subscribe = self.notifications.subscribe_notifications(notificationtypeid=7,subscribe=True)
        except (RequestFailed,Exception) as e:
            print('There was an error subscribing new open high findings vrr')
            print(e)
            exit()

        return subscribe

    def unsubscribe_new_open_high_findings_vrr(self,client_id:int=None):

        """
        Unsubscribe the user from new open high findings based on vrr

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The response to the subscription that was performed
        :rtype:     dict

        """

        if client_id is None:
            client_id = self._use_default_client_id()
        self.notifications=Notifications(self.profile)
        try:
            print(client_id)
            subscribe = self.notifications.unsubscribe_notifications(notificationtypeid=7)
        except (RequestFailed,Exception) as e:
            print('There was an error unsubscribing new open high findings vrr')
            print(e)
            exit()

        return subscribe

    def subscribe_new_open_high_findings_severity(self,client_id:int=None):

        """
        Subscribes the user to new open high findings based on severity

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The response to the subscription that was performed
        :rtype:     dict

        """

        if client_id is None:
            client_id = self._use_default_client_id()
        
        self.notifications=Notifications(self.profile)
        try:
            subscribe = self.notifications.subscribe_notifications(notificationtypeid=8,subscribe=True)
        except (RequestFailed,Exception) as e:
            print('There was an error subscribing new open high findings severity')
            print(e)
            exit()

        return subscribe

    def unsubscribe_new_open_high_findings_severity(self,client_id:int=None):

        """
        Unsubscribes the user from new open high findings based on severity

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The response to the subscription that was performed
        :rtype:     dict

        """

        if client_id is None:
            client_id = self._use_default_client_id()
        
        self.notifications=Notifications(self.profile)
        try:
            print(client_id)
            subscribe = self.notifications.unsubscribe_notifications(notificationtypeid=8)
        except (RequestFailed,Exception) as e:
            print('There was an error unsubscribing to new open high findings severity')
            print(e)
            exit()

        return subscribe

    def update_due_date(self, search_filters:list, due_date:str,csvdump:bool=False, client_id:int=None):

        """
        Update the due date for remediation of an application finding.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param due_date:        The due date to assign.  Must be in "YYYY-MM-DD" format.
        :type  due_date:        str

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :return:    The job ID in the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """




        if client_id is None:
            client_id = self._use_default_client_id()[0]

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()


        url = self.api_base_url.format(str(client_id)) + "/update-due-date"
        
        body = {
            "filterRequest": {
                "filters": search_filters
            },
            "dueDate": due_date
        }
        
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There was an error updating due date')
            print(e)
            exit()
        
        if csvdump==True:
            self.downloadfilterinexport('applicationfindingsduedateupdated',search_filters)

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id
    
    def self_assign(self,filterfields:list,userid:list,csvdump:bool=False,client_id:int=None):

        """
        The application findings fetched are assigned to the current user

        :param filterfields:  A list of dictionaries containing filter parameters.
        :type  filterfields:  list

        :param userid:           A list of user IDs to be assigned to hostfinding(s).
        :type  userid:           list

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :return:    The job ID in the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """
        
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/self-assign"

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()
 
        if csvdump==True:
            self.downloadfilterinexport('applicationfindingsselfassign',filterfields)

        body = {
                "filters": filterfields,
                "userIds": userid
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There was an error performing self assignment')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id
    
    def self_unassign(self,filterfields:list,userid:list,csvdump=False,client_id:int=None,):

        """
        The application findings fetched are unassigned from the current user

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param userid:           A list of user IDs to be assigned to hostfinding(s).
        :type  userid:           list

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The job ID in the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """
        
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/self-unassign"

        if csvdump==True:
            self.downloadfilterinexport('applicationfindingsselfunassign',filterfields)

        body = {
                "filters": filterfields,
                "userIds": userid
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There was an error performing self unassignment')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def add_note(self, search_filters:list, note:str,csvdump:bool=False, client_id:int=None):

        """
        Add a note to application finding(s).

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param note:            A note to assign to the application findings.
        :type  note:            str

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :return:    The job ID in the platform is returned.
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
            print('There was an error adding notes')
            print(e)
            exit()
        
        if csvdump==True:
            self.downloadfilterinexport('addnote',search_filters)

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def add_ticket_tag(self,search_filters:list,tag_id,client_id:int=None):

        """
        The application findings fetched are unassigned from the current user

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The job ID in the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """
        

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+f'/api/v1//client/{client_id}/search/applicationFinding/job/tag'

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

    def delete_manage_observations(self,applicationfindingid:int,vulnrequestid:int,csvdump:bool=False,client_id:int=None):

        """
        Delete manage observations

        :param applicationfindingid:    Application finding id
        :type  applicationfindingid:       int

        :param vulnrequestid:     Vulnerability request id
        :type  vulnrequestid:      int

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:        Client id of user, if none gets default client id
        :type  client_id:        int

        :return jsonified_response:   Success
        :type  jsonified_response:       bool
        
        """

        if client_id is None:
                client_id = self._use_default_client_id()[0]

        url = url = self.api_base_url.format(str(client_id)) + "/{}/request/{}".format(applicationfindingid,vulnrequestid)

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()
        
        if csvdump==True:
            self.downloadfilterinexport('deletemanageobservations',[{"field":"id","exclusive":False,"operator":"IN","value":f"{applicationfindingid}"}])

        try:
                raw_response = self.request_handler.make_request(ApiRequestHandler.DELETE, url=url)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        success=True
        return success
        
            

    def delete(self, search_filters:list, csvdump:bool=False,client_id:int=None):

        """
        Delete application findings based on filter(s).

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param csvdump:       csvdump is a boolean which you can make true if you want to dump the data from system filters in a csv. Keep it false if its not needed.
        :type  csvdump:       bool

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The job ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        
        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        if csvdump==True:
            self.downloadfilterinexport('applicationfindingsthataredeleted',search_filters)
        
        url = self.api_base_url.format(str(client_id)) + "/delete"

        body = {
            "filterRequest": {
                "filters": search_filters
            }
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There was an error delete application findings')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def _tag(self, search_filters:list, tag_id:int, is_remove=False,client_id:int=None):

        """
        Add/Remove a tag to application findings.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param tag_id:          The tag ID to apply.
        :type  tag_id:          int

        :param is_remove:       remove tag? Mention true if need to be removed or false if to add
        :type  is_remove:       bool
       
        :param client_id:       Client ID.
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
            "isRemove": is_remove,
            "filterRequest": {
                "filters": search_filters
            }
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There was an error fetching adding or removing tag for application findings')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def map_findings(self, filter_request:list,workflowtype:str,workflowuuid:str,csvdump:bool=False, client_id:int=None):

        """
        Maps findings to a worklow request based on workflow uuid.

        :param filter_request:      A list of dictionaries containing filter parameters.
        :type  filter_request:      list

        :param workflowtype:         Type of workflow, either falsePositive,remediation,acceptance,severityChange. Please use the exact names as above for workflow type.
        :type  workflowtype:        str

        :param workflowuuid:        Uuid of the workflow.
        :type  workflowuuid:        str

        :param csvdump:       csvdump is a boolean which you can make true if you want to dump the data from system filters in a csv. Keep it false if its not needed.
        :type  csvdump:       bool

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

        url = self.profile.platform_url+'/api/v1/client/{}/workflowBatch/{}/{}/map'.format(str(client_id),workflowtype,workflowuuid)

        body = {"subject":"applicationFinding","filterRequest":{"filters":filter_request}}

        
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There was an error mapping application findings data')
            print(e)
            exit()
        
        if csvdump==True:
            self.downloadfilterinexport('applicationfindingsmappedtotheworkflow',filter_request)

        success=True
        
        return success

    def unmap_findings(self, filter_request:list,workflowtype:str,workflowuuid:str,csvdump:bool=False,client_id:int=None):

        """
        Unmaps findings from worklow request based on workflow uuid.

        :param filter_request:      A list of dictionaries containing filter parameters.
        :type  filter_request:      list
        :param workflowtype:      Type of workflow, either falsePositive,remediation,acceptance,severityChange. Please use the exact names as above for workflow type
        :type  workflowtype:      str

        :param workflowuuid:        Uuid of the workflow.
        :type  workflowuuid:        str

        :param csvdump:       csvdump is a boolean which you can make true if you want to dump the data from system filters in a csv. Keep it false if its not needed.
        :type  csvdump:       bool

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The job ID is returned.
        :rtype:     int

        :raises RequestFailed:
        """


        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+'/api/v1/client/{}/workflowBatch/{}/{}/unmap'.format(str(client_id),workflowtype.lower(),workflowuuid)

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        if csvdump==True:
            self.downloadfilterinexport('applicationfindingsunmappedfromkworkflow',filter_request)

        body = {"subject":"applicationFinding","filterRequest":{"filters":filter_request}}



        try:

            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There was an error performing unmap of application findings')
            print(e)
            exit()
        success= True

        return success



    ##### BEGIN PRIVATE FUNCTIONS #####################################################

 


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
