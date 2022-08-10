"""
Users
"""
""" *******************************************************************************************************************
|
|  Name        :  __users.py
|  Module      :  risksense_api
|  Description :  A class to be used for getting information about RiskSense platform users.
|  Copyright   :  (c) RiskSense, Inc.
|  License     :  Apache-2.0 (http://www.apache.org/licenses/LICENSE-2.0)
|
******************************************************************************************************************* """

import json
from multiprocessing import Value
import uuid
from ..__exports import ExportFileType
from ..__exports import ExportRowNumbers
from ...__subject import Subject
from ..._params import *
from ..._api_request_handler import *
from ..__exports import Exports
import sys
import zipfile
import csv


class Users(Subject):

    """ Users Class """

    def __init__(self, profile):

        """
        Initialization of Users object.

        :param profile:     Profile Object
        :type  profile:     _profile

        """

        self.subject_name = "user"
        Subject.__init__(self, profile, self.subject_name)
        self.api_base_url = self.profile.platform_url + "/api/v1/"
    def downloadfilterinexport(self,filename,filters,client_id=None):
        if client_id is None:
            client_id= self._use_default_client_id()[0]
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
        except(RequestFailed,MaxRetryError,StatusCodeError, ValueError):
                    print(ex)
                    print()
                    print("Unable to retrieve file. Exiting.")
                    sys.exit(1)
  

    def remove_users(self,useruuid,client_id=None):

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url + "/client/{}/user/{}".format(str(client_id),useruuid)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.DELETE, url)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)
        user_profile = jsonified_response

        return user_profile
   
    def get_user_iaminfo(self,useruuid,client_id=None):

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url + "/client/{}/user/{}/iam".format(str(client_id),useruuid)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)
        iam = jsonified_response

        return iam


    def get_filter(self,client_id=None):

        if client_id is None:
            client_id = self._use_default_client_id()[1]

        url = self.api_base_url + "/client/{}/user/filter".format(str(client_id))

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)
        iam = jsonified_response

        return iam
    
    def assign_group(self,filter,targetgroupids,client_id=None):

        if client_id is None:
            client_id = self._use_default_client_id()[1]

        url = self.api_base_url + "/client/{}/user/assign-group".format(str(client_id))

        body= {
                "filterRequest": filter,
                "targetGroupIds": targetgroupids
                }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def unassign_group(self,filter,targetgroupids,client_id=None):

        if client_id is None:
            client_id = self._use_default_client_id()[1]

        url = self.api_base_url + "/client/{}/user/unassign-group".format(str(client_id))

        body= {
                "filterRequest": filter,
                "targetGroupIds": targetgroupids
                }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def get_my_profile(self,csvdump=False):

        """
        Get the profile for the user that owns the API key being used.

        :return:    A dictionary containing the user's profile.
        :rtype:     dict

        :raises RequestFailed:
        """

        url = self.api_base_url + "user/profile"

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)
        user_profile = jsonified_response
        if csvdump==True:
            field_names = []
            for item in user_profile.keys():
                field_names.append(item)
            try:
                with open('user_profile.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    writer.writerow(user_profile)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)
        return user_profile

    def disallow_tokens(self, user_id):

        """
        Disallow use of tokens for a user.

        :param user_id:     The ID of the user to be disallowed from token use.
        :type  user_id:     int

        :return:    True/False indicating success or failure of submission of the operation.
        :rtype:     bool

        :raises RequestFailed:
        """

        url = self.api_base_url + "/clients/user/" + str(user_id) + "/tokenAllowed"

        body = {
            "allowed": False
        }

        try:
            self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
            success = True
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        return success

    def allow_tokens(self, user_id):

        """
        Allow use of tokens for a user.

        :param user_id:     The ID of the user to be allowed token use.
        :type  user_id:     int

        :return:    True/False indicating success or failure of submission of the operation.
        :rtype:     bool

        :raises RequestFailed:
        """

        url = self.api_base_url + "/clients/user/" + str(user_id) + "/tokenAllowed"

        body = {
            "allowed": True
        }

        try:
            self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
            success = True
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        return success

    def getexporttemplate(self,client_id=None):
        
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

        url = self.api_base_url+"client/{}/user/export/template".format(str(client_id))
        print(url)
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
        :param file_type:       File type to export.  ExportFileType.CSV, ExportFileType.XML, or ExportFileType.XLSX
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
        print(func_args)
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

    def get_single_search_page(self, search_filters, page_num=0, page_size=150,
                               sort_field=SortField.ID, sort_dir=SortDirection.ASC, client_id=None):

        """
        Searches for and returns users based on the provided filter(s) and other parameters.

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

        :return:    Paginated JSON response from the platform.

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url + "client/{}/user/search".format(str(client_id))

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

    def systemuser_get_single_search_page(self, search_filters, page_num=0, page_size=150,
                               sort_field="username", sort_dir=SortDirection.DESC, client_id=None):

        """
        Searches for and returns users based on the provided filter(s) and other parameters.

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

        :return:    Paginated JSON response from the platform.

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[1]
        url = self.api_base_url + "clients/systemUser/search?client_ids={}".format(str(client_id))
        print(url)
        body = {
            "filters": search_filters,
            "projection": "internal",
            "sort": [
                {
                    "field": sort_field,
                    "direction": sort_dir
                }
            ],
            "page": page_num,
            "size": page_size
        }
        
        jsonified_response = json.loads(raw_response.text)
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        return jsonified_response

    def search(self, search_filters, page_size=150, sort_field=SortField.ID, sort_dir=SortDirection.ASC,csvdump=False, client_id=None):

        """
        Searches for and returns users based on the provided filter(s) and other parameters.  Rather
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
        func_args.pop('csvdump')

        if client_id is None:
            client_id = self._use_default_client_id()[0]
            func_args['client_id']=self._use_default_client_id()[0]
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
            self.downloadfilterinexport('userexport',search_filters)
        return all_results
    
    def list_user_filter_fields(self,client_id=None):

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



    def get_user_info(self, user_id=None, client_id=None):

        """
        Get info for a specific user.  If user_id is not specified, the info for the requesting user is returned.

        :param user_id:     User ID
        :type  user_id:     int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    User information.
        :rtype:     dict

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        params = {}

        url = self.api_base_url + "/user"

        if user_id is not None:
            params.update({"userId": user_id})

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url, params=params)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)
        for keys,value in jsonified_response.items():
            print(keys,':',value)
        return jsonified_response

    def create(self, username, first_name, last_name, email_address,
                group_ids, client_id=None, **kwargs):

        """
        Create a new user.

        :param username:        Username
        :type  username:        str

        :param first_name:      First Name
        :type  first_name:      str

        :param last_name:       Last Name
        :type  last_name:       str

        :param email_address:   E-mail address
        :type  email_address:   str

        :param phone_num:       Phone Number
        :type  phone_num:       str

        :param read_only:       Read Only
        :type  read_only:       bool

        :param group_ids:       Group IDs to assign user to
        :type  group_ids:       list

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword use_saml:      Is a SAML user?             (bool)
        :keyword saml_attr_1:   SAML Attribute 1            (str)
        :keyword saml_attr_2:   SAML Attribute 2            (str)
        :keyword exp_date:      Expiration Date YYYY-MM-DD  (str)

        :return:    job ID
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url + "client/{}/user".format(str(client_id))

        use_saml = kwargs.get("use_saml", None)
        saml_attr_1 = kwargs.get("saml_attr_l", None)
        saml_attr_2 = kwargs.get("saml_attr_2", None)
        exp_date = kwargs.get("exp_date", None)

        body = {
            "username": username,
            "firstName": first_name,
            "lastName": last_name,
            "email": email_address,
            "groupIds": group_ids,
            "useSamlAuthentication": use_saml,
            "samlAttribute1": saml_attr_1,
            "samlAttribute2": saml_attr_2,
            "expirationDate": exp_date
        }

        body = self._strip_nones_from_dict(body)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        if raw_response.status_code==201:
            jsonified_response = json.loads(raw_response.text)
            user_id = jsonified_response['id']

            return user_id

    def update_user_role(self, currentrole,currentexpiration,newrole,newexpiration,user_uuid=None, client_id=None,):

        """
        Update user role.

        :param search_filter:   Filter to identify users to be updated
        :type  search_filter:   list

        :param role:            User role
        :type  role:            str

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    Job ID
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url + "client/{}/user/{}/role".format(str(client_id),user_uuid)

        body = {
                "roles": [
                    {
                    "role": currentrole,
                    "expirationDate": currentexpiration
                    },
                    {
                    "role": newrole,
                    "expirationDate": newexpiration
                    }
                ]
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

    def update_user(self, user_uuid, client_id=None, **kwargs):

        """
        Update a user.

        :param user_uuid:   User UUID
        :type  user_uuid:   str

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :keyword username:      Username                    (str)
        :keyword first_name:    First Name                  (str)
        :keyword last_name:     Last Name                   (str)
        :keyword email:         Email                       (str)
        :keyword phone:         Phone Num.                  (str)
        :keyword group_ids:     Group IDs                   (list)
        :keyword read_only:     Read-Only                   (bool)
        :keyword use_saml:      Use SAML?                   (bool)
        :keyword saml_attr_1:   SAML Attribute 1            (str)
        :keyword saml_attr_2:   SAML Attribute 2            (str)
        :keyword exp_date:      Expiration Date YYYY-MM-DD  (str)

        :return:    Job ID
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url + "client/{}/user/{}".format(str(client_id), user_uuid)

        username = kwargs.get("username", None)
        first_name = kwargs.get("firstName", None)
        last_name = kwargs.get("lastName", None)
        email_address = kwargs.get("email", None)
        phone_num = kwargs.get("phone", None)
        group_ids = kwargs.get("group_ids", None)
        read_only = kwargs.get("read_only", None)
        use_saml = kwargs.get("use_saml", None)
        saml_attr_1 = kwargs.get("saml_attr_l", None)
        saml_attr_2 = kwargs.get("saml_attr_2", None)
        exp_date = kwargs.get("exp_date", None)

        body = {
            "username": username,
            "firstName": first_name,
            "lastName": last_name,
            "email": email_address,
            "phone": phone_num,
            "groupIds": group_ids,
            "readOnly": read_only,
            "useSamlAuthentication": use_saml,
            "samlAttribute1": saml_attr_1,
            "samlAttribute2": saml_attr_2,
            "expirationDate": exp_date
        }

        body = self._strip_nones_from_dict(body)

        if body == {}:
            raise ValueError("No new valid user properties provided.")

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

    def send_welcome_email(self, search_filter, client_id=None):

        """
        Send welcome e-mail to users identified by the search filter(s) provided.

        :param search_filter:   Search filter(s)
        :type  search_filter:   list

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    Job ID
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url + "client/{}/user/sendWelcomeEmail".format(str(client_id))

        body = {
            "filterRequest": {
                "filters": search_filter
            }
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

    def get_roles(self, client_id=None):

        """
        Send welcome e-mail to users identified by the search filter(s) provided.

        :param search_filter:   Search filter(s)
        :type  search_filter:   list

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    Job ID
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        
        roleurl=self.api_base_url + "client/{}/role?page=0&size=500".format(str(client_id))
        try:
            roles = self.request_handler.make_request(ApiRequestHandler.GET, roleurl)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        jsonified_response = json.loads(roles.text)
        
        return jsonified_response

    def assign_clients(self,searchfilter,expirationdate,replacexistingroles=False,assignallgroups=False, client_id=None,client_idtouse=None):

        """
        Send welcome e-mail to users identified by the search filter(s) provided.

        :param search_filter:   Search filter(s)
        :type  search_filter:   list

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    Job ID
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        
        roleurl=self.api_base_url + "client/{}/role?page=0&size=500".format(str(client_id))
        try:
            roles = self.request_handler.make_request(ApiRequestHandler.GET, roleurl)
            roles=json.loads(roles.text)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        for i in range(len(roles['_embedded']['roles'])):
            print(f'Index No:{i},Name:{roles["_embedded"]["roles"][i]["name"]}')
        inputsofroles=[roles["_embedded"]["roles"][int(i)]["id"] for i in input('Please enter the indexes of the roles that you want you want the user to have:').split(',')]  

        body = {"filterRequest":{"filters":searchfilter},"roles":inputsofroles,"replaceExistingRoles":replacexistingroles,"expirationDate":f"{expirationdate}T00:00:00.000Z","assignAllGroups":assignallgroups}

        url = self.api_base_url + "client/{}/assignUsers".format(str(client_idtouse))


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

    def assign_roles(self,userid,expirationdate=None,replacexistingroles=False,assignallgroups=False, client_id=None,client_idtouse=None):

        """
        Send welcome e-mail to users identified by the search filter(s) provided.

        :param search_filter:   Search filter(s)
        :type  search_filter:   list

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    Job ID
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        if client_idtouse is None:
            client_idtouse=client_id
        
        uuid=self.get_user_info(user_id=userid)['uuid']

        getroles=self.get_user_iaminfo(client_id=client_idtouse,useruuid=uuid)
 
        existingrole=getroles['roles']
        newroleaddition=[]


        roles=self.get_roles(client_id=client_idtouse)

        for i in range(len(roles['_embedded']['roles'])):
            print(f'Index No:{i},Name:{roles["_embedded"]["roles"][i]["name"]}')
        inputsofroles=roles["_embedded"]["roles"][int(input('Please enter the index of the roles that you want you want the user to have:'))]["id"]

        for i in range(len(existingrole)): 
            temp={}
            temp['client_id']=client_idtouse
            temp['role']=existingrole[i]['id']
            temp['expirationDate']=existingrole[i]['expirationDate']
            newroleaddition.append(temp)
    
        newroleaddition.append({"client_id":client_idtouse,"role":inputsofroles,"expirationDate":expirationdate})

        body={"roles":newroleaddition}



        url = self.api_base_url + "client/{}/user/{}/role".format(str(client_idtouse),uuid)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def remove_roles(self,userid,client_idtouse=None, client_id=None,):

        """
        Send welcome e-mail to users identified by the search filter(s) provided.

        :param search_filter:   Search filter(s)
        :type  search_filter:   list

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    Job ID
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        
        uuid=self.get_user_info(user_id=userid)['uuid']

        getroles=self.get_user_iaminfo(client_id=client_idtouse,useruuid=uuid)
 
        existingrole=getroles['roles']
        newroleadditon=[]
        for i in range(len(existingrole)):
            print(f'Index No:{i},Name:{existingrole[i]["name"]}')
        
        existingrole.remove(existingrole[int(input('Which role would you like to delete, please enter the index number'))])
    
        print(existingrole)

        for i in range(len(existingrole)): 
            temp={}
            temp['role']=existingrole[i]['id']
            temp['expirationDate']=existingrole[i]['expirationDate']
            newroleadditon.append(temp)
        print(newroleadditon)
        body={"roles":newroleadditon}

        url = self.api_base_url + "client/{}/user/{}/role".format(str(client_idtouse),uuid)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def clientrolefiltering(self,client_ids=None,rolelabels=None,client_id=None):

        """
        Send welcome e-mail to users identified by the search filter(s) provided.

        :param search_filter:   Search filter(s)
        :type  search_filter:   list

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    Job ID
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        

        body={"client_ids":client_ids,"clientNames":[],"roleLabels":rolelabels}

        url = self.api_base_url + f"clients/usersByRole/search?client_ids={','.join([str(i) for i in client_ids ])}"
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response


    def get_model(self, client_id=None):

        """
        Get available projections and models for Users.

        :param client_id:   Client ID
        :type  client_id:   int

        :return:    Users projections and models are returned.
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

    def import_users_csv(self, file_name, path_to_file, client_id=None):

        """
        Add a file to an upload.

        :param upload_id:   Upload ID
        :type  upload_id:   int

        :param file_name:   The name to be used for the uploaded file.
        :type  file_name:   str

        :param path_to_file:   Full path to the file to be uploaded.
        :type  path_to_file:   str

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The file ID is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises FileNotFoundError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url + "client/{}/user/importUsersCsv".format(str(client_id))
        upload_file = {'csvdata': (file_name, open(path_to_file, 'rb'))}

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, files=upload_file)
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

        jsonified_response = json.loads(raw_response.text)
        file_id = jsonified_response[0]['id']

        return file_id


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
