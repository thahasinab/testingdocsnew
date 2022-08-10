""" *******************************************************************************************************************
|
|  Name        :  __tags.py
|  Module      :  risksense_api
|  Description :  A class to be used for searching for and updating tags on the RiskSense Platform.
|  Copyright   :  (c) RiskSense, Inc.
|  License     :  Apache-2.0 (http://www.apache.org/licenses/LICENSE-2.0)
|
******************************************************************************************************************* """

import json
from tokenize import Triple
from ..__exports import ExportFileType
from ..__exports import ExportRowNumbers
from ...__subject import Subject
from ..._params import *
from ..._api_request_handler import *
from ..__exports import Exports
import sys
import zipfile
import csv
import pandas as pd


class TagType:
    """ TagType class and attributes"""

    COMPLIANCE = 'COMPLIANCE'
    LOCATION = 'LOCATION'
    CUSTOM = 'CUSTOM'
    REMEDIATION = 'REMEDIATION'
    PEOPLE = 'PEOPLE'
    PROJECT = 'PROJECT'
    SCANNER = 'SCANNER'
    CMDB = 'CMDB'


class Tags(Subject):

    """ Tags class """

    def __init__(self, profile):

        """
        Initialization of Tags object.

        :param profile:     Profile Object
        :type  profile:     _profile
        """

        self.subject_name = "tag"
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
        except(RequestFailed,MaxRetryError,StatusCodeError, ValueError):
                    print(ex)
                    print()
                    print("Unable to retrieve file. Exiting.")
                    sys.exit(1)
  
    
    def create(self, tag_type:str, name:str, desc:str, owner:int, color:str="#648d9f", locked:bool=False, propagate:bool=True,csvdump:bool=False, client_id=None):

        """
        Create a new tag for the client.

        :param tag_type:    Type of tag to be created. (TagType.COMPLIANCE,
                                                                TagType.LOCATION,
                                                                TagType.CUSTOM,
                                                                TagType.REMEDIATION,
                                                                TagType.PEOPLE,
                                                                TagType.PROJECT,
                                                                TagType.SCANNER,
                                                                TagType.CMDB)
        :type  tag_type:    TagType attribute

        :param name:        Name of tag
        :type  name:        str

        :param desc:        Description of tag
        :type  desc:        str

        :param owner:       User ID of tag owner
        :type  owner:       int

        :param color:       Hex value of the color to be used for this tag.
        :type  color:       str

        :param locked:      Reflects whether or not the tag should be locked.
        :type  locked:      bool

        :param propagate    Propagate tag to all findings?
        :type  propagate:   bool

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The new tag ID will be returned.
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        list_of_tag_types = [
            TagType.COMPLIANCE,
            TagType.LOCATION,
            TagType.CUSTOM,
            TagType.REMEDIATION,
            TagType.PEOPLE,
            TagType.PROJECT,
            TagType.SCANNER,
            TagType.CMDB
        ]

        tag_type = tag_type.upper()
        if tag_type not in list_of_tag_types:
            raise ValueError(f"Tag Type provided ({tag_type}) is not supported.")

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
        
        url = self.api_base_url.format(str(client_id))

        body = {
            "fields": [
                {
                    "uid": "TAG_TYPE",
                    "value": tag_type
                },
                {
                    "uid": "NAME",
                    "value": name
                },
                {
                    "uid": "DESCRIPTION",
                    "value": desc
                },
                {
                    "uid": "OWNER",
                    "value": owner
                },
                {
                    "uid": "COLOR",
                    "value": color
                },
                {
                    "uid": "LOCKED",
                    "value": locked
                },
                {
                    "uid": "PROPAGATE_TO_ALL_FINDINGS",
                    "value": propagate
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
        new_tag_id = jsonified_response['id']

        if csvdump==True:
            tagid={'jobid':[jsonified_response['id']]}
            df = pd.DataFrame(tagid)
            df.to_csv('tagidcreated.csv',index=False)

        return new_tag_id

    def getexporttemplate(self,client_id:int=None):
        
        """
        Gets configurable export template for Tags.

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
        except RequestFailed as e:
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

    def export(self, search_filters:list, file_name:str, row_count=ExportRowNumbers.ROW_ALL,file_type=ExportFileType.CSV, client_id:int=None):

        """
        Initiates an export job on the platform for Tag(s) based on the
        provided filter(s).

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param file_name:       The name to be used for the exported file.
        :type  file_name:       str

        :param row_count:       No of rows to be exported. Possible options : (ExportRowNumbers.ROW_5000,ExportRowNumbers.ROW_10000,ExportRowNumbers.ROW_25000,ExportRowNumbers.ROW_50000",ExportRowNumbers.ROW_100000",ExportRowNumbers.ROW_ALL)
        :type  row_count:       str

        :param exportable_filter:       Exportable filter
        :type  exportable_filter:       list
        :param file_type:       File type to export.  ExportFileType.CSV, ExportFileType.JSON, or ExportFileType.XLSX
        :type  file_type:       str

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The job ID in the platform from is returned.
        :rtype:     int

        :raises RequestFailed:
        """
        func_args = locals()
        exportablefilter=self.getexporttemplate()
        func_args['exportable_filter']=exportablefilter
        func_args.pop('self')
        if client_id is None:
            func_args['client_id'] = self._use_default_client_id()[1]
        try:
            export_id = self._export(self.subject_name, **func_args)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        return export_id


    def create_compliance_tag(self, name:str, desc:str, owner:int, color:str="#648d9f", locked:bool=False,csvdump:bool=False, client_id:int=None):

        """
        Create a new COMPLIANCE tag.

        :param name:        Name of tag
        :type  name:        str

        :param desc:        Description of tag
        :type  desc:        str

        :param owner:       User ID of tag owner
        :type  owner:       int

        :param color:       Hex value of the color to be used for this tag.
        :type  color:       str

        :param locked:      Reflects whether or not the tag should be locked.
        :type  locked:      bool

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The new tag ID will be returned.
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            tag_id = self.create(TagType.COMPLIANCE, name, desc, owner, color, locked, client_id)
        except (RequestFailed, ValueError) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        if csvdump==True:
            tagid={'tagid':[tag_id]}
            df = pd.DataFrame(tagid)
            df.to_csv('tagcreated.csv',index=False)
        
        return tag_id

    def create_location_tag(self, name:str, desc:str, owner:int, color:str="#648d9f", locked:bool=False,csvdump:bool=False, client_id:int=None):

        """
        Create a new LOCATION tag.

        :param name:        Name of tag
        :type  name:        str

        :param desc:        Description of tag
        :type  desc:        str

        :param owner:       User ID of tag owner
        :type  owner:       int

        :param color:       Hex value of the color to be used for this tag.
        :type  color:       str

        :param locked:      Reflects whether or not the tag should be locked.
        :type  locked:      bool

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The new tag ID will be returned.
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        
        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            tag_id = self.create(TagType.LOCATION, name, desc, owner, color, locked, client_id)
        except (RequestFailed, ValueError) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        
        if csvdump==True:
            tagid={'tagid':[tag_id]}
            df = pd.DataFrame(tagid)
            df.to_csv('tagcreated.csv',index=False)
        return tag_id

    def create_custom_tag(self, name:str, desc:str, owner:int, color:str="#648d9f", locked:bool=False,csvdump:bool=False, client_id:int=None):

        """
        Create a new CUSTOM tag.

        :param name:        Name of tag
        :type  name:        str

        :param desc:        Description of tag
        :type  desc:        str

        :param owner:       User ID of tag owner
        :type  owner:       int

        :param color:       Hex value of the color to be used for this tag.
        :type  color:       str

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param locked:      Reflects whether or not the tag should be locked.
        :type  locked:      bool

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    Tag ID
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')        

        try:
            tag_id = self.create(TagType.CUSTOM, name, desc, owner, color, locked, client_id)
        except (RequestFailed, ValueError) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        
        if csvdump==True:
            tagid={'tagid':[tag_id]}
            df = pd.DataFrame(tagid)
            df.to_csv('tagcreated.csv',index=False)
    
        return tag_id

    def create_remediation_tag(self, name:str, desc:str, owner:int, color:str="#648d9f", locked:bool=False,csvdump:bool=False, client_id:int=None):

        """
        Create a new REMEDIATION tag.

        :param name:        Name of tag
        :type  name:        str

        :param desc:        Description of tag
        :type  desc:        str

        :param owner:       User ID of tag owner
        :type  owner:       int

        :param color:       Hex value of the color to be used for this tag.
        :type  color:       str

        :param locked:      Reflects whether or not the tag should be locked.
        :type  locked:      bool

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :return:    The new tag ID will be returned.
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')    

        try:
            tag_id = self.create(TagType.REMEDIATION, name, desc, owner, color, locked, client_id)
        except (RequestFailed, ValueError) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        
        if csvdump==True:
            tagid={'tagid':[tag_id]}
            df = pd.DataFrame(tagid)
            df.to_csv('tagcreated.csv',index=False)

        return tag_id

    def create_people_tag(self, name:str, desc:str, owner:int, color:str="#648d9f", locked:bool=False,csvdump:bool=False, client_id:int=None):

        """
        Create a new PEOPLE tag.

        :param name:        Name of tag
        :type  name:        str

        :param desc:        Description of tag
        :type  desc:        str

        :param owner:       User ID of tag owner
        :type  owner:       int

        :param color:       Hex value of the color to be used for this tag.
        :type  color:       str

        :param locked:      Reflects whether or not the tag should be locked.
        :type  locked:      bool

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The new tag ID will be returned.
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            tag_id = self.create(TagType.PEOPLE, name, desc, owner, color, locked, client_id)
        except (RequestFailed, ValueError) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        
        if csvdump==True:
            tagid={'tagid':[tag_id]}
            df = pd.DataFrame(tagid)
            df.to_csv('tagcreated.csv',index=False)

        return tag_id

    def create_project_tag(self, name:str, desc:str, owner:int, color:str="#648d9f", locked:bool=False,csvdump:bool=False, client_id:int=None):

        """
        Create a new PROJECT tag.

        :param name:        Name of tag
        :type  name:        str

        :param desc:        Description of tag
        :type  desc:        str

        :param owner:       User ID of tag owner
        :type  owner:       int

        :param color:       Hex value of the color to be used for this tag.
        :type  color:       str

        :param locked:      Reflects whether or not the tag should be locked.
        :type  locked:      bool

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :return:    The new tag ID will be returned.
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            tag_id = self.create(TagType.PROJECT, name, desc, owner, color, locked, client_id)
        except (RequestFailed, ValueError) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        if csvdump==True:
            tagid={'tagid':[tag_id]}
            df = pd.DataFrame(tagid)
            df.to_csv('tagcreated.csv',index=False)

        return tag_id

    def create_scanner_tag(self, name:str, desc:str, owner:int, color:str="#648d9f", locked:bool=False,csvdump:bool=False, client_id:int=None):

        """
        Create a new SCANNER tag.

        :param name:        Name of tag
        :type  name:        str

        :param desc:        Description of tag
        :type  desc:        str

        :param owner:       User ID of tag owner
        :type  owner:       int

        :param color:       Hex value of the color to be used for this tag.
        :type  color:       str

        :param locked:      Reflects whether or not the tag should be locked.
        :type  locked:      bool

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The new tag ID will be returned.
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            tag_id = self.create(TagType.SCANNER, name, desc, owner, color, locked, client_id)
        except (RequestFailed, ValueError) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        if csvdump==True:
            tagid={'tagid':[tag_id]}
            df = pd.DataFrame(tagid)
            df.to_csv('tagcreated.csv',index=False)

        return tag_id

    def create_cmdb_tag(self, name:str, desc:str, owner:int,csvdump:bool=False, color:str="#648d9f", locked:bool=False, client_id:int=None):

        """
        Create a new CMDB tag.

        :param name:        Name of tag
        :type  name:        str

        :param desc:        Description of tag
        :type  desc:        str

        :param owner:       User ID of tag owner
        :type  owner:       int

        :param color:       Hex value of the color to be used for this tag.
        :type  color:       str

        :param locked:      Reflects whether or not the tag should be locked.
        :type  locked:      bool

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The new tag ID will be returned.
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            tag_id = self.create(TagType.CMDB, name, desc, owner, color, locked, client_id)
        except (RequestFailed, ValueError) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        if csvdump==True:
            tagid={'tagid':[tag_id]}
            df = pd.DataFrame(tagid)
            df.to_csv('tagcreated.csv',index=False)
        return tag_id

    def list_tag_filter_fields(self,client_id:int=None):

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

    def export(self, search_filters:list, file_name:str, row_count=ExportRowNumbers.ROW_ALL,file_type=ExportFileType.CSV, client_id=None):

        """
        Initiates an export job on the platform for Tag(s) based on the
        provided filter(s).

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param file_name:       The name to be used for the exported file.
        :type  file_name:       str

        :param row_count:       No of rows to be exported. Possible options : (ExportRowNumbers.ROW_5000,ExportRowNumbers.ROW_10000,ExportRowNumbers.ROW_25000,ExportRowNumbers.ROW_50000",ExportRowNumbers.ROW_100000",ExportRowNumbers.ROW_ALL)
        :type  row_count:       str

        :param exportable_filter:       Exportable filter
        :type  exportable_filter:       list
        :param file_type:       File type to export.  ExportFileType.CSV, ExportFileType.JSON, or ExportFileType.XLSX
        :type  file_type:       str

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The job ID in the platform from is returned.
        :rtype:     int

        :raises RequestFailed:
        """
        func_args = locals()
        exportablefilter=self.getexporttemplate()
        func_args['exportable_filter']=exportablefilter
        func_args.pop('self')
        if client_id is None:
            func_args['client_id'] = self._use_default_client_id()[1]
        try:
            export_id = self._export(self.subject_name, **func_args)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        return export_id



    def update(self, tag_id:int, tag_type:str, name:str, desc:str, owner:int, color:str, locked:bool, propagate:bool=True,csvdump:bool=False, client_id:int=None):

        """
        Update an existing tag.

        :param tag_id:      The tag ID to be updated.
        :type  tag_id:      int

        :param tag_type:    The type of tag.
        :type  tag_type:    str

        :param name:        The name of the tag.
        :type  name:        str

        :param desc:        A description for the tag.
        :type  desc:        str

        :param owner:       The owner(s) of the tag, represented by user IDs, delimited by commas.  Ex: "1234,567,890"
        :type  owner:       str

        :param color:       The color for the tag.  A hex value.
        :type  color:       str

        :param locked:      Whether or not the tag should be locked.
        :type  locked       bool

        :param propagate    Propagate tag to all findings?
        :type propagate:    bool

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool


        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The job ID will be returned.
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        list_of_tag_types = [
            TagType.COMPLIANCE,
            TagType.LOCATION,
            TagType.CUSTOM,
            TagType.REMEDIATION,
            TagType.PEOPLE,
            TagType.PROJECT,
            TagType.SCANNER,
            TagType.CMDB
        ]

        if tag_type not in list_of_tag_types:
            raise ValueError("Invalid tag type")

        body = {
            "fields": [
                {
                    "uid": "TAG_TYPE",
                    "value": tag_type
                },
                {
                    "uid": "NAME",
                    "value": name
                },
                {
                    "uid": "DESCRIPTION",
                    "value": desc
                },
                {
                    "uid": "OWNER",
                    "value": owner
                },
                {
                    "uid": "COLOR",
                    "value": color
                },
                {
                    "uid": "LOCKED",
                    "value": locked
                },
                {
                    "uid": "PROPAGATE_TO_ALL_FINDINGS",
                    "value": propagate
                }
            ]
        }

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        url = self.api_base_url.format(str(client_id)) + "/{}".format(str(tag_id))

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)
        response_id = jsonified_response['id']

        if csvdump==True:
            self.downloadfilterinexport('tagupdated',[{"field":"id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":f"{tag_id}"}])

        return response_id

    def delete(self, tag_id:int, force_delete:bool=True,csvdump:bool=False, client_id:int=None,):

        """
        Delete a tag.

        :param tag_id:          Tag ID to delete.
        :type  tag_id:          int

        :param force_delete:    Indicates whether or not deletion should be forced.
        :type  force_delete:    bool

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:  Boolean reflecting the indication from the platform as to whether or not the deletion was successful.

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        body = {
            "forceDeleteTicket": force_delete
        }

        url = self.api_base_url.format(str(client_id)) + "/{}".format(str(tag_id))

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
        
        if csvdump==True:
            self.downloadfilterinexport('tagtobedeleted',[{"field":"id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":f"{tag_id}"}])
        try:
            self.request_handler.make_request(ApiRequestHandler.DELETE, url, body=body)
        except (RequestFailed,Exception) as e:
            print('Error in deleting the tag')
            print()
            print(e)
            exit()

        success = True

        return success

    def bulk_tag_delete(self, search_filters:list, force_delete:bool=True,csvdump:bool=False,client_id:int=None,):

        """
        Delete a tag.

        :param tag_id:          Tag ID to delete.
        :type  tag_id:          int

        :param force_delete:    Indicates whether or not deletion should be forced.
        :type  force_delete:    bool

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:  Boolean reflecting the indication from the platform as to whether
                  or not the deletion was successful.

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        body = {
                "filterRequest": {
                    "filters":search_filters
                },
                "forceDeleteTicket": True
                }

        url = self.api_base_url.format(str(client_id))

        if csvdump==True:
            self.downloadfilterinexport('tagsthatarebeingdeleted',search_filters)
        try:
            self.request_handler.make_request(ApiRequestHandler.DELETE, url, body=body)
            success = True
            return success
        except (RequestFailed,Exception) as e:
            print('Error in deleting the tag')
            print()
            print(e)
            exit()

    def get_history(self, tag_id:int, page_num:int, page_size:int,csvdump:bool=False,client_id:int=None):

        """
        Get the history for a tag.

        :param tag_id:      Tag ID
        :type  tag_id:      int

        :param page_num:    Page number to retrieve.
        :type  page_num:    int

        :param page_size:   Number of items to be returned per page
        :type  page_size:   int

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    A paginated JSON response from the platform is returned.
        :rtype:     dict

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}/history".format(str(tag_id))

        paginated_url = url + "?size=" + str(page_size) + "&page=" + str(page_num)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, paginated_url)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)


        if csvdump==True:
            field_names = []
            print(jsonified_response)
            with open('taghistory.json','w') as f:
                f.write(json.dumps(jsonified_response))
            for item in jsonified_response['_embedded']['tagHistories'][0]:
                field_names.append(item)
            try:
                with open('get_taghistory.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    for item in jsonified_response['_embedded']['tagHistories']:
                        writer.writerow(item)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)

        return jsonified_response

    def get_single_search_page(self, search_filters:list, projection=Projection.BASIC, page_num=0, page_size=150,
                               sort_field=SortField.ID, sort_dir=SortDirection.ASC, client_id=None):

        """
        Searches for and returns tags based on the provided filter(s) and other parameters.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param page_num:        Page number of results to be returned.
        :type  page_num:        int

        :param page_size:       Number of results to be returned per page.
        :type  page_size:       int

        :param projection:      Projection to use for query.  Default is "basic"
        :type  projection:      Projection attribute

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
               sort_field=SortField.ID, sort_dir=SortDirection.ASC,csvdump:bool=False,client_id:int=None):

        """
        Searches for and returns tags based on the provided filter(s) and other parameters.  Rather
        than returning paginated results, this function cycles through all pages of results and returns
        them all in a single list.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param projection:      Projection to be used in API request.  "basic" or "detail"
        :type  projection:      Projection attribute

        :param page_size:       The number of results per page to be returned.
        :type  page_size:       int

        :param sort_field:      Name of field to sort results on.
        :type  sort_field:      SortField attribute

        :param sort_dir:        Direction to sort. SortDirection.ASC or SortDirection.DESC
        :type sort_dir:         SortDirection attribute

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

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
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
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

        if csvdump==True:
            self.downloadfilterinexport('tagsearch',search_filters)
        return all_results



    def lock_tag(self, tag_id:int,csvdump:bool=False, client_id:int=None):

        """
        Lock an existing tag.

        :param tag_id:      The tag ID to be locked.
        :type  tag_id:      int

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The tag ID
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}".format(str(tag_id))

        body = {
            "fields": [
                {
                    'uid': 'LOCKED',
                    'value': True
                }
            ]
        }

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
    

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        

        jsonified_response = json.loads(raw_response.text)
        response_id = jsonified_response['id']

        if csvdump==True:
            self.downloadfilterinexport('tagslocked',[{"field":"id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":f"{tag_id}"}])

        return response_id

    def unlock_tag(self, tag_id:int,csvdump:bool=False, client_id:int=None):

        """
        Unlock an existing tag.

        :param tag_id:      The tag ID to be unlocked.
        :type  tag_id:      int

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The tag ID
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}".format(str(tag_id))

        body = {
            "fields": [
                {
                    'uid': 'LOCKED',
                    'value': False
                }
            ]
        }

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        


        jsonified_response = json.loads(raw_response.text)
        response_id = jsonified_response['id']

        if csvdump==True:
            self.downloadfilterinexport('tagunlocked',[{"field":"id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":f"{tag_id}"}])

        return response_id

    def get_model(self, client_id:int=None):

        """
        Get available projections and models for Tags.

        :param client_id:   Client ID
        :type  client_id:   int

        :return:    Tags projections and models are returned.
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
