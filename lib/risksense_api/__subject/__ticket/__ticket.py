""" *******************************************************************************************************************
|
|  Name        :  __tags.py
|  Module      :  risksense_api
|  Description :  A class to be used for searching for and updating tags on the RiskSense Platform.
|  Copyright   :  (c) RiskSense, Inc.
|  License     :  Apache-2.0 (http://www.apache.org/licenses/LICENSE-2.0)
|
******************************************************************************************************************* """

from http import client
import json
from ..__exports import ExportFileType
from ..__exports import ExportRowNumbers
from .. import Subject
from ..._params import *
from ..._api_request_handler import *


class Ticket(Subject):

    """ Ticket class """

    def __init__(self, profile):

        """
        Initialization of Ticket object.

        :param profile:     Profile Object
        :type  profile:     _profile
        """

        self.subject_name = "ticket"
        Subject.__init__(self, profile, self.subject_name)

    def getconnectorfields(self,connector_id, client_id=None):

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

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The new tag ID will be returned.
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]


        url =self.profile.platform_url+ "/api/v1/client/{}/connector/{}/ticket".format(str(client_id),str(connector_id))


        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('There was an error fetching template')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response




    def gettemplateid(self,connector_id, client_id=None):

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

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The new tag ID will be returned.
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]


        url = self.profile.platform_url+f'/api/v1/client/{client_id}/connector/{connector_id}/template'

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('There was an error fetching template')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response


    def getfieldsfromtemplateid(self,connector_id,template_id, client_id=None):

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

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The new tag ID will be returned.
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]


        url = self.profile.platform_url+f'/api/v1/client/{client_id}/connector/{connector_id}/template/{template_id}/field'

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('There was an error fetching template')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def getcatalogitemfield(self,connector_id, client_id=None):

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

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The new tag ID will be returned.
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]


        url = self.profile.platform_url+f'/api/v1/client/{client_id}/connector/{connector_id}/catalogItemField'

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('There was an error fetching template')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def getissuetypefield(self,connector_id, client_id=None):

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

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The new tag ID will be returned.
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]


        url = self.profile.platform_url+f'/api/v1/client/{client_id}/connector/{connector_id}/issueTypeField'

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('There was an error fetching issue type field')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def getticketinfo(self,ticket_id, client_id=None):

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

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The new tag ID will be returned.
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]


        url = self.api_base_url.format(str(client_id))+'/{}'.format(str(ticket_id))

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('There was an error fetching ticket information')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def deleteticket(self,ticket_uuid, client_id=None):

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

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The new tag ID will be returned.
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]


        url = self.api_base_url.format(str(client_id))+'/{}'.format(str(ticket_uuid))

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.DELETE, url)
        except (RequestFailed,Exception) as e:
            print('There was an error fetching ticket information')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def create_ticket(self,tag_id,body,client_id=None):

        if client_id is None:
            client_id = self._use_default_client_id()[0]


        url = self.api_base_url.format(str(client_id))+'/{}'.format(str(tag_id))

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except (RequestFailed,Exception) as e:
            print('There was an error fetching ticket information')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response
    
    def ivanti_itsm_fetch_ticketField_values(self, connector_id, client_id=None):

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+f'/api/v1/client/{client_id}/connector/{connector_id}/ivanti/fetchTicketFields'

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('There was an error fetching ticket information')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response        


    def ivanti_itsm_retrieve_ticketFields(self, connector_id, ticket_type,client_id=None):
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+f'/api/v1/client/{client_id}/connector/{connector_id}/ivanti/retriveTicketFields'
        body = {
            "type": "IVANTIITSM",
            "ticketType": ticket_type,
            "connectorId": connector_id
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except (RequestFailed,Exception) as e:
            print('There was an error fetching ticket information')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response  


    def ivanti_itsm_fetch_customers(self, connector_id, client_id=None):
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+f'/api/v1/client/{client_id}/connector/{connector_id}/ivanti/fetchCustomers/Frs_CompositeContract_Contacts'

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('There was an error fetching ticket information')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response  


    def ivanti_itsm_fetch_fieldValue_wrt_dependentField(self, ticket_type, connector_id, current_field, dependent_field, dependent_field_value, client_id=None):
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+f'/api/v1/client/{client_id}/connector/{connector_id}/ivanti/fetchValidatedFieldValue'

        body = {"type":"IVANTIITSM","ticketType":ticket_type,"connectorId":connector_id,"actualField":current_field,"dependentField":dependent_field,"dependentFieldValue":dependent_field_value}

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There was an error fetching ticket information')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response  


    def ivanti_itsm_fetch_validation(self, body, client_id=None):
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+f"/api/v1/client/{client_id}/connector/{body['connectorId']}/ivanti/formValidation"

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There was an error fetching ticket information')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response  


    def ivanti_itsm_fetch_releaseLink(self, connector_id, client_id=None):
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+f'/api/v1/client/{client_id}/connector/{connector_id}/ivanti/fetchCustomers/ReleaseProjects'

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('There was an error fetching ticket information')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response  


    def ivanti_itsm_fetch_requestorLink(self, connector_id, client_id=None):
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+f'/api/v1/client/{client_id}/connector/{connector_id}/ivanti/fetchCustomers/Employees'

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('There was an error fetching ticket information')
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
