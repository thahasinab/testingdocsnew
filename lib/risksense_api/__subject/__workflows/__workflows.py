""" *******************************************************************************************************************
|
|  Name        :  __workflows.py
|  Description :  Create functions for various utilities of the workflow endpoints
|  Project     :  risksense_api
|  Copyright   :  2022 RiskSense, Inc.
|  License     :  Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
******************************************************************************************************************* """

import json
from pickle import NONE
from tkinter import E
from tkinter.tix import Tree
from ...__subject import Subject
from ..._params import *
from ..._api_request_handler import *
import datetime
import csv
import pandas as pd

class Workflows(Subject):

    """ Workflows class """

    class OverrideControl:

        NONE = "NONE"
        AUTHORIZED = "AUTHORIZED"
    
    class Workflowtype:

        FALSEPOSITIVE = "falsePositive"
        REMEDIATION = "remediation"
        ACCEPTANCE= "acceptance"
        SEVERITYCHANGE="severityChange"
    


    def __init__(self, profile):

        """
        Initialization of Workflows object.

        :param profile:     Profile Object
        :type  profile:     _profile
        """

        self.subject_name = "workflowBatch"
        Subject.__init__(self, profile, self.subject_name)

    def search(self, search_filters:list, projection=Projection.BASIC, page_size=150,
               sort_field=SortField.ID, sort_dir=SortDirection.ASC ,csvdump:bool=False,client_id:int=None):

        """
        Searches for and returns workflows based on the provided filter(s) and other parameters.  Rather
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

        :return:    A list containing all workflows returned by the search using the filter provided.
        :rtype:     list

        :raises RequestFailed:
        :raises Exception:
        """
        csvdumpval=csvdump

        func_args = locals()
        func_args.pop('self')
        func_args.pop('csvdumpval')
        func_args.pop('csvdump')
        if client_id is None:
            client_id, func_args['client_id'] = self._use_default_client_id()

        page_info = self._get_page_info(self.subject_name, search_filters, page_size=page_size, client_id=client_id)
        num_pages = page_info[1]
        page_range = range(0, num_pages)

        
        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            all_results = self._search(self.subject_name, self.get_single_search_page, page_range, **func_args)
        except (RequestFailed, Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()
        try:
            if csvdumpval==True:
                newdump=[]
                for i in all_results:
                    temp={}
                    for key,value in i.items():
                        temp[key]=value
                        if key=='affectedAssets':
                            temp['affectedAssets']=value['value']
                        if key=='affectedFindings':
                            temp['affectedFindings']=value['value']
                        if key=='currentUser':
                            temp['currentuser_username']=value['username']
                            temp['currentuser_firstname']=value['firstName']
                            temp['currentuser_lastname']=value['lastName']
                            temp.pop('currentUser')
                        if key=='filter':
                            temp.pop('filter')
                    newdump.append(temp)
                field_names = []     
                for item in newdump[0]:
                    field_names.append(item)
                try:
                    with open('workflow_batch.csv', 'w') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=field_names)
                        writer.writeheader()
                        for item in newdump:
                            writer.writerow(item)
                except (FileNotFoundError,Exception) as fnfe:
                    print("An exception has occurred while attempting to write the .csv file.")
                    print()
                    print(fnfe)
        except (FileNotFoundError,Exception) as fnfe:
                    print("An exception has occurred")
                    print()
                    print(fnfe)
        return all_results

    def list_workflowbatch_model(self,client_id:int=None):

        """
        Get available projections and models for Workflowbatch.

        :param client_id:   Client ID
        :type  client_id:   int

        :return:    Workflow batch models and projections
        :rtype:     dict

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))+'/model'
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)

        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def list_workflowbatch_filter_fields(self,client_id:int=None):

        """
        List filter endpoints for workflow batch.

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

    def get_single_search_page(self, search_filters:list, projection=Projection.BASIC, page_num=0, page_size=150,
                               sort_field=SortField.ID, sort_dir=SortDirection.ASC, client_id:int=None):

        """
        Searches for and returns workflows based on the provided filter(s) and other parameters.

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
            print('Error in getting workflow details')
            print()
            print(e)
        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def get_model(self, client_id:int=None):

        """
        Get available projections and models for Workflows.

        :param client_id:   Client ID
        :type  client_id:   int

        :return:    Workflows projections and models are returned.
        :rtype:     dict

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            response = self._model(self.subject_name, client_id)
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
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
            print('There seems to be an exception')
            print()
            print(e)
            exit()

        return response


    def request_acceptance(self, search_filter:list, workflow_name:str, description:str, reason:str,finding_type:str,expiration_date:str=None,override_control:str=OverrideControl.AUTHORIZED, compensating_controls:str="NONE", attachment:str=None, client_id:int=None):

        """
        Request acceptance for applicationFindings / hostfFindings as defined in the filter_request parameter.

        :param finding_type:            Finding type. Possible options : ("hostFinding" or "applicationFinding")
        :type  finding_type:            str

        :param search_filter:           A list of dictionaries containing filter parameters.
        :type  search_filter:           list

        :param workflow_name:           Workflow Name
        :type  workflow_name:           str

        :param description:             A description of the request.
        :type  description:             str

        :param reason:                  A reason for the request.
        :type  reason:                  str

        :param override_control:        A description of override controls applied to this finding. Option available : ('NONE', 'AUTHORIZED')
        :type  override_control:        str

        :param compensating_controls:   A description of compensating controls applied to this finding. Option available : ("DLP", "Deemed not exploitable", "Endpoint Security", "IDS/IPS", "MFA Enforced", "Multiple: See Description", "Network Firewall", "Network Segmentation", "Other: See Description", "Web Application Firewall" or "NONE")
        :type  compensating_controls:   str

        :param expiration_date:         An expiration date.  Should be in "YYYY-MM-DD" format.
        :type  expiration_date:         str

        :param attachment:              A path to a file to be uploaded and attached to the request.
        :type  attachment:              str
        

        :param client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:               int

        :return:    Success whether request occured
        :rtype:     bool

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/acceptance/request"

        body = {"subject": finding_type, 
            "filterRequest": {
                "filters": search_filter
                }
            }
        multiform_data = {
            "name": (None,workflow_name),
            "subjectFilterRequest": (None,json.dumps(body)),
            "description": (None,description),
            "reason": (None,reason),
            "overrideControl": (None,override_control),
            "compensatingControls": (None,compensating_controls),
            "files": attachment,
            "expirationDate": (None,expiration_date),
            "isEmptyWorkflow":(None,"false")
            }

        body = self._strip_nones_from_dict(body)
        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, files=multiform_data)
            if raw_response.status_code==201:
                success=True
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

        return success


    def request_false_positive(self, finding_type:str, search_filter:list, workflow_name:str, description:str, reason:str, override_control:str=OverrideControl.AUTHORIZED, expiration_date:str=None, attachment:str=None, client_id:int=None):

        """
        Request false positive for applicationFindings / hostFindings as defined in the filter_request parameter.

        :param finding_type:            Finding type. Possible options : ("hostFinding" or "applicationFinding")
        :type  finding_type:            str

        :param search_filter:           A list of dictionaries containing filter parameters.
        :type  search_filter:           list

        :param workflow_name:           Workflow Name
        :type  workflow_name:           str

        :param description:             A description of the request.
        :type  description:             str

        :param reason:                  A reason for the request.
        :type  reason:                  str

        :param override_control:        A description of override controls applied to this finding. Option available : ('NONE', 'AUTHORIZED')
        :type  override_control:        str

        :param expiration_date:         An expiration date.  Should be in "YYYY-MM-DD" format.
        :type  expiration_date:         str

        :param attachment:              A path to a file to be uploaded and attached to the request.
        :type  attachment:              str

        :param client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:               int

        :return:    Success whether request occured
        :rtype:     bool

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/falsePositive/request"

        body = {"subject": finding_type, 
            "filterRequest": {
                "filters": search_filter
                }
            }
        multiform_data = {
            "name": (None,workflow_name),
            "subjectFilterRequest": (None,json.dumps(body)),
            "description": (None,description),
            "reason": (None,reason),
            "overrideControl": (None,override_control),
            "files": attachment,
            "expirationDate": (None,expiration_date),
            "isEmptyWorkflow":(None,"false")
            }

        body = self._strip_nones_from_dict(body)

        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, files=multiform_data)
            if raw_response.status_code==201:
                success=True
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

        return success


    def request_remediation(self, finding_type:str, search_filter:list, workflow_name:str, description:str, reason:str, override_control:str=OverrideControl.AUTHORIZED, expiration_date:str=None, attachment:str=None, client_id:int=None):

        """
        Request remediation for applicationFindings / hostFindings as defined in the filter_request parameter.

        :param finding_type:            Finding type. Possible options : ("hostFinding" or "applicationFinding")
        :type  finding_type:            str

        :param search_filter:           A list of dictionaries containing filter parameters.
        :type  search_filter:           list

        :param workflow_name:           Workflow Name
        :type  workflow_name:           str

        :param description:             A description of the request.
        :type  description:             str

        :param reason:                  A reason for the request.
        :type  reason:                  str

        :param override_control:        A description of override controls applied to this finding. Option available : ('NONE', 'AUTHORIZED')
        :type  override_control:        str

        :param expiration_date:         An expiration date.  Should be in "YYYY-MM-DD" format.
        :type  expiration_date:         str

        :param attachment:              A path to a file to be uploaded and attached to the request.
        :type  attachment:              str

        :param client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:               int

        :return:    Success whether request occured
        :rtype:     bool

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/remediation/request"

        body = {"subject": finding_type, 
            "filterRequest": {
                "filters": search_filter
                }
            }
        multiform_data = {
            "name": (None,workflow_name),
            "subjectFilterRequest": (None,json.dumps(body)),
            "description": (None,description),
            "reason": (None,reason),
            "overrideControl": (None,override_control),
            "files": attachment,
            "expirationDate": (None,expiration_date),
            "isEmptyWorkflow":(None,"false")
            }

        body = self._strip_nones_from_dict(body)

        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, files=multiform_data)
            if raw_response.status_code==201:
                success=True
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

        return success

    def request_severity_change(self, finding_type:str, search_filter:list, workflow_name:str, description:str, reason:str,  severity_change:str,override_control:str=OverrideControl.AUTHORIZED, expiration_date:str=None, attachment:str=None, client_id:int=None):

        """
        Request severity change for applicationFindings / hostFindings as defined in the filter_request parameter.

        :param finding_type:            Finding type. Possible options : ("hostFinding" or "applicationFinding")
        :type  finding_type:            str

        :param search_filter:           A list of dictionaries containing filter parameters.
        :type  search_filter:           list

        :param workflow_name:           Workflow Name
        :type  workflow_name:           str

        :param description:             A description of the request.
        :type  description:             str

        :param reason:                  A reason for the request.
        :type  reason:                  str

        :param override_control:        A description of override controls applied to this finding. Option available : ('NONE', 'AUTHORIZED')
        :type  override_control:        str

        :param compensating_controls:   Severity change for this finding. Option available : ("1" to "10")
        :type  compensating_controls:   str

        :param expiration_date:         An expiration date.  Should be in "YYYY-MM-DD" format.
        :type  expiration_date:         str

        :param attachment:              A path to a file to be uploaded and attached to the request.
        :type  attachment:              str

        :param client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:               int

        :return:    Success whether request occured
        :rtype:     bool

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/severityChange/request"

        body = {"subject": finding_type, 
            "filterRequest": {
                "filters": search_filter
                }
            }

        multiform_data = {
            "name": (None,workflow_name),
            "subjectFilterRequest": (None,json.dumps(body)),
            "description": (None,description),
            "reason": (None,reason),
            "overrideControl": (None,override_control),
            "severity": (None,severity_change),
            "files": attachment,
            "expirationDate": (None,expiration_date),
            "isEmptyWorkflow":(None,"false")
            }
        

        body = self._strip_nones_from_dict(body)

        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, files=multiform_data)
            if raw_response.status_code==201:
                success=True
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

        return success

    def reject_acceptance(self, filter_request:list, description:str,csvdump:bool=False, client_id:int=None):

        """
        Reject an acceptance request.

        :param filter_request:      A list of dictionaries containing filter parameters.
        :type  filter_request:      list

        :param description:         A description of the rejection.
        :type  description:         str

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The job ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        search_response = self.get_single_search_page(filter_request)
        uuid = search_response['_embedded']['workflowBatches'][0]['uuid']

        url = self.api_base_url.format(str(client_id)) + "/acceptance/reject"

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        body = {
            "workflowBatchUuid":uuid,
            "description":description
            }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        if csvdump==True:
            workflowid={'jobid':[jsonified_response['id']]}
            df = pd.DataFrame(workflowid)
            df.to_csv('rejectworkflow.csv',index=False)

        return job_id

    def reject_false_positive(self, filter_request:list, description:str,csvdump:bool=False, client_id:int=None):

        """
        Reject a false positive request.

        :param filter_request:      A list of dictionaries containing filter parameters.
        :type  filter_request:      list

        :param description:         A description of the rejection.
        :type  description:         str

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The job ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        search_response = self.get_single_search_page(filter_request)
        uuid = search_response['_embedded']['workflowBatches'][0]['uuid']

        url = self.api_base_url.format(str(client_id)) + "/falsePositive/reject"

        body = {
            "workflowBatchUuid":uuid,
            "description":description
            }

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        if csvdump==True:
            workflowid={'jobid':[jsonified_response['id']]}
            df = pd.DataFrame(workflowid)
            df.to_csv('rejectworkflow.csv',index=False)

        return job_id

    def reject_remediation(self, filter_request:list, description:str, csvdump:bool=False,client_id:int=None):

        """
        Reject a remediation request.

        :param filter_request:      A list of dictionaries containing filter parameters.
        :type  filter_request:      list

        :param description:         A description of the rejection.
        :type  description:         str

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The job ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        search_response = self.get_single_search_page(filter_request)
        uuid = search_response['_embedded']['workflowBatches'][0]['uuid']

        url = self.api_base_url.format(str(client_id)) + "/remediation/reject"

        body = {
            "workflowBatchUuid":uuid,
            "description":description
            }
        
        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        if csvdump==True:
            workflowid={'jobid':[jsonified_response['id']]}
            df = pd.DataFrame(workflowid)
            df.to_csv('rejectworkflow.csv',index=False)

        return job_id

    def reject_severity_change(self, filter_request:list, description:str,csvdump:bool=False, client_id:int=None):

        """
        Reject a severity change request.

        param filter_request:      A list of dictionaries containing filter parameters.
        :type  filter_request:      list

        :param description:         A description of the rejection.
        :type  description:         str

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The job ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        search_response = self.get_single_search_page(filter_request)
        uuid = search_response['_embedded']['workflowBatches'][0]['uuid']

        url = self.api_base_url.format(str(client_id)) + "/severityChange/reject"

        body = {
            "workflowBatchUuid":uuid,
            "description":description
            }
        
        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        if csvdump==True:
            workflowid={'jobid':[jsonified_response['id']]}
            df = pd.DataFrame(workflowid)
            df.to_csv('rejectworkflow.csv',index=False)

        return job_id


    def rework_acceptance(self, filter_request:list, description:str,csvdump:bool=False, client_id:int=None):

        """
        Request a rework of an acceptance.

        :param filter_request:      A list of dictionaries containing filter parameters.
        :type  filter_request:      list

        :param description:         A description of the rework.
        :type  description:         str

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The job ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        search_response = self.get_single_search_page(filter_request)
        uuid = search_response['_embedded']['workflowBatches'][0]['uuid']

        url = self.api_base_url.format(str(client_id)) + "/acceptance/rework"

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        body = {
            "workflowBatchUuid":uuid,
            "description":description
            }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        if csvdump==True:
            workflowid={'jobid':[jsonified_response['id']]}
            df = pd.DataFrame(workflowid)
            df.to_csv('reworkworkflow.csv',index=False)

        return job_id

    def rework_false_positive(self, filter_request:list, description:str, csvdump:bool=False,client_id=None):

        """
        Request a rework of a false positive.

        :param filter_request:      A list of dictionaries containing filter parameters.
        :type  filter_request:      list

        :param description:         A description of the rework.
        :type  description:         str

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The job ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        search_response = self.get_single_search_page(filter_request)
        uuid = search_response['_embedded']['workflowBatches'][0]['uuid']

        url = self.api_base_url.format(str(client_id)) + "/falsePositive/rework"

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        body = {
            "workflowBatchUuid":uuid,
            "description":description
            }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        if csvdump==True:
            workflowid={'jobid':[jsonified_response['id']]}
            df = pd.DataFrame(workflowid)
            df.to_csv('reworkworkflow.csv',index=False)

        return job_id

    def rework_remediation(self, filter_request:list, description:str, csvdump:bool=False, client_id:int=None):

        """
        Request a rework of a remediation.

        :param filter_request:      A list of dictionaries containing filter parameters.
        :type  filter_request:      list

        :param description:         A description of the rework.
        :type  description:         str

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The job ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        search_response = self.get_single_search_page(filter_request)
        uuid = search_response['_embedded']['workflowBatches'][0]['uuid']

        url = self.api_base_url.format(str(client_id)) + "/remediation/rework"

        body = {
            "workflowBatchUuid":uuid,
            "description":description
            }

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        if csvdump==True:
            workflowid={'jobid':[jsonified_response['id']]}
            df = pd.DataFrame(workflowid)
            df.to_csv('reworkworkflow.csv',index=False)

        return job_id

    def rework_severity_change(self, filter_request:list, description:str,csvdump:bool=False ,client_id:int=None):

        """
        Request a rework of a severity change.

        :param filter_request:      A list of dictionaries containing filter parameters.
        :type  filter_request:      list

        :param description:         A description of the rework.
        :type  description:         str

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The job ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        search_response = self.get_single_search_page(filter_request)
        uuid = search_response['_embedded']['workflowBatches'][0]['uuid']

        url = self.api_base_url.format(str(client_id)) + "/severityChange/rework"

        body = {
            "workflowBatchUuid":uuid,
            "description":description
            }
        
        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        if csvdump==True:
            workflowid={'jobid':[jsonified_response['id']]}
            df = pd.DataFrame(workflowid)
            df.to_csv('reworkworkflow.csv',index=False)

        return job_id

    def approve_acceptance(self, filter_request:list, override_exp_date:bool=False,
                           expiration_date:str=(datetime.date.today() + datetime.timedelta(days=14)),csvdump:bool=False, client_id:int=None):

        """
        Approve a acceptance request.

        :param filter_request:      A list of dictionaries containing filter parameters.
        :type  filter_request:      list

        :param override_exp_date:   True/False indicating whether or not an expiration date should be overridden.
        :type  override_exp_date:   bool

        :param expiration_date:     An expiration date for the approval.  Should be in "YYYY-MM-DD" format.
        :type  expiration_date:     str

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The job ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """
       
        try:

            if client_id is None:
                client_id = self._use_default_client_id()[0]

            search_response = self.get_single_search_page(filter_request)
            
            uuid = search_response['_embedded']['workflowBatches'][0]['uuid']
            url = self.api_base_url.format(str(client_id)) + "/acceptance/approve"

            body = {
                "workflowBatchUuid": uuid,
                "expirationDate": str(expiration_date),
                "overrideExpirationDate": override_exp_date
            }
            if type(csvdump)!=bool:
                print('Error in csvdump value,Please provide either true or false')
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
            jsonified_response = json.loads(raw_response.text)
            job_id = jsonified_response['id']
            if csvdump==True:
                workflowid={'jobid':[jsonified_response['id']]}
                df = pd.DataFrame(workflowid)
                df.to_csv('approveworkflow.csv',index=False)
            return job_id
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

    def approve_false_positive(self, filter_request:list, override_exp_date:bool=False,expiration_date:str=(datetime.date.today() + datetime.timedelta(days=14)),csvdump:bool=False, client_id:int=None):

        """
        Approve a false positive change request.

        :param filter_request:      A list of dictionaries containing filter parameters.
        :type  filter_request:      list

        :param override_exp_date:   True/False indicating whether or not an expiration date should be overridden.
        :type  override_exp_date:   bool

        :param expiration_date:     An expiration date for the approval.  Should be in "YYYY-MM-DD" format.
        :type  expiration_date:     str

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The job ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        search_response = self.get_single_search_page(filter_request)
        uuid = search_response['_embedded']['workflowBatches'][0]['uuid']

        url = self.api_base_url.format(str(client_id)) + "/falsePositive/approve"

        body = {
            "workflowBatchUuid": uuid,
            "expirationDate": str(expiration_date),
            "overrideExpirationDate": override_exp_date
        }

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        if csvdump==True:
                workflowid={'jobid':[jsonified_response['id']]}
                df = pd.DataFrame(workflowid)
                df.to_csv('approveworkflow.csv',index=False)

        return job_id

    def approve_remediation(self, filter_request:list, override_exp_date:bool=False,expiration_date:str=(datetime.date.today() + datetime.timedelta(days=14)),csvdump:bool=False, client_id:int=None):

        """
        Approve a remediation request.

        :param filter_request:      A list of dictionaries containing filter parameters.
        :type  filter_request:      list

        :param override_exp_date:   True/False indicating whether or not an expiration date should be overridden.
        :type  override_exp_date:   bool

        :param expiration_date:     An expiration date for the approval.  Should be in "YYYY-MM-DD" format.
        :type  expiration_date:     str

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The job ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        search_response = self.get_single_search_page(filter_request)
        uuid = search_response['_embedded']['workflowBatches'][0]['uuid']

        url = self.api_base_url.format(str(client_id)) + "/remediation/approve"

        body = {
            "workflowBatchUuid": uuid,
            "expirationDate": str(expiration_date),
            "overrideExpirationDate": override_exp_date
        }

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        if csvdump==True:
                workflowid={'jobid':[jsonified_response['id']]}
                df = pd.DataFrame(workflowid)
                df.to_csv('approveworkflow.csv',index=False)

        return job_id

    def approve_severity_change(self, filter_request:list, override_exp_date:bool=False,expiration_date:str=(datetime.date.today() + datetime.timedelta(days=14)),csvdump:bool=False, client_id:int=None):

        """
        Approve a severity change request.

        :param filter_request:      A list of dictionaries containing filter parameters.
        :type  filter_request:      list

        :param override_exp_date:   True/False indicating whether or not an expiration date should be overridden.
        :type  override_exp_date:   bool

        :param expiration_date:     An expiration date for the approval.  Should be in "YYYY-MM-DD" format.
        :type  expiration_date:     str

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int


        :return:    The job ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        search_response = self.get_single_search_page(filter_request)
        uuid = search_response['_embedded']['workflowBatches'][0]['uuid']

        url = self.api_base_url.format(str(client_id)) + "/severityChange/approve"

        body = {
            "workflowBatchUuid": uuid,
            "expirationDate": str(expiration_date),
            "overrideExpirationDate": override_exp_date
        }

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        if csvdump==True:
                workflowid={'jobid':[jsonified_response['id']]}
                df = pd.DataFrame(workflowid)
                df.to_csv('approveworkflow.csv',index=False)

        return job_id

    def update_acceptance_workflow(self,workflowBatchUuid:str,name:str,expirationDate:str,description:str,reason:str,compensatingControl:str,overrideControl:str=OverrideControl.AUTHORIZED,csvdump:bool=False, client_id:int=None):

        #acceptance,falsePositive,severityChange,remediation
        """
        Update an acceptance workflow.

        :param workflowBatchUuid:      Workflow UUID
        :type  workflowBatchUuid:      str

        :param name:      Workflow name
        :type  name:      str

        :param expiration_date:     An expiration date for the approval.  Should be in "YYYY-MM-DD" format.
        :type  expiration_date:     str

        :param description:         A description of the rejection.
        :type  description:         str

        :param reason:         A reason for the rejection.
        :type  reason:         str

        :param compensating_controls:   A description of compensating controls applied to this finding. Option available : ("DLP", "Deemed not exploitable", "Endpoint Security", "IDS/IPS", "MFA Enforced", "Multiple: See Description", "Network Firewall", "Network Segmentation", "Other: See Description", "Web Application Firewall" or "NONE")
        :type  compensating_controls:   str

        :param overrideControl:        A description of override controls applied to this finding. Option available : ('NONE', 'AUTHORIZED')
        :type  overrideControl:        str

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The jsonified response.
        :rtype:     dict

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + f"/acceptance/update/"

        body = {"workflowBatchUuid":workflowBatchUuid,"name": name,"expirationDate":expirationDate,"description":description,"reason":reason,"compensatingControl":compensatingControl,"overrideControl":overrideControl}

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        if csvdump==True:
            field_names = []
            for item in jsonified_response:
                field_names.append(item)
            try:
                with open('updateworkflow.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    writer.writerow(jsonified_response)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)
        return jsonified_response


    def update_falsepositive_workflow(self,workflowBatchUuid:str,name:str,expirationDate:str,description:str,reason:str,compensatingControl:str,overrideControl:str=OverrideControl.AUTHORIZED,csvdump:bool=False, client_id:int=None):

        #acceptance,falsePositive,severityChange,remediation
        """
        Update a false positive workflow.

        :param workflowBatchUuid:      Workflow UUID
        :type  workflowBatchUuid:      str

        :param name:      Workflow name
        :type  name:      str

        :param expiration_date:     An expiration date for the approval.  Should be in "YYYY-MM-DD" format.
        :type  expiration_date:     str

        :param description:         A description of the rejection.
        :type  description:         str

        :param reason:         A reason for the rejection.
        :type  reason:         str

        :param compensating_controls:   A description of compensating controls applied to this finding. Option available : ("DLP", "Deemed not exploitable", "Endpoint Security", "IDS/IPS", "MFA Enforced", "Multiple: See Description", "Network Firewall", "Network Segmentation", "Other: See Description", "Web Application Firewall" or "NONE")
        :type  compensating_controls:   str

        :param overrideControl:        A description of override controls applied to this finding. Option available : ('NONE', 'AUTHORIZED')
        :type  overrideControl:        str

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The jsonified response.
        :rtype:     dict

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + f"/falsePositive/update/"

        body = {"workflowBatchUuid":workflowBatchUuid,"name": name,"expirationDate":expirationDate,"description":description,"reason":reason,"compensatingControl":compensatingControl,"overrideControl":overrideControl}

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        if csvdump==True:
            field_names = []
            for item in jsonified_response:
                field_names.append(item)
            try:
                with open('updateworkflow.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    writer.writerow(jsonified_response)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)
        
        return jsonified_response

    def update_remediation_workflow(self,workflowBatchUuid:str,name:str,expirationDate:str,description:str,reason:str,compensatingControl:str,overrideControl:str=OverrideControl.AUTHORIZED,csvdump:bool=False, client_id:int=None):

        #acceptance,falsePositive,severityChange,remediation
        """
        
        Update a remediation workflow.

        :param workflowBatchUuid:      Workflow UUID
        :type  workflowBatchUuid:      str

        :param name:      Workflow name
        :type  name:      str

        :param expiration_date:     An expiration date for the approval.  Should be in "YYYY-MM-DD" format.
        :type  expiration_date:     str

        :param description:         A description of the rejection.
        :type  description:         str

        :param reason:         A reason for the rejection.
        :type  reason:         str

        :param compensating_controls:   A description of compensating controls applied to this finding. Option available : ("DLP", "Deemed not exploitable", "Endpoint Security", "IDS/IPS", "MFA Enforced", "Multiple: See Description", "Network Firewall", "Network Segmentation", "Other: See Description", "Web Application Firewall" or "NONE")
        :type  compensating_controls:   str

        :param overrideControl:        A description of override controls applied to this finding. Option available : ('NONE', 'AUTHORIZED')
        :type  overrideControl:        str

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The jsonified response.
        :rtype:     dict

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + f"/remediation/update/"

        body = {"workflowBatchUuid":workflowBatchUuid,"name": name,"expirationDate":expirationDate,"description":description,"reason":reason,"compensatingControl":compensatingControl,"overrideControl":overrideControl}

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        if csvdump==True:
            field_names = []
            for item in jsonified_response:
                field_names.append(item)
            try:
                with open('updateworkflow.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    writer.writerow(jsonified_response)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)

        return jsonified_response

    def update_severitychange_workflow(self,workflowBatchUuid:str,name:str,expirationDate:str,description:str,reason:str,severity:str,compensatingControl:str,overrideControl:str=OverrideControl.AUTHORIZED, csvdump:bool=False,client_id:int=None):

        #acceptance,falsePositive,severityChange,remediation
        """
        Update an severity change workflow.

        :param workflowBatchUuid:      Workflow UUID
        :type  workflowBatchUuid:      str

        :param name:      Workflow name
        :type  name:      str

        :param expiration_date:     An expiration date for the approval.  Should be in "YYYY-MM-DD" format.
        :type  expiration_date:     str

        :param description:         A description of the rejection.
        :type  description:         str

        :param reason:         A reason for the rejection.
        :type  reason:         str

        :param compensating_controls:   A description of compensating controls applied to this finding. Option available : ("DLP", "Deemed not exploitable", "Endpoint Security", "IDS/IPS", "MFA Enforced", "Multiple: See Description", "Network Firewall", "Network Segmentation", "Other: See Description", "Web Application Firewall" or "NONE")
        :type  compensating_controls:   str

        :param overrideControl:        A description of override controls applied to this finding. Option available : ('NONE', 'AUTHORIZED')
        :type  overrideControl:        str

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The jsonified response.
        :rtype:     dict

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + f"/severityChange/update/"

        body = {"workflowBatchUuid":workflowBatchUuid,"name": name,"expirationDate":expirationDate,"description":description,"reason":reason,"severity":severity,"compensatingControl":compensatingControl,"overrideControl":overrideControl}

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There seems to be an exception')
            print()
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        if csvdump==True:
            field_names = []
            for item in jsonified_response:
                field_names.append(item)
            try:
                with open('updateworkflow.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    writer.writerow(jsonified_response)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)
        return jsonified_response

    def map_findings_acceptance(self,subject:str, filter_request:list,workflowuuid:str,workflowtype:str=Workflowtype.ACCEPTANCE, client_id:int=None):

        """
        Map findings to an acceptance workflow for applicationFindings / hostfFindings as defined in the filter_request parameter.

        :param subject:            Finding type. Possible options : ("hostFinding" or "applicationFinding")
        :type  subject:            str

        :param filter_request:           A list of dictionaries containing filter parameters.
        :type  filter_request:           list

        :param workflowuuid:           Workflow Name
        :type  workflowuuid:           str

        :param workflowtype:             By default acceptance
        :type  workflowtype:             str

        :param client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:               int

        :return:    Success whether request occured
        :rtype:     bool

        :raises RequestFailed:
        """

        if subject.lower()=='hostfinding':
            subject='hostFinding'
        if subject.lower()=='applicationfinding':
            subject='applicationFinding'

        if client_id is None:
            client_id = self._use_default_client_id()[0]


        url = self.profile.platform_url+'/api/v1/client/{}/workflowBatch/{}/{}/map'.format(str(client_id),workflowtype,workflowuuid)

        body = {"subject":subject,"filterRequest":{"filters":filter_request}}

        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
            if raw_response.status_code==200:
                success=True
        except (RequestFailed,Exception) as e:
            print('There was an error mapping data')
            print(e)
            exit()

        return success

    def map_findings_severitychange(self,subject:str, filter_request:list,workflowuuid:str,workflowtype:str=Workflowtype.SEVERITYCHANGE, client_id:int=None):

        """
        Map findings to an severity change workflow for applicationFindings / hostfFindings as defined in the filter_request parameter.

        :param subject:            Finding type. Possible options : ("hostFinding" or "applicationFinding")
        :type  subject:            str

        :param filter_request:           A list of dictionaries containing filter parameters.
        :type  filter_request:           list

        :param workflowuuid:           Workflow Name
        :type  workflowuuid:           str

        :param workflowtype:             By default severity change
        :type  workflowtype:             str

        :param client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:               int

        :return:    Success whether request occured
        :rtype:     bool

        :raises RequestFailed:
        """
        if subject.lower()=='hostfinding':
            subject='hostFinding'
        if subject.lower()=='applicationfinding':
            subject='applicationFinding'

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        

        url = self.profile.platform_url+'/api/v1/client/{}/workflowBatch/{}/{}/map'.format(str(client_id),workflowtype,workflowuuid)

        body = {"subject":subject,"filterRequest":{"filters":filter_request}}

        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
            if raw_response==200:
                success=True
        except (RequestFailed,Exception) as e:
            print('There was an error mapping data')
            print(e)
            exit()

        return success

    def map_findings_falsepositive(self,subject:str, filter_request:list,workflowuuid:str,workflowtype:str=Workflowtype.FALSEPOSITIVE, client_id:int=None):

        """
        Map findings to an false positive workflow for applicationFindings / hostFindings as defined in the filter_request parameter.

        :param subject:            Finding type. Possible options : ("hostFinding" or "applicationFinding")
        :type  subject:            str

        :param filter_request:           A list of dictionaries containing filter parameters.
        :type  filter_request:           list

        :param workflowuuid:           Workflow Name
        :type  workflowuuid:           str

        :param workflowtype:             By default false positive
        :type  workflowtype:             str

        :param client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:               int

        :return:    Success whether request occured
        :rtype:     bool

        :raises RequestFailed:
        """

        if subject.lower()=='hostfinding':
            subject='hostFinding'
        if subject.lower()=='applicationfinding':
            subject='applicationFinding'

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+'/api/v1/client/{}/workflowBatch/{}/{}/map'.format(str(client_id),workflowtype,workflowuuid)

        body = {"subject":subject,"filterRequest":{"filters":filter_request}}

        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
            if raw_response.status_code==200:
                    success=True
        except (RequestFailed,Exception) as e:
            print('There was an error mapping data')
            print(e)
            exit()

        return success


    def map_findings_remediation(self,subject:str, filter_request:list,workflowuuid:str,workflowtype:str=Workflowtype.REMEDIATION, client_id:int=None):

        """
        Map findings to an remediation workflow for applicationFindings / hostFindings as defined in the filter_request parameter.

        :param subject:            Finding type. Possible options : ("hostFinding" or "applicationFinding")
        :type  subject:            str

        :param filter_request:           A list of dictionaries containing filter parameters.
        :type  filter_request:           list

        :param workflowuuid:           Workflow Name
        :type  workflowuuid:           str

        :param workflowtype:             By default remediation
        :type  workflowtype:             str

        :param client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:               int

        :return:    Success whether request occured
        :rtype:     bool

        :raises RequestFailed:
        """

        if subject.lower()=='hostfinding':
            subject='hostFinding'
        if subject.lower()=='applicationfinding':
            subject='applicationFinding'

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+'/api/v1/client/{}/workflowBatch/{}/{}/map'.format(str(client_id),workflowtype,workflowuuid)

        body = {"subject":subject,"filterRequest":{"filters":filter_request}}



        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
            if raw_response.status_code==200:
                    success=True
        except (RequestFailed,Exception) as e:
            print('There was an error mapping data')
            print(e)
            exit()

        return success

    def unmap_findings_acceptance(self, subject:str,filter_request:list,workflowuuid:str,workflowtype:str=Workflowtype.ACCEPTANCE ,client_id:int=None):

        """
        Unmap findings to an acceptance workflow for applicationFindings / hostFindings as defined in the filter_request parameter.

        :param subject:            Finding type. Possible options : ("hostFinding" or "applicationFinding")
        :type  subject:            str

        :param filter_request:           A list of dictionaries containing filter parameters.
        :type  filter_request:           list

        :param workflowuuid:           Workflow Name
        :type  workflowuuid:           str

        :param workflowtype:             By default acceptance
        :type  workflowtype:             str

        :param client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:               int

        :return:    Success whether request occured
        :rtype:     bool

        :raises RequestFailed:
        """
        if subject.lower()=='hostfinding':
            subject='hostFinding'
        if subject.lower()=='applicationfinding':
            subject='applicationFinding'

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+'/api/v1/client/{}/workflowBatch/{}/{}/unmap'.format(str(client_id),workflowtype,workflowuuid)

        body = {"subject":subject,"filterRequest":{"filters":filter_request}}

        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
            if raw_response.status_code==200:
                    success=True
        except (RequestFailed,Exception) as e:
            print('There was an error mapping data')
            print(e)
            exit()

        return success

    def unmap_findings_severitychange(self, subject:str,filter_request:list,workflowuuid:str,workflowtype:str=Workflowtype.SEVERITYCHANGE, client_id:int=None):

        """
        Unmap findings to a severity change workflow for applicationFindings / hostFindings as defined in the filter_request parameter.

        :param subject:            Finding type. Possible options : ("hostFinding" or "applicationFinding")
        :type  subject:            str

        :param filter_request:           A list of dictionaries containing filter parameters.
        :type  filter_request:           list

        :param workflowuuid:           Workflow Name
        :type  workflowuuid:           str

        :param workflowtype:             By default acceptance
        :type  workflowtype:             str

        :param client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:               int

        :return:    Success whether request occured
        :rtype:     bool

        :raises RequestFailed:
        """

        if subject.lower()=='hostfinding':
            subject='hostFinding'
        if subject.lower()=='applicationfinding':
            subject='applicationFinding'

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+'/api/v1/client/{}/workflowBatch/{}/{}/unmap'.format(str(client_id),workflowtype,workflowuuid)

        body = {"subject":subject,"filterRequest":{"filters":filter_request}}

        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
            if raw_response.status_code==200:
                    success=True
        except (RequestFailed,Exception) as e:
            print('There was an error mapping data')
            print(e)
            exit()

        return success

    def unmap_findings_falsepositive(self, subject:str,filter_request:list,workflowuuid:str,workflowtype:str=Workflowtype.FALSEPOSITIVE, client_id:int=None):


        """
        Unmap findings to a false positive  workflow for applicationFindings / hostFindings as defined in the filter_request parameter.

        :param subject:            Finding type. Possible options : ("hostFinding" or "applicationFinding")
        :type  subject:            str

        :param filter_request:           A list of dictionaries containing filter parameters.
        :type  filter_request:           list

        :param workflowuuid:           Workflow Name
        :type  workflowuuid:           str

        :param workflowtype:             By default false positive
        :type  workflowtype:             str

        :param client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:               int

        :return:    Success whether request occured
        :rtype:     bool

        :raises RequestFailed:
        """
        if subject.lower()=='hostfinding':
            subject='hostFinding'
        if subject.lower()=='applicationfinding':
            subject='applicationFinding'

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+'/api/v1/client/{}/workflowBatch/{}/{}/unmap'.format(str(client_id),workflowtype,workflowuuid)

        body = {"subject":subject,"filterRequest":{"filters":filter_request}}

        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
            if raw_response.status_code==200:
                    success=True
        except (RequestFailed,Exception) as e:
            print('There was an error mapping data')
            print(e)
            exit()

        return success

    def unmap_findings_remediation(self, subject:str,filter_request:list,workflowuuid:str,workflowtype:str=Workflowtype.REMEDIATION, client_id:int=None):

        """
        Unmap findings to a remediation workflow for applicationFindings / hostFindings as defined in the filter_request parameter.

        :param subject:            Finding type. Possible options : ("hostFinding" or "applicationFinding")
        :type  subject:            str

        :param filter_request:           A list of dictionaries containing filter parameters.
        :type  filter_request:           list

        :param workflowuuid:           Workflow Name
        :type  workflowuuid:           str

        :param workflowtype:             By default remediation
        :type  workflowtype:             str

        :param client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:               int

        :return:    Success whether request occured
        :rtype:     bool

        :raises RequestFailed:
        """
        if subject.lower()=='hostfinding':
            subject='hostFinding'
        if subject.lower()=='applicationfinding':
            subject='applicationFinding'

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+'/api/v1/client/{}/workflowBatch/{}/{}/unmap'.format(str(client_id),workflowtype,workflowuuid)

        body = {"subject":subject,"filterRequest":{"filters":filter_request}}

        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
            if raw_response.status_code==200:
                    success=True
        except (RequestFailed,Exception) as e:
            print('There was an error mapping data')
            print(e)
            exit()

        return success

    def get_attachments_acceptance(self, workflowbatchuuid:str, subject:str, client_id:int=None):

        """
        Get attachments from an acceptance workflow

        :param workflowbatchuuid:  Workflowbatch uuid
        :type  workflowbatchuuid:  str

        :param subject:     Subject whether hostFinding or applicationFinding
        :type  subject:      str

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    Jsonified response
        :rtype:     text

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+'/api/v1/client/{}/{}/acceptance/{}/attachments'.format(str(client_id),subject,workflowbatchuuid)
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('Error in getting workflow details')
            print()
            print(e)
        jsonified_response = raw_response.text

        return jsonified_response

    def get_attachments_severitychange(self, workflowbatchuuid:str, subject:str, client_id:int=None):

        """
        Get attachments from a severity change workflow

        :param workflowbatchuuid:  Workflowbatch uuid
        :type  workflowbatchuuid:  str

        :param subject:     Subject whether hostFinding or applicationFinding
        :type  subject:      str

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    Jsonified response
        :rtype:     text

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        url = self.profile.platform_url+'/api/v1/client/{}/{}/severityChange/{}/attachments'.format(str(client_id),subject,workflowbatchuuid)
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('Error in getting workflow details')
            print()
            print(e)
        
        jsonified_response = raw_response.text

        return jsonified_response

    def get_attachments_remediation(self, workflowbatchuuid:str, subject:str, client_id:int=None):

        """
        Get attachments from a remediation workflow

        :param workflowbatchuuid:  Workflowbatch uuid
        :type  workflowbatchuuid:  str

        :param subject:     Subject whether hostFinding or applicationFinding
        :type  subject:      str

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    Jsonified response
        :rtype:     text

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+'/api/v1/client/{}/{}/remediation/{}/attachments'.format(str(client_id),subject,workflowbatchuuid)
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('Error in getting workflow details')
            print()
            print(e)
        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def get_attachments_falsepositive(self, workflowbatchuuid:str, subject:str, client_id:int=None):

        """
        Get attachments from a false positive workflow

        :param workflowbatchuuid:  Workflowbatch uuid
        :type  workflowbatchuuid:  str

        :param subject:     Subject whether hostFinding or applicationFinding
        :type  subject:      str

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    Jsonified response
        :rtype:     text

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+'/api/v1/client/{}/{}/falsePositive/{}/attachments'.format(str(client_id),subject,workflowbatchuuid)
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('Error in getting workflow details')
            print()
            print(e)
        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def download_workflowbatch_attachments_acceptance(self, fileuuid:str,subject:str,workflowcategory:str='CLOSE_REQUEST', client_id:int=None):

        """
        Download attachments from an acceptance workflow

        :param fileuuid:  File uuid
        :type  fileuuid:  str

        :param subject:     Subject whether hostFinding or applicationFinding
        :type  subject:      str

        :param workflowcategory:     Workflow category either CLOSE_REQUEST or CHANGE_REQUEST
        :type  workflowcategory:      str

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    Success
        :rtype:     bool

        :raises RequestFailed:
        """
        if subject.lower()=='hostfinding':
                subject='hostFinding'
        if subject.lower()=='applicationfinding':
                subject='applicationFinding'

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+'/api/v1/client/{}/{}/download/acceptance/{}/{}'.format(str(client_id),subject,workflowcategory,fileuuid)
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
            with open(raw_response.headers['Content-Disposition'][22:-1],'wb') as f:
                f.write((raw_response.content))
            return raw_response
        except (RequestFailed,Exception) as e:
            print('Error in getting workflow details')
            print(e)
        

    def download_workflowbatch_attachments_severitychange(self, fileuuid:str, subject:str,workflowcategory:str='CLOSE_REQUEST', client_id:int=None):

        """
        Download attachments from an severity change workflow

        :param fileuuid:  File uuid
        :type  fileuuid:  str

        :param subject:     Subject whether hostFinding or applicationFinding
        :type  subject:      str

        :param workflowcategory:     Workflow category either CLOSE_REQUEST or CHANGE_REQUEST
        :type  workflowcategory:      str

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    Success
        :rtype:     bool

        :raises RequestFailed:
        """

        if subject.lower()=='hostfinding':
                subject='hostFinding'
        if subject.lower()=='applicationfinding':
                subject='applicationFinding'

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+'/api/v1/client/{}/{}/download/severityChange/{}/{}'.format(str(client_id),subject,workflowcategory,fileuuid)
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
            with open(raw_response.headers['Content-Disposition'][22:-1],'wb') as f:
                f.write((raw_response.content))
        except (RequestFailed,Exception) as e:
            print('Error in getting workflow details')
            print()
            print(e)
        success=True

        return success

    def download_workflowbatch_attachments_falsepositive(self, fileuuid:str, subject:str,workflowcategory:str='CLOSE_REQUEST', client_id:int=None):

        """
        Download attachments from an False positive workflow

        :param fileuuid:  File uuid
        :type  fileuuid:  str

        :param subject:     Subject whether hostFinding or applicationFinding
        :type  subject:      str

        :param workflowcategory:     Workflow category either CLOSE_REQUEST or CHANGE_REQUEST
        :type  workflowcategory:      str

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    Success
        :rtype:     bool

        :raises RequestFailed:
        """

        if subject.lower()=='hostfinding':
                subject='hostFinding'
        if subject.lower()=='applicationfinding':
                subject='applicationFinding'

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+'/api/v1/client/{}/{}/download/falsePositive/{}/{}'.format(str(client_id),subject,workflowcategory,fileuuid)
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
            with open(raw_response.headers['Content-Disposition'][22:-1],'wb') as f:
                f.write((raw_response.content))
        except (RequestFailed,Exception) as e:
            print('Error in getting workflow details')
            print()
            print(e)
        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def download_workflowbatch_attachments_remediation(self, fileuuid:str, subject:str,workflowcategory:str='CLOSE_REQUEST', client_id:int=None):

        """
        Download attachments from an remediation workflow

        :param fileuuid:  File uuid
        :type  fileuuid:  str

        :param subject:     Subject whether hostFinding or applicationFinding
        :type  subject:      str

        :param workflowcategory:     Workflow category either CLOSE_REQUEST or CHANGE_REQUEST
        :type  workflowcategory:      str

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    Success
        :rtype:     bool

        :raises RequestFailed:
        """

        if subject.lower()=='hostfinding':
                subject='hostFinding'
        if subject.lower()=='applicationfinding':
                subject='applicationFinding'

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+'/api/v1/client/{}/{}/download/remediation/{}/{}'.format(str(client_id),subject,workflowcategory,fileuuid)
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
            with open(raw_response.headers['Content-Disposition'][22:-1],'wb') as f:
                f.write((raw_response.content))
        except (RequestFailed,Exception) as e:
            print('Error in getting workflow details')
            print()
            print(e)

    def attach_files_acceptance(self,workflowbatchuuid:str,subject:str, file_name:str, path_to_file:str, client_id:int=None):

        """
        Attach an acceptance file to workflow

        :param workflowBatchUuid:      Workflow UUID
        :type  workflowBatchUuid:      str

        :param subject:            Finding type. Possible options : ("hostFinding" or "applicationFinding")
        :type  subject:            str

        :param file_name:   The name to be used for the uploaded file.
        :type  file_name:   str

        :param path_to_file:   Full path to the file to be uploaded.
        :type  path_to_file:   str

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    Success whether attachment is done
        :rtype:     bool

        :raises RequestFailed:
        :raises FileNotFoundError:
        """
        try:
            if subject.lower()=='hostfinding':
                subject='hostFinding'
            if subject.lower()=='applicationfinding':
                subject='applicationFinding'

            if client_id is None:
                client_id = self._use_default_client_id()[0]
            url = self.profile.platform_url + f"/api/v1/client/{client_id}/workflowBatch/acceptance/{workflowbatchuuid}/attach"
            multiform_data = {
                "subject": (None,subject),
                "files": (file_name,open(path_to_file, 'rb')),
                }
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, files=multiform_data)
            if raw_response.status_code==200:
                success=True
            return success
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()


    def attach_files_remediation(self,workflowbatchuuid:str,subject:str, file_name:str, path_to_file:str, client_id:int=None):

        """
        Attach an file to remediation workflow

        :param workflowBatchUuid:      Workflow UUID
        :type  workflowBatchUuid:      str

        :param subject:            Finding type. Possible options : ("hostFinding" or "applicationFinding")
        :type  subject:            str

        :param file_name:   The name to be used for the uploaded file.
        :type  file_name:   str

        :param path_to_file:   Full path to the file to be uploaded.
        :type  path_to_file:   str

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    Success whether attachment is done
        :rtype:     bool

        :raises RequestFailed:
        :raises FileNotFoundError:
        """

        if subject.lower()=='hostfinding':
            subject='hostFinding'
        if subject.lower()=='applicationfinding':
            subject='applicationFinding'

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        url = self.profile.platform_url + f"/api/v1/client/{client_id}/workflowBatch/remediation/{workflowbatchuuid}/attach"
        multiform_data = {
            "subject": (None,subject),
            "files": (file_name,open(path_to_file, 'rb')),
            }
        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, files=multiform_data)
            if raw_response.status_code==200:
                success=True
            return success
        except (RequestFailed,Exception,FileNotFoundError) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

    def attach_files_falsepositive(self,workflowbatchuuid:str,subject:str, file_name:str, path_to_file:str, client_id:int=None):

        """
        Attach a  file to false positive workflow

        :param workflowBatchUuid:      Workflow UUID
        :type  workflowBatchUuid:      str

        :param subject:            Finding type. Possible options : ("hostFinding" or "applicationFinding")
        :type  subject:            str

        :param file_name:   The name to be used for the uploaded file.
        :type  file_name:   str

        :param path_to_file:   Full path to the file to be uploaded.
        :type  path_to_file:   str

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    Success whether attachment is done
        :rtype:     bool

        :raises RequestFailed:
        :raises FileNotFoundError:
        """

        if subject.lower()=='hostfinding':
            subject='hostFinding'
        if subject.lower()=='applicationfinding':
            subject='applicationFinding'

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        url = self.profile.platform_url + f"/api/v1/client/{client_id}/workflowBatch/falsePositive/{workflowbatchuuid}/attach"
        multiform_data = {
            "subject": (None,subject),
            "files": (file_name,open(path_to_file, 'rb')),
            }
        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, files=multiform_data)
            if raw_response.status_code==200:
                success=True
            return success
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        except FileNotFoundError as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

    def attach_files_severitychange(self,workflowbatchuuid:str,subject:str, file_name:str, path_to_file:str, client_id:int=None):

        """
        Attach a file to severiy change workflow

        :param workflowBatchUuid:      Workflow UUID
        :type  workflowBatchUuid:      str

        :param subject:            Finding type. Possible options : ("hostFinding" or "applicationFinding")
        :type  subject:            str

        :param file_name:   The name to be used for the uploaded file.
        :type  file_name:   str

        :param path_to_file:   Full path to the file to be uploaded.
        :type  path_to_file:   str

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    Success whether attachment is done
        :rtype:     bool

        :raises RequestFailed:
        :raises FileNotFoundError:
        """

        if subject.lower()=='hostfinding':
            subject='hostFinding'
        if subject.lower()=='applicationfinding':
            subject='applicationFinding'

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        url = self.profile.platform_url + f"/api/v1/client/{client_id}/workflowBatch/severityChange/{workflowbatchuuid}/attach"
        multiform_data = {
            "subject": (None,subject),
            "files": (file_name,open(path_to_file, 'rb')),
            }
        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, files=multiform_data)
            if raw_response.status_code==200:
                success=True
            return success
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        except FileNotFoundError as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()


    def detach_files_acceptance(self,workflowbatchuuid:str,attachmentuuids:list,subject:str, client_id=None):

        """
        Detach a file from acceptance workflow

        :param workflowBatchUuid:      Workflow UUID
        :type  workflowBatchUuid:      str

        :param subject:            Finding type. Possible options : ("hostFinding" or "applicationFinding")
        :type  subject:            str

        :param attachmentuuids:      Attchment UUID
        :type  attachmentuuids:      list

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    Success whether detachment is done
        :rtype:     bool

        :raises RequestFailed:
        :raises FileNotFoundError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        
        if subject.lower()=='hostfinding':
            subject='hostFinding'
        if subject.lower()=='applicationfinding':
            subject='applicationFinding'
        
        url = self.profile.platform_url + f"/api/v1/client/{client_id}/workflowBatch/acceptance/{workflowbatchuuid}/detach"
        body={
                "attachmentUuid": attachmentuuids,
                "subject": subject
                }
        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.DELETE, url, body=body)
            if raw_response.status_code==200:
                success=True
            return success
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        except FileNotFoundError as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

    def detach_files_falsepositive(self,workflowbatchuuid:str,attachmentuuids:list,subject:str, client_id:int=None):

        """
        Detach a file from false positive workflow

        :param workflowBatchUuid:      Workflow UUID
        :type  workflowBatchUuid:      str

        :param subject:            Finding type. Possible options : ("hostFinding" or "applicationFinding")
        :type  subject:            str

        :param attachmentuuids:      Attchment UUID
        :type  attachmentuuids:      list

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    Success whether detachment is done
        :rtype:     bool

        :raises RequestFailed:
        :raises FileNotFoundError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        
        if subject.lower()=='hostfinding':
            subject='hostFinding'
        if subject.lower()=='applicationfinding':
            subject='applicationFinding'
        
        url = self.profile.platform_url + f"/api/v1/client/{client_id}/workflowBatch/falsePositive/{workflowbatchuuid}/detach"
        body={
                "attachmentUuid": attachmentuuids,
                "subject": subject
                }
        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.DELETE, url, body=body)
            if raw_response.status_code==200:
                success=True
            return success
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        except FileNotFoundError as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

    def detach_files_remediation(self,workflowbatchuuid:str,attachmentuuids:list,subject:str, client_id:int=None):

        """
        Detach a file from remediation workflow

        :param workflowBatchUuid:      Workflow UUID
        :type  workflowBatchUuid:      str

        :param subject:            Finding type. Possible options : ("hostFinding" or "applicationFinding")
        :type  subject:            str

        :param attachmentuuids:      Attchment UUID
        :type  attachmentuuids:      list

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    Success whether detachment is done
        :rtype:     bool

        :raises RequestFailed:
        :raises FileNotFoundError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        
        if subject.lower()=='hostfinding':
            subject='hostFinding'
        if subject.lower()=='applicationfinding':
            subject='applicationFinding'
        
        url = self.profile.platform_url + f"/api/v1/client/{client_id}/workflowBatch/remediation/{workflowbatchuuid}/detach"
        
        body={
                "attachmentUuid": attachmentuuids,
                "subject": subject
                }
        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.DELETE, url, body=body)
            if raw_response.status_code==200:
                success=True
            return success
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        except FileNotFoundError as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

    def detach_files_severitychange(self,workflowbatchuuid:str,attachmentuuids:list,subject:str, client_id:int=None):

        """
        Detach a file from severity change workflow

        :param workflowBatchUuid:      Workflow UUID
        :type  workflowBatchUuid:      str

        :param subject:            Finding type. Possible options : ("hostFinding" or "applicationFinding")
        :type  subject:            str

        :param attachmentuuids:      Attchment UUID
        :type  attachmentuuids:      list

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    Success whether detachment is done
        :rtype:     bool

        :raises RequestFailed:
        :raises FileNotFoundError:
        """
        

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        
        if subject.lower()=='hostfinding':
            subject='hostFinding'
        if subject.lower()=='applicationfinding':
            subject='applicationFinding'
        
        url = self.profile.platform_url + f"/api/v1/client/{client_id}/workflowBatch/severityChange/{workflowbatchuuid}/detach"
        
        body={
                "attachmentUuid": attachmentuuids,
                "subject": subject
                }
        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.DELETE, url, body=body)
            if raw_response.status_code==200:
                success=True
            return success
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        except FileNotFoundError as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()


        return raw_response.text



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