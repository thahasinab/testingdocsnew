""" *******************************************************************************************************************
|
|  Name        : __connectors.py
|  Module      : risksense_api
|  Description : A class to be used for interacting with connectors on the RiskSense Platform.
|  Copyright   : (c) RiskSense, Inc.
|  License     : Apache-2.0 (http://www.apache.org/licenses/LICENSE-2.0)
|
******************************************************************************************************************* """

from http import client
import json
from json.encoder import INFINITY
from re import I, template
from turtle import title
from unicodedata import name
from ...__subject import Subject
from ..._api_request_handler import *
import csv


class Connectors(Subject):

    """ Connectors class """

    class Type:
        """ Connectors.Type class """
        NESSUS = 'NESSUS'
        QUALYS_VULN = 'QUALYS_VULN_FILE_PICKUP'
        QUALYS_VMDR= 'QUALYS_API_VULNERABILITY'
        QUALYS_ASSET = 'QUALYS_ASSET'
        NEXPOSE = 'NEXPOSE_FILE_PICKUP'
        TENEBLE_SEC_CENTER = 'TENEBLE_SECURITY_CENTER'
        BURPSUITE= "BURPSUITE"
        CROWDSTRIKE="FALCONSPOTLIGHT"
        QUALYS_WAS="QUALYS_WAS"
        VERACODE="VERACODE"
        SONAR_CLOUD="SONARCLOUD"
        JIRA = "JIRA"
        SERVICENOW_INCIDENT = "SERVICE_NOW"
        SERVICENOW_SERVICEREQUEST="SNOW_SERVICE_REQUEST"
        CHECKMARX_OSA = "CHECKMARXOSA"
        CHECKMARX_SAST = "CHECKMARXSAST"
        HCL_APPSCAN = "HCL_ASOC"
        QUALYS_PC="QUALYS_PC"
        CHERWELL="CHERWELL"
        SERVICENOW_CTC="GENERIC_SNOW"
        AWSINSPECTOR="AWS_INSPECTOR"
        EXPANDER="EXPANDER"
        NEXPOSE_ASSET="NEXPOSE_ASSET_TAG_FILE_PICKUP"


    class ScheduleFreq:
        """ Connectors.ScheduleFreq class """
        DAILY = "DAILY"
        WEEKLY = "WEEKLY"
        MONTHLY = "MONTHLY"

    def __init__(self, profile):

        """
        Initialization of Connectors object.

        :param profile:     Profile Object
        :type  profile:     _profile

        """

        self.subject_name = "connector"
        Subject.__init__(self, profile, self.subject_name)

    def get_single_connector(self,connector_id:int, csvdump:bool=False,client_id:int=None):

        """
        Get a connector detail based on connector id.

        :param connector_id:    The page number of results to be returned.
        :type  connector_id:    int

        :param csvdump:         Whether to dump the assessment history in a csv, true to dump and false to not dump
        :type  csvdump:         bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON response from the platform is returned.
        :rtype:     dict

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))+'/{}'.format(str(connector_id))

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print()
            print('Error in getting list')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        if csvdump==True:
            field_names = []
            for item in jsonified_response.keys():
                field_names.append(item)
            try:
                with open('get_singleconnectorlist.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    writer.writerow(jsonified_response)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)

        return jsonified_response
    
    def get_snow_category(self, snow_username:str, snow_password_or_token:str, snow_url:str,catalogid:str, client_id:int=None):
        """
        Get Service Now Category information.

        :param username:                    Service Now username
        :type username:                     str

        :param password_or_api_token:       Service Now API Token/Password
        :type password_or_api_token:        str

        :param snow_url:                    Service Now Platform URL
        :type snow_url:                     str

        :param catalogid:                    Catalog id to get category of
        :type  catalogid:                    str
        
        :param client_id:                   RS Client ID
        :type client_id:                    int

        :return json:                       jsonified response of category data
        :rtype json:                        dict

        """      

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        url = self.api_base_url.format(str(client_id)) + "/populate/catalog/{}/category".format(catalogid)

        connector_populate_body = {
            "type": Connectors.Type.SERVICENOW_SERVICEREQUEST,
            "username": snow_username,
            "password": snow_password_or_token,
            "url": snow_url,
        }		

        try:
            cred_authorize = self.request_handler.make_request(ApiRequestHandler.POST, url, body=connector_populate_body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()    

        if cred_authorize.status_code == 200:
            return json.loads(cred_authorize.text)

    def get_snow_item(self, snow_username:str, snow_password_or_token:str, snow_url:str,catalogid:str,categoryid:str, client_id:int=None):
        
        """
        Get Service Now item data

        :param username:                    Service Now username
        :type username:                     str

        :param password_or_api_token:       Service Now API Token/Password
        :type password_or_api_token:        str

        :param snow_url:                    Service Now Platform URL
        :type  snow_url:                    str

        :param catalogid:                   Service Now catalog id
        :type  catalogid:                   str

        :param categoryid:                   Service Now category id
        :type  categoryid:                   str

        :param client_id:                   RS Client ID
        :type client_id:                    int

        :return ticket_sync_string:         Service Now Ticket sync string
        :rtype ticket_sync_string:          str

        :return json:                       jsonified response of item data
        :rtype json:                        dict
        """      

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        url = self.api_base_url.format(str(client_id)) + "/populate/catalog/{}/category/{}/item".format(catalogid,categoryid)

        connector_populate_body = {
            "type": Connectors.Type.SERVICENOW_SERVICEREQUEST,
            "username": snow_username,
            "password": snow_password_or_token,
            "url": snow_url,
        }		

        try:
            cred_authorize = self.request_handler.make_request(ApiRequestHandler.POST, url, body=connector_populate_body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()    

        if cred_authorize.status_code == 200:
            return json.loads(cred_authorize.text)

    def get_snow_catalogitemvariables(self, snow_username:str, snow_password_or_token:str, snow_url:str,catalogid:str,categoryid:str,catalogitemid:str, client_id:int=None):
        
        """
        Get fields item data from items 

        :param username:                    Service Now username
        :type username:                     str

        :param password_or_api_token:       Service Now API Token/Password
        :type password_or_api_token:        str

        :param snow_url:                    Service Now Platform URL
        :type  snow_url:                     str

        :param catalogid:                   Service Now catalog id
        :type  catalogid:                   str

        :param categoryid:                   Service Now category id
        :type  categoryid:                   str

        :param catalogitemid:                Service Now item id
        :type  catalogitemid:                 str

        :param client_id:                    RS Client ID
        :type client_id:                     int

        :return json:                        jsonified response of item data
        :rtype json:                         dict
        """      

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        url = self.api_base_url.format(str(client_id)) + "/populate/catalog/{}/category/{}/item/{}".format(catalogid,categoryid,catalogitemid)

        connector_populate_body = {
            "type": Connectors.Type.SERVICENOW_SERVICEREQUEST,
            "username": snow_username,
            "password": snow_password_or_token,
            "url": snow_url,
        }		

        try:
            cred_authorize = self.request_handler.make_request(ApiRequestHandler.POST, url, body=connector_populate_body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()    

        if cred_authorize.status_code == 200:
            return json.loads(cred_authorize.text)

    def run_connector(self, connectorid:int, client_id:int=None):
        """
        Run connector based on connector id

        :param connectorid:                    Service Now connector
        :type connectorid:                     str

        :param client_id:                   RS Client ID
        :type client_id:                    int

        :return json:                       Json response of connector run
        :rtype json:                        dict

        """      

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        url = self.api_base_url.format(str(client_id)) + "/{}/run".format(connectorid)		

        try:
            cred_authorize = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()    

        if cred_authorize.status_code == 200:
            return json.loads(cred_authorize.text)

    def paginate_connector(self, page_num:int=0, page_size:int=150, csvdump:bool=False,client_id:int=None):

        """
        Get a paginated list of connectors associated with the client.

        :param page_num:        The page number of results to be returned.
        :type  page_num:        int

        :param page_size:       The number of results to return per page.
        :type  page_size:       int

        :param csvdump:             Whether to dump the connector data in a csv, true to dump and false to not dump
        :type  csvdump:             bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON response from the platform is returned.
        :rtype:     dict

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "?size=" + str(page_size) + "&page=" + str(page_num)

        if type(csvdump)!=bool:
            print('Please provide either true or false')
            exit()


        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print()
            print('Error in getting list')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        if csvdump==True:
            field_names = []
            for i in range(len(jsonified_response["_embedded"]["connectors"])):
                for item in jsonified_response["_embedded"]["connectors"][i].keys():
                    if item not in field_names:
                        field_names.append(item)
            try:
                with open('get_connectorlist.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    for item in jsonified_response["_embedded"]["connectors"]:
                        writer.writerow(item)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)

        return jsonified_response
    
    def connector_populate(self,body:dict,client_id:int=None):

        """
        Populate data of connector.

        :param body:        Populate body
        :type  body:        dict

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return jsonified_response:    The JSON response from the platform is returned.
        :rtype jsonified_response:     dict

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]
            
        populateurl= self.api_base_url.format(str(client_id))+'/populate'

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url=populateurl,body=body)
        except (RequestFailed,Exception) as e:
            print()
            print('Error in connector populate')
            print(e)
            exit()
        if raw_response.status_code == 200:   
            jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def create_scanning_connector(self, conn_name:str, conn_type:str, conn_url:str, schedule_freq:str, network_id:int,username_or_access_key:str, password_or_secret_key:str, auto_urba:bool=True, client_id:int=None, **kwargs):

        """
        Create a new scanning connector.

        :param conn_name:       The connector name.
        :type  conn_name:       str

        :param conn_type:       The connector type. (Valid options are: Connectors.Type.NESSUS, Connectors.Type.NEXPOSE,Connectors.Type.
                                                                        Connectors.Type.QUALYS_VULN,Connectors.Type.QUALYS_VMDR, Connectors.Type.QUALYS_ASSET,Connectors.Type.NEXPOSE,Connectors.Type.NEXPOSE_ASSET,Connectors.Type.BURPSUITE,Connectors.Type.CROWDSTRIKE,Connectors.Type.QUALYS_WAS,Connectors.Type.VERACODE,Connectors.Type.SONAR_CLOUD,Connectors.Type.HCL_APPSCAN,Connectors.Type.QUALYS_PC,Connectors.Type.AWSINSPECTOR,Connectors.Type.EXPANDER,Connectors.Type.TENEBLE_SEC_CENTER NESSUS = 'NESSUS'
        :type  conn_type:       str

        :param conn_url:        The URL for the connector to communicate with.
        :type  conn_url:        str

        :param schedule_freq:   The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                        Connectors.ScheduleFreq.WEEKLY,
                                                                        Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:   str

        :param network_id:      The network ID
        :type  network_id:      int

        :param username_or_access_key:      The username to use for connector authentication.
        :type  username_or_access_key:      str

        :param password_or_secret_key:      The password to use for connector authentication.
        :type  password_or_secret_key:      str

        :param auto_urba:       Automatically run URBA after connector runs
        :type  auto_urba:       bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword ssl_cert:      Optional SSL certificate.
        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31
        :keyword template:      Template data
        :keyword create_asset: Create asset data
        :keyword reportnameprefix: Report Name Prefix
        :keyword authmechanism: Auth mechanism
        
        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))

        ssl_cert = kwargs.get('ssl_cert', None)
        hour_of_day = kwargs.get('hour_of_day', None)
        day_of_week = kwargs.get('day_of_week', None)
        day_of_month = kwargs.get('day_of_month', None)
        template=kwargs.get('template','None')
        createassetifzerovulnfoundinfile=kwargs.get('create_asset',False)
        reportNamePrefix=kwargs.get('reportnameprefix','')
        authmechanism=kwargs.get('authmechanism','APIKey')

        if conn_type == Connectors.Type.NESSUS:

            attributes = {
                "accessKey": username_or_access_key,
                "secretKey": password_or_secret_key
            }
        elif conn_type ==Connectors.Type.BURPSUITE:

            attributes ={"username":username_or_access_key,
            "password":password_or_secret_key,"createAssetsIfZeroVulnFoundInFile":createassetifzerovulnfoundinfile}
        
        elif conn_type==Connectors.Type.AWSINSPECTOR:
            attributes ={"username":username_or_access_key,
            "password":password_or_secret_key,"template":template}


        elif conn_type ==Connectors.Type.SONAR_CLOUD:
            ingestionfindingstype = kwargs.get('ingestionfindingstype',[])
            attributes ={"username":username_or_access_key,
            "password":password_or_secret_key,"createAssetsIfZeroVulnFoundInFile":createassetifzerovulnfoundinfile,"ingestionfindingsType":ingestionfindingstype}

        
        elif conn_type ==Connectors.Type.NEXPOSE or conn_type == Connectors.Type.QUALYS_WAS or conn_type == Connectors.Type.QUALYS_PC or conn_type == Connectors.Type.NEXPOSE_ASSET:

            attributes ={"username":username_or_access_key,
                "password":password_or_secret_key,
                "reportNamePrefix": reportNamePrefix}
        elif conn_type == Connectors.Type.VERACODE:
            attributes= {"username":username_or_access_key,
                "password":password_or_secret_key,"authMechanism":authmechanism}

        elif conn_type ==Connectors.Type.QUALYS_VULN or conn_type==Connectors.Type.EXPANDER:

            attributes ={"username":username_or_access_key,
                "password":password_or_secret_key,
                "reportNamePrefix": reportNamePrefix}

        else:
            attributes = {
                "username": username_or_access_key,
                "password": password_or_secret_key
            }

        body = {
            "type": conn_type,
            "name": conn_name,
            "connection": {
                "url": conn_url
            },
            "networkId": network_id,
            "attributes": attributes,
            "autoUrba": auto_urba
        }

        if ssl_cert is not None:
            body['connection'].update(sslCertificates=ssl_cert)

        if schedule_freq == Connectors.ScheduleFreq.DAILY:

            if hour_of_day is None:
                hour_of_day = 12

            connector_schedule = {
                "enabled": True,
                "type": schedule_freq,
                "hourOfDay": hour_of_day
            }

        elif schedule_freq == Connectors.ScheduleFreq.WEEKLY:

            if day_of_week is None:
                day_of_week = 1

            if hour_of_day is None:
                hour_of_day = 12

            connector_schedule = {
                "enabled": True,
                "type": schedule_freq,
                "hourOfDay": hour_of_day,
                "daysOfWeek": day_of_week
            }

        elif schedule_freq == Connectors.ScheduleFreq.MONTHLY:

            if day_of_month is None:
                day_of_month = 1

            if hour_of_day is None:
                hour_of_day = 12

            connector_schedule = {
                "enabled": True,
                "type": schedule_freq,
                "hourOfDay": hour_of_day,
                "daysOfMonth": day_of_month
            }

        else:
            raise ValueError("Schedule freq. should be DAILY, WEEKLY, or MONTHLY.")

        body.update(schedule=connector_schedule)
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print()
            print('Error in creating scanning connector')
            print(e)
            exit()
        if raw_response.status_code == 201:
            jsonified_response = json.loads(raw_response.text)
            job_id = jsonified_response['id']

        return job_id
    
    def create_expander(self, conn_name:str, conn_url:str, schedule_freq:str, network_id:int,username:str, apikey:str,auto_urba:bool=True, client_id:bool=None, **kwargs):

        """
        Create a new expander connector.

        :param conn_name:       The connector name.
        :type  conn_name:       str

        :param conn_url:        The URL for the connector to communicate with.
        :type  conn_url:        str

        :param schedule_freq:   The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,Connectors.ScheduleFreq.WEEKLY,Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:   str

        :param network_id:      The network ID
        :type  network_id:      int

        :param username:      The username to use for connector authentication.
        :type  username:      str

        :param apikey:      The password to use for connector authentication.
        :type  apikey:      str

        :param auto_urba:       Automatically run URBA after connector runs?
        :type  auto_urba:       bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword ssl_cert:      Optional SSL certificate.
        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            connector_id = self.create_scanning_connector(conn_name, Connectors.Type.EXPANDER, conn_url, schedule_freq, network_id,
                                       username,apikey, auto_urba, client_id, **kwargs)
        except (RequestFailed,Exception) as e:
            print()
            print('Error in creating expander connector')
            print(e)
            exit()

        return connector_id
    
    def cherwellincident_connector_populate(self,body:dict,client_id:int=None):

        """
        Populates cherwell incident connector data based on body

        :param body:       Body for connector populate.
        :type  body:        dict

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON response from the platform is returned.
        :rtype:     dict

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]
            
        populateurl= self.api_base_url.format(str(client_id))+'/populate/ticketType/Incident'

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url=populateurl,body=body)
        except (RequestFailed,Exception) as e:
            print()
            print('Error in setting address type')
            print(e)
            exit()
        if raw_response.status_code == 200:
            jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def cherwellproblem_connector_populate(self,body:dict,client_id:int=None):

        """
        Populates cherwell problem connector data based on body

        :param body:       Body for connector populate.
        :type  body:        dict

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON response from the platform is returned.
        :rtype:     dict

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]
            
        populateurl= self.api_base_url.format(str(client_id))+'/populate/ticketType/Problem'

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url=populateurl,body=body)
        except (RequestFailed,Exception) as e:
            print()
            print('Error in populating cherwell problem connector')
            print(e)
            exit()
        if raw_response.status_code == 200:
            jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def cherwellmakerequest_connector_populate(self,body:dict,client_id:int=None):

        """
        Populates cherwell make request connector data based on body

        :param body:       Body for connector populate.
        :type  body:        dict

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON response from the platform is returned.
        :rtype:     dict

        :raises RequestFailed:
        """
        
        if client_id is None:
            client_id = self._use_default_client_id()[0]
            
        populateurl= self.api_base_url.format(str(client_id))+'/populate/ticketType/ChangeRequest'

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url=populateurl,body=body)
        except (RequestFailed,Exception) as e:
            print()
            print('Error in populating cherwell make request connector')
            print(e)
            exit()
        if raw_response.status_code == 200:
            jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def create_cherwell_incident_connector(self,cw_name:str,cw_username:str,cw_password:str,clientid_key:str,cw_url:str,autourba:bool=False,client_id:int=None):
        
        """
        Creates cherwell connector type incident

        :param cw_name:       Cherwell connector name.
        :type  cw_name:       str

        :param cw_username:   Cherwell connector username.
        :type  cw_username:   str

        :param cw_password:   Cherwell connector password.
        :type  cw_password:    str

        :param clientid_key:   Cherwell connector client id key.
        :type  clientid_key:   str

        :param cw_url:   Cherwell connector url.
        :type  cw_url:   str

        :param autourba:  Switch to enable auto urba.
        :type  autourba:   bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    Id of connector
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
                client_id = self._use_default_client_id()[0]
        populateitembody={"username":cw_username,"password":cw_password,"url":cw_url,"clientIdKey":clientid_key,"type":Connectors.Type.CHERWELL}
        cherwellincident_connector_populate=self.cherwellincident_connector_populate(populateitembody)
        a={}
        choices={}
        dynamicdropdownfields={}
        dynamicdropdown=[]
        try:
            for i in range(len(cherwellincident_connector_populate['dynamicDropDownFields'])):
                a[cherwellincident_connector_populate['dynamicDropDownFields'][i]['value']]=i
                dynamicdropdownfields[cherwellincident_connector_populate['dynamicDropDownFields'][i]['value']]={"connectorCredentials":{"username":cw_username,"password":cw_password,"url":cw_url,"clientIdKey":clientid_key},"type":"CHERWELL","busObId":cherwellincident_connector_populate['dynamicDropDownFields'][i]["dependentKey"],"fieldId":cherwellincident_connector_populate['dynamicDropDownFields'][i]["fieldValue"],"fieldName":cherwellincident_connector_populate['dynamicDropDownFields'][i]["value"],"fields":[]}
                if cherwellincident_connector_populate['dynamicDropDownFields'][i]['parentField']!="":
                    j=a[cherwellincident_connector_populate['dynamicDropDownFields'][i]['parentField']]
                    while(True):
                        b={"dirty":"true","displayName":cherwellincident_connector_populate['dynamicDropDownFields'][j]['value'],"fieldId":cherwellincident_connector_populate['dynamicDropDownFields'][j]["fieldValue"],"value":""}
                        dynamicdropdownfields[cherwellincident_connector_populate['dynamicDropDownFields'][i]['value']]['fields'].append(b)
                        if cherwellincident_connector_populate['dynamicDropDownFields'][j]['parentField']!="":
                            j=a[cherwellincident_connector_populate['dynamicDropDownFields'][j]['parentField']]
                        else:
                            break
        except Exception as e:
            print(e)
            exit()
        enabled=[]
        for index in range(len(cherwellincident_connector_populate["supportedDescriptionFields"])):
            print(f"Index Number - {index} - {cherwellincident_connector_populate['supportedDescriptionFields'][index]['value']}:")
            enabled.append({"key":cherwellincident_connector_populate['supportedDescriptionFields'][index]['value'],"enabled":False})
            lockedfieldchoice=[]
        try:
            temp=input('Please enter the supported description fields index number seperated by commas:').split(',')
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        for i in temp:
            enabled[int(i)]['enabled']=True

        for key in dynamicdropdownfields:
                    if dynamicdropdownfields[key]['fields']!=[]:
                        for i in range(len(dynamicdropdownfields[key]['fields'])):
                            for j in choices:  
                                if dynamicdropdownfields[key]['fields'][i]['displayName']==j:
                                    dynamicdropdownfields[key]['fields'][i]['value']=choices[j]
                    fieldlookup=self.api_base_url.format(str(client_id))+"/populate/ticketType/Incident/fieldvalueslookup"
                    body=dynamicdropdownfields[key]
                    try:
                        fieldvalueslookup = self.request_handler.make_request(ApiRequestHandler.POST, fieldlookup, body=dynamicdropdownfields[key])
                    except (RequestFailed,Exception) as e:
                            print()
                            print('Error in getting field values lookup')
                            print(e)
                            exit()
                    if fieldvalueslookup.status_code == 200:
                        fieldvalueslookup=json.loads(fieldvalueslookup.text)
                    for i in range(len(fieldvalueslookup['values'])):
                        print(f"Index Number - {i} - {fieldvalueslookup['values'][i]}")
                    try:
                        k=int(input(f'Please enter {key}:'))
                    except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
                    choices[key]=fieldvalueslookup['values'][k]
                    dynamicdropdown.append({ "displayValue":key,"value":fieldvalueslookup['values'][k],"key":dynamicdropdownfields[key]["fieldId"]})

        optionaldropdownlist={}
        for i in range(len(cherwellincident_connector_populate["optionalDropdownList"])):
            a[cherwellincident_connector_populate["optionalDropdownList"][i]["label"]]=i
            optionaldropdownlist[cherwellincident_connector_populate["optionalDropdownList"][i]['value']]={"connectorCredentials":{"username":cw_username,"password":cw_password,"url":cw_url,"clientIdKey":clientid_key},"type":"CHERWELL","busObId":cherwellincident_connector_populate["optionalDropdownList"][i]["dependentKey"],"fieldId":cherwellincident_connector_populate["optionalDropdownList"][i]["fieldValue"],"fieldName":cherwellincident_connector_populate["optionalDropdownList"][i]["value"],"fields":[]}
        fieldlookup=self.api_base_url.format(str(client_id))+"/populate/ticketType/Incident/fieldvalueslookup"
        try:
            status = self.request_handler.make_request(ApiRequestHandler.POST, fieldlookup, body=optionaldropdownlist["Status"])
        except (RequestFailed,Exception) as e:
            print()
            print('There was an error in field values lookup')
            print(e) 
            exit()
        extradata={}
        if status.status_code == 200:
            status=json.loads(status.text)
        for index in range(len(status['values'])):
            print(f"Index Number - {index} - {status['values'][index]}:")
        lockedfieldchoice=[]
        try:
            temp=input('Please enter the index seperated by commas').split(',')
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        for i in temp:
            lockedfieldchoice.append(status['values'][int(i)])
        extradata["closeStatusesOfTicketToUpdate"]=lockedfieldchoice
        try:
            extradata["closedStateKey"]=status['values'][int(input('Enter the index number of close status field that you want to select:'))]
            extradata["closedStateLabel"]=extradata["closedStateKey"]
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        dynamicFieldDetailValue=[]
        fieldslist=["dynamicFieldDetailValue","tagTypeDefaultOptions","slaDateFieldOptions","lockedFields"]
        try:
            for fields in fieldslist:
                extradata[fields]=[]
                if fields=="dynamicFieldDetailValue":
                    for i in range(len(cherwellincident_connector_populate[fields])):
                        a=input(f'Please enter a value for {cherwellincident_connector_populate[fields][i]["label"]}')
                        dynamicFieldDetailValue.append({"displayValue":cherwellincident_connector_populate[fields][i]['label'],"value":a,"key":cherwellincident_connector_populate[fields][i]["fieldValue"]})
                elif fields=="lockedFields":
                    for i in range(len(cherwellincident_connector_populate[fields])):
                        print(f'{i}-{cherwellincident_connector_populate[fields][i]}')
                    lockedfieldchoice=[]
                    temp=input('Please enter the index numbers of locked fields that you want to select in comma seperated values:').split(',')
                    for i in temp:
                        lockedfieldchoice.append(cherwellincident_connector_populate[fields][int(i)]['value'])
                    extradata[fields]=lockedfieldchoice
                else:
                    for i in range(len(cherwellincident_connector_populate[fields])):
                        print(f"Index Number - {i} - {cherwellincident_connector_populate[fields][i]['displayValue']}")
                    extradata[fields]=cherwellincident_connector_populate[fields][int(input(f'Please enter the index number for {fields}:'))]
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        postconnectorbody={
                "name": cw_name,
                "type": Connectors.Type.CHERWELL,
                "schedule": {
                    "enabled": True,
                    "type": "DAILY",
                    "hourOfDay": 0
                },
                "attributes": {
                    "username": cw_username,
                    "password": cw_password,
                    "clientIdKey": clientid_key
                },
                "connection": {
                    "url": cw_url
                },
                "connectorField": {
                    "type": Connectors.Type.CHERWELL,
                    "clientIdKey": clientid_key,
                    "ticketType": {
                        "displayValue": "Incident",
                        "value": "Incident"
                    },
                    "descriptionFields": enabled
                    ,
                    "dynamicDropdownFields": dynamicdropdown,
                    "dynamicFieldDetailValue": dynamicFieldDetailValue,
                    "optionalMandatoryFieldDetailValue": [],
                    "lockedFields": lockedfieldchoice,
                    "slaDateField":extradata["slaDateFieldOptions"]["displayValue"],"tagTypeDefaultValue":extradata["tagTypeDefaultOptions"]["displayValue"],
                    "connectorSettings": {
                        "closeFindingsOnTicketCloseEnabled": False,
                        "closeStatusesOfTicketToUpdate": ','.join(extradata['closeStatusesOfTicketToUpdate']),
                        "closeTicketOnFindingsCloseEnabled": False,
                        "closedStateKey":(extradata['closedStateKey']),
                        "closedStateLabel": extradata['closedStateKey'],
                        "enabledTagRemoval": True,
                        "enabledUploadAttachment": True,
                        "initialState": ""
                    },
                    "usePluginInfoFields": [],
                    "isTagRemovalEnabled": True,
                    "isTicketingConnector": True,
                    "autoUrba": autourba
                }
            }
        connectorcreateurl=self.api_base_url.format(str(client_id))
        try:
            postconnectorcreate = self.request_handler.make_request(ApiRequestHandler.POST, connectorcreateurl, body=postconnectorbody)
        except (RequestFailed,Exception) as e:
            print()
            print('There was an error in connector creation')
            print(e)
            exit()
        if postconnectorcreate.status_code == 200:
            populateitems_json = json.loads(postconnectorcreate.text)
            id=populateitems_json['id']
        else:
            print(postconnectorcreate.status_code)
        
        return id

    def create_cherwell_problem_connector(self,cw_name:str,cw_username:str,cw_password:str,clientid_key:str,cw_url:str,autourba:bool=False,client_id:int=None):
    
        """
        Creates cherwell connector type problem

        :param cw_name:       Cherwell connector name.
        :type  cw_name:       str

        :param cw_username:   Cherwell connector username.
        :type  cw_username:   str

        :param cw_password:   Cherwell connector password.
        :type  cw_password:    str

        :param clientid_key:   Cherwell connector client id key.
        :type  clientid_key:   str

        :param cw_url:   Cherwell connector url.
        :type  cw_url:   str

        :param autourba:  Switch to enable auto urba.
        :type  autourba:   bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    Connector id
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
                client_id = self._use_default_client_id()[0]
        populateitembody={"username":cw_username,"password":cw_password,"url":cw_url,"clientIdKey":clientid_key,"type":Connectors.Type.CHERWELL}
        cherwellproblem_connector_populate=self.cherwellproblem_connector_populate(populateitembody)
        a={}
        choices={}
        dynamicdropdownfields={}
        dynamicdropdown=[]
        try:
            for i in range(len(cherwellproblem_connector_populate['dynamicDropDownFields'])):
                a[cherwellproblem_connector_populate['dynamicDropDownFields'][i]['value']]=i
                dynamicdropdownfields[cherwellproblem_connector_populate['dynamicDropDownFields'][i]['value']]={"connectorCredentials":{"username":cw_username,"password":cw_password,"url":cw_url,"clientIdKey":clientid_key},"type":"CHERWELL","busObId":cherwellproblem_connector_populate['dynamicDropDownFields'][i]["dependentKey"],"fieldId":cherwellproblem_connector_populate['dynamicDropDownFields'][i]["fieldValue"],"fieldName":cherwellproblem_connector_populate['dynamicDropDownFields'][i]["value"],"fields":[]}
                if cherwellproblem_connector_populate['dynamicDropDownFields'][i]['parentField']!="":
                    j=a[cherwellproblem_connector_populate['dynamicDropDownFields'][i]['parentField']]
                    while(True):
                        b={"dirty":"true","displayName":cherwellproblem_connector_populate['dynamicDropDownFields'][j]['value'],"fieldId":cherwellproblem_connector_populate['dynamicDropDownFields'][j]["fieldValue"],"value":""}
                        dynamicdropdownfields[cherwellproblem_connector_populate['dynamicDropDownFields'][i]['value']]['fields'].append(b)
                        if cherwellproblem_connector_populate['dynamicDropDownFields'][j]['parentField']!="":
                            j=a[cherwellproblem_connector_populate['dynamicDropDownFields'][j]['parentField']]
                        else:
                            break
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        enabled=[]

        for index in range(len(cherwellproblem_connector_populate["supportedDescriptionFields"])):
            print(f"Index Number - {index} - {cherwellproblem_connector_populate['supportedDescriptionFields'][index]['value']}:")
            enabled.append({"key":cherwellproblem_connector_populate['supportedDescriptionFields'][index]['value'],"enabled":False})
            lockedfieldchoice=[]
        try:
            temp=input('Please enter the support description fields seperated by commas').split(',')
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        for i in temp:
            enabled[int(i)]['enabled']=True
        for key in dynamicdropdownfields:
                    if dynamicdropdownfields[key]['fields']!=[]:
                        for i in range(len(dynamicdropdownfields[key]['fields'])):
                            for j in choices:  
                                if dynamicdropdownfields[key]['fields'][i]['displayName']==j:
                                    dynamicdropdownfields[key]['fields'][i]['value']=choices[j]
                    fieldlookup=self.api_base_url.format(str(client_id))+"/populate/ticketType/Problem/fieldvalueslookup"
                    body=dynamicdropdownfields[key]
                    try:
                        fieldvalueslookup = self.request_handler.make_request(ApiRequestHandler.POST, fieldlookup, body=dynamicdropdownfields[key])
                    except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
                    fieldvalueslookup=json.loads(fieldvalueslookup.text)
                    for i in range(len(fieldvalueslookup['values'])):
                        print(f"Index Number - {i} - {fieldvalueslookup['values'][i]}")
                    try:
                        k=int(input(f'Please enter {key}:'))
                        choices[key]=fieldvalueslookup['values'][k]
                        dynamicdropdown.append({ "displayValue":key,"value":fieldvalueslookup['values'][k],"key":dynamicdropdownfields[key]["fieldId"]})
                    except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        optionaldropdownlist={}
        for i in range(len(cherwellproblem_connector_populate["optionalDropdownList"])):
            a[cherwellproblem_connector_populate["optionalDropdownList"][i]["label"]]=i
            optionaldropdownlist[cherwellproblem_connector_populate["optionalDropdownList"][i]['value']]={"connectorCredentials":{"username":cw_username,"password":cw_password,"url":cw_url,"clientIdKey":clientid_key},"type":"CHERWELL","busObId":cherwellproblem_connector_populate["optionalDropdownList"][i]["dependentKey"],"fieldId":cherwellproblem_connector_populate["optionalDropdownList"][i]["fieldValue"],"fieldName":cherwellproblem_connector_populate["optionalDropdownList"][i]["value"],"fields":[]}
        fieldlookup=self.api_base_url.format(str(client_id))+"/populate/ticketType/Problem/fieldvalueslookup"
        try:
            status = self.request_handler.make_request(ApiRequestHandler.POST, fieldlookup, body=optionaldropdownlist["Status"])
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        extradata={}
        status=json.loads(status.text)
        for index in range(len(status['values'])):
            print(f"Index Number - {index} - {status['values'][index]}:")
        lockedfieldchoice=[]
        try:
            temp=input('Please enter the index number of ticket sync state in comma seperated values').split(',')
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        for i in temp:
            lockedfieldchoice.append(status['values'][i])
        try:
            extradata["closeStatusesOfTicketToUpdate"]=lockedfieldchoice
            extradata["closedStateKey"]=status['values'][int(input('Enter the index number of close status field that you want to select:'))]
            extradata["closedStateLabel"]=extradata["closedStateKey"]
            dynamicFieldDetailValue=[]
            fieldslist=["dynamicFieldDetailValue","tagTypeDefaultOptions","slaDateFieldOptions","lockedFields"]
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        try:
            for fields in fieldslist:
                extradata[fields]=[]
                if fields=="dynamicFieldDetailValue":
                    for i in range(len(cherwellproblem_connector_populate[fields])):
                        a=input(f'Please enter a value for {cherwellproblem_connector_populate[fields][i]["label"]}')
                        dynamicFieldDetailValue.append({"displayValue":cherwellproblem_connector_populate[fields][i]['label'],"value":a,"key":cherwellproblem_connector_populate[fields][i]["fieldValue"]})
                elif fields=="lockedFields":
                    for i in range(len(cherwellproblem_connector_populate[fields])):
                        print(f'{i}-{cherwellproblem_connector_populate[fields][i]}')
                    lockedfieldchoice=[]
                    temp=input('Please enter the index number of the locked fields that you want to select in comma seperated values').split(',')
                    for i in temp:
                        lockedfieldchoice.append(cherwellproblem_connector_populate[fields][i]['value'])
                    extradata[fields]=lockedfieldchoice
                else:
                    for i in range(len(cherwellproblem_connector_populate[fields])):
                        print(f"Index Number - {i} - {cherwellproblem_connector_populate[fields][i]['displayValue']}")
                    extradata[fields]=cherwellproblem_connector_populate[fields][int(input(f'Please enter the index number for {fields}:'))]

            postconnectorbody={
                    "name": cw_name,
                    "type": Connectors.Type.CHERWELL,
                    "schedule": {
                        "enabled": True,
                        "type": "DAILY",
                        "hourOfDay": 0
                    },
                    "attributes": {
                        "username": cw_username,
                        "password": cw_password,
                        "clientIdKey": clientid_key
                    },
                    "connection": {
                        "url": cw_url
                    },
                    "connectorField": {
                        "type": Connectors.Type.CHERWELL,
                        "clientIdKey": clientid_key,
                        "ticketType": {
                            "displayValue": "Problem",
                            "value": "Problem"
                        },
                        "descriptionFields": enabled
                        ,
                        "dynamicDropdownFields": dynamicdropdown,
                        "dynamicFieldDetailValue": dynamicFieldDetailValue,
                        "optionalMandatoryFieldDetailValue": [],
                        "lockedFields": lockedfieldchoice,
                        "slaDateField":extradata["slaDateFieldOptions"]["displayValue"],"tagTypeDefaultValue":extradata["tagTypeDefaultOptions"]["displayValue"],
                        "connectorSettings": {
                            "closeFindingsOnTicketCloseEnabled": False,
                            "closeStatusesOfTicketToUpdate": ','.join(extradata['closeStatusesOfTicketToUpdate']),
                            "closeTicketOnFindingsCloseEnabled": False,
                            "closedStateKey":(extradata['closedStateKey']),
                            "closedStateLabel": extradata['closedStateKey'],
                            "enabledTagRemoval": True,
                            "enabledUploadAttachment": True,
                            "initialState": ""
                        },
                        "usePluginInfoFields": [],
                        "isTagRemovalEnabled": True,
                        "isTicketingConnector": True,
                        "autoUrba": autourba
                    }
                }
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        connectorcreateurl=self.api_base_url.format(str(client_id))
        try:
            postconnectorcreate = self.request_handler.make_request(ApiRequestHandler.POST, connectorcreateurl, body=postconnectorbody)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        if postconnectorcreate.status_code == 200:
            populateitems_json = json.loads(postconnectorcreate.text)
            id=populateitems_json['id']
        
        return id

    def create_cherwell_makerequest_connector(self,cw_name:str,cw_username:str,cw_password:str,clientid_key:str,cw_url:str,autourba:bool=False,client_id:int=None):

        """
        Creates cherwell connector type make request

        :param cw_name:       Cherwell connector name.
        :type  cw_name:       str

        :param cw_username:   Cherwell connector username.
        :type  cw_username:   str

        :param cw_password:   Cherwell connector password.
        :type  cw_password:    str

        :param clientid_key:   Cherwell connector client id key.
        :type  clientid_key:   str

        :param cw_url:   Cherwell connector url.
        :type  cw_url:   str

        :param autourba:  Switch to enable auto urba.
        :type  autourba:   bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    Connector id
        :rtype:     int


        :raises RequestFailed:
        """

        if client_id is None:
                client_id = self._use_default_client_id()[0]
        populateitembody={"username":cw_username,"password":cw_password,"url":cw_url,"clientIdKey":clientid_key,"type":Connectors.Type.CHERWELL}
        cherwellmakerequest_connector_populate=self.cherwellmakerequest_connector_populate(populateitembody)
        a={}
        choices={}
        dynamicdropdownfields={}
        dynamicdropdown=[]
        try:
            for i in range(len(cherwellmakerequest_connector_populate['dynamicDropDownFields'])):
                a[cherwellmakerequest_connector_populate['dynamicDropDownFields'][i]['value']]=i
                dynamicdropdownfields[cherwellmakerequest_connector_populate['dynamicDropDownFields'][i]['value']]={"connectorCredentials":{"username":cw_username,"password":cw_password,"url":cw_url,"clientIdKey":clientid_key},"type":"CHERWELL","busObId":cherwellmakerequest_connector_populate['dynamicDropDownFields'][i]["dependentKey"],"fieldId":cherwellmakerequest_connector_populate['dynamicDropDownFields'][i]["fieldValue"],"fieldName":cherwellmakerequest_connector_populate['dynamicDropDownFields'][i]["value"],"fields":[]}
                if cherwellmakerequest_connector_populate['dynamicDropDownFields'][i]['parentField']!="":
                    j=a[cherwellmakerequest_connector_populate['dynamicDropDownFields'][i]['parentField']]
                    while(True):
                        b={"dirty":"true","displayName":cherwellmakerequest_connector_populate['dynamicDropDownFields'][j]['value'],"fieldId":cherwellmakerequest_connector_populate['dynamicDropDownFields'][j]["fieldValue"],"value":""}
                        dynamicdropdownfields[cherwellmakerequest_connector_populate['dynamicDropDownFields'][i]['value']]['fields'].append(b)
                        if cherwellmakerequest_connector_populate['dynamicDropDownFields'][j]['parentField']!="":
                            j=a[cherwellmakerequest_connector_populate['dynamicDropDownFields'][j]['parentField']]
                        else:
                            break
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        enabled=[]
        for index in range(len(cherwellmakerequest_connector_populate["supportedDescriptionFields"])):
            print(f"Index Number - {index} - {cherwellmakerequest_connector_populate['supportedDescriptionFields'][index]['value']}:")
            enabled.append({"key":cherwellmakerequest_connector_populate['supportedDescriptionFields'][index]['value'],"enabled":False})
            lockedfieldchoice=[]
        try:
            temp=input('Please enter the supported description fields seperated by commas').split(',')
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        for i in temp:
            enabled[int(i)]['enabled']=True
        for key in dynamicdropdownfields:
                    if dynamicdropdownfields[key]['fields']!=[]:
                        for i in range(len(dynamicdropdownfields[key]['fields'])):
                            for j in choices:  
                                if dynamicdropdownfields[key]['fields'][i]['displayName']==j:
                                    dynamicdropdownfields[key]['fields'][i]['value']=choices[j]
                    fieldlookup=self.api_base_url.format(str(client_id))+"/populate/ticketType/ChangeRequest/fieldvalueslookup"
                    body=dynamicdropdownfields[key]
                    try:
                        fieldvalueslookup = self.request_handler.make_request(ApiRequestHandler.POST, fieldlookup, body=dynamicdropdownfields[key])
                    except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
                    fieldvalueslookup=json.loads(fieldvalueslookup.text)
                    for i in range(len(fieldvalueslookup['values'])):
                        print(f"Index Number - {i} - {fieldvalueslookup['values'][i]}")
                    try:
                        k=int(input(f'Please enter {key}:'))
                    except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
                    choices[key]=fieldvalueslookup['values'][k]
                    dynamicdropdown.append({ "displayValue":key,"value":fieldvalueslookup['values'][k],"key":dynamicdropdownfields[key]["fieldId"]})

        optionaldropdownlist={}
        for i in range(len(cherwellmakerequest_connector_populate["optionalDropdownList"])):
            a[cherwellmakerequest_connector_populate["optionalDropdownList"][i]["label"]]=i
            optionaldropdownlist[cherwellmakerequest_connector_populate["optionalDropdownList"][i]['value']]={"connectorCredentials":{"username":cw_username,"password":cw_password,"url":cw_url,"clientIdKey":clientid_key},"type":"CHERWELL","busObId":cherwellmakerequest_connector_populate["optionalDropdownList"][i]["dependentKey"],"fieldId":cherwellmakerequest_connector_populate["optionalDropdownList"][i]["fieldValue"],"fieldName":cherwellmakerequest_connector_populate["optionalDropdownList"][i]["value"],"fields":[]}
        fieldlookup=self.api_base_url.format(str(client_id))+"/populate/ticketType/ChangeRequest/fieldvalueslookup"
        try:
            status = self.request_handler.make_request(ApiRequestHandler.POST, fieldlookup, body=optionaldropdownlist["Status"])
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        extradata={}
        status=json.loads(status.text)
        for index in range(len(status['values'])):
            print(f"Index Number - {index} - {status['values'][index]}:")
        lockedfieldchoice=[]
        try:
            temp=input('Enter the index number of ticket sync state that you want to select seperated by commas:').split(',')
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        for i in temp:
            lockedfieldchoice.append(status['values'][int(i)])
        extradata["closeStatusesOfTicketToUpdate"]=lockedfieldchoice
        try:
            extradata["closedStateKey"]=status['values'][int(input('Enter the index number of close status field that you want to select:'))]
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        extradata["closedStateLabel"]=extradata["closedStateKey"]
        dynamicFieldDetailValue=[]
        fieldslist=["dynamicFieldDetailValue","tagTypeDefaultOptions","slaDateFieldOptions","lockedFields"]
        for fields in fieldslist:
            extradata[fields]=[]
            if fields=="dynamicFieldDetailValue":
                for i in range(len(cherwellmakerequest_connector_populate[fields])):
                    try:
                        a=input(f'Please enter a value for {cherwellmakerequest_connector_populate[fields][i]["label"]}')
                    except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
                    dynamicFieldDetailValue.append({"displayValue":cherwellmakerequest_connector_populate[fields][i]['label'],"value":a,"key":cherwellmakerequest_connector_populate[fields][i]["fieldValue"]})
            elif fields=="lockedFields":
                for i in range(len(cherwellmakerequest_connector_populate[fields])):
                    print(f'{i}-{cherwellmakerequest_connector_populate[fields][i]}')
                lockedfieldchoice=[]
                try:
                    temp=input('Please enter the locked fields you want seperated by commas').split(',')
                except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
                for i in temp:
                    lockedfieldchoice.append(cherwellmakerequest_connector_populate[fields][int(i)]['value'])
                extradata[fields]=lockedfieldchoice
            else:
                for i in range(len(cherwellmakerequest_connector_populate[fields])):
                    print(f"Index Number - {i} - {cherwellmakerequest_connector_populate[fields][i]['displayValue']}")
                try:
                    extradata[fields]=cherwellmakerequest_connector_populate[fields][int(input(f'Please enter the index number for {fields}:'))]
                except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()


        postconnectorbody={
                "name": cw_name,
                "type": Connectors.Type.CHERWELL,
                "schedule": {
                    "enabled": True,
                    "type": "DAILY",
                    "hourOfDay": 0
                },
                "attributes": {
                    "username": cw_username,
                    "password": cw_password,
                    "clientIdKey": clientid_key
                },
                "connection": {
                    "url": cw_url
                },
                "connectorField": {
                    "type": Connectors.Type.CHERWELL,
                    "clientIdKey": clientid_key,
                    "ticketType": {
                        "displayValue": "Change Request",
                        "value": "ChangeRequest"
                    },
                    "descriptionFields": enabled
                    ,
                    "dynamicDropdownFields": dynamicdropdown,
                    "dynamicFieldDetailValue": dynamicFieldDetailValue,
                    "optionalMandatoryFieldDetailValue": [],
                    "lockedFields": lockedfieldchoice,
                    "slaDateField":extradata["slaDateFieldOptions"]["displayValue"],"tagTypeDefaultValue":extradata["tagTypeDefaultOptions"]["displayValue"],
                    "connectorSettings": {
                        "closeFindingsOnTicketCloseEnabled": False,
                        "closeStatusesOfTicketToUpdate": ','.join(extradata['closeStatusesOfTicketToUpdate']),
                        "closeTicketOnFindingsCloseEnabled": False,
                        "closedStateKey":(extradata['closedStateKey']),
                        "closedStateLabel": extradata['closedStateKey'],
                        "enabledTagRemoval": True,
                        "enabledUploadAttachment": True,
                        "initialState": ""
                    },
                    "usePluginInfoFields": [],
                    "isTagRemovalEnabled": True,
                    "isTicketingConnector": True,
                    "autoUrba": autourba
                }
            }
        connectorcreateurl=self.api_base_url.format(str(client_id))
        try:
            postconnectorcreate = self.request_handler.make_request(ApiRequestHandler.POST, connectorcreateurl, body=postconnectorbody)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        if postconnectorcreate.status_code == 201:
            populateitems_json = json.loads(postconnectorcreate.text)
            id=populateitems_json['id']
        
        return id

    def create_qualyspc(self, conn_name:str, conn_url:str, schedule_freq:str, network_id:int, username:str, password:str, auto_urba:bool=True, client_id:int=None, **kwargs):

        """
        Create a new qualys pc connector.

        :param conn_name:       The connector name.
        :type  conn_name:       str

        :param conn_url:        The URL for the connector to communicate with.
        :type  conn_url:        str

        :param schedule_freq:   The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                        Connectors.ScheduleFreq.WEEKLY,
                                                                        Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:   str

        :param network_id:      The network ID
        :type  network_id:      int

        :param username:      The username to use for connector authentication.
        :type  username:      str

        :param password:      The password to use for connector authentication.
        :type  password:      str

        :param auto_urba:       Automatically run URBA after connector runs?
        :type  auto_urba:       bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword ssl_cert:      Optional SSL certificate.
        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31
        :keyword reportnameprefix: Report Name Prefix

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            connector_id = self.create_scanning_connector(conn_name, Connectors.Type.QUALYS_PC, conn_url, schedule_freq, network_id,
                                       username, password, auto_urba, client_id, **kwargs)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        return connector_id            

    def create_hclappscan(self, conn_name:str, conn_url:str, schedule_freq:str, network_id:int,username:str, password:str, auto_urba:bool=True, client_id:int=None, **kwargs):

        """
        Create a new hcl appscan connector.

        :param conn_name:       The connector name.
        :type  conn_name:       str

        :param conn_url:        The URL for the connector to communicate with.
        :type  conn_url:        str

        :param schedule_freq:   The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                        Connectors.ScheduleFreq.WEEKLY,
                                                                        Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:   str

        :param network_id:      The network ID
        :type  network_id:      int

        :param username:      The username to use for connector authentication.
        :type  username:      str

        :param password:      The password to use for connector authentication.
        :type  password:      str

        :param auto_urba:       Automatically run URBA after connector runs?
        :type  auto_urba:       bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword ssl_cert:      Optional SSL certificate.
        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            connector_id = self.create_scanning_connector(conn_name, Connectors.Type.HCL_APPSCAN, conn_url, schedule_freq, network_id,
                                       username, password, auto_urba, client_id, **kwargs)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        return connector_id            

    def create_veracode(self, conn_name:str, conn_url:str, schedule_freq:str, network_id:int,access_key:str, secret_key:str, auto_urba:bool=True, client_id:int=None, **kwargs):

        """
        Create a new veracode connector.

        :param conn_name:       The connector name.
        :type  conn_name:       str

        :param conn_url:        The URL for the connector to communicate with.
        :type  conn_url:        str

        :param schedule_freq:   The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                        Connectors.ScheduleFreq.WEEKLY,
                                                                        Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:   str

        :param network_id:      The network ID
        :type  network_id:      int

        :param access_key:      The username to use for connector authentication.
        :type  access_key:      str

        :param secret_key:      The password to use for connector authentication.
        :type  secret_key:      str

        :param auto_urba:       Automatically run URBA after connector runs?
        :type  auto_urba:       bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword ssl_cert:      Optional SSL certificate.
        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31
        :keyword authmechanism: Auth mechanism


        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            connector_id = self.create_scanning_connector(conn_name, Connectors.Type.VERACODE, conn_url, schedule_freq, network_id,access_key, secret_key, auto_urba, client_id, **kwargs)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        return connector_id

    def create_sonar_cloud(self, conn_name:str, conn_url:str, schedule_freq:str, network_id:int,access_key:str, secret_key:str, auto_urba:bool=True, client_id:int=None, **kwargs):

        """
        Create a new sonar cloud connector.

        :param conn_name:       The connector name.
        :type  conn_name:       str

        :param conn_url:        The URL for the connector to communicate with.
        :type  conn_url:        str

        :param schedule_freq:   The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                        Connectors.ScheduleFreq.WEEKLY,
                                                                        Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:   str

        :param network_id:      The network ID
        :type  network_id:      int

        :param access_key:      The username to use for connector authentication.
        :type  access_key:      str

        :param secret_key:      The password to use for connector authentication.
        :type  secret_key:      str

        :param auto_urba:       Automatically run URBA after connector runs?
        :type  auto_urba:       bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword ssl_cert:      Optional SSL certificate.
        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            connector_id = self.create_scanning_connector(conn_name, Connectors.Type.SONAR_CLOUD, conn_url, schedule_freq, network_id,
                                       access_key, secret_key, auto_urba, client_id, **kwargs)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        return connector_id

    def create_nessus(self, conn_name:str, conn_url:str, schedule_freq:str, network_id:int,access_key:str, secret_key:str, auto_urba:bool=True, client_id:int=None, **kwargs):

        """
        Create a new Nessus connector.

        :param conn_name:       The connector name.
        :type  conn_name:       str

        :param conn_url:        The URL for the connector to communicate with.
        :type  conn_url:        str

        :param schedule_freq:   The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                        Connectors.ScheduleFreq.WEEKLY,
                                                                        Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:   str

        :param network_id:      The network ID
        :type  network_id:      int

        :param access_key:      The username to use for connector authentication.
        :type  access_key:      str

        :param secret_key:      The password to use for connector authentication.
        :type  secret_key:      str

        :param auto_urba:       Automatically run URBA after connector runs?
        :type  auto_urba:       bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword ssl_cert:      Optional SSL certificate.
        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            connector_id = self.create_scanning_connector(conn_name, Connectors.Type.NESSUS, conn_url, schedule_freq, network_id,
                                       access_key, secret_key, auto_urba, client_id, **kwargs)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        return connector_id

    def create_tenableio(self, conn_name:str, conn_url:str, schedule_freq:str, network_id:int,access_key:str, secret_key:str, auto_urba:bool=True,client_id:int=None, **kwargs):

        """
        Create a new tenable io connector.

        :param conn_name:       The connector name.
        :type  conn_name:       str

        :param conn_url:        The URL for the connector to communicate with.
        :type  conn_url:        str

        :param schedule_freq:   The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                        Connectors.ScheduleFreq.WEEKLY,
                                                                        Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:   str

        :param network_id:      The network ID
        :type  network_id:      int

        :param access_key:      The username to use for connector authentication.
        :type  access_key:      str

        :param secret_key:      The password to use for connector authentication.
        :type  secret_key:      str

        :param auto_urba:       Automatically run URBA after connector runs?
        :type  auto_urba:       bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword ssl_cert:      Optional SSL certificate.
        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            connector_id = self.create_scanning_connector(conn_name, Connectors.Type.NESSUS, conn_url, schedule_freq, network_id,
                                       access_key, secret_key, auto_urba, client_id, **kwargs)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        return connector_id

    def create_awsinspector(self, conn_name:str, conn_url:str, schedule_freq:str, network_id:int,username:str, password:str, auto_urba:bool=True, client_id:int=None,**kwargs):

        """
        Create a new aws inspector connector.

        :param conn_name:       The connector name.
        :type  conn_name:       str

        :param conn_url:        The URL for the connector to communicate with.
        :type  conn_url:        str

        :param schedule_freq:   The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                        Connectors.ScheduleFreq.WEEKLY,
                                                                        Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:   str

        :param network_id:      The network ID
        :type  network_id:      int

        :param username:      The username to use for connector authentication.
        :type  username:      str

        :param password:      The password to use for connector authentication.
        :type  password:      str

        :param auto_urba:       Automatically run URBA after connector runs?
        :type  auto_urba:       bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword ssl_cert:      Optional SSL certificate.
        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

        awsinspector={"username":username,"password":password,"url":conn_url,"name":conn_name,"type": Connectors.Type.AWSINSPECTOR,"projection":"internal"}

        print(type(awsinspector))
        print(awsinspector)
        populatedate=self.connector_populate(body=awsinspector)
        choice=[]

        print("[+] These are the available templates for aws inspector\n")
        print(len(populatedate))
        for ind in range(len(populatedate['templates'])):
            print(f"Index Number - {ind} - {populatedate['templates'][ind]['displayValue']}")
            print()
        try:
            temp=input('Please enter the templates seperated by commas').split(',')
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        templatevalues=','.join(populatedate['templates'][int(x)]['value'] for x in temp)
        print(templatevalues)

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            connector_id = self.create_scanning_connector(conn_name, Connectors.Type.AWSINSPECTOR, conn_url, schedule_freq, network_id,
                                       username,password,auto_urba, client_id,template=templatevalues,**kwargs)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        return connector_id
    
    def create_burpsuite(self, conn_name:str, conn_url:str, schedule_freq:str, network_id:int,username:str, apikey:str, auto_urba:bool=True, client_id:int=None, **kwargs):

        """
        Create a new burpsuite connector.

        :param conn_name:       The connector name.
        :type  conn_name:       str

        :param conn_url:        The URL for the connector to communicate with.
        :type  conn_url:        str

        :param schedule_freq:   The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                        Connectors.ScheduleFreq.WEEKLY,
                                                                        Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:   str

        :param network_id:      The network ID
        :type  network_id:      int

        :param username:      The username to use for connector authentication.
        :type  username:      str

        :param apikey:      The password to use for connector authentication.
        :type  apikey:      str

        :param auto_urba:       Automatically run URBA after connector runs?
        :type  auto_urba:       bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword ssl_cert:      Optional SSL certificate.
        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            connector_id = self.create_scanning_connector(conn_name, Connectors.Type.BURPSUITE, conn_url, schedule_freq, network_id,
                                       username,apikey, auto_urba, client_id, **kwargs)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        return connector_id
    
    def create_crowdstrike(self, conn_name:str, conn_url:str, schedule_freq:str, network_id:int,username:str, password:str, auto_urba:bool=True, client_id:int=None, **kwargs):
        """
        Create a new crowdstrike connector.

        :param conn_name:       The connector name.
        :type  conn_name:       str

        :param conn_url:        The URL for the connector to communicate with.
        :type  conn_url:        str

        :param schedule_freq:   The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                        Connectors.ScheduleFreq.WEEKLY,
                                                                        Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:   str

        :param network_id:      The network ID
        :type  network_id:      int

        :param username:      The username to use for connector authentication.
        :type  username:      str

        :param password:      The password to use for connector authentication.
        :type  password:      str

        :param auto_urba:       Automatically run URBA after connector runs?
        :type  auto_urba:       bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword ssl_cert:      Optional SSL certificate.
        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31

        :return:    The connector ID from the platform is returned.
        :rtype:     int


        :raises RequestFailed:
        :raises ValueError:
        """

    
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            connector_id = self.create_scanning_connector(conn_name, Connectors.Type.CROWDSTRIKE, conn_url, schedule_freq,
                                       network_id, username, password, auto_urba, client_id, **kwargs)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        return connector_id

    def create_snow_customtableconfig(self, conn_name:str, conn_url:str,
                           username:str, password:str,tablename:str,statusfield:str,ticketidfield:str,enabletagremoval:bool=False,enableuploadattachment:bool=True, client_id:int=None, **kwargs):
        """
        Create a new snow custom table configuration connector.

        :param conn_name:                  The connector name.
        :type  conn_name:                  str

        :param conn_url:                   The URL for the connector to communicate with.
        :type  conn_url:                   str

        :param username:                   The username to use for connector authentication.
        :type  username:                   str

        :param password:                   The password to use for connector authentication.
        :type  password:                   str

        :param tablename:                  Name of the table.
        :type  tablename:                   str

        :param statusfield:                The status field.
        :type  statusfield:                str

        :param ticketidfield:             Ticket id field.
        :type  ticketidfield:             str

        :param enabletagremoval:          Enable tag removal switch
        :type  enabletagremoval:          bool

        :param enableuploadattachment:    Enable upload attachment switch
        :type  enableuploadattachment:    bool

        :param client_id:                 Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:                 int

        :return:                          The connector ID from the platform is returned.
        :rtype:                           int

        :raises RequestFailed:
        :raises ValueError:
        """
        descriptiondropdownbody={"type":Connectors.Type.SERVICENOW_CTC,"username":username,"password":password,"url":conn_url,"projection":"internal"}
        connect_populate=self.connector_populate(descriptiondropdownbody)
        descriptiondropdown=[]
        tablefields=[]
        if client_id is None:
                client_id = self._use_default_client_id()[0]
        for index in range(len(connect_populate["descriptionFieldDropDownOptions"])):
            print(f"Index Number - {index} - {connect_populate['descriptionFieldDropDownOptions'][index]['value']}:")
        try:
            temp=input('Please provide description field drop down index number seperated by comma: ').split(',')
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        for x in temp:
            try:
                data=input(f'Please enter the value for {connect_populate["descriptionFieldDropDownOptions"][int(x)]["value"]}')
            except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            descriptiondropdown.append({"descriptionField":connect_populate["descriptionFieldDropDownOptions"][int(x)]["value"],"tableField":data})
        while(True):
            try:
                tablefields.append({"key":input('Please provide a table field:'),"value":
                input('Please provide value')})
                yesorno=input('Would you like to exit: yes or no:')
                print()
                if yesorno.lower()!='no':
                    break
            except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        postconnectorbody={
            "name": conn_name,
            "type": Connectors.Type.SERVICENOW_CTC,
            "schedule": {
                "enabled":True,
                "type": "DAILY",
                "hourOfDay": 0
            },
            "attributes": {
                "username": username,
                "password": password
            },
            "connection": {
                "url": conn_url
            },
            "connectorField": {
                "type": Connectors.Type.SERVICENOW_CTC,
                "tableName":tablename,
                "statusField":statusfield,
                "ticketIdField":ticketidfield,
                "enabledTagRemoval":enabletagremoval,
                "descriptionFieldToTableFields":descriptiondropdown,
                "tableFields":tablefields,
                "enabledUploadAttachment":enableuploadattachment
            }
        }
        connectorcreateurl=self.api_base_url.format(str(client_id))
        try:
            postconnectorcreate = self.request_handler.make_request(ApiRequestHandler.POST, connectorcreateurl, body=postconnectorbody)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        if postconnectorcreate.status_code == 201:
            connector_create_json = json.loads(postconnectorcreate.text)
            connector_id = connector_create_json['id']
        return connector_id

    def get_jira_project(self, username:str, password_or_api_token:str, jira_url:str, client_id:int=None):
        """
        Get JIRA Project

        :param username:                    JIRA username
        :type username:                     str

        :param password_or_api_token:       JIRA API Token/Password
        :type password_or_api_token:        str

        :param jira_url:                    JIRA Platform URL
        :type jira_url:                     str

        :param client_id:                   RS Client ID
        :type client_id:                    int

        :return project_name:               JIRA Project Name
        :rtype project_name:                str

        :return project_key:                JIRA Project Key
        :rtype project_key:                 str

        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/populate"
        connector_populate_body = {
            "type": Connectors.Type.JIRA,
            "username": username,
            "password": password_or_api_token,
            "url": jira_url,
            "projection": "internal"
        }	
        try:
            cred_authorize = self.request_handler.make_request(ApiRequestHandler.POST, url, body=connector_populate_body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()      
        if cred_authorize.status_code == 200:
            cred_authorize_json = json.loads(cred_authorize.text)
            print("[+] These are the available projects in the JIRA platform\n")
            for ind in range(len(cred_authorize_json['projects'])):
                print(f"Index Number - {ind} - {cred_authorize_json['projects'][ind]['displayValue']}")
            print()
            try:
                project_index = int(input('Enter the index number of project that you want to select: '))
            except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            project_name = cred_authorize_json['projects'][project_index]['displayValue']
            project_key = cred_authorize_json['projects'][project_index]['value']
            enabled=[]
            for index in range(len(cred_authorize_json["supportedDescriptionFields"])):
                print(f"Index Number - {index} - {cred_authorize_json['supportedDescriptionFields'][index]['value']}:")
                enabled.append({"key":cred_authorize_json['supportedDescriptionFields'][index]['value'],"enabled":False})
            try:
                temp=input('Please enter the supported description fields seperated by commas').split(',')
            except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            for i in temp:
                enabled[int(i)]['enabled']=True
        print()
        return project_name, project_key,enabled

    def get_jira_issuetype(self, username:str, password_or_api_token:str, jira_url:str, project_key:str, client_id:int=None):
        """
        Get JIRA Issue Type

        :param username:                    JIRA username
        :type username:                     str

        :param password_or_api_token:       JIRA API Token/Password
        :type password_or_api_token:        str

        :param jira_url:                    JIRA Platform URL
        :type jira_url:                     str

        :param project_key:                 JIRA Project Key
        :type project_key:                  str

        :param client_id:                   RS Client ID
        :type client_id:                    int

        :return issue_type_name:            JIRA Issue Type Name
        :rtype issue_type_name:             str

        :return issue_type_key:             JIRA Issue Type Key
        :rtype issue_type_key:              str

        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + f"/populate/project/{project_key}/issueType"

        connector_populate_body = {
            "type": Connectors.Type.JIRA,
            "username": username,
            "password": password_or_api_token,
            "url": jira_url,
            "projection": "internal"
        }
        try:
            issue_type = self.request_handler.make_request(ApiRequestHandler.POST, url, body=connector_populate_body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()            

        if issue_type.status_code == 200:
            issue_type_json = json.loads(issue_type.text)
            print("[+] These are the available issue type for this project\n")
            for ind in range(len(issue_type_json['issueTypes'])):
                print(f"Index Number - {ind} - {issue_type_json['issueTypes'][ind]['displayValue']}")
            print()
            try:
                issue_type_index = int(input('Enter the index number of issue type that you want to select: '))
            except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            issue_type_name = issue_type_json['issueTypes'][issue_type_index]['displayValue']
            issue_type_key = issue_type_json['issueTypes'][issue_type_index]['value']
        print()
        return issue_type_name, issue_type_key

    def get_jira_issuetypefields(self, username:str, password_or_api_token:str, jira_url:str, project_key:str,issuetypeid:str, client_id:int=None):
        """
        Get JIRA Issue Type

        :param username:                    JIRA username
        :type username:                     str

        :param password_or_api_token:       JIRA API Token/Password
        :type password_or_api_token:        str

        :param jira_url:                    JIRA Platform URL
        :type jira_url:                     str

        :param project_key:                 JIRA Project Key
        :type project_key:                  str

        :param issuetypeid:                 JIRA Issue type id
        :type issuetypeid:                  str

        :param client_id:                   RS Client ID
        :type client_id:                    int

        :return issue_type_name:            JIRA Issue Type Name
        :rtype issue_type_name:             str

        :return issue_type_key:             JIRA Issue Type Key
        :rtype issue_type_key:              str

        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + f"/populate/project/{project_key}/issueType/{issuetypeid}"

        connector_populate_body = {
            "type": Connectors.Type.JIRA,
            "username": username,
            "password": password_or_api_token,
            "url": jira_url,
            "projection": "internal"
        }
        try:
            issue_type = self.request_handler.make_request(ApiRequestHandler.POST, url, body=connector_populate_body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()            

        if issue_type.status_code == 200:
            issue_type_json = json.loads(issue_type.text)
            print("[+] These are the available issue type for this project\n")
            for ind in range(len(issue_type_json['issueTypes'])):
                print(f"Index Number - {ind} - {issue_type_json['issueTypes'][ind]['displayValue']}")
            print()
            try:
                issue_type_index = int(input('Enter the index number of issue type that you want to select: '))
            except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            issue_type_name = issue_type_json['issueTypes'][issue_type_index]['displayValue']
            issue_type_key = issue_type_json['issueTypes'][issue_type_index]['value']
        print()
        return issue_type_name, issue_type_key

    def get_jira_tagtype_ticketstatus(self, username:str, password_or_api_token:str, jira_url:str, project_key:str, issue_type_key:str, client_id:int=None):
        """
        Get JIRA Tag Type and Ticket Status options

        :param username:                    JIRA username
        :type username:                     str

        :param password_or_api_token:       JIRA API Token/Password
        :type password_or_api_token:        str

        :param jira_url:                    JIRA Platform URL
        :type jira_url:                     str

        :param project_key:                 JIRA Project Key
        :type project_key:                  str

        :param issue_type_key:              JIRA Issue Type Key
        :type issue_type_key:               str

        :param client_id:                   RS Client ID
        :type client_id:                    int

        :return tag_type_name:              JIRA Issue Type Name
        :rtype tag_type_name:               str

        :return closed_status_value:        JIRA Closed status name
        :rtype closed_status_value:         str

        :return closed_status_key:          JIRA Closed status Key
        :rtype closed_status_key:           str

        :return ticket_sync_string:         JIRA Ticket sync string
        :rtype ticket_sync_string:          str

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + f"/populate/project/{project_key}/issueType/{issue_type_key}"

        connector_populate_body = {
            "type": Connectors.Type.JIRA,
            "username": username,
            "password": password_or_api_token,
            "url": jira_url,
            "projection": "internal"
        }	

        try:
            connector_fill = self.request_handler.make_request(ApiRequestHandler.POST, url, body=connector_populate_body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()           

        if connector_fill.status_code == 200:
            connector_fill_json = json.loads(connector_fill.text)
            print("[+] These are the available tag type in the RS platform\n")
            for ind in range(len(connector_fill_json['tagTypeDefaultOptions'])):
                print(f"Index Number - {ind} - {connector_fill_json['tagTypeDefaultOptions'][ind]['displayValue']}")
            print()
            try:
                tag_type_index = int(input('Enter the index number of tag type that you want to select: '))
            except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            tag_type_name = connector_fill_json['tagTypeDefaultOptions'][tag_type_index]['displayValue']
            print()
            print("[+] These are the available ticket status options for this project\n")
            ticket_sync_status = []
            for ind in range(len(connector_fill_json['connectorSettings']['statusOptions'])):
                ticket_sync_status.append(connector_fill_json['connectorSettings']['statusOptions'][ind]['displayValue'])
                print(f"Index Number - {ind} - {connector_fill_json['connectorSettings']['statusOptions'][ind]['displayValue']}")
            print()
            try:
                closed_status_index = int(input('Enter the index number of ticket closed status that you want to select: '))
            except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            closed_status_value = connector_fill_json['connectorSettings']['statusOptions'][closed_status_index]['displayValue']
            closed_status_key = connector_fill_json['connectorSettings']['statusOptions'][closed_status_index]['value']
            ticket_sync_status.remove(closed_status_value)
            ticket_sync_string = ",".join(ticket_sync_status)
        print()
        return tag_type_name, closed_status_value, closed_status_key, ticket_sync_string

    def create_jira_connector(self, jira_connector_name:str, username:str, password_or_api_token:str, jira_url:str, project_name:str, project_key:str, issue_type_name:str, issue_type_key:str, tag_type_name:str, closed_status_key:str, closed_status_value:str, ticket_sync_string:str,supporteddescription:list, client_id:int=None):
        """
        Create a JIRA Connector

        :param jira_connector_name:         JIRA Connector Name
        :type jira_connector_name:          str

        :param username:                    JIRA username
        :type username:                     str

        :param password_or_api_token:       JIRA API Token/Password
        :type password_or_api_token:        str

        :param jira_url:                    JIRA Platform URL
        :type jira_url:                     str

        :param project_name:                JIRA Project Name
        :type project_name:                 str

        :param project_key:                 JIRA Project Key
        :type project_key:                  str

        :param issue_type_name:             JIRA Issue Type Name
        :type issue_type_name:              str

        :param issue_type_key:              JIRA Issue Type Key
        :type issue_type_key:               str

        :param client_id:                   RS Client ID
        :type client_id:                    int

        :param tag_type_name:               JIRA Issue Type Name
        :type tag_type_name:                str

        :param closed_status_value:         JIRA Closed status name
        :type closed_status_value:          str

        :param closed_status_key:           JIRA Closed status Key
        :type closed_status_key:            str

        :param ticket_sync_string:          JIRA Ticket sync string
        :type ticket_sync_string:           str

        :param supporteddescription:        Supported description
        :type supporteddescription:         list

        :return connector_id:               Created JIRA connector ID
        :rtype connector_id:                int

        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))

        connector_creation_body = {
                "name": jira_connector_name,
                "type": Connectors.Type.JIRA,
                "schedule": {
                    "enabled": True,
                    "type": "DAILY",
                    "hourOfDay": 0
                },
                "attributes": {
                    "username": username,
                    "password": password_or_api_token
                },
                "connection": {
                    "url": jira_url
                },
                "connectorField": {
                    "type": Connectors.Type.JIRA,
                    "project": {
                        "displayValue": project_name,
                        "value": project_key
                    },
                    "issueType": {
                        "displayValue": issue_type_name,
                        "value": issue_type_key
                    },
                    "descriptionFields": supporteddescription,
                    "dynamicFields": [
                        {
                            "key": "priority",
                            "value": "10000",
                            "displayValue": "NoPrio"
                        },
                        {
                            "key": "summary",
                            "value": "",
                            "displayValue": ""
                        }
                    ],
                    "tagSyncField": "",
                    "slaDateField": "",
                    "tagTypeDefaultValue": tag_type_name,
                    "usePluginInfoFields": [
                        "summary",
                        "description"
                    ],
                    "lockedFields": [],
                    "connectorSettings": {
                        "initialState": "",
                        "enabledTagRemoval": False,
                        "closeFindingsOnTicketCloseEnabled": False,
                        "closeTicketOnFindingsCloseEnabled": True,
                        "closedStateKey": closed_status_key,
                        "closedStateLabel": closed_status_value,
                        "enabledUploadAttachment": True,
                        "closeStatusesOfTicketToUpdate": ticket_sync_string
                    }
                }
            }
        try:
            connector_create = self.request_handler.make_request(ApiRequestHandler.POST, url, body=connector_creation_body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        if connector_create.status_code == 201:
            connector_create_json = json.loads(connector_create.text)
            connector_id = connector_create_json['id']

        return connector_id

    def get_snow_fields(self, snow_username:str, snow_password_or_token:str, snow_url:str, client_id:int=None):
        """
        Get Service Now Incident type connector Fields

        :param snow_username:                    Service Now username
        :type snow_username:                     str

        :param snow_password_or_token:       Service Now API Token/Password
        :type snow_password_or_token:        str

        :param snow_url:                    Service Now Platform URL
        :type snow_url:                     str

        :param client_id:                   RS Client ID
        :type client_id:                    int

        :return tag_type_name:              Service Now Issue Type Name
        :rtype tag_type_name:               str

        :return closed_status_value:        Service Now Closed status name
        :rtype closed_status_value:         str

        :return closed_status_key:          Service Now Closed status Key
        :rtype closed_status_key:           str

        :return ticket_sync_string:         Service Now Ticket sync string
        :rtype ticket_sync_string:          str

        :return enabled:         Support description fields enabled
        :rtype enabled:          list



        """      

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/populate"

        connector_populate_body = {
            "type": Connectors.Type.SERVICENOW_INCIDENT,
            "username": snow_username,
            "password": snow_password_or_token,
            "url": snow_url,
            "projection": "internal"
        }	
        try:
            cred_authorize = self.request_handler.make_request(ApiRequestHandler.POST, url, body=connector_populate_body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()    

        if cred_authorize.status_code == 200:
            cred_authorize_json = json.loads(cred_authorize.text)
            print("[+] These are the available tag type in the RS platform\n")
            for ind in range(len(cred_authorize_json['tagTypeFieldOptions'])):
                print(f"Index Number - {ind} - {cred_authorize_json['tagTypeFieldOptions'][ind]['displayValue']}")
            print()
            try:			
                tag_type_index = int(input('Enter the index number of tag type that you want to select: '))
            except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            tag_type_name = cred_authorize_json['tagTypeFieldOptions'][tag_type_index]['displayValue']
            print()
            print("[+] These are the available ticket status options for this project\n")
            ticket_sync_status = []
            for ind in range(len(cred_authorize_json['connectorSettings']['statusOptions'])):
                ticket_sync_status.append(cred_authorize_json['connectorSettings']['statusOptions'][ind]['displayValue'])
                print(f"Index Number - {ind} - {cred_authorize_json['connectorSettings']['statusOptions'][ind]['displayValue']}")
            print()
            try:
                closed_status_index = int(input('Enter the index number of ticket closed status that you want to select: '))
            except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            enabled=[]
            for ind in range(len(cred_authorize_json['supportedDescriptionFields'])):
                print(f"Index Number - {ind} - {cred_authorize_json['supportedDescriptionFields'][ind]['displayValue']}")
                print()
                enabled.append({"key":cred_authorize_json['supportedDescriptionFields'][ind]['value'],"enabled":False})
            try:
                temp=input('Please enter the supported description fields seperated by commas: ').split(',')
            except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            for i in temp:
                enabled[int(i)]['enabled']=True
            closed_status_value = cred_authorize_json['connectorSettings']['statusOptions'][closed_status_index]['displayValue']
            closed_status_key = cred_authorize_json['connectorSettings']['statusOptions'][closed_status_index]['value']
            ticket_sync_status.remove(closed_status_value)
            ticket_sync_string = ",".join(ticket_sync_status)	
        print()

        return tag_type_name, closed_status_value, closed_status_key, ticket_sync_string,enabled

    def get_snow_catalog(self, snow_username:str, snow_password_or_token:str, snow_url:str, client_id:int=None):
        """
        Get Service Now connector data

        :param snow_username:                   Service Now username
        :type snow_username:                    str

        :param snow_password_or_token:          Service Now API Token/Password
        :type snow_password_or_token:           str

        :param snow_url:                        Service Now Platform URL
        :type snow_url:                         str

        :param client_id:                       RS Client ID
        :type client_id:                        int

        :return populatedata:                   Catalog,category,item information,close status key etc in populate data 
        :rtype populatedata:                    dict

        """      

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        populateddata={}
        url = self.api_base_url.format(str(client_id)) + "/populate"

        connector_populate_body = {
            "type": Connectors.Type.SERVICENOW_SERVICEREQUEST,
            "username": snow_username,
            "password": snow_password_or_token,
            "url": snow_url,
            "projection": "internal"
        }		

        try:
            cred_authorize = self.request_handler.make_request(ApiRequestHandler.POST, url, body=connector_populate_body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()    

        if cred_authorize.status_code == 200:
            cred_authorize_json = json.loads(cred_authorize.text)
            print("[+] These are the available catalogs for this connector\n")
            for ind in range(len(cred_authorize_json['catalogs'])):
                print(f"Index Number - {ind} - {cred_authorize_json['catalogs'][ind]['displayValue']}")
            print()	
            try:			
                 catalog_index = int(input('Enter the index number of catalog that you want to select: '))
            except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            catalog_name = cred_authorize_json['catalogs'][catalog_index]['displayValue']
            catalog_value = cred_authorize_json['catalogs'][catalog_index]['value']
        categoryurl=url+f'/catalog/{catalog_value}/category'
        try:
            category_check = self.request_handler.make_request(ApiRequestHandler.POST, categoryurl, body=connector_populate_body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()  

        if category_check.status_code == 200:
            category_check_json = json.loads(category_check.text)
            if len(category_check_json['categories'])==0:
                print('Cannot retrieve category please choose another catalog,Exiting..')
                exit()	
            else:
                print("[+] These are the available categories for this catalog\n")
                for ind in range(len(category_check_json['categories'])):
                    
                    print(f"Index Number - {ind} - {category_check_json['categories'][ind]['displayValue']}")
                try:
                    categorynumber=int(input('These are the number'))
                except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
                category_name=category_check_json['categories'][categorynumber]['displayValue']
                category_value=category_check_json['categories'][categorynumber]['value']
        catalogitemurl=url+f'/catalog/{catalog_value}/category/{category_value}/item'
        try:
            catalogitem_check = self.request_handler.make_request(ApiRequestHandler.POST, catalogitemurl, body=connector_populate_body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        if catalogitem_check.status_code == 200:
            catalogitemcheck_json = json.loads(catalogitem_check.text)
            if len(catalogitemcheck_json['catalogItems'])==0:
                print('Cannot retrieve item please choose another category,Exiting..')
                exit()	
            else:
                print("[+] These are the available catalog items for this catalog\n")
                for ind in range(len(catalogitemcheck_json['catalogItems'])):
                    
                    print(f"Index Number - {ind} - {catalogitemcheck_json['catalogItems'][ind]['displayValue']}")
                try:
                    catalogitemnumber=int(input('These are the numbers:'))
                except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
                catalogitem_name=catalogitemcheck_json['catalogItems'][catalogitemnumber]['displayValue']
                catalogitem_value=catalogitemcheck_json['catalogItems'][catalogitemnumber]['value']
        catalogitemurl=url+f'/catalog/{catalog_value}/category/{category_value}/item/{catalogitem_value}'
        try:
            ticketstatus = self.request_handler.make_request(ApiRequestHandler.POST, catalogitemurl, body=connector_populate_body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit() 
        if ticketstatus.status_code == 200:
            ticketstatus = json.loads(ticketstatus.text)
        ticketsyncstatus=[]
        print("[+] Please choose your options for ticket sync status\n")
        for ind in range(len(ticketstatus['connectorSettings']['statusOptions'])):
            print(f"Index Number - {ind} - {ticketstatus['connectorSettings']['statusOptions'][ind]['displayValue']}")
            print()
        try:
            temp=input('Please provide ticket sync status index numbers by seperating them in commas').split(',')
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        ticketsyncstatus=','.join([ticketstatus['connectorSettings']['statusOptions'][int(choice)]['displayValue'] for choice in temp])
        print("[+] Please choose your option for Close state\n")
        for ind in range(len(ticketstatus['connectorSettings']['statusOptions'])):
            print(f"Index Number - {ind} - {ticketstatus['connectorSettings']['statusOptions'][ind]['displayValue']}")
            print()
        try:
            closestate=int(input('Enter the index number of ticket sync status that you want to select: ')) 
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        closestatelabel=ticketstatus['connectorSettings']['statusOptions'][closestate]['displayValue']
        closestatekey=ticketstatus['connectorSettings']['statusOptions'][closestate]['value']
    
        populateddata['catalog_name']=catalog_name
        populateddata['catalog_value']=catalog_value
        populateddata['category_name']=category_name
        populateddata['category_value']=category_value
        populateddata['catalogitem_name']=catalogitem_name
        populateddata['catalogitem_value']=catalogitem_value
        populateddata['ticket_sync_states']=ticketsyncstatus
        populateddata['close_state']=closestatelabel
        populateddata['close_state_key']=closestatekey
        return populateddata

    def get_cherwell_makerequestdata(self, snow_username:str, snow_password_or_token:str, snow_url:str, client_id:int=None):
        """
        Get cherwell make request data

        :param snow_username:                   Service Now username
        :type snow_username:                    str

        :param snow_password_or_token:          Service Now API Token/Password
        :type snow_password_or_token:           str

        :param snow_url:                        Service Now Platform URL
        :type snow_url:                         str

        :param client_id:                       RS Client ID
        :type client_id:                        int

        :return populatedata:                   Catalog,category,item information etc in populate data 
        :rtype populatedata:                    dict

        """      

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        populateddata={}
        url = self.api_base_url.format(str(client_id)) + "/populate/ticketType/ChangeRequest/fieldvalueslookup"

        connector_populate_body = {
            "type": Connectors.Type.SERVICENOW_SERVICEREQUEST,
            "username": snow_username,
            "password": snow_password_or_token,
            "url": snow_url,
            "projection": "internal"
        }		

        try:
            cred_authorize = self.request_handler.make_request(ApiRequestHandler.POST, url, body=connector_populate_body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()    

        if cred_authorize.status_code == 200:
            cred_authorize_json = json.loads(cred_authorize.text)
            print("[+] These are the available catalogs for this connector\n")
            for ind in range(len(cred_authorize_json['catalogs'])):
                print(f"Index Number - {ind} - {cred_authorize_json['catalogs'][ind]['displayValue']}")
            print()
            try:		
                catalog_index = int(input('Enter the index number of catalog that you want to select: '))
            except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            catalog_name = cred_authorize_json['catalogs'][catalog_index]['displayValue']
            catalog_value = cred_authorize_json['catalogs'][catalog_index]['value']
        categoryurl=url+f'/catalog/{catalog_value}/category'
        try:
            category_check = self.request_handler.make_request(ApiRequestHandler.POST, categoryurl, body=connector_populate_body)
            print(category_check)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()   

        if category_check.status_code == 200:
            category_check_json = json.loads(category_check.text)
            if len(category_check_json['categories'])==0:
                print('Cannot retrieve category please choose another catalog,Exiting..')
                exit()	
            else:
                print("[+] These are the available categories for this catalog\n")
                for ind in range(len(category_check_json['categories'])):
                    
                    print(f"Index Number - {ind} - {category_check_json['categories'][ind]['displayValue']}")
                try:
                    categorynumber=int(input('These are the number'))
                except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
                category_name=category_check_json['categories'][categorynumber]['displayValue']
                category_value=category_check_json['categories'][categorynumber]['value']
        catalogitemurl=url+f'/catalog/{catalog_value}/category/{category_value}/item'
        try:
            catalogitem_check = self.request_handler.make_request(ApiRequestHandler.POST, catalogitemurl, body=connector_populate_body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        if catalogitem_check.status_code == 200:
            catalogitemcheck_json = json.loads(catalogitem_check.text)
            print(catalogitemcheck_json)
            if len(catalogitemcheck_json['catalogItems'])==0:
                print('Cannot retrieve item please choose another category,Exiting..')
                exit()	
            else:
                print("[+] These are the available catalog items for this catalog\n")
                for ind in range(len(catalogitemcheck_json['catalogItems'])):
                    
                    print(f"Index Number - {ind} - {catalogitemcheck_json['catalogItems'][ind]['displayValue']}")
                try:
                    catalogitemnumber=int(input('These are the numbers:'))
                except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
                catalogitem_name=catalogitemcheck_json['catalogItems'][catalogitemnumber]['displayValue']
                catalogitem_value=catalogitemcheck_json['catalogItems'][catalogitemnumber]['value']
        populateddata['catalog_name']=catalog_name
        populateddata['catalog_value']=catalog_value
        populateddata['category_name']=category_name
        populateddata['category_value']=category_value
        populateddata['catalogitem_name']=catalogitem_name
        populateddata['catalogitem_value']=catalogitem_value
        return populateddata
    

    def populate_editform_cmdb(self, filters:list,client_id:int=None):
        """
        Populate editform cmdb data

        :param filters:                    Connector populate filters
        :type filters:                     list

        :param client_id:                   RS Client ID
        :type client_id:                    int

        :return jsonifieid response:        Jsonified response of editform populatedata
        :rtype  jsonifieid response:        dict

        """      

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/cmdb/field/editForm/populate"

        connector_populate_body = {
                  "filters": filters
                    }	

        try:
            cred_authorize = self.request_handler.make_request(ApiRequestHandler.POST, url, body=connector_populate_body)
            jsonified_response=json.loads(cred_authorize.text)
            for i in jsonified_response['fields']:
                for key,value in i.items():
                    if key!='isCurrentlySelected':
                        print(key,value)
                print()
            return jsonified_response
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

    def populate_lockform_cmdb(self, filters:str,client_id:int=None):
        """
        Populate lockform cmdb data

        :param filters:                    Connector populate filters
        :type filters:                     list

        :param client_id:                   RS Client ID
        :type client_id:                    int

        :return jsonifieid response:        Jsonified response of lockform populatedata
        :rtype  jsonifieid response:        dict

        """       

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/cmdb/field/lockForm/populate"

        connector_populate_body = {
                  "filters": filters
                    }	

        try:
            cred_authorize = self.request_handler.make_request(ApiRequestHandler.POST, url, body=connector_populate_body)
            jsonified_response=json.loads(cred_authorize.text)
            for i in jsonified_response['fields']:
                for key,value in i.items():
                    if key!='isCurrentlySelected':
                        print(key,value)
                print()
            return jsonified_response
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

    def list_cmdb_custom_fields(self,client_id:int=None):
        """
        Populate cmdb custom field data

        :param client_id:                   RS Client ID
        :type client_id:                    int

        :return jsonifieid response:        Jsonified response of editform populatedata
        :rtype  jsonifieid response:        dict

        """          

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/cmdb/customField/label"

        try:
            cred_authorize = self.request_handler.make_request(ApiRequestHandler.GET, url)
            jsonified_response=json.loads(cred_authorize.text)
            for i in jsonified_response:
                for key,value in i.items():
                    if key=='label' or key=='key':
                        print(key,value)
                print()
            return jsonified_response
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

    def add_cmdb_custom_fields(self,cmdbcustomfields:list,client_id:int=None):
        """
        Add cmdb custom fields data

        :param cmdbcustomfields:           Connector populate filters
        :type filters:                     list

        :param client_id:                   RS Client ID
        :type client_id:                    int

        :return jsonifieid response:        Jsonified response of editform populatedata
        :rtype  jsonifieid response:        dict

        """    
              

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/cmdb/customField/label"

        body=cmdbcustomfields

        try:
            success=True
            cred_authorize = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
            return success
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

    def get_multiplematches(self,subject:str,assetid:int,client_id:int=None):
        """
        Get list of assets that have multiple matches

        :param subject:                    Subject specified information of the asset id
        :type subject:                     str

        :param assetid:                     Asset id to check for multiple matches
        :type password_or_api_token:        int

        :param client_id:                   RS Client ID
        :type client_id:                    int

        :return jsonified response:         Jsonified response of multiple matches
        :rtype ticket_sync_string:          dict

        """      

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        asseturl = self.profile.platform_url+'/api/v1/client/{}/{}/{}/cmdb/multipleFound'.format(str(client_id),subject,assetid)

        try:
            cred_authorize = self.request_handler.make_request(ApiRequestHandler.GET, url=asseturl)
            return json.load(cred_authorize.text)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

    def get_multiplematches_connector(self,subject:str,assetid:int,connectorid:int,hostid:int,sysid:int,table:str,client_id:int=None):
        """
        Get list of multiple matches of cmdb data 

        :param subject:                    Subject specified information of the asset id
        :type subject:                     str

        :param assetid:                    Asset id to check for multiple matches
        :type assetid:                     int

        :param connectorid:                Connector id
        :type connectorid:                 int

        :param hostid:                     Host id
        :type  hostid:                     int

        :param sysid:                      Sys id
        :type  sysid:                      int

        :param table:                      Table information
        :type table:                       str

        :return json:                      Json data
        :rtype json:                       dict

        """      

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        asseturl = self.profile.platform_url+'/api/v1/client/{}/{}/{}/connector/{}/cmdb/mergeMultipleFound'.format(str(client_id),subject,assetid,connectorid)

        body={
            "hostId": hostid,
            "sysId": sysid,
            "table": table
            }

        try:
            cred_authorize = self.request_handler.make_request(ApiRequestHandler.POST, url=asseturl,body=body)
            return json.load(cred_authorize.text)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

    def create_asset_snowcmdb(self,subject:str,assetid:int,connectorid:int,client_id:int=None):
        """
        Create an asset in snow cmdb

        :param subject:                    Subject specified information of the asset id
        :type subject:                     str

        :param assetid:                    Asset id to check for multiple matches
        :type assetid:                     int

        :param connectorid:                Connector id
        :type connectorid:                 int

        :param client_id:                  RS Client ID,if none takes the default client id
        :type client_id:                   int

        :return json:                      Json data
        :rtype json:                       dict
        """      

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        asseturl = self.profile.platform_url+'/api/v1/client/{}/{}/{}/connector/{}/cmdb/createAsset'.format(str(client_id),subject,str(assetid),str(connectorid))
        try:
            cred_authorize = self.request_handler.make_request(ApiRequestHandler.GET, url=asseturl)
            return json.load(cred_authorize.text)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

    def sync_asset_snowcmdb(self,subject,assetid,connectorid,client_id=None):
        """
        Sync asset in snow cmdb

        :param subject:                    Subject specified information of the asset id
        :type subject:                     str

        :param assetid:                    Asset id to check for multiple matches
        :type assetid:                     int

        :param connectorid:                Connector id
        :type connectorid:                 int

        :param client_id:                  RS Client ID
        :type client_id:                   int

        :return json:                      Json data
        :rtype json:                       dict
        """    

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        asseturl = self.profile.platform_url+'/api/v1/client/{}/{}/{}/connector/{}/cmdb/syncSingleAsset'.format(str(client_id),subject,str(assetid),str(connectorid))
        try:
            cred_authorize = self.request_handler.make_request(ApiRequestHandler.GET, url=asseturl)
            return json.load(cred_authorize.text)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()


    def create_snow_connector(self, snow_connector_name:str, snow_username:str, snow_password_or_token:str, snow_url:str, tag_type_name:str, closed_status_value:str, closed_status_key:str, ticket_sync_string:str,supporteddescriptionfields:list,selected_optional_fields:list,client_id:int=None):
        """
        Create a Service Now Incident type Connector

        :param snow_connector_name:         JIRA Connector Name
        :type snow_connector_name:          str

        :param snow_username:                    JIRA username
        :type snow_username:                     str

        :param snow_password_or_api_token:       JIRA API Token/Password
        :type snow_password_or_api_token:        str

        :param snow_url:                    JIRA Platform URL
        :type snow_url:                     str

        :param client_id:                   RS Client ID
        :type client_id:                    int

        :param tag_type_name:               JIRA Issue Type Name
        :type tag_type_name:                str

        :param closed_status_value:         JIRA Closed status name
        :type closed_status_value:          str

        :param closed_status_key:           JIRA Closed status Key
        :type closed_status_key:            str

        :param ticket_sync_string:          JIRA Ticket sync string
        :type ticket_sync_string:           str

        :return connector_id:               Created JIRA connector ID
        :rtype connector_id:                int

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))    

        connector_creation_body = {
            "name": snow_connector_name,
            "type": Connectors.Type.SERVICENOW_INCIDENT,
            "schedule": {
                "enabled": True,
                "type": "DAILY",
                "hourOfDay": 0
            },
            "attributes": {
                "username":snow_username,
                "password": snow_password_or_token
            },
            "connection": {
                "url": snow_url
            },
            "connectorField": {
                "type": Connectors.Type.SERVICENOW_INCIDENT,
                "defaultTemplateId": "",
                "templates": [],
                "descriptionFields": supporteddescriptionfields,
                "selectedOptionalFields": selected_optional_fields,
                "defaultSupportedFieldValues": [
                    {
                        "key": "priority",
                        "value": "3",
                        "displayValue": "3 - Moderate"
                    },
                    {
                        "key": "urgency",
                        "value": "2",
                        "displayValue": "2 - Medium"
                    }
                ],
                "tagSyncField": "",
                "slaDateField": "due_date",
                "tagTypeDefaultValue": tag_type_name,
                "connectorSettings": {
                    "initialState": "",
                    "enabledTagRemoval": False,
                    "closeFindingsOnTicketCloseEnabled": False,
                    "closeTicketOnFindingsCloseEnabled": True,
                    "closedStateKey": closed_status_key,
                    "closedStateLabel": closed_status_value,
                    "enabledUploadAttachment": True,
                    "closeStatusesOfTicketToUpdate":ticket_sync_string
                },
                "usePluginInfoFields": [
                    "description",
                    "short_description"
                ]
            }
        }

        try:
            connector_create = self.request_handler.make_request(ApiRequestHandler.POST, url, body=connector_creation_body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        if connector_create.status_code == 201:
            connector_create_json = json.loads(connector_create.text)
            connector_id = connector_create_json['id']

        return connector_id

    def create_snow_service_connector(self, snow_connector_name:str, snow_username:str, snow_password_or_token:str, snow_url:str, ticket_description:str='false',client_id:int=None,):
        """
        Create a Service Now Service Request type Connector

        :param snow_connector_name:          SNOW Service type Connector Name
        :type snow_connector_name:           str

        :param snow_username:                SNOW username
        :type snow_username:                 str

        :param snow_password_or_token:       SNOW API Token/Password
        :type snow_password_or_token:        str

        :param snow_url:                     SNOW Platform URL
        :type snow_url:                      str

        :param ticket_description:           To provide ticket description or not,'true' to provide,'false' to not provide
        :type ticket_description:            str       

        :param client_id:                   RS Client ID
        :type client_id:                    int

        :return connector_id:               Created SNOW Service request connector ID
        :rtype connector_id:                int

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        enabled=[]
        if ticket_description.lower() == 'true':
            getticketdescriptionbody={"type":Connectors.Type.SERVICENOW_SERVICEREQUEST,"username":snow_username,"password":snow_password_or_token,"url":snow_url,"projection":"internal"}
            ticketdescriptionfields=self.connector_populate(getticketdescriptionbody)
            for ind in range(len(ticketdescriptionfields['supportedDescriptionFields'])):
                print(f"Index Number - {ind} - {ticketdescriptionfields['supportedDescriptionFields'][ind]['displayValue']}")
                print()
                enabled.append({"key":ticketdescriptionfields['supportedDescriptionFields'][ind]['value'],"enabled":False})
            try:
                temp=input('Please enter the supported description fields seperated by commas').split(',')
            except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            for i in temp:
                enabled[int(i)]['enabled']=True
        url = self.api_base_url.format(str(client_id))
        populateddata= self.get_snow_catalog(snow_username, snow_password_or_token, snow_url)
        connector_creation_body = {
            "name": snow_connector_name,
            "type": Connectors.Type.SERVICENOW_SERVICEREQUEST,
            "schedule": {
                "enabled": True,
                "type": "DAILY",
                "hourOfDay": 0
            },
            "attributes": {
                "username": snow_username,
                "password": snow_password_or_token
            },
            "connection": {
                "url": snow_url
            },
            "connectorField": {
                "type": "SNOW_SERVICE_REQUEST",
                "catalog": {
                    "displayValue": populateddata['catalog_name'],
                    "value": populateddata['catalog_value']
                },
                "category": {
                    "displayValue": populateddata['category_name'],
                    "value": populateddata['category_value']
                },
                "catalogItem": {
                    "displayValue": populateddata['catalogitem_name'],
                    "value": populateddata['catalogitem_value']
                },
                "dynamicFields": [],
                "descriptionFields": enabled,
                "defaultSupportedFieldValues": [],
                "tagSyncField": "",
                "lockedFields": [],
                "connectorSettings": {
                    "initialState": "",
                    "enabledTagRemoval": True,
                    "closeFindingsOnTicketCloseEnabled": False,
                    "closeTicketOnFindingsCloseEnabled": False,
                    "closedStateKey": populateddata['close_state_key'],
                    "closedStateLabel": populateddata['close_state'],
                    "enabledUploadAttachment": True,
                    "closeStatusesOfTicketToUpdate": populateddata['ticket_sync_states']
                }
            }
        }
        try:
            connector_create = self.request_handler.make_request(ApiRequestHandler.POST, url, body=connector_creation_body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        if connector_create.status_code == 201:
            connector_create_json = json.loads(connector_create.text)
            connector_id = connector_create_json['id']

        return connector_id


    def create_checkmarx_osa_connector(self, conn_name:str, conn_url:str, username:str, password:str, conn_status:str, schedule_freq:str, network_id:int, auto_urba:bool=True, client_id:int=None, **kwargs):
        """
        Create a new Checkmarx OSA scanning connector.

        :param conn_name:       The connector name.
        :type  conn_name:       str

        :param conn_url:        The URL for the connector to communicate with.
        :type  conn_url:        str

        :param username:        The username to use for connector authentication.
        :type  username:        str

        :param password:        The password to use for connector authentication.
        :type  password:        str

        :param conn_status:     Whether enabled or disabled 
        :type  conn_status:     bool

        :param schedule_freq:   The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                        Connectors.ScheduleFreq.WEEKLY,
                                                                        Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:   str

        :param network_id:      The network ID
        :type  network_id:      int

        :param auto_urba:       Automatically run URBA after connector runs?
        :type  auto_urba:       bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword ssl_cert:      Optional SSL certificate.
        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run, Type : Str, Available values : 1-7
        :keyword day_of_month:  The day of the month the connector should run, Type : Str, Available values : 1-31
        :keyword createAssetsIfZeroVulnFoundInFile: Create assets if zero vulnerability found in file. Type : Bool, Available values : True or False
        :keyword maxDaysToRetrieve: Max days to retrieve scan data. Type : Integer, Available values : 30,60,90,180,365

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0] 

        ssl_cert = kwargs.get('ssl_cert', None)
        hour_of_day = kwargs.get('hour_of_day', None)
        day_of_week = kwargs.get('day_of_week', None)
        day_of_month = kwargs.get('day_of_month', None)
        createAssetsIfZeroVulnFoundInFile = kwargs.get('createAssetsIfZeroVulnFoundInFile', None)
        maxDaysToRetrieve = kwargs.get('maxDaysToRetrieve', None)
        try:
            project_selection = input("Select \"ALL\" projects in checkmarx? Please enter 'y' if YES or enter 'n' if NO: ")
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        if project_selection == 'n':
            print("\n[+] As you selected No, these are the list of projects available in checkmarx:\n")
            populate_url = self.api_base_url.format(str(client_id)) + "/populate"
            connector_populate_body = {
                "type": Connectors.Type.CHECKMARX_OSA,
                "username": username,
                "password": password,
                "url": conn_url,
                "projection": "internal"
            }	
            try:
                cred_authorize = self.request_handler.make_request(ApiRequestHandler.POST, populate_url, body=connector_populate_body)
            except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()            

            if cred_authorize.status_code == 200:
                cred_authorize_json = json.loads(cred_authorize.text) 
                for ind in range(len(cred_authorize_json['projectList'])):
                    print(f"Index Number - {ind} - {cred_authorize_json['projectList'][ind]['displayValue']}")
                print()
                try:
                    project_indexes_list = list(map(int, input("Enter the index numbers of projects that you want to select. Enter index numbers as comma separated values if multiple projects need to be selected: ").split(",")))
                except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
                project_selected_list = []
                for value in project_indexes_list:
                    project_selected_list.append(cred_authorize_json['projectList'][value]['value'])
                project_selected_string = ",".join(project_selected_list)
                print(project_selected_string)
        elif project_selection == 'y':
            project_selected_string = "ALL"

        connector_create_url = self.api_base_url.format(str(client_id))

        if maxDaysToRetrieve is None:
            max_days = 30

        connector_create_body = {
            "type": Connectors.Type.CHECKMARX_OSA,
            "name": conn_name,
            "networkId": network_id,
            "connection": {
                "url": conn_url
            },
            "schedule": {
            },
            "attributes": {
                "username": username,
                "password": password,
                "maxDaysToRetrieve": max_days,
                "enableFortifyToPullFPRIntegratedFile": True,
                "checkmarxChosenProjectListToPull": project_selected_string,
                "findingTypeTobePulled": [
                    "vulnerabilities",
                    "licenses"
                ]
            },
            "autoUrba": auto_urba
        }

        if ssl_cert is not None:
            connector_create_body['connection'].update(sslCertificates=ssl_cert)

        if schedule_freq == Connectors.ScheduleFreq.DAILY:

            if hour_of_day is None:
                hour_of_day = 0

            connector_schedule = {
                "enabled": conn_status,
                "type": schedule_freq,
                "hourOfDay": hour_of_day,
                "daysOfWeek": "1",
                "daysOfMonth": "1",
                "cronSchdule":None
            }

        elif schedule_freq == Connectors.ScheduleFreq.WEEKLY:

            if day_of_week is None:
                day_of_week = "1"

            if hour_of_day is None:
                hour_of_day = 0

            connector_schedule = {
                "enabled": conn_status,
                "type": schedule_freq,
                "hourOfDay": hour_of_day,
                "daysOfWeek": day_of_week,
                "daysOfMonth": "1",
                "cronSchdule":None
            }

        elif schedule_freq == Connectors.ScheduleFreq.MONTHLY:

            if day_of_month is None:
                day_of_month = "1"

            if hour_of_day is None:
                hour_of_day = 0

            connector_schedule = {
                "enabled": conn_status,
                "type": schedule_freq,
                "hourOfDay": hour_of_day,
                "daysOfWeek": "1",
                "daysOfMonth": day_of_month,
                "cronSchdule":None
            }

        else:
            raise ValueError("Schedule freq. should be DAILY, WEEKLY, or MONTHLY.")

        connector_create_body.update(schedule=connector_schedule)

        if createAssetsIfZeroVulnFoundInFile is None:
            create_asset = True
        
        connector_create_body['attributes'].update(createAssetsIfZeroVulnFoundInFile=create_asset)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, connector_create_url, body=connector_create_body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id        

    def create_checkmarx_sast_connector(self, conn_name:str, conn_url:str, username:str, password:str, conn_status:str, schedule_freq:str, network_id:int, auto_urba:bool=True, client_id:int=None, **kwargs):
        """
        Create a new Checkmarx SAST scanning connector.

        :param conn_name:       The connector name.
        :type  conn_name:       str

        :param conn_url:        The URL for the connector to communicate with.
        :type  conn_url:        str

        :param username:        The username to use for connector authentication.
        :type  username:        str

        :param password:        The password to use for connector authentication.
        :type  password:        str

        :param conn_status:     Whether enabled or disabled 
        :type  conn_status:     bool

        :param schedule_freq:   The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                        Connectors.ScheduleFreq.WEEKLY,
                                                                        Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:   str

        :param network_id:      The network ID
        :type  network_id:      int

        :param auto_urba:       Automatically run URBA after connector runs?
        :type  auto_urba:       bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword ssl_cert:      Optional SSL certificate.
        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run, Type : Str, Available values : 1-7
        :keyword day_of_month:  The day of the month the connector should run, Type : Str, Available values : 1-31
        :keyword createAssetsIfZeroVulnFoundInFile: Create assets if zero vulnerability found in file. Type : Bool, Available values : True or False
        :keyword generateShortDescription: Generate Short Description. Type : Bool, Available values : True or False

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0] 

        ssl_cert = kwargs.get('ssl_cert', None)
        hour_of_day = kwargs.get('hour_of_day', None)
        day_of_week = kwargs.get('day_of_week', None)
        day_of_month = kwargs.get('day_of_month', None)
        createAssetsIfZeroVulnFoundInFile = kwargs.get('createAssetsIfZeroVulnFoundInFile', None)
        generateShortDescription = kwargs.get('generateShortDescription', None)        

        try:
            project_selection = input("Select \"ALL\" projects in checkmarx? Please enter 'y' if YES or enter 'n' if NO: ")
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        if project_selection == 'n':
            print("\n[+] As you selected No, these are the list of projects available in checkmarx:\n")
            populate_url = self.api_base_url.format(str(client_id)) + "/populate"
            connector_populate_body = {
                "type": Connectors.Type.CHECKMARX_OSA,
                "username": username,
                "password": password,
                "url": conn_url,
                "projection": "internal"
            }	
            try:
                cred_authorize = self.request_handler.make_request(ApiRequestHandler.POST, populate_url, body=connector_populate_body)
            except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()           

            if cred_authorize.status_code == 200:
                cred_authorize_json = json.loads(cred_authorize.text) 
                for ind in range(len(cred_authorize_json['projectList'])):
                    print(f"Index Number - {ind} - {cred_authorize_json['projectList'][ind]['displayValue']}")
                print()
                try:
                    project_indexes_list = list(map(int, input("Enter the index numbers of projects that you want to select. Enter index numbers as comma separated values if multiple projects need to be selected: ").split(",")))
                except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
                project_selected_list = []
                for value in project_indexes_list:
                    project_selected_list.append(cred_authorize_json['projectList'][value]['value'])
                project_selected_string = ",".join(project_selected_list)
                print(project_selected_string)
        elif project_selection == 'y':
            project_selected_string = "ALL"

        connector_create_url = self.api_base_url.format(str(client_id))

        if generateShortDescription is None:
            generate_short_description = True

        connector_create_body = {
            "type": Connectors.Type.CHECKMARX_SAST,
            "name": conn_name,
            "networkId": network_id,
            "attributes": {
                "username": username,
                "password": password,
                "checkmarxChosenProjectListToPull": project_selected_string,
                "generateShortDescription": generate_short_description
            },
            "connection": {
                "url": conn_url
            },
            "schedule": {
            },
            "autoUrba": auto_urba
        }

        if ssl_cert is not None:
            connector_create_body['connection'].update(sslCertificates=ssl_cert)

        if schedule_freq == Connectors.ScheduleFreq.DAILY:

            if hour_of_day is None:
                hour_of_day = 0

            connector_schedule = {
                "enabled": conn_status,
                "type": schedule_freq,
                "hourOfDay": hour_of_day,
                "daysOfWeek": "1",
                "daysOfMonth": "1",
                "cronSchdule":None
            }

        elif schedule_freq == Connectors.ScheduleFreq.WEEKLY:

            if day_of_week is None:
                day_of_week = "1"

            if hour_of_day is None:
                hour_of_day = 0

            connector_schedule = {
                "enabled": conn_status,
                "type": schedule_freq,
                "hourOfDay": hour_of_day,
                "daysOfWeek": day_of_week,
                "daysOfMonth": "1",
                "cronSchdule":None
            }

        elif schedule_freq == Connectors.ScheduleFreq.MONTHLY:

            if day_of_month is None:
                day_of_month = "1"

            if hour_of_day is None:
                hour_of_day = 0

            connector_schedule = {
                "enabled": conn_status,
                "type": schedule_freq,
                "hourOfDay": hour_of_day,
                "daysOfWeek": "1",
                "daysOfMonth": day_of_month,
                "cronSchdule":None
            }

        else:
            raise ValueError("Schedule freq. should be DAILY, WEEKLY, or MONTHLY.")

        connector_create_body.update(schedule=connector_schedule)

        if createAssetsIfZeroVulnFoundInFile is None:
            create_asset = True
        
        connector_create_body['attributes'].update(createAssetsIfZeroVulnFoundInFile=create_asset)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, connector_create_url, body=connector_create_body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id        

    def create_qualys_was(self, conn_name:str, conn_url:str, schedule_freq:str, network_id:int,username:str, password:str, auto_urba:bool=True, client_id:int=None, **kwargs):

        """
        Create a new Qualys Web application connector.

        :param conn_name:       The connector name.
        :type  conn_name:       str

        :param conn_url:        The URL for the connector to communicate with.
        :type  conn_url:        str

        :param schedule_freq:   The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                        Connectors.ScheduleFreq.WEEKLY,
                                                                        Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:   str

        :param network_id:      The network ID
        :type  network_id:      int

        :param username:        The username to use for connector authentication.
        :type  username:        str

        :param password:        The password to use for connector authentication.
        :type  password:        str

        :param auto_urba:       Automatically run URBA after connector runs?
        :type  auto_urba:       bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword ssl_cert:      Optional SSL certificate.
        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31
        :keyword reportnameprefix: Report Name Prefix


        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            connector_id = self.create_scanning_connector(conn_name, Connectors.Type.QUALYS_WAS, conn_url, schedule_freq,
                                       network_id, username, password, auto_urba, client_id, **kwargs)
        except (RequestFailed, ValueError):
            raise

        return connector_id

    def create_qualys_vuln(self, conn_name:str, conn_url:str, schedule_freq:str, network_id:int,username:str, password:str, auto_urba:bool=True, client_id:int=None, **kwargs):

        """
        Create a new Qualys Vulnerability connector.

        :param conn_name:       The connector name.
        :type  conn_name:       str

        :param conn_url:        The URL for the connector to communicate with.
        :type  conn_url:        str

        :param schedule_freq:   The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                        Connectors.ScheduleFreq.WEEKLY,
                                                                        Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:   str

        :param network_id:      The network ID
        :type  network_id:      int

        :param username:        The username to use for connector authentication.
        :type  username:        str

        :param password:        The password to use for connector authentication.
        :type  password:        str

        :param auto_urba:       Automatically run URBA after connector runs?
        :type  auto_urba:       bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword ssl_cert:      Optional SSL certificate.
        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31
        :keyword reportnameprefix: Report Name Prefix


        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            connector_id = self.create_scanning_connector(conn_name, Connectors.Type.QUALYS_VULN, conn_url, schedule_freq,
                                       network_id, username, password, auto_urba, client_id, **kwargs)
        except (RequestFailed, ValueError):
            raise

        return connector_id

    def create_qualys_asset(self, conn_name:str, conn_url:str, schedule_freq:str, network_id:int,username:str, password:str, auto_urba:bool=True, client_id:int=None, **kwargs):

        """
        Create a new Qualys Asset connector.

        :param conn_name:       The connector name.
        :type  conn_name:       str

        :param conn_url:        The URL for the connector to communicate with.
        :type  conn_url:        str

        :param schedule_freq:   The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                        Connectors.ScheduleFreq.WEEKLY,
                                                                        Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:   str

        :param network_id:      The network ID
        :type  network_id:      int

        :param username:        The username to use for connector authentication.
        :type  username:        str

        :param password:        The password to use for connector authentication.
        :type  password:        str

        :param auto_urba:       Automatically run URBA after connector runs?
        :type  auto_urba:       bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword ssl_cert:      Optional SSL certificate.
        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31
        :keyword reportnameprefix: Report Name Prefix


        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            connector_id = self.create_scanning_connector(conn_name, Connectors.Type.QUALYS_ASSET, conn_url, schedule_freq,
                                       network_id, username, password, auto_urba, client_id, **kwargs)
        except (RequestFailed, ValueError):
            raise

        return connector_id

    def create_nexpose_asset_tag(self, conn_name:str, conn_url:str, schedule_freq:str, network_id:int,username:str, password:str, auto_urba:bool=True, client_id:int=None, **kwargs):

        """
        Create a new Nexpose Asset connector.

        :param conn_name:       The connector name.
        :type  conn_name:       str

        :param conn_url:        The URL for the connector to communicate with.
        :type  conn_url:        str

        :param schedule_freq:   The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                        Connectors.ScheduleFreq.WEEKLY,
                                                                        Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:   str

        :param network_id:      The network ID
        :type  network_id:      int

        :param username:        The username to use for connector authentication.
        :type  username:        str

        :param password:        The password to use for connector authentication.
        :type  password:        str

        :param auto_urba:       Automatically run URBA after connector runs?
        :type  auto_urba:       bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword ssl_cert:      Optional SSL certificate.
        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31
        :keyword reportnameprefix: the report name prefix

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            connector_id = self.create_scanning_connector(conn_name, Connectors.Type.NEXPOSE_ASSET, conn_url, schedule_freq,
                                       network_id, username, password, auto_urba, client_id, **kwargs)
        except (RequestFailed, ValueError):
            raise

        return connector_id


    def create_qualys_vmdr(self, conn_name:str, conn_url:str, schedule_freq:str, network_id:int,username:str, password:str, auto_urba:bool=True, client_id:int=None, **kwargs):

        """
        Create a new qualys vmdr connector.

        :param conn_name:       The connector name.
        :type  conn_name:       str

        :param conn_url:        The URL for the connector to communicate with.
        :type  conn_url:        str

        :param schedule_freq:   The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                        Connectors.ScheduleFreq.WEEKLY,
                                                                        Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:   str

        :param network_id:      The network ID
        :type  network_id:      int

        :param username:        The username to use for connector authentication.
        :type  username:        str

        :param password:        The password to use for connector authentication.
        :type  password:        str

        :param auto_urba:       Automatically run URBA after connector runs?
        :type  auto_urba:       bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword ssl_cert:      Optional SSL certificate.
        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            connector_id = self.create_scanning_connector(conn_name, Connectors.Type.QUALYS_VMDR, conn_url, schedule_freq,
                                       network_id, username, password, auto_urba, client_id, **kwargs)
        except (RequestFailed, ValueError):
            raise

        return connector_id


    def create_nexpose(self, conn_name:str, conn_url:str, schedule_freq:str, network_id:int,username:str, password:str, auto_urba:bool=True, client_id:int=None, **kwargs):

        """
        Create a new Nexpose connector.

        :param conn_name:       The connector name.
        :type  conn_name:       str

        :param conn_url:        The URL for the connector to communicate with.
        :type  conn_url:        str

        :param schedule_freq:   The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                        Connectors.ScheduleFreq.WEEKLY,
                                                                        Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:   str

        :param network_id:      The network ID
        :type  network_id:      int

        :param username:        The username to use for connector authentication.
        :type  username:        str

        :param password:        The password to use for connector authentication.
        :type  password:        str

        :param auto_urba:       Automatically run URBA after connector runs?
        :type  auto_urba:       bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword ssl_cert:      Optional SSL certificate.
        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31
        :keyword reportnameprefix: Report Name Prefix

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            connector_id = self.create_scanning_connector(conn_name, Connectors.Type.NEXPOSE, conn_url, schedule_freq, network_id,
                                       username, password, auto_urba, client_id, **kwargs)
        except (RequestFailed, ValueError):
            raise

        return connector_id


    def create_teneble(self, conn_name:str, conn_url:str, schedule_freq:str, network_id:int,username:str, password:str, auto_urba:bool=True, client_id:int=None, **kwargs):

        """
        Create a new Teneble Security Center connector.

        :param conn_name:       The connector name.
        :type  conn_name:       str

        :param conn_url:        The URL for the connector to communicate with.
        :type  conn_url:        str

        :param schedule_freq:   The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                        Connectors.ScheduleFreq.WEEKLY,
                                                                        Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:   str

        :param network_id:      The network ID
        :type  network_id:      int

        :param username:        The username to use for connector authentication.
        :type  username:        str

        :param password:        The password to use for connector authentication.
        :type  password:        str

        :param auto_urba:       Automatically run URBA after connector runs?
        :type  auto_urba:       bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword ssl_cert:      Optional SSL certificate.
        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            connector_id = self.create_scanning_connector(conn_name, Connectors.Type.TENEBLE_SEC_CENTER, conn_url, schedule_freq,
                                       network_id, username, password, auto_urba, client_id, **kwargs)
        except (RequestFailed, ValueError):
            raise

        return connector_id


    def get_connector_detail(self, connector_id:int, client_id:int=None):

        """
        Get the details associated with a specific connector.

        :param connector_id:    The connector ID.
        :type  connector_id:    int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON response from the platform is returned.
        :rtype:     dict

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}".format(str(connector_id))

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def update(self, connector_id:int, conn_type:str, conn_name:str, conn_url:str, network_id:int, schedule_freq:str,username_or_access_key:str, password_or_secret_key:str, auto_urba:bool=True, client_id:int=None, **kwargs):

        """
        Update an existing connector

        :param connector_id:            Connector ID to update
        :type  connector_id:            int

        :param conn_type:               Type of Connector (Valid options are: Connectors.Type.NESSUS,
                                                                              Connectors.Type.NEXPOSE,
                                                                              Connectors.Type.QUALYS_VULN,
                                                                              Connectors.Type.QUALYS_ASSET,
                                                                              Connectors.Type.TENEBLE_SEC_CENTER)
        :type  conn_type:               str

        :param conn_name:               The name for the connector
        :type  conn_name:               str

        :param conn_url:                The URL for the connector to communicate with.
        :type  conn_url:                str

        :param network_id:              The network ID
        :type  network_id:              int

        :param schedule_freq:           The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                                Connectors.ScheduleFreq.WEEKLY,
                                                                                Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:           str

        :param username_or_access_key:  The username or access key to be used
        :type  username_or_access_key:  str

        :param password_or_secret_key:  The password or secret key to be used
        :type  password_or_secret_key:  str

        :param auto_urba:   Indicates whether URBA should be automatically run after connector runs.
        :type  auto_urba:   bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        connector_schedule = None

        url = self.api_base_url.format(str(client_id)) + "/{}".format(str(connector_id))

        ssl_cert = kwargs.get('ssl_cert', None)
        hour_of_day = kwargs.get('hour_of_day', None)
        day_of_week = kwargs.get('day_of_week', None)
        day_of_month = kwargs.get('day_of_month', None)
        template=kwargs.get('template','None')
        createassetifzerovulnfoundinfile=kwargs.get('create_asset',False)
        reportNamePrefix=kwargs.get('reportnameprefix','')
        authmechanism=kwargs.get('authmechanism','APIKey')

        if schedule_freq == Connectors.ScheduleFreq.DAILY:

            if hour_of_day is None:
                hour_of_day = 12

            connector_schedule = {
                "type": schedule_freq,
                "hourOfDay": hour_of_day
            }

        elif schedule_freq == Connectors.ScheduleFreq.WEEKLY:

            if day_of_week is None:
                day_of_week = 1

            if hour_of_day is None:
                hour_of_day = 12

            connector_schedule = {
                "type": schedule_freq,
                "hourOfDay": hour_of_day,
                "dayOfWeek": day_of_week
            }

        elif schedule_freq == Connectors.ScheduleFreq.MONTHLY:

            if day_of_month is None:
                day_of_month = 1

            if hour_of_day is None:
                hour_of_day = 12

            connector_schedule = {
                "type": schedule_freq,
                "hourOfDay": hour_of_day,
                "dayOfMonth": day_of_month
            }
        
        

        if conn_type == Connectors.Type.NESSUS:
            attributes = {
                "accessKey": username_or_access_key,
                "secretKey": password_or_secret_key
            }
        elif conn_type ==Connectors.Type.BURPSUITE:

            attributes ={"username":username_or_access_key,
            "password":password_or_secret_key,"createAssetsIfZeroVulnFoundInFile":createassetifzerovulnfoundinfile}
        elif conn_type==Connectors.Type.AWSINSPECTOR:
            attributes ={"username":username_or_access_key,
            "password":password_or_secret_key,"template":template}
        elif conn_type ==Connectors.Type.SONAR_CLOUD:
            ingestionfindingstype = kwargs.get('ingestionfindingstype',[])
            attributes ={"username":username_or_access_key,
            "password":password_or_secret_key,"createAssetsIfZeroVulnFoundInFile":createassetifzerovulnfoundinfile,"ingestionfindingsType":ingestionfindingstype}
        elif conn_type ==Connectors.Type.SONAR_CLOUD:
            ingestionfindingstype = kwargs.get('ingestionfindingstype',[])
            attributes ={"username":username_or_access_key,
            "password":password_or_secret_key,"createAssetsIfZeroVulnFoundInFile":createassetifzerovulnfoundinfile,"ingestionfindingsType":ingestionfindingstype}
        elif conn_type ==Connectors.Type.NEXPOSE or conn_type == Connectors.Type.QUALYS_WAS or conn_type == Connectors.Type.QUALYS_PC:

            attributes ={"username":username_or_access_key,
                "password":password_or_secret_key,
                "reportNamePrefix": reportNamePrefix}
        elif conn_type == Connectors.Type.VERACODE:
            attributes= {"username":username_or_access_key,
                "password":password_or_secret_key,"authMechanism":authmechanism}

        elif conn_type ==Connectors.Type.QUALYS_VULN or conn_type==Connectors.Type.EXPANDER:

            attributes ={"username":username_or_access_key,
                "password":password_or_secret_key,
                "reportNamePrefix": reportNamePrefix}

        else:
            attributes = {
                "username": username_or_access_key,
                "password": password_or_secret_key
            }

        body = {
            "type": conn_type,
            "name": conn_name,
            "connection": {
                "url": conn_url
            },
            "schedule": connector_schedule,
            "networkId": network_id,
            "attributes": attributes,
            "autoUrba": auto_urba
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        jsonified_response = json.loads(raw_response.text)
        returned_id = jsonified_response['id']

        return returned_id
    
    def update_expander(self,conn_id:int, conn_name:str, conn_url:str, schedule_freq:str, network_id:int,username_or_access_key:str, password_or_secret_key:str,auto_urba:bool=True, client_id:int=None, **kwargs):

        """
        Update expander connector.

        :param conn_id:          Connector id
        :type  conn_id:          int

        :param conn_name:       The connector name.
        :type  conn_name:       str

        :param conn_url:        The URL for the connector to communicate with.
        :type  conn_url:        str

        :param schedule_freq:   The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                        Connectors.ScheduleFreq.WEEKLY,
                                                                        Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:   str

        :param network_id:      The network ID
        :type  network_id:      int

        :param username_or_access_key:      The username to use for connector authentication.
        :type  username_or_access_key:      str

        :param password_or_secret_key:      The password to use for connector authentication.
        :type  password_or_secret_key:      str

        :param auto_urba:       Automatically run URBA after connector runs?
        :type  auto_urba:       bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword ssl_cert:      Optional SSL certificate.
        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            connector_id= self.update(conn_id, Connectors.Type.EXPANDER, conn_name, conn_url, network_id, schedule_freq,
                                      username_or_access_key, password_or_secret_key, auto_urba, client_id, **kwargs)
        except (RequestFailed,Exception) as e:
            print()
            print('Error in creating expander connector')
            print(e)
            exit()

        return connector_id
    
    def update_crowdstrike(self,conn_id:int, conn_name:str, conn_url:str, schedule_freq:str, network_id:int, username:str, password:str, auto_urba:bool=True, client_id:int=None, **kwargs):
        """
        Update crowdstrike connector.
        
        :param conn_id:          Connector id
        :type  conn_id:          int

        :param conn_name:       The connector name.
        :type  conn_name:       str

        :param conn_url:        The URL for the connector to communicate with.
        :type  conn_url:        str

        :param schedule_freq:   The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                        Connectors.ScheduleFreq.WEEKLY,
                                                                        Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:   str

        :param network_id:      The network ID
        :type  network_id:      int

        :param username:      The username to use for connector authentication.
        :type  username:      str

        :param password:      The password to use for connector authentication.
        :type  password:      str

        :param auto_urba:       Automatically run URBA after connector runs?
        :type  auto_urba:       bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword ssl_cert:      Optional SSL certificate.
        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

    
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            connector_id = self.update(conn_id, Connectors.Type.CROWDSTRIKE,conn_name, conn_url, network_id,schedule_freq,
                                        username, password, auto_urba, client_id, **kwargs)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        return connector_id

    def update_qualys_vmdr(self,connector_id:int, conn_name:str, conn_url:str, schedule_freq:str, network_id:int,username:str, password:str, auto_urba:bool=True, client_id:int=None, **kwargs):

        """
        Update qualys vm connector.

        :param conn_id:          Connector id
        :type  conn_id:          int

        :param conn_name:       The connector name.
        :type  conn_name:       str

        :param conn_url:        The URL for the connector to communicate with.
        :type  conn_url:        str

        :param schedule_freq:   The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                        Connectors.ScheduleFreq.WEEKLY,
                                                                        Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:   str

        :param network_id:      The network ID
        :type  network_id:      int

        :param username:        The username to use for connector authentication.
        :type  username:        str

        :param password:        The password to use for connector authentication.
        :type  password:        str

        :param auto_urba:       Automatically run URBA after connector runs?
        :type  auto_urba:       bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword ssl_cert:      Optional SSL certificate.
        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            connector_id = self.update(connector_id, Connectors.Type.QUALYS_VMDR,conn_name, conn_url, network_id,schedule_freq, username, password, auto_urba, client_id, **kwargs)
        except (RequestFailed, ValueError):
            raise

        return connector_id

    def update_nessus_connector(self, connector_id:int, conn_name:str, conn_url:str, network_id:int, schedule_freq:str, username_or_access_key:str, password_or_secret_key:str, auto_urba:bool=True, client_id:int=None, **kwargs):

        """
        Update an existing Nessus connector

        :param connector_id:            Connector ID to update
        :type  connector_id:            int

        :param conn_name:               The name for the connector
        :type  conn_name:               str

        :param conn_url:                The URL for the connector to communicate with.
        :type  conn_url:                str

        :param network_id:              The network ID
        :type  network_id:              int

        :param schedule_freq:           The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                                Connectors.ScheduleFreq.WEEKLY,
                                                                                Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:           str

        :param username_or_access_key:  The username or access key to be used
        :type  username_or_access_key:  str

        :param password_or_secret_key:  The password or secret key to be used
        :type  password_or_secret_key:  str

        :param auto_urba:   Indicates whether URBA should be automatically run after connector runs.
        :type  auto_urba:   bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_id = self.update(connector_id, Connectors.Type.NESSUS, conn_name, conn_url, network_id, schedule_freq,
                                      username_or_access_key, password_or_secret_key, auto_urba, client_id, **kwargs)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        return returned_id

    def update_sonarcloud(self, connector_id:int, conn_name:str, conn_url:str, network_id:int, schedule_freq:str,username_or_access_key:str, password_or_secret_key:str, auto_urba:bool=True, client_id:int=None, **kwargs):

        """
        Update an existing Sonarcloud connector

        :param connector_id:            Connector ID to update
        :type  connector_id:            int

        :param conn_name:               The name for the connector
        :type  conn_name:               str

        :param conn_url:                The URL for the connector to communicate with.
        :type  conn_url:                str

        :param network_id:              The network ID
        :type  network_id:              int

        :param schedule_freq:           The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                                Connectors.ScheduleFreq.WEEKLY,
                                                                                Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:           str

        :param username_or_access_key:  The username or access key to be used
        :type  username_or_access_key:  str

        :param password_or_secret_key:  The password or secret key to be used
        :type  password_or_secret_key:  str

        :param auto_urba:               Indicates whether URBA should be automatically run after connector runs.
        :type  auto_urba:               bool

        :param client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:               int

        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_id = self.update(connector_id, Connectors.Type.SONAR_CLOUD, conn_name, conn_url, network_id, schedule_freq,
                                      username_or_access_key, password_or_secret_key, auto_urba, client_id, **kwargs)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        return returned_id

    def update_veracode(self, connector_id:int, conn_name:str, conn_url:str, network_id:int, schedule_freq:str,username_or_access_key:str, password_or_secret_key:str, auto_urba:bool=True, client_id:int=None, **kwargs):

        """
        Update an existing Veracode connector

        :param connector_id:            Connector ID to update
        :type  connector_id:            int

        :param conn_name:               The name for the connector
        :type  conn_name:               str

        :param conn_url:                The URL for the connector to communicate with.
        :type  conn_url:                str

        :param network_id:              The network ID
        :type  network_id:              int

        :param schedule_freq:           The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                                Connectors.ScheduleFreq.WEEKLY,
                                                                                Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:           str

        :param username_or_access_key:  The username or access key to be used
        :type  username_or_access_key:  str

        :param password_or_secret_key:  The password or secret key to be used
        :type  password_or_secret_key:  str

        :param auto_urba:               Indicates whether URBA should be automatically run after connector runs.
        :type  auto_urba:               bool

        :param client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:               int

        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_id = self.update(connector_id, Connectors.Type.VERACODE, conn_name, conn_url, network_id, schedule_freq,
                                      username_or_access_key, password_or_secret_key, auto_urba, client_id, **kwargs)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        return returned_id

    def update_tenableio(self, connector_id:int, conn_name:str, conn_url:str, network_id:int, schedule_freq:str,username_or_access_key:str, password_or_secret_key:str, auto_urba:bool=True, client_id:int=None, **kwargs):

        """
        Update an existing Tenable io connector

        :param connector_id:            Connector ID to update
        :type  connector_id:            int

        :param conn_name:               The name for the connector
        :type  conn_name:               str

        :param conn_url:                The URL for the connector to communicate with.
        :type  conn_url:                str

        :param network_id:              The network ID
        :type  network_id:              int

        :param schedule_freq:           The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                                Connectors.ScheduleFreq.WEEKLY,
                                                                                Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:           str

        :param username_or_access_key:  The username or access key to be used
        :type  username_or_access_key:  str

        :param password_or_secret_key:  The password or secret key to be used
        :type  password_or_secret_key:  str

        :param auto_urba:               Indicates whether URBA should be automatically run after connector runs.
        :type  auto_urba:               bool

        :param client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:               int

        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_id = self.update(connector_id, Connectors.Type.NESSUS, conn_name, conn_url, network_id, schedule_freq,
                                      username_or_access_key, password_or_secret_key, auto_urba, client_id, **kwargs)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        return returned_id

    def update_teneble(self, connector_id:int,conn_name:str, conn_url:str, schedule_freq:str, network_id:int,username:str, password:str, auto_urba:bool=True, client_id:int=None, **kwargs):

        """
        Update an existing Teneble Security Center connector.

        :param conn_id:          Connector id
        :type  conn_id:          int

        :param conn_name:       The connector name.
        :type  conn_name:       str

        :param conn_url:        The URL for the connector to communicate with.
        :type  conn_url:        str

        :param schedule_freq:   The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                        Connectors.ScheduleFreq.WEEKLY,
                                                                        Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:   str

        :param network_id:      The network ID
        :type  network_id:      int

        :param username:        The username to use for connector authentication.
        :type  username:        str

        :param password:        The password to use for connector authentication.
        :type  password:        str

        :param auto_urba:       Automatically run URBA after connector runs?
        :type  auto_urba:       bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword ssl_cert:      Optional SSL certificate.
        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            connector_id = self.update(connector_id, Connectors.Type.TENEBLE_SEC_CENTER,conn_name,conn_url,  network_id,schedule_freq, username, password, auto_urba, client_id, **kwargs)
        except (RequestFailed, ValueError):
            raise

        return connector_id

    def update_hclappscan(self, connector_id:int, conn_name:str, conn_url:str, network_id:int, schedule_freq:str,username_or_access_key:str, password_or_secret_key:str, auto_urba:bool=True, client_id:int=None, **kwargs):

        """
        Update an existing hclappscan connector

        :param connector_id:            Connector ID to update
        :type  connector_id:            int

        :param conn_name:               The name for the connector
        :type  conn_name:               str

        :param conn_url:                The URL for the connector to communicate with.
        :type  conn_url:                str

        :param network_id:              The network ID
        :type  network_id:              int

        :param schedule_freq:           The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                                Connectors.ScheduleFreq.WEEKLY,
                                                                                Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:           str

        :param username_or_access_key:  The username or access key to be used
        :type  username_or_access_key:  str

        :param password_or_secret_key:  The password or secret key to be used
        :type  password_or_secret_key:  str

        :param auto_urba:               Indicates whether URBA should be automatically run after connector runs.
        :type  auto_urba:               bool

        :param client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:               int

        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_id = self.update(connector_id, Connectors.Type.HCL_APPSCAN, conn_name, conn_url, network_id, schedule_freq,
                                      username_or_access_key, password_or_secret_key, auto_urba, client_id, **kwargs)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        return returned_id

    def update_awsinspector(self, connector_id:int,conn_name:str, conn_url:str, schedule_freq:str, network_id:int,username:str, password:str, auto_urba:bool=True, client_id:int=None,**kwargs):

        """
        Update an existing aws inspector connector.

        :param connector_id:       The connector id.
        :type  connector_id:       str

        :param conn_name:       The connector name.
        :type  conn_name:       str

        :param conn_url:        The URL for the connector to communicate with.
        :type  conn_url:        str

        :param schedule_freq:   The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                        Connectors.ScheduleFreq.WEEKLY,
                                                                        Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:   str

        :param network_id:      The network ID
        :type  network_id:      int

        :param access_key:      The username to use for connector authentication.
        :type  access_key:      str

        :param secret_key:      The password to use for connector authentication.
        :type  secret_key:      str

        :param auto_urba:       Automatically run URBA after connector runs?
        :type  auto_urba:       bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword ssl_cert:      Optional SSL certificate.
        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

        awsinspector={"username":username,"password":password,"url":conn_url,"name":conn_name,"type": Connectors.Type.AWSINSPECTOR,"projection":"internal"}

        print(type(awsinspector))
        print(awsinspector)
        populatedate=self.connector_populate(body=awsinspector)
        choice=[]

        print("[+] These are the available templates for aws inspector\n")
        print(len(populatedate))
        for ind in range(len(populatedate['templates'])):
            print(f"Index Number - {ind} - {populatedate['templates'][ind]['displayValue']}")
            print()
        try:
            temp=input('Please enter the templates seperated by commas').split(',')
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        templatevalues=','.join(populatedate['templates'][int(x)]['value'] for x in temp)
        print(templatevalues)

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            connector_id = self.update(connector_id, Connectors.Type.AWSINSPECTOR,conn_name, conn_url,  network_id,schedule_freq,
                                       username,password,auto_urba, client_id,template=templatevalues,**kwargs)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        return connector_id
    
    def update_burpsuite(self,connector_id:int, conn_name:str, conn_url:str, schedule_freq:str, network_id:int,username:str, apikey:str, auto_urba:bool=True, client_id:int=None, **kwargs):

        """
        Update an existing burpsuite connector.

        :param connector_id:       The connector id.
        :type  connector_id:       str

        :param conn_name:       The connector name.
        :type  conn_name:       str

        :param conn_url:        The URL for the connector to communicate with.
        :type  conn_url:        str

        :param schedule_freq:   The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                        Connectors.ScheduleFreq.WEEKLY,
                                                                        Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:   str

        :param network_id:      The network ID
        :type  network_id:      int

        :param access_key:      The username to use for connector authentication.
        :type  access_key:      str

        :param secret_key:      The password to use for connector authentication.
        :type  secret_key:      str

        :param auto_urba:       Automatically run URBA after connector runs?
        :type  auto_urba:       bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword ssl_cert:      Optional SSL certificate.
        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            connector_id = self.update(connector_id, Connectors.Type.BURPSUITE,conn_name, conn_url,  network_id,schedule_freq,
                                       username,apikey, auto_urba, client_id, **kwargs)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        return connector_id
    
    def update_nexpose(self, connector_id:int,conn_name:str, conn_url:str, schedule_freq:str, network_id:int,username:str, password:str, auto_urba:bool=True, client_id:int=None, **kwargs):

        """
        Update an existing Nexpose connector.

        :param connector_id:       The connector id.
        :type  connector_id:       id
        
        :param conn_name:       The connector name.
        :type  conn_name:       str

        :param conn_url:        The URL for the connector to communicate with.
        :type  conn_url:        str

        :param schedule_freq:   The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                        Connectors.ScheduleFreq.WEEKLY,
                                                                        Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:   str

        :param network_id:      The network ID
        :type  network_id:      int

        :param username:        The username to use for connector authentication.
        :type  username:        str

        :param password:        The password to use for connector authentication.
        :type  password:        str

        :param auto_urba:       Automatically run URBA after connector runs?
        :type  auto_urba:       bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword ssl_cert:      Optional SSL certificate.
        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            connector_id = self.update(connector_id, Connectors.Type.NEXPOSE,conn_name, conn_url,  network_id,schedule_freq,
                                       username, password, auto_urba, client_id, **kwargs)
        except (RequestFailed, ValueError):
            raise

        return connector_id

    def update_qualys_vm_connector(self, connector_id:int, conn_name:str, conn_url:str, network_id:int, schedule_freq:str,username_or_access_key:str, password_or_secret_key:str, auto_urba:bool=True, client_id:int=None, **kwargs):

        """
        Update an existing QUALYS VM connector

        :param connector_id:            Connector ID to update
        :type  connector_id:            int

        :param conn_name:               The name for the connector
        :type  conn_name:               str

        :param conn_url:                The URL for the connector to communicate with.
        :type  conn_url:                str

        :param network_id:              The network ID
        :type  network_id:              int

        :param schedule_freq:           The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                                Connectors.ScheduleFreq.WEEKLY,
                                                                                Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:           str

        :param username_or_access_key:  The username or access key to be used
        :type  username_or_access_key:  str

        :param password_or_secret_key:  The password or secret key to be used
        :type  password_or_secret_key:  str

        :param auto_urba:               Indicates whether URBA should be automatically run after connector runs.
        :type  auto_urba:               bool

        :param client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:               int

        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_id = self.update(connector_id, Connectors.Type.QUALYS_VMDR, conn_name, conn_url, network_id, schedule_freq,
                                      username_or_access_key, password_or_secret_key, auto_urba, client_id, **kwargs)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        return returned_id

    def update_qualys_pc_connector(self, connector_id:int, conn_name:str, conn_url:str, network_id:int, schedule_freq:str,username_or_access_key:str, password_or_secret_key:str, auto_urba:bool=True, client_id:int=None, **kwargs):

        """
        Update an existing QUALYS PC connector

        :param connector_id:            Connector ID to update
        :type  connector_id:            int

        :param conn_name:               The name for the connector
        :type  conn_name:               str

        :param conn_url:                The URL for the connector to communicate with.
        :type  conn_url:                str

        :param network_id:              The network ID
        :type  network_id:              int

        :param schedule_freq:           The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                                Connectors.ScheduleFreq.WEEKLY,
                                                                                Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:           str

        :param username_or_access_key:  The username or access key to be used
        :type  username_or_access_key:  str

        :param password_or_secret_key:  The password or secret key to be used
        :type  password_or_secret_key:  str

        :param auto_urba:               Indicates whether URBA should be automatically run after connector runs.
        :type  auto_urba:               bool

        :param client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:               int

        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_id = self.update(connector_id, Connectors.Type.QUALYS_PC, conn_name, conn_url, network_id, schedule_freq,
                                      username_or_access_key, password_or_secret_key, auto_urba, client_id, **kwargs)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        return returned_id
    
    def update_nexpose_asset(self, connector_id:int, conn_name:str, conn_url:str, network_id:int, schedule_freq:str,username_or_access_key:str, password_or_secret_key:str, auto_urba:bool=True, client_id:int=None, **kwargs):

        """
        Update an existing QUALYS PC connector

        :param connector_id:            Connector ID to update
        :type  connector_id:            int

        :param conn_name:               The name for the connector
        :type  conn_name:               str

        :param conn_url:                The URL for the connector to communicate with.
        :type  conn_url:                str

        :param network_id:              The network ID
        :type  network_id:              int

        :param schedule_freq:           The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                                Connectors.ScheduleFreq.WEEKLY,
                                                                                Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:           str

        :param username_or_access_key:  The username or access key to be used
        :type  username_or_access_key:  str

        :param password_or_secret_key:  The password or secret key to be used
        :type  password_or_secret_key:  str

        :param auto_urba:               Indicates whether URBA should be automatically run after connector runs.
        :type  auto_urba:               bool

        :param client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:               int

        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_id = self.update(connector_id, Connectors.Type.NEXPOSE_ASSET, conn_name, conn_url, network_id, schedule_freq,
                                      username_or_access_key, password_or_secret_key, auto_urba, client_id, **kwargs)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        return returned_id
    

    def search_query_parameter(self,body:dict,client_id:int=None):

        """
        Get option drop down fields based on search query parameters

        :param body:    The body that contains connector information
        :type  body:    dict

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON response from the platform is returned.
        :rtype:     dict

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        query_parameter_url = self.api_base_url.format(str(client_id))+'/field/option'
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url=query_parameter_url,body=body)
        except (RequestFailed,Exception) as e:
            print()
            print('Error in connector populate')
            print(e)
            exit()
            
        jsonified_response = json.loads(raw_response.text)

        return jsonified_response


    def update_jira_connector(self, connector_id:int, jira_connector_name:str, username:str, password_or_api_token:str, jira_url:str, project_name:str, project_key:str, issue_type_name:str, issue_type_key:str, tag_type_name:str, closed_status_key:str, closed_status_value:str, ticket_sync_string:str, client_id:int=None):
        """
        Updates a JIRA Connector
        :param connector_id:                The Connector Id
        :type connector_id:                 str

        :param jira_connector_name:         JIRA Connector Name
        :type jira_connector_name:          str

        :param username:                    JIRA username
        :type username:                     str

        :param password_or_api_token:       JIRA API Token/Password
        :type password_or_api_token:        str

        :param jira_url:                    JIRA Platform URL
        :type jira_url:                     str

        :param project_name:                JIRA Project Name
        :type project_name:                 str

        :param project_key:                 JIRA Project Key
        :type project_key:                  str

        :param issue_type_name:             JIRA Issue Type Name
        :type issue_type_name:              str

        :param issue_type_key:              JIRA Issue Type Key
        :type issue_type_key:               str

        :param client_id:                   RS Client ID
        :type client_id:                    int

        :param tag_type_name:               JIRA Issue Type Name
        :type tag_type_name:                str

        :param closed_status_value:         JIRA Closed status name
        :type closed_status_value:          str

        :param closed_status_key:           JIRA Closed status Key
        :type closed_status_key:            str

        :param ticket_sync_string:          JIRA Ticket sync string
        :type ticket_sync_string:           str

        :return connector_id:               Created JIRA connector ID
        :rtype connector_id:                int

        """        
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}".format(str(connector_id))

        connector_creation_body = {
                "name": jira_connector_name,
                "type": Connectors.Type.JIRA,
                "schedule": {
                    "enabled": True,
                    "type": "DAILY",
                    "hourOfDay": 0
                },
                "attributes": {
                    "username": username,
                    "password": password_or_api_token
                },
                "connection": {
                    "url": jira_url
                },
                "id": connector_id,
                "connectorField": {
                    "type": Connectors.Type.JIRA,
                    "project": {
                        "displayValue": project_name,
                        "value": project_key
                    },
                    "issueType": {
                        "displayValue": issue_type_name,
                        "value": issue_type_key
                    },
                    "descriptionFields": [
                        {
                            "key": "owner",
                            "enabled": False
                        },
                        {
                            "key": "name",
                            "enabled": False
                        },
                        {
                            "key": "description",
                            "enabled": False
                        },
                        {
                            "key": "priority",
                            "enabled": False
                        },
                        {
                            "key": "start_date",
                            "enabled": False
                        },
                        {
                            "key": "due_date",
                            "enabled": False
                        },
                        {
                            "key": "percentage_complete",
                            "enabled": False
                        },
                        {
                            "key": "days_remaining",
                            "enabled": False
                        },
                        {
                            "key": "open_findings",
                            "enabled": False
                        },
                        {
                            "key": "total_findings",
                            "enabled": False
                        },
                        {
                            "key": "host_findings",
                            "enabled": False
                        },
                        {
                            "key": "app_findings",
                            "enabled": False
                        },
                        {
                            "key": "assigned_users",
                            "enabled": False
                        },
                        {
                            "key": "data_refresh",
                            "enabled": False
                        },
                        {
                            "key": "assigned",
                            "enabled": False
                        },
                        {
                            "key": "unassigned",
                            "enabled": False
                        },
                        {
                            "key": "accepted",
                            "enabled": False
                        },
                        {
                            "key": "False_positive",
                            "enabled": False
                        }
                    ],
                    "dynamicFields": [
                        {
                            "key": "priority",
                            "value": "10000",
                            "displayValue": "NoPrio"
                        },
                        {
                            "key": "summary",
                            "value": "",
                            "displayValue": ""
                        }
                    ],
                    "tagSyncField": "",
                    "slaDateField": "",
                    "tagTypeDefaultValue": tag_type_name,
                    "usePluginInfoFields": [
                        "summary",
                        "description"
                    ],
                    "lockedFields": [],
                    "connectorSettings": {
                        "initialState": "",
                        "enabledTagRemoval": False,
                        "closeFindingsOnTicketCloseEnabled": False,
                        "closeTicketOnFindingsCloseEnabled": True,
                        "closedStateKey": closed_status_key,
                        "closedStateLabel": closed_status_value,
                        "enabledUploadAttachment": True,
                        "closeStatusesOfTicketToUpdate": ticket_sync_string
                    }
                }
            }
        try:
            connector_create = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=connector_creation_body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        if connector_create.status_code == 200:
            connector_create_json = json.loads(connector_create.text)
            connector_id = connector_create_json['id']

        return connector_id

    def update_snow_connector(self, connector_id:int, snow_connector_name:str, snow_username:str, snow_password_or_token:str, snow_url:str, tag_type_name:str, closed_status_value:str, closed_status_key:str, ticket_sync_string:str, client_id:int=None):
        """
        Update a Service Now Incident type Connector

        :param connector_id:                The Connector Id
        :type connector_id:                 int

        :param snow_connector_name:         JIRA Connector Name
        :type snow_connector_name:          str

        :param snow_username:                    JIRA username
        :type snow_username:                     str

        :param snow_password_or_api_token:       JIRA API Token/Password
        :type snow_password_or_api_token:        str

        :param snow_url:                    JIRA Platform URL
        :type snow_url:                     str

        :param client_id:                   RS Client ID
        :type client_id:                    int

        :param tag_type_name:               JIRA Issue Type Name
        :type tag_type_name:                str

        :param closed_status_value:         JIRA Closed status name
        :type closed_status_value:          str

        :param closed_status_key:           JIRA Closed status Key
        :type closed_status_key:            str

        :param ticket_sync_string:          JIRA Ticket sync string
        :type ticket_sync_string:           str

        :return connector_id:               Created JIRA connector ID
        :rtype connector_id:                int

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + f"/{connector_id}"  

        connector_creation_body = {
            "name": snow_connector_name,
            "type": Connectors.Type.SERVICENOW_INCIDENT,
            "schedule": {
                "enabled": True,
                "type": "DAILY",
                "hourOfDay": 0
            },
            "attributes": {
                "username":snow_username,
                "password": snow_password_or_token
            },
            "connection": {
                "url": snow_url
            },
            "id": connector_id,
            "connectorField": {
                "type": Connectors.Type.SERVICENOW_INCIDENT,
                "defaultTemplateId": "",
                "templates": [],
                "descriptionFields": [
                    {
                        "key": "accepted",
                        "enabled": False
                    },
                    {
                        "key": "app_findings",
                        "enabled": False
                    },
                    {
                        "key": "assigned",
                        "enabled": False
                    },
                    {
                        "key": "assigned_users",
                        "enabled": False
                    },
                    {
                        "key": "data_refresh",
                        "enabled": False
                    },
                    {
                        "key": "days_remaining",
                        "enabled": False
                    },
                    {
                        "key": "description",
                        "enabled": False
                    },
                    {
                        "key": "due_date",
                        "enabled": False
                    },
                    {
                        "key": "False_positive",
                        "enabled": False
                    },
                    {
                        "key": "host_findings",
                        "enabled": False
                    },
                    {
                        "key": "name",
                        "enabled": False
                    },
                    {
                        "key": "open_findings",
                        "enabled": False
                    },
                    {
                        "key": "owner",
                        "enabled": False
                    },
                    {
                        "key": "percentage_complete",
                        "enabled": False
                    },
                    {
                        "key": "priority",
                        "enabled": False
                    },
                    {
                        "key": "start_date",
                        "enabled": False
                    },
                    {
                        "key": "total_findings",
                        "enabled": False
                    },
                    {
                        "key": "unassigned",
                        "enabled": False
                    }
                ],
                "selectedOptionalFields": [
                    "priority",
                    "description",
                    "short_description",
                    "assignment_group",
                    "urgency",
                    "due_date"
                ],
                "defaultSupportedFieldValues": [
                    {
                        "key": "priority",
                        "value": "3",
                        "displayValue": "3 - Moderate"
                    },
                    {
                        "key": "urgency",
                        "value": "2",
                        "displayValue": "2 - Medium"
                    }
                ],
                "tagSyncField": "",
                "slaDateField": "due_date",
                "tagTypeDefaultValue": tag_type_name,
                "connectorSettings": {
                    "initialState": "",
                    "enabledTagRemoval": False,
                    "closeFindingsOnTicketCloseEnabled": False,
                    "closeTicketOnFindingsCloseEnabled": True,
                    "closedStateKey": closed_status_key,
                    "closedStateLabel": closed_status_value,
                    "enabledUploadAttachment": True,
                    "closeStatusesOfTicketToUpdate":ticket_sync_string
                },
                "usePluginInfoFields": [
                    "description",
                    "short_description"
                ]
            }
        }

        try:
            connector_create = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=connector_creation_body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        if connector_create.status_code == 200:
            connector_create_json = json.loads(connector_create.text)
            connector_id = connector_create_json['id']

        return connector_id

    def update_snow_customtableconfig(self,connector_id:int, conn_name:str, conn_url:str,
                           username:str, password:str,tablename:str,statusfield:str,ticketidfield:str,enabletagremoval:bool=False,enableuploadattachment:bool=True, client_id:int=None, **kwargs):
        """
        Update an existing snow custom table configuration connector.

        :param connector_id:                The Connector Id
        :type connector_id:                 int

        :param conn_name:                  The connector name.
        :type  conn_name:                  str

        :param conn_url:                   The URL for the connector to communicate with.
        :type  conn_url:                   str

        :param username:                   The username to use for connector authentication.
        :type  username:                   str

        :param password:                   The password to use for connector authentication.
        :type  password:                   str

        :param tablename:                  Name of the table.
        :type  password:                   str

        :param statusfield:                status field.
        :type  statusfield:                str

        :param ticketidfield:             Ticket id field.
        :type  ticketidfield:             str

        :param enabletagremoval:          Enable tag removal switch
        :type  enabletagremoval:          bool

        :param enableuploadattachment:    Enable upload attachment switch
        :type  enableuploadattachment:    bool

        :param client_id:                 Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:                 int

        :return:                          The connector ID from the platform is returned.
        :rtype:                           int

        :raises RequestFailed:
        :raises ValueError:
        """
        
        descriptiondropdownbody={"type":Connectors.Type.SERVICENOW_CTC,
        "username":username,"password":password,"url":conn_url,"projection":"internal"}
        connect_populate=self.connector_populate(descriptiondropdownbody)
        descriptiondropdown=[]
        tablefields=[]
        print(connect_populate)
        if client_id is None:
                client_id = self._use_default_client_id()[0]
        for index in range(len(connect_populate["descriptionFieldDropDownOptions"])):
            print(f"Index Number - {index} - {connect_populate['descriptionFieldDropDownOptions'][index]['value']}:")
        try:
            temp=input('Please provide description field drop down index number seperated by comma: ').split(',')
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        for x in temp:
            try:
                data=input(f'Please enter the value for {connect_populate["descriptionFieldDropDownOptions"][int(x)]["value"]}')
            except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            descriptiondropdown.append({"descriptionField":connect_populate["descriptionFieldDropDownOptions"][int(x)]["value"],"tableField":data})
        while(True):
            try:
                tablefields.append({"key":input('Please provide a table field:'),"value":
                input('Please provide value')})
                yesorno=input('Would you like to exit: y or n:')
                print(yesorno)
                if yesorno.lower()!='n':
                    break
            except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        postconnectorbody={
            "name": conn_name,
            "type": Connectors.Type.SERVICENOW_CTC,
            "schedule": {
                "enabled":True,
                "type": "DAILY",
                "hourOfDay": 0
            },
            "attributes": {
                "username": username,
                "password": password
            },
            "connection": {
                "url": conn_url
            },
            "connectorField": {
                "type": Connectors.Type.SERVICENOW_CTC,
                "tableName":tablename,
                "statusField":statusfield,
                "ticketIdField":ticketidfield,
                "enabledTagRemoval":enabletagremoval,
                "descriptionFieldToTableFields":descriptiondropdown,
                "tableFields":tablefields,
                "enabledUploadAttachment":enableuploadattachment
            }
        }
        connectorcreateurl=self.api_base_url.format(str(client_id))+'/{}'.format(str(connector_id))
        try:
            updateconnector = self.request_handler.make_request(ApiRequestHandler.PUT, connectorcreateurl, body=postconnectorbody)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        if updateconnector.status_code == 201:
            connector_create_json = json.loads(updateconnector.text)
            connector_id = connector_create_json['id']
        return connector_id



    def update_snow_service_connector(self,snow_connectorid:int, snow_connector_name:str, snow_username:str, snow_password_or_token:str, snow_url:str,ticket_description:str='false', client_id:int=None):
        
        """
        Update existing Service Now Service Request type Connector

        :param connector_id:                The Connector Id
        :type connector_id:                 int

        :param snow_connector_name:          SNOW Service type Connector Name
        :type snow_connector_name:           str

        :param snow_username:                SNOW username
        :type snow_username:                 str

        :param snow_password_or_token:       SNOW API Token/Password
        :type snow_password_or_token:        str

        :param snow_url:                     SNOW Platform URL
        :type snow_url:                      str

        :param ticket_description:           To provide ticket description or not,'true' to provide,'false' to not provide
        :type ticket_description:            str       

        :param client_id:                   RS Client ID
        :type client_id:                    int

        :return connector_id:               Created SNOW Service request connector ID
        :rtype connector_id:                int

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        enabled=[]
        print(ticket_description.lower())
        if ticket_description.lower() == 'true':
            getticketdescriptionbody={"type":Connectors.Type.SERVICENOW_SERVICEREQUEST,"username":snow_username,"password":snow_password_or_token,"url":snow_url,"projection":"internal"}
            ticketdescriptionfields=self.connector_populate(getticketdescriptionbody)
            for ind in range(len(ticketdescriptionfields['supportedDescriptionFields'])):
                print(f"Index Number - {ind} - {ticketdescriptionfields['supportedDescriptionFields'][ind]['displayValue']}")
                print()
                enabled.append({"key":ticketdescriptionfields['supportedDescriptionFields'][ind]['value'],"enabled":False})
            try:
                temp=input('Please enter the supported description fields seperated by commas').split(',')
            except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
            for i in temp:
                enabled[int(i)]['enabled']=True
        url = self.api_base_url.format(str(client_id))+'/{}'.format(str(snow_connectorid))
        populateddata= self.get_snow_catalog(snow_username, snow_password_or_token, snow_url)
        connector_creation_body = {
            "name": snow_connector_name,
            "type": Connectors.Type.SERVICENOW_SERVICEREQUEST,
            "schedule": {
                "enabled": True,
                "type": "DAILY",
                "hourOfDay": 0
            },
            "attributes": {
                "username": snow_username,
                "password": snow_password_or_token
            },
            "connection": {
                "url": snow_url
            },
            "connectorField": {
                "type": "SNOW_SERVICE_REQUEST",
                "catalog": {
                    "displayValue": populateddata['catalog_name'],
                    "value": populateddata['catalog_value']
                },
                "category": {
                    "displayValue": populateddata['category_name'],
                    "value": populateddata['category_value']
                },
                "catalogItem": {
                    "displayValue": populateddata['catalogitem_name'],
                    "value": populateddata['catalogitem_value']
                },
                "dynamicFields": [],
                "descriptionFields": enabled,
                "defaultSupportedFieldValues": [],
                "tagSyncField": "",
                "lockedFields": [],
                "connectorSettings": {
                    "initialState": "",
                    "enabledTagRemoval": True,
                    "closeFindingsOnTicketCloseEnabled": False,
                    "closeTicketOnFindingsCloseEnabled": False,
                    "closedStateKey": populateddata['close_state_key'],
                    "closedStateLabel": populateddata['close_state'],
                    "enabledUploadAttachment": True,
                    "closeStatusesOfTicketToUpdate": ','.join(populateddata['ticket_sync_states'])
                }
            }
        }
        try:
            connector_create = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=connector_creation_body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        if connector_create.status_code == 201:
            connector_create_json = json.loads(connector_create.text)
            connector_id = connector_create_json['id']

        return connector_id

    def update_cherwell_incident_connector(self,cw_id:int,cw_name:str,cw_username:str,cw_password:str,clientid_key:str,cw_url:str,autourba:bool=False,client_id:int=None):
        
        """
        Update cherwell connector type incident

        :param connector_id:                The Connector Id
        :type connector_id:                 int

        :param cw_name:       Cherwell connector name.
        :type  cw_name:       str

        :param cw_username:   Cherwell connector username.
        :type  cw_username:   str

        :param cw_password:   Cherwell connector password.
        :type  cw_password:    str

        :param clientid_key:   Cherwell connector client id key.
        :type  clientid_key:   str

        :param cw_url:   Cherwell connector url.
        :type  cw_url:   str

        :param autourba:  Switch to enable auto urba.
        :type  autourba:   bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON response from the platform is returned.
        :rtype:     dict

        :raises RequestFailed:
        """

        if client_id is None:
                client_id = self._use_default_client_id()[0]
        
        populateitembody={"username":cw_username,"password":cw_password,"url":cw_url,"clientIdKey":clientid_key,"type":Connectors.Type.CHERWELL}
        cherwellincident_connector_populate=self.cherwellincident_connector_populate(populateitembody)
        a={}
        choices={}
        dynamicdropdownfields={}
        dynamicdropdown=[]
        try:
            for i in range(len(cherwellincident_connector_populate['dynamicDropDownFields'])):
                a[cherwellincident_connector_populate['dynamicDropDownFields'][i]['value']]=i
                dynamicdropdownfields[cherwellincident_connector_populate['dynamicDropDownFields'][i]['value']]={"connectorCredentials":{"username":cw_username,"password":cw_password,"url":cw_url,"clientIdKey":clientid_key},"type":"CHERWELL","busObId":cherwellincident_connector_populate['dynamicDropDownFields'][i]["dependentKey"],"fieldId":cherwellincident_connector_populate['dynamicDropDownFields'][i]["fieldValue"],"fieldName":cherwellincident_connector_populate['dynamicDropDownFields'][i]["value"],"fields":[]}
                if cherwellincident_connector_populate['dynamicDropDownFields'][i]['parentField']!="":
                    j=a[cherwellincident_connector_populate['dynamicDropDownFields'][i]['parentField']]
                    while(True):
                        b={"dirty":"true","displayName":cherwellincident_connector_populate['dynamicDropDownFields'][j]['value'],"fieldId":cherwellincident_connector_populate['dynamicDropDownFields'][j]["fieldValue"],"value":""}
                        dynamicdropdownfields[cherwellincident_connector_populate['dynamicDropDownFields'][i]['value']]['fields'].append(b)
                        if cherwellincident_connector_populate['dynamicDropDownFields'][j]['parentField']!="":
                            j=a[cherwellincident_connector_populate['dynamicDropDownFields'][j]['parentField']]
                        else:
                            break
        except Exception as e:
            print(e)
            exit()
        enabled=[]
        for index in range(len(cherwellincident_connector_populate["supportedDescriptionFields"])):
            print(f"Index Number - {index} - {cherwellincident_connector_populate['supportedDescriptionFields'][index]['value']}:")
            enabled.append({"key":cherwellincident_connector_populate['supportedDescriptionFields'][index]['value'],"enabled":False})
            lockedfieldchoice=[]
        try:
            temp=input('Please enter the supported description fields index number seperated by commas:').split(',')
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        for i in temp:
            enabled[int(i)]['enabled']=True

        for key in dynamicdropdownfields:
                    if dynamicdropdownfields[key]['fields']!=[]:
                        for i in range(len(dynamicdropdownfields[key]['fields'])):
                            for j in choices:  
                                if dynamicdropdownfields[key]['fields'][i]['displayName']==j:
                                    dynamicdropdownfields[key]['fields'][i]['value']=choices[j]
                    fieldlookup=self.api_base_url.format(str(client_id))+"/populate/ticketType/Incident/fieldvalueslookup"
                    body=dynamicdropdownfields[key]
                    try:
                        fieldvalueslookup = self.request_handler.make_request(ApiRequestHandler.POST, fieldlookup, body=dynamicdropdownfields[key])
                    except (RequestFailed,Exception) as e:
                            print()
                            print('Error in getting field values lookup')
                            print(e)
                            exit()
                    if fieldvalueslookup.status_code == 200:
                        fieldvalueslookup=json.loads(fieldvalueslookup.text)
                    for i in range(len(fieldvalueslookup['values'])):
                        print(f"Index Number - {i} - {fieldvalueslookup['values'][i]}")
                    try:
                        k=int(input(f'Please enter {key}:'))
                    except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
                    choices[key]=fieldvalueslookup['values'][k]
                    dynamicdropdown.append({ "displayValue":key,"value":fieldvalueslookup['values'][k],"key":dynamicdropdownfields[key]["fieldId"]})

        optionaldropdownlist={}
        for i in range(len(cherwellincident_connector_populate["optionalDropdownList"])):
            a[cherwellincident_connector_populate["optionalDropdownList"][i]["label"]]=i
            optionaldropdownlist[cherwellincident_connector_populate["optionalDropdownList"][i]['value']]={"connectorCredentials":{"username":cw_username,"password":cw_password,"url":cw_url,"clientIdKey":clientid_key},"type":"CHERWELL","busObId":cherwellincident_connector_populate["optionalDropdownList"][i]["dependentKey"],"fieldId":cherwellincident_connector_populate["optionalDropdownList"][i]["fieldValue"],"fieldName":cherwellincident_connector_populate["optionalDropdownList"][i]["value"],"fields":[]}
        fieldlookup=self.api_base_url.format(str(client_id))+"/populate/ticketType/Incident/fieldvalueslookup"
        try:
            status = self.request_handler.make_request(ApiRequestHandler.POST, fieldlookup, body=optionaldropdownlist["Status"])
        except (RequestFailed,Exception) as e:
            print()
            print('There was an error in field values lookup')
            print(e) 
            exit()
        extradata={}
        if status.status_code == 200:
            status=json.loads(status.text)
        for index in range(len(status['values'])):
            print(f"Index Number - {index} - {status['values'][index]}:")
        lockedfieldchoice=[]
        try:
            temp=input('Please enter the index seperated by commas').split(',')
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        for i in temp:
            lockedfieldchoice.append(status['values'][int(i)])
        extradata["closeStatusesOfTicketToUpdate"]=lockedfieldchoice
        try:
            extradata["closedStateKey"]=status['values'][int(input('Enter the index number of close status field that you want to select:'))]
            extradata["closedStateLabel"]=extradata["closedStateKey"]
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        dynamicFieldDetailValue=[]
        fieldslist=["dynamicFieldDetailValue","tagTypeDefaultOptions","slaDateFieldOptions","lockedFields"]
        try:
            for fields in fieldslist:
                extradata[fields]=[]
                if fields=="dynamicFieldDetailValue":
                    for i in range(len(cherwellincident_connector_populate[fields])):
                        a=input(f'Please enter a value for {cherwellincident_connector_populate[fields][i]["label"]}')
                        dynamicFieldDetailValue.append({"displayValue":cherwellincident_connector_populate[fields][i]['label'],"value":a,"key":cherwellincident_connector_populate[fields][i]["fieldValue"]})
                elif fields=="lockedFields":
                    for i in range(len(cherwellincident_connector_populate[fields])):
                        print(f'{i}-{cherwellincident_connector_populate[fields][i]}')
                    lockedfieldchoice=[]
                    temp=input('Please enter the index numbers of locked fields that you want to select in comma seperated values:').split(',')
                    for i in temp:
                        lockedfieldchoice.append(cherwellincident_connector_populate[fields][int(i)]['value'])
                    extradata[fields]=lockedfieldchoice
                else:
                    for i in range(len(cherwellincident_connector_populate[fields])):
                        print(f"Index Number - {i} - {cherwellincident_connector_populate[fields][i]['displayValue']}")
                    extradata[fields]=cherwellincident_connector_populate[fields][int(input(f'Please enter the index number for {fields}:'))]
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        postconnectorbody={
                "name": cw_name,
                "type": Connectors.Type.CHERWELL,
                "schedule": {
                    "enabled": True,
                    "type": "DAILY",
                    "hourOfDay": 0
                },
                "attributes": {
                    "username": cw_username,
                    "password": cw_password,
                    "clientIdKey": clientid_key
                },
                "connection": {
                    "url": cw_url
                },
                "connectorField": {
                    "type": Connectors.Type.CHERWELL,
                    "clientIdKey": clientid_key,
                    "ticketType": {
                        "displayValue": "Incident",
                        "value": "Incident"
                    },
                    "descriptionFields": enabled
                    ,
                    "dynamicDropdownFields": dynamicdropdown,
                    "dynamicFieldDetailValue": dynamicFieldDetailValue,
                    "optionalMandatoryFieldDetailValue": [],
                    "lockedFields": lockedfieldchoice,
                    "slaDateField":extradata["slaDateFieldOptions"]["displayValue"],"tagTypeDefaultValue":extradata["tagTypeDefaultOptions"]["displayValue"],
                    "connectorSettings": {
                        "closeFindingsOnTicketCloseEnabled": False,
                        "closeStatusesOfTicketToUpdate": ','.join(extradata['closeStatusesOfTicketToUpdate']),
                        "closeTicketOnFindingsCloseEnabled": False,
                        "closedStateKey":(extradata['closedStateKey']),
                        "closedStateLabel": extradata['closedStateKey'],
                        "enabledTagRemoval": True,
                        "enabledUploadAttachment": True,
                        "initialState": ""
                    },
                    "usePluginInfoFields": [],
                    "isTagRemovalEnabled": True,
                    "isTicketingConnector": True,
                    "autoUrba": autourba
                }
            }
        connectorcreateurl=self.api_base_url.format(str(client_id))+'/{}'.format(str(cw_id))
        try:
            postconnectorcreate = self.request_handler.make_request(ApiRequestHandler.PUT, connectorcreateurl, body=postconnectorbody)
        except (RequestFailed,Exception) as e:
            print()
            print('There was an error in connector creation')
            print(e)
            exit()
        if postconnectorcreate.status_code == 200:
            populateitems_json = json.loads(postconnectorcreate.text)
            id=populateitems_json['id']
        else:
            print(postconnectorcreate.status_code)
        
        return id

    def update_cherwell_problem_connector(self,cw_id:int,cw_name:str,cw_username:str,cw_password:str,clientid_key:str,cw_url:str,autourba:bool=False,client_id:int=None):
        
        
        """
        Update cherwell connector type problem

        :param cw_id:                The Connector Id
        :type cw_id:                 int

        :param cw_name:       Cherwell connector name.
        :type  cw_name:       str

        :param cw_username:   Cherwell connector username.
        :type  cw_username:   str

        :param cw_password:   Cherwell connector password.
        :type  cw_password:    str

        :param clientid_key:   Cherwell connector client id key.
        :type  clientid_key:   str

        :param cw_url:   Cherwell connector url.
        :type  cw_url:   str

        :param autourba:  Switch to enable auto urba.
        :type  autourba:   bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON response from the platform is returned.
        :rtype:     dict

        :raises RequestFailed:
        """

        if client_id is None:
                client_id = self._use_default_client_id()[0]
        populateitembody={"username":cw_username,"password":cw_password,"url":cw_url,"clientIdKey":clientid_key,"type":Connectors.Type.CHERWELL}
        cherwellproblem_connector_populate=self.cherwellproblem_connector_populate(populateitembody)
        a={}
        choices={}
        dynamicdropdownfields={}
        dynamicdropdown=[]
        try:
            for i in range(len(cherwellproblem_connector_populate['dynamicDropDownFields'])):
                a[cherwellproblem_connector_populate['dynamicDropDownFields'][i]['value']]=i
                dynamicdropdownfields[cherwellproblem_connector_populate['dynamicDropDownFields'][i]['value']]={"connectorCredentials":{"username":cw_username,"password":cw_password,"url":cw_url,"clientIdKey":clientid_key},"type":"CHERWELL","busObId":cherwellproblem_connector_populate['dynamicDropDownFields'][i]["dependentKey"],"fieldId":cherwellproblem_connector_populate['dynamicDropDownFields'][i]["fieldValue"],"fieldName":cherwellproblem_connector_populate['dynamicDropDownFields'][i]["value"],"fields":[]}
                if cherwellproblem_connector_populate['dynamicDropDownFields'][i]['parentField']!="":
                    j=a[cherwellproblem_connector_populate['dynamicDropDownFields'][i]['parentField']]
                    while(True):
                        b={"dirty":"true","displayName":cherwellproblem_connector_populate['dynamicDropDownFields'][j]['value'],"fieldId":cherwellproblem_connector_populate['dynamicDropDownFields'][j]["fieldValue"],"value":""}
                        dynamicdropdownfields[cherwellproblem_connector_populate['dynamicDropDownFields'][i]['value']]['fields'].append(b)
                        if cherwellproblem_connector_populate['dynamicDropDownFields'][j]['parentField']!="":
                            j=a[cherwellproblem_connector_populate['dynamicDropDownFields'][j]['parentField']]
                        else:
                            break
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        enabled=[]

        for index in range(len(cherwellproblem_connector_populate["supportedDescriptionFields"])):
            print(f"Index Number - {index} - {cherwellproblem_connector_populate['supportedDescriptionFields'][index]['value']}:")
            enabled.append({"key":cherwellproblem_connector_populate['supportedDescriptionFields'][index]['value'],"enabled":False})
            lockedfieldchoice=[]
        try:
            temp=input('Please enter the support description fields seperated by commas').split(',')
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        for i in temp:
            enabled[int(i)]['enabled']=True
        for key in dynamicdropdownfields:
                    if dynamicdropdownfields[key]['fields']!=[]:
                        for i in range(len(dynamicdropdownfields[key]['fields'])):
                            for j in choices:  
                                if dynamicdropdownfields[key]['fields'][i]['displayName']==j:
                                    dynamicdropdownfields[key]['fields'][i]['value']=choices[j]
                    fieldlookup=self.api_base_url.format(str(client_id))+"/populate/ticketType/Problem/fieldvalueslookup"
                    body=dynamicdropdownfields[key]
                    try:
                        fieldvalueslookup = self.request_handler.make_request(ApiRequestHandler.POST, fieldlookup, body=dynamicdropdownfields[key])
                    except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
                    fieldvalueslookup=json.loads(fieldvalueslookup.text)
                    for i in range(len(fieldvalueslookup['values'])):
                        print(f"Index Number - {i} - {fieldvalueslookup['values'][i]}")
                    try:
                        k=int(input(f'Please enter {key}:'))
                        choices[key]=fieldvalueslookup['values'][k]
                        dynamicdropdown.append({ "displayValue":key,"value":fieldvalueslookup['values'][k],"key":dynamicdropdownfields[key]["fieldId"]})
                    except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        optionaldropdownlist={}
        for i in range(len(cherwellproblem_connector_populate["optionalDropdownList"])):
            a[cherwellproblem_connector_populate["optionalDropdownList"][i]["label"]]=i
            optionaldropdownlist[cherwellproblem_connector_populate["optionalDropdownList"][i]['value']]={"connectorCredentials":{"username":cw_username,"password":cw_password,"url":cw_url,"clientIdKey":clientid_key},"type":"CHERWELL","busObId":cherwellproblem_connector_populate["optionalDropdownList"][i]["dependentKey"],"fieldId":cherwellproblem_connector_populate["optionalDropdownList"][i]["fieldValue"],"fieldName":cherwellproblem_connector_populate["optionalDropdownList"][i]["value"],"fields":[]}
        fieldlookup=self.api_base_url.format(str(client_id))+"/populate/ticketType/Problem/fieldvalueslookup"
        try:
            status = self.request_handler.make_request(ApiRequestHandler.POST, fieldlookup, body=optionaldropdownlist["Status"])
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        extradata={}
        status=json.loads(status.text)
        for index in range(len(status['values'])):
            print(f"Index Number - {index} - {status['values'][index]}:")
        lockedfieldchoice=[]
        try:
            temp=input('Please enter the index number of ticket sync state in comma seperated values').split(',')
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        for i in temp:
            lockedfieldchoice.append(status['values'][i])
        try:
            extradata["closeStatusesOfTicketToUpdate"]=lockedfieldchoice
            extradata["closedStateKey"]=status['values'][int(input('Enter the index number of close status field that you want to select:'))]
            extradata["closedStateLabel"]=extradata["closedStateKey"]
            dynamicFieldDetailValue=[]
            fieldslist=["dynamicFieldDetailValue","tagTypeDefaultOptions","slaDateFieldOptions","lockedFields"]
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        try:
            for fields in fieldslist:
                extradata[fields]=[]
                if fields=="dynamicFieldDetailValue":
                    for i in range(len(cherwellproblem_connector_populate[fields])):
                        a=input(f'Please enter a value for {cherwellproblem_connector_populate[fields][i]["label"]}')
                        dynamicFieldDetailValue.append({"displayValue":cherwellproblem_connector_populate[fields][i]['label'],"value":a,"key":cherwellproblem_connector_populate[fields][i]["fieldValue"]})
                elif fields=="lockedFields":
                    for i in range(len(cherwellproblem_connector_populate[fields])):
                        print(f'{i}-{cherwellproblem_connector_populate[fields][i]}')
                    lockedfieldchoice=[]
                    temp=input('Please enter the index number of the locked fields that you want to select in comma seperated values').split(',')
                    for i in temp:
                        lockedfieldchoice.append(cherwellproblem_connector_populate[fields][i]['value'])
                    extradata[fields]=lockedfieldchoice
                else:
                    for i in range(len(cherwellproblem_connector_populate[fields])):
                        print(f"Index Number - {i} - {cherwellproblem_connector_populate[fields][i]['displayValue']}")
                    extradata[fields]=cherwellproblem_connector_populate[fields][int(input(f'Please enter the index number for {fields}:'))]

            postconnectorbody={
                    "name": cw_name,
                    "type": Connectors.Type.CHERWELL,
                    "schedule": {
                        "enabled": True,
                        "type": "DAILY",
                        "hourOfDay": 0
                    },
                    "attributes": {
                        "username": cw_username,
                        "password": cw_password,
                        "clientIdKey": clientid_key
                    },
                    "connection": {
                        "url": cw_url
                    },
                    "connectorField": {
                        "type": Connectors.Type.CHERWELL,
                        "clientIdKey": clientid_key,
                        "ticketType": {
                            "displayValue": "Problem",
                            "value": "Problem"
                        },
                        "descriptionFields": enabled
                        ,
                        "dynamicDropdownFields": dynamicdropdown,
                        "dynamicFieldDetailValue": dynamicFieldDetailValue,
                        "optionalMandatoryFieldDetailValue": [],
                        "lockedFields": lockedfieldchoice,
                        "slaDateField":extradata["slaDateFieldOptions"]["displayValue"],"tagTypeDefaultValue":extradata["tagTypeDefaultOptions"]["displayValue"],
                        "connectorSettings": {
                            "closeFindingsOnTicketCloseEnabled": False,
                            "closeStatusesOfTicketToUpdate": ','.join(extradata['closeStatusesOfTicketToUpdate']),
                            "closeTicketOnFindingsCloseEnabled": False,
                            "closedStateKey":(extradata['closedStateKey']),
                            "closedStateLabel": extradata['closedStateKey'],
                            "enabledTagRemoval": True,
                            "enabledUploadAttachment": True,
                            "initialState": ""
                        },
                        "usePluginInfoFields": [],
                        "isTagRemovalEnabled": True,
                        "isTicketingConnector": True,
                        "autoUrba": autourba
                    }
                }
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        connectorcreateurl=self.api_base_url.format(str(client_id))+'/{}'.format(str(cw_id))
        try:
            postconnectorcreate = self.request_handler.make_request(ApiRequestHandler.PUT, connectorcreateurl, body=postconnectorbody)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        if postconnectorcreate.status_code == 200:
            populateitems_json = json.loads(postconnectorcreate.text)
            id=populateitems_json['id']
        
        return id

    def update_cherwell_makerequest_connector(self,cw_id:int,cw_name:str,cw_username:str,cw_password:str,clientid_key:int,cw_url:str,autourba:bool=False,client_id:int=None):

        """
        Updates an existing cherwell connector type make request

        :param cw_id:                The Connector Id
        :type cw_id:                 int

        :param cw_name:       Cherwell connector name.
        :type  cw_name:       str

        :param cw_username:   Cherwell connector username.
        :type  cw_username:   str

        :param cw_password:   Cherwell connector password.
        :type  cw_password:    str

        :param clientid_key:   Cherwell connector client id key.
        :type  clientid_key:   str

        :param cw_url:   Cherwell connector url.
        :type  cw_url:   str

        :param autourba:  Switch to enable auto urba.
        :type  autourba:   bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON response from the platform is returned.
        :rtype:     dict

        :raises RequestFailed:
        """

        if client_id is None:
                client_id = self._use_default_client_id()[0]
        populateitembody={"username":cw_username,"password":cw_password,"url":cw_url,"clientIdKey":clientid_key,"type":Connectors.Type.CHERWELL}
        cherwellmakerequest_connector_populate=self.cherwellmakerequest_connector_populate(populateitembody)
        a={}
        choices={}
        dynamicdropdownfields={}
        dynamicdropdown=[]
        try:
            for i in range(len(cherwellmakerequest_connector_populate['dynamicDropDownFields'])):
                a[cherwellmakerequest_connector_populate['dynamicDropDownFields'][i]['value']]=i
                dynamicdropdownfields[cherwellmakerequest_connector_populate['dynamicDropDownFields'][i]['value']]={"connectorCredentials":{"username":cw_username,"password":cw_password,"url":cw_url,"clientIdKey":clientid_key},"type":"CHERWELL","busObId":cherwellmakerequest_connector_populate['dynamicDropDownFields'][i]["dependentKey"],"fieldId":cherwellmakerequest_connector_populate['dynamicDropDownFields'][i]["fieldValue"],"fieldName":cherwellmakerequest_connector_populate['dynamicDropDownFields'][i]["value"],"fields":[]}
                if cherwellmakerequest_connector_populate['dynamicDropDownFields'][i]['parentField']!="":
                    j=a[cherwellmakerequest_connector_populate['dynamicDropDownFields'][i]['parentField']]
                    while(True):
                        b={"dirty":"true","displayName":cherwellmakerequest_connector_populate['dynamicDropDownFields'][j]['value'],"fieldId":cherwellmakerequest_connector_populate['dynamicDropDownFields'][j]["fieldValue"],"value":""}
                        dynamicdropdownfields[cherwellmakerequest_connector_populate['dynamicDropDownFields'][i]['value']]['fields'].append(b)
                        if cherwellmakerequest_connector_populate['dynamicDropDownFields'][j]['parentField']!="":
                            j=a[cherwellmakerequest_connector_populate['dynamicDropDownFields'][j]['parentField']]
                        else:
                            break
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        enabled=[]
        for index in range(len(cherwellmakerequest_connector_populate["supportedDescriptionFields"])):
            print(f"Index Number - {index} - {cherwellmakerequest_connector_populate['supportedDescriptionFields'][index]['value']}:")
            enabled.append({"key":cherwellmakerequest_connector_populate['supportedDescriptionFields'][index]['value'],"enabled":False})
            lockedfieldchoice=[]
        try:
            temp=input('Please enter the supported description fields seperated by commas').split(',')
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        for i in temp:
            enabled[int(i)]['enabled']=True
        for key in dynamicdropdownfields:
                    if dynamicdropdownfields[key]['fields']!=[]:
                        for i in range(len(dynamicdropdownfields[key]['fields'])):
                            for j in choices:  
                                if dynamicdropdownfields[key]['fields'][i]['displayName']==j:
                                    dynamicdropdownfields[key]['fields'][i]['value']=choices[j]
                    fieldlookup=self.api_base_url.format(str(client_id))+"/populate/ticketType/ChangeRequest/fieldvalueslookup"
                    body=dynamicdropdownfields[key]
                    try:
                        fieldvalueslookup = self.request_handler.make_request(ApiRequestHandler.POST, fieldlookup, body=dynamicdropdownfields[key])
                    except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
                    fieldvalueslookup=json.loads(fieldvalueslookup.text)
                    for i in range(len(fieldvalueslookup['values'])):
                        print(f"Index Number - {i} - {fieldvalueslookup['values'][i]}")
                    try:
                        k=int(input(f'Please enter {key}:'))
                    except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
                    choices[key]=fieldvalueslookup['values'][k]
                    dynamicdropdown.append({ "displayValue":key,"value":fieldvalueslookup['values'][k],"key":dynamicdropdownfields[key]["fieldId"]})

        optionaldropdownlist={}
        for i in range(len(cherwellmakerequest_connector_populate["optionalDropdownList"])):
            a[cherwellmakerequest_connector_populate["optionalDropdownList"][i]["label"]]=i
            optionaldropdownlist[cherwellmakerequest_connector_populate["optionalDropdownList"][i]['value']]={"connectorCredentials":{"username":cw_username,"password":cw_password,"url":cw_url,"clientIdKey":clientid_key},"type":"CHERWELL","busObId":cherwellmakerequest_connector_populate["optionalDropdownList"][i]["dependentKey"],"fieldId":cherwellmakerequest_connector_populate["optionalDropdownList"][i]["fieldValue"],"fieldName":cherwellmakerequest_connector_populate["optionalDropdownList"][i]["value"],"fields":[]}
        fieldlookup=self.api_base_url.format(str(client_id))+"/populate/ticketType/ChangeRequest/fieldvalueslookup"
        try:
            status = self.request_handler.make_request(ApiRequestHandler.POST, fieldlookup, body=optionaldropdownlist["Status"])
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        extradata={}
        status=json.loads(status.text)
        for index in range(len(status['values'])):
            print(f"Index Number - {index} - {status['values'][index]}:")
        lockedfieldchoice=[]
        try:
            temp=input('Enter the index number of ticket sync state that you want to select seperated by commas:').split(',')
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        for i in temp:
            lockedfieldchoice.append(status['values'][int(i)])
        extradata["closeStatusesOfTicketToUpdate"]=lockedfieldchoice
        try:
            extradata["closedStateKey"]=status['values'][int(input('Enter the index number of close status field that you want to select:'))]
        except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        extradata["closedStateLabel"]=extradata["closedStateKey"]
        dynamicFieldDetailValue=[]
        fieldslist=["dynamicFieldDetailValue","tagTypeDefaultOptions","slaDateFieldOptions","lockedFields"]
        for fields in fieldslist:
            extradata[fields]=[]
            if fields=="dynamicFieldDetailValue":
                for i in range(len(cherwellmakerequest_connector_populate[fields])):
                    try:
                        a=input(f'Please enter a value for {cherwellmakerequest_connector_populate[fields][i]["label"]}')
                    except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
                    dynamicFieldDetailValue.append({"displayValue":cherwellmakerequest_connector_populate[fields][i]['label'],"value":a,"key":cherwellmakerequest_connector_populate[fields][i]["fieldValue"]})
            elif fields=="lockedFields":
                for i in range(len(cherwellmakerequest_connector_populate[fields])):
                    print(f'{i}-{cherwellmakerequest_connector_populate[fields][i]}')
                lockedfieldchoice=[]
                try:
                    temp=input('Please enter the locked fields you want seperated by commas').split(',')
                except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
                for i in temp:
                    lockedfieldchoice.append(cherwellmakerequest_connector_populate[fields][int(i)]['value'])
                extradata[fields]=lockedfieldchoice
            else:
                for i in range(len(cherwellmakerequest_connector_populate[fields])):
                    print(f"Index Number - {i} - {cherwellmakerequest_connector_populate[fields][i]['displayValue']}")
                try:
                    extradata[fields]=cherwellmakerequest_connector_populate[fields][int(input(f'Please enter the index number for {fields}:'))]
                except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()


        postconnectorbody={
                "name": cw_name,
                "type": Connectors.Type.CHERWELL,
                "schedule": {
                    "enabled": True,
                    "type": "DAILY",
                    "hourOfDay": 0
                },
                "attributes": {
                    "username": cw_username,
                    "password": cw_password,
                    "clientIdKey": clientid_key
                },
                "connection": {
                    "url": cw_url
                },
                "connectorField": {
                    "type": Connectors.Type.CHERWELL,
                    "clientIdKey": clientid_key,
                    "ticketType": {
                        "displayValue": "Change Request",
                        "value": "ChangeRequest"
                    },
                    "descriptionFields": enabled
                    ,
                    "dynamicDropdownFields": dynamicdropdown,
                    "dynamicFieldDetailValue": dynamicFieldDetailValue,
                    "optionalMandatoryFieldDetailValue": [],
                    "lockedFields": lockedfieldchoice,
                    "slaDateField":extradata["slaDateFieldOptions"]["displayValue"],"tagTypeDefaultValue":extradata["tagTypeDefaultOptions"]["displayValue"],
                    "connectorSettings": {
                        "closeFindingsOnTicketCloseEnabled": False,
                        "closeStatusesOfTicketToUpdate": ','.join(extradata['closeStatusesOfTicketToUpdate']),
                        "closeTicketOnFindingsCloseEnabled": False,
                        "closedStateKey":(extradata['closedStateKey']),
                        "closedStateLabel": extradata['closedStateKey'],
                        "enabledTagRemoval": True,
                        "enabledUploadAttachment": True,
                        "initialState": ""
                    },
                    "usePluginInfoFields": [],
                    "isTagRemovalEnabled": True,
                    "isTicketingConnector": True,
                    "autoUrba": autourba
                }
            }
        connectorcreateurl=self.api_base_url.format(str(client_id))+'/{}'.format(str(cw_id))
        try:
            postconnectorcreate = self.request_handler.make_request(ApiRequestHandler.PUT, connectorcreateurl, body=postconnectorbody)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        if postconnectorcreate.status_code == 201:
            populateitems_json = json.loads(postconnectorcreate.text)
            id=populateitems_json['id']
        
        return id

    def update_checkmarx_osa_connector(self, connector_id:int,conn_name:str,  conn_url:str, username:str, password:str, conn_status:bool, schedule_freq:str, network_id:int, auto_urba:bool=True, client_id:int=None, **kwargs): 
        """
        Update a new Checkmarx OSA scanning connector.

        
        :param connector_id:    The connector ID.
        :type  connector_id:    int

        :param conn_name:       The connector name.
        :type conn_name:        str

        :type  conn_type:       str

        :param conn_url:        The URL for the connector to communicate with.
        :type  conn_url:        str

        :param username:        The username to use for connector authentication.
        :type  username:        str

        :param password:        The password to use for connector authentication.
        :type  password:        str

        :param conn_status:     Schedule enabled or disabled
        :type  conn_status:     bool

        :param schedule_freq:   The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                        Connectors.ScheduleFreq.WEEKLY,
                                                                        Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:   str

        :param network_id:      The network ID
        :type  network_id:      int

        :param auto_urba:       Automatically run URBA after connector runs?
        :type  auto_urba:       bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword ssl_cert:      Optional SSL certificate.
        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run, Type : Str, Available values : 1-7
        :keyword day_of_month:  The day of the month the connector should run, Type : Str, Available values : 1-31
        :keyword createAssetsIfZeroVulnFoundInFile: Create assets if zero vulnerability found in file. Type : Bool, Available values : True or False
        :keyword maxDaysToRetrieve: Max days to retrieve scan data. Type : Integer, Available values : 30,60,90,180,365

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0] 

        ssl_cert = kwargs.get('ssl_cert', None)
        hour_of_day = kwargs.get('hour_of_day', None)
        day_of_week = kwargs.get('day_of_week', None)
        day_of_month = kwargs.get('day_of_month', None)
        createAssetsIfZeroVulnFoundInFile = kwargs.get('createAssetsIfZeroVulnFoundInFile', None)
        maxDaysToRetrieve = kwargs.get('maxDaysToRetrieve', None)

        project_selection = input("Select \"ALL\" projects in checkmarx? Please enter 'y' if YES or enter 'n' if NO: ")
        if project_selection == 'n':
            print("\n[+] As you selected No, these are the list of projects available in checkmarx:\n")
            populate_url = self.api_base_url.format(str(client_id)) + "/populate"
            connector_populate_body = {
                "type": Connectors.Type.CHECKMARX_OSA,
                "username": username,
                "password": password,
                "url": conn_url,
                "projection": "internal"
            }	
            try:
                cred_authorize = self.request_handler.make_request(ApiRequestHandler.POST, populate_url, body=connector_populate_body)
            except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()            

            if cred_authorize.status_code == 200:
                cred_authorize_json = json.loads(cred_authorize.text) 
                for ind in range(len(cred_authorize_json['projectList'])):
                    print(f"Index Number - {ind} - {cred_authorize_json['projectList'][ind]['displayValue']}")
                print()
                try:
                    project_indexes_list = list(map(int, input("Enter the index numbers of projects that you want to select. Enter index numbers as comma separated values if multiple projects need to be selected: ").split(",")))
                except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
                project_selected_list = []
                for value in project_indexes_list:
                    project_selected_list.append(cred_authorize_json['projectList'][value]['value'])
                project_selected_string = ",".join(project_selected_list)
                print(project_selected_string)
        elif project_selection == 'y':
            project_selected_string = "ALL"

        connector_create_url = self.api_base_url.format(str(client_id)) + f"/{str(connector_id)}"

        if maxDaysToRetrieve is None:
            max_days = 30

        connector_create_body = {
            "type": Connectors.Type.CHECKMARX_OSA,
            "name": conn_name,
            "networkId": network_id,
            "connection": {
                "url": conn_url
            },
            "schedule": {
            },
            "attributes": {
                "username": username,
                "password": password,
                "maxDaysToRetrieve": max_days,
                "enableFortifyToPullFPRIntegratedFile": True,
                "checkmarxChosenProjectListToPull": project_selected_string,
                "findingTypeTobePulled": [
                    "vulnerabilities",
                    "licenses"
                ]
            },
            "id": connector_id,
            "autoUrba": auto_urba
        }

        if ssl_cert is not None:
            connector_create_body['connection'].update(sslCertificates=ssl_cert)

        if schedule_freq == Connectors.ScheduleFreq.DAILY:

            if hour_of_day is None:
                hour_of_day = 0

            connector_schedule = {
                "enabled": conn_status,
                "type": schedule_freq,
                "hourOfDay": hour_of_day,
                "daysOfWeek": "1",
                "daysOfMonth": "1",
                "cronSchdule":None
            }

        elif schedule_freq == Connectors.ScheduleFreq.WEEKLY:

            if day_of_week is None:
                day_of_week = "1"

            if hour_of_day is None:
                hour_of_day = 0

            connector_schedule = {
                "enabled": conn_status,
                "type": schedule_freq,
                "hourOfDay": hour_of_day,
                "daysOfWeek": day_of_week,
                "daysOfMonth": "1",
                "cronSchdule":None
            }

        elif schedule_freq == Connectors.ScheduleFreq.MONTHLY:

            if day_of_month is None:
                day_of_month = "1"

            if hour_of_day is None:
                hour_of_day = 0

            connector_schedule = {
                "enabled": conn_status,
                "type": schedule_freq,
                "hourOfDay": hour_of_day,
                "daysOfWeek": "1",
                "daysOfMonth": day_of_month,
                "cronSchdule":None
            }

        else:
            raise ValueError("Schedule freq. should be DAILY, WEEKLY, or MONTHLY.")

        connector_create_body.update(schedule=connector_schedule)

        if createAssetsIfZeroVulnFoundInFile is None:
            create_asset = True
        
        connector_create_body['attributes'].update(createAssetsIfZeroVulnFoundInFile=create_asset)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, connector_create_url, body=connector_create_body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id  

    def update_checkmarx_sast_connector(self, connector_id:int,conn_name:str,  conn_url:str, username:str, password:str, conn_status:bool, schedule_freq:str, network_id:int, auto_urba:bool=True, client_id:int=None, **kwargs): 
        """
        Update a new Checkmarx SAST scanning connector.

        :param connector_id:    The connector ID.
        :type  connector_id:    int

        :param conn_name:       The connector name.
        :type conn_name:        str

        :type  conn_type:       str

        :param conn_url:        The URL for the connector to communicate with.
        :type  conn_url:        str
        

        :param username:        The username to use for connector authentication.
        :type  username:        str

        :param password:        The password to use for connector authentication.
        :type  password:        str

        :param conn_status:     Schedule enabled or disabled
        :type  conn_status:     bool


        :param schedule_freq:   The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                        Connectors.ScheduleFreq.WEEKLY,
                                                                        Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:   str

        :param network_id:      The network ID
        :type  network_id:      int

        :param auto_urba:       Automatically run URBA after connector runs?
        :type  auto_urba:       bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword ssl_cert:      Optional SSL certificate.
        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run, Type : Str, Available values : 1-7
        :keyword day_of_month:  The day of the month the connector should run, Type : Str, Available values : 1-31
        :keyword createAssetsIfZeroVulnFoundInFile: Create assets if zero vulnerability found in file. Type : Bool, Available values : True or False
        :keyword maxDaysToRetrieve: Max days to retrieve scan data. Type : Integer, Available values : 30,60,90,180,365

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0] 

        ssl_cert = kwargs.get('ssl_cert', None)
        hour_of_day = kwargs.get('hour_of_day', None)
        day_of_week = kwargs.get('day_of_week', None)
        day_of_month = kwargs.get('day_of_month', None)
        createAssetsIfZeroVulnFoundInFile = kwargs.get('createAssetsIfZeroVulnFoundInFile', None)
        generateShortDescription = kwargs.get('generateShortDescription', None)        

        project_selection = input("Select \"ALL\" projects in checkmarx? Please enter 'y' if YES or enter 'n' if NO: ")
        if project_selection == 'n':
            print("\n[+] As you selected No, these are the list of projects available in checkmarx:\n")
            populate_url = self.api_base_url.format(str(client_id)) + "/populate"
            connector_populate_body = {
                "type": Connectors.Type.CHECKMARX_OSA,
                "username": username,
                "password": password,
                "url": conn_url,
                "projection": "internal"
            }	
            try:
                cred_authorize = self.request_handler.make_request(ApiRequestHandler.POST, populate_url, body=connector_populate_body)
            except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()           

            if cred_authorize.status_code == 200:
                cred_authorize_json = json.loads(cred_authorize.text) 
                for ind in range(len(cred_authorize_json['projectList'])):
                    print(f"Index Number - {ind} - {cred_authorize_json['projectList'][ind]['displayValue']}")
                print()
                try:
                    project_indexes_list = list(map(int, input("Enter the index numbers of projects that you want to select. Enter index numbers as comma separated values if multiple projects need to be selected: ").split(",")))
                except (Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
                project_selected_list = []
                for value in project_indexes_list:
                    project_selected_list.append(cred_authorize_json['projectList'][value]['value'])
                project_selected_string = ",".join(project_selected_list)
                print(project_selected_string)
        elif project_selection == 'y':
            project_selected_string = "ALL"

        connector_create_url = self.api_base_url.format(str(client_id)) + f"/{str(connector_id)}"

        if generateShortDescription is None:
            generate_short_description = True

        connector_create_body = {
            "type": Connectors.Type.CHECKMARX_SAST,
            "name": conn_name,
            "networkId": network_id,
            "attributes": {
                "username": username,
                "password": password,
                "checkmarxChosenProjectListToPull": project_selected_string,
                "generateShortDescription": generate_short_description
            },
            "connection": {
                "url": conn_url
            },
            "schedule": {
            },
            "id": connector_id,
            "autoUrba": auto_urba
        }

        if ssl_cert is not None:
            connector_create_body['connection'].update(sslCertificates=ssl_cert)

        if schedule_freq == Connectors.ScheduleFreq.DAILY:

            if hour_of_day is None:
                hour_of_day = 0

            connector_schedule = {
                "enabled": conn_status,
                "type": schedule_freq,
                "hourOfDay": hour_of_day,
                "daysOfWeek": "1",
                "daysOfMonth": "1",
                "cronSchdule":None
            }

        elif schedule_freq == Connectors.ScheduleFreq.WEEKLY:

            if day_of_week is None:
                day_of_week = "1"

            if hour_of_day is None:
                hour_of_day = 0

            connector_schedule = {
                "enabled": conn_status,
                "type": schedule_freq,
                "hourOfDay": hour_of_day,
                "daysOfWeek": day_of_week,
                "daysOfMonth": "1",
                "cronSchdule":None
            }

        elif schedule_freq == Connectors.ScheduleFreq.MONTHLY:

            if day_of_month is None:
                day_of_month = "1"

            if hour_of_day is None:
                hour_of_day = 0

            connector_schedule = {
                "enabled": conn_status,
                "type": schedule_freq,
                "hourOfDay": hour_of_day,
                "daysOfWeek": "1",
                "daysOfMonth": day_of_month,
                "cronSchdule":None
            }

        else:
            raise ValueError("Schedule freq. should be DAILY, WEEKLY, or MONTHLY.")

        connector_create_body.update(schedule=connector_schedule)

        if createAssetsIfZeroVulnFoundInFile is None:
            create_asset = True
        
        connector_create_body['attributes'].update(createAssetsIfZeroVulnFoundInFile=create_asset)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, connector_create_url, body=connector_create_body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id        

    def update_qualys_was_connector(self, connector_id:int, conn_name:str, conn_url:str, network_id:int, schedule_freq:str,
                                     username_or_access_key:str, password_or_secret_key:str, auto_urba=True, client_id=None, **kwargs):

        """
        Update an existing QUALYS was connector

        :param connector_id:            Connector ID to update
        :type  connector_id:            int

        :param conn_name:               The name for the connector
        :type  conn_name:               str

        :param conn_url:                The URL for the connector to communicate with.
        :type  conn_url:                str

        :param network_id:              The network ID
        :type  network_id:              int

        :param schedule_freq:           The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                                Connectors.ScheduleFreq.WEEKLY,
                                                                                Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:           str

        :param username_or_access_key:  The username or access key to be used
        :type  username_or_access_key:  str

        :param password_or_secret_key:  The password or secret key to be used
        :type  password_or_secret_key:  str

        :param auto_urba:               Indicates whether URBA should be automatically run after connector runs.
        :type  auto_urba:               bool

        :param client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:               int

        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_id = self.update(connector_id, Connectors.Type.QUALYS_WAS, conn_name, conn_url, network_id, schedule_freq,
                                      username_or_access_key, password_or_secret_key, auto_urba, client_id, **kwargs)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        return returned_id

    def update_qualys_vuln_connector(self, connector_id:int, conn_name:str, conn_url:str, network_id:int, schedule_freq:str,username_or_access_key:str, password_or_secret_key:str, auto_urba:bool=True, client_id:int=None, **kwargs):

        """
        Update an existing QUALYS VULN connector

        :param connector_id:            Connector ID to update
        :type  connector_id:            int

        :param conn_name:               The name for the connector
        :type  conn_name:               str

        :param conn_url:                The URL for the connector to communicate with.
        :type  conn_url:                str

        :param network_id:              The network ID
        :type  network_id:              int

        :param schedule_freq:           The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                                Connectors.ScheduleFreq.WEEKLY,
                                                                                Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:           str

        :param username_or_access_key:  The username or access key to be used
        :type  username_or_access_key:  str

        :param password_or_secret_key:  The password or secret key to be used
        :type  password_or_secret_key:  str

        :param auto_urba:               Indicates whether URBA should be automatically run after connector runs.
        :type  auto_urba:               bool

        :param client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:               int

        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_id = self.update(connector_id, Connectors.Type.QUALYS_VULN, conn_name, conn_url, network_id, schedule_freq,
                                      username_or_access_key, password_or_secret_key, auto_urba, client_id, **kwargs)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        return returned_id

    def update_qualys_asset_connector(self, connector_id:int, conn_name:str, conn_url:str, network_id:int, schedule_freq:str,username_or_access_key:str, password_or_secret_key:str, auto_urba:bool=True, client_id:int=None, **kwargs):

        """
        Update an existing QUALYS ASSET connector

        :param connector_id:            Connector ID to update
        :type  connector_id:            int

        :param conn_name:               The name for the connector
        :type  conn_name:               str

        :param conn_url:                The URL for the connector to communicate with.
        :type  conn_url:                str

        :param network_id:              The network ID
        :type  network_id:              int

        :param schedule_freq:           The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                                Connectors.ScheduleFreq.WEEKLY,
                                                                                Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:           str

        :param username_or_access_key:  The username or access key to be used
        :type  username_or_access_key:  str

        :param password_or_secret_key:  The password or secret key to be used
        :type  password_or_secret_key:  str

        :param auto_urba:               Indicates whether URBA should be automatically run after connector runs.
        :type  auto_urba:               bool

        :param client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:               int

        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_id = self.update(connector_id, Connectors.Type.QUALYS_ASSET, conn_name, conn_url, network_id, schedule_freq,
                                      username_or_access_key, password_or_secret_key, auto_urba, client_id, **kwargs)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        return returned_id

    def update_nexpose_connector(self, connector_id:int, conn_name:str, conn_url:str, network_id:int, schedule_freq:str,
                                 username_or_access_key:str, password_or_secret_key:str, auto_urba:bool=True, client_id:int=None, **kwargs):

        """
        Update an existing NEXPOSE connector

        :param connector_id:            Connector ID to update
        :type  connector_id:            int

        :param conn_name:               The name for the connector
        :type  conn_name:               str

        :param conn_url:                The URL for the connector to communicate with.
        :type  conn_url:                str

        :param network_id:              The network ID
        :type  network_id:              int

        :param schedule_freq:           The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                                Connectors.ScheduleFreq.WEEKLY,
                                                                                Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:           str

        :param username_or_access_key:  The username or access key to be used
        :type  username_or_access_key:  str

        :param password_or_secret_key:  The password or secret key to be used
        :type  password_or_secret_key:  str

        :param auto_urba:   Indicates whether URBA should be automatically run after connector runs.
        :type  auto_urba:   bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_id = self.update(connector_id, Connectors.Type.NEXPOSE, conn_name, conn_url, network_id, schedule_freq,
                                      username_or_access_key, password_or_secret_key, auto_urba, client_id, **kwargs)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        return returned_id

    def update_teneble_connector(self, connector_id:int, conn_name:str, conn_url:str, network_id:int, schedule_freq:str,
                                 username_or_access_key:str, password_or_secret_key:str, auto_urba:bool=True, client_id:int=None, **kwargs):

        """
        Update an existing TENEBLE SECURITY CENTER connector

        :param connector_id:            Connector ID to update
        :type  connector_id:            int

        :param conn_name:               The name for the connector
        :type  conn_name:               str

        :param conn_url:                The URL for the connector to communicate with.
        :type  conn_url:                str

        :param network_id:              The network ID
        :type  network_id:              int

        :param schedule_freq:           The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                                Connectors.ScheduleFreq.WEEKLY,
                                                                                Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:           str

        :param username_or_access_key:  The username or access key to be used
        :type  username_or_access_key:  str

        :param password_or_secret_key:  The password or secret key to be used
        :type  password_or_secret_key:  str

        :param auto_urba:               Indicates whether URBA should be automatically run after connector runs.
        :type  auto_urba:               bool

        :param client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:               int

        :keyword hour_of_day:   The time the connector should run. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Integer. 1-31

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            returned_id = self.update(connector_id, Connectors.Type.TENEBLE_SEC_CENTER, conn_name, conn_url, network_id, schedule_freq,
                                      username_or_access_key, password_or_secret_key, auto_urba, client_id, **kwargs)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        return returned_id

    def delete(self, connector_id:int, delete_tag:bool=True, client_id:int=None):

        """
        Delete a connector.

        :param connector_id:    The connector ID.
        :type  connector_id:    int

        :param delete_tag:      Force delete tag associated with connector?
        :type  delete_tag:      bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    Indicator reflecting whether or not the operation was successful.
        :rtype:     bool

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}".format(str(connector_id))

        body = {
            "deleteTag": delete_tag
        }

        try:
            self.request_handler.make_request(ApiRequestHandler.DELETE, url, body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        success = True

        return success

    def get_jobs(self, connector_id:int, page_num:int=0, page_size:int=150, csvdump:bool=False,client_id:int=None):

        """
        Get the jobs associated with a connector.

        :param connector_id:    The connector ID.
        :type  connector_id:    int

        :param page_num:        The page number of results to be returned.
        :type  page_num:        int

        :param page_size:       The number of results to return per page.
        :type page_size:        int

        
        :param csvdump:         Whether to dump the assessment history in a csv, true to dump and false to not dump
        :type  csvdump:         bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int
        

        :return:    The JSON response from the platform is returned.
        :rtype:     dict

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}/job".format(str(connector_id))

        params = {'page': page_num, 'size': page_size}

        if type(csvdump)!=bool:
            print('Please provide either true or false')
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url, params=params)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        jsonified_response = json.loads(raw_response.text)

        if csvdump==True:
            field_names = []
            for item in jsonified_response["_embedded"]["connectorJobs"][0].keys():
                field_names.append(item)
            try:
                with open('get_connectorjob.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    for item in jsonified_response["_embedded"]["connectorJobs"]:
                        writer.writerow(item)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)

        return jsonified_response

    def get_logs(self, connector_id:int, page_num:int=0, page_size:int=150,csvdump:bool=False, client_id:int=None):

        """
        Get the jobs associated with a connector.

        :param connector_id:    The connector ID.
        :type  connector_id:    int

        :param page_num:        The page number of results to be returned.
        :type  page_num:        int

        :param page_size:       The number of results to return per page.
        :type page_size:        int


        :param csvdump:         Whether to dump the assessment history in a csv, true to dump and false to not dump
        :type  csvdump:         bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON response from the platform is returned.
        :rtype:     dict

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}/log".format(str(connector_id))

        params = {'page': page_num, 'size': page_size}

        if type(csvdump)!=bool:
            print('Please provide either true or false')
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url, params=params)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        jsonified_response = json.loads(raw_response.text)
        if csvdump==True:
            field_names = []
            for item in jsonified_response["_embedded"]["connectorLogModels"][0].keys():
                field_names.append(item)
            try:
                with open('get_connectorlog.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    for item in jsonified_response["_embedded"]["connectorLogModels"]:
                        writer.writerow(item)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)



        return jsonified_response

    def update_schedule(self, connector_id:int, schedule_freq:str, enabled:bool, client_id:int=None, **kwargs):

        """
        Update the schedule of an existing Connector.

        :param connector_id:    Connector ID
        :type  connector_id:    int

        :param schedule_freq:   The frequency for the connector to run. Connectors.ScheduleFreq.DAILY,
                                                                        Connectors.ScheduleFreq.WEEKLY,
                                                                        Connectors.ScheduleFreq.MONTHLY
        :type  schedule_freq:   str

        :param enabled:         Enable connector?
        :type  enabled:         bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword hour_of_day:   The time the connector should run. Req. for DAILY, WEEKLY, and MONTHLY. Integer. 0-23.
        :keyword day_of_week:   The day of the week the connector should run.  Req. for WEEKLY. Integer. 1-7
        :keyword day_of_month:  The day of the month the connector should run. Req. for MONTHLY. Integer. 1-31

        :return:    The connector ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        hour_of_day = kwargs.get('hour_of_day', None)
        day_of_week = kwargs.get('day_of_week', None)
        day_of_month = kwargs.get('day_of_month', None)

        url = self.api_base_url.format(str(client_id)) + "/{}/schedule".format(str(connector_id))

        body = {
            "type": schedule_freq,
            "enabled": enabled
        }

        if schedule_freq == Connectors.ScheduleFreq.DAILY:

            if hour_of_day is None:
                raise ValueError("hour_of_day is required for a DAILY connector schedule.")

            body.update(hourOfDay=hour_of_day)

        elif schedule_freq == Connectors.ScheduleFreq.WEEKLY:

            if day_of_week is None and hour_of_day is None:
                raise ValueError("hour_of_day and day_of_week are required for a WEEKLY connector schedule.")

            if day_of_week is None:
                raise ValueError("day_of_week is required for a WEEKLY connector schedule.")

            if hour_of_day is None:
                raise ValueError("hour_of_day is required for a WEEKLY connector schedule.")

            body.update(hourOfDay=hour_of_day)
            body.update(dayOfWeek=day_of_week)

        elif schedule_freq == Connectors.ScheduleFreq.MONTHLY:

            if day_of_month is None and hour_of_day is None:
                raise ValueError("day_of_month and day_of_week are required for a WEEKLY connector schedule.")

            if day_of_month is None:
                raise ValueError("day_of_month is required for a WEEKLY connector schedule.")

            if hour_of_day is None:
                raise ValueError("hour_of_day is required for a WEEKLY connector schedule.")

            body.update(hourOfDay=hour_of_day)
            body.update(dayOfMonth=day_of_month)

        else:
            raise ValueError("schedule_freq should be one of DAILY, WEEKLY, or MONTHLY")

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        jsonified_response = json.loads(raw_response.text)
        returned_id = jsonified_response['id']

        return returned_id



    def itsm_get_fields_for_ticket_type(self, ticket_type:str, connector_url:str, connector_name:str, api_key:str, username:str='admin',client_id:int=None) -> json:
        """
        Get fields available for ticket type of a connector

        :param ticket_type: Ticket type
        :type ticket_type: str

        :param connector_url: ITSM Connector URL
        :type connector_url: str

        :param connector_name: ITSM Connector Name
        :type connector_name: str

        :param api_key: ITSM API Key
        :type api_key: str

        :param username: ITSM Username, defaults to 'admin'
        :type username: str, optional

        :param client_id: RS Client Id, defaults to None
        :type client_id: int, optional

        :return: Jsonified response
        :rtype: json

        """                      

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        
        url = self.api_base_url.format(str(client_id))+f'/ivanti/populate/ticketType/{ticket_type}'

        body = {
            "username": username,
            "password": api_key,
            "url": connector_url,
            "name": connector_name,
            "type": "IVANTIITSM"
        }
        
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url=url,body=body)
        except (RequestFailed,Exception) as e:
            print()
            print('Error in connector populate')
            print(e)
            exit()
        
        jsonified_response = json.loads(raw_response.text)

        return jsonified_response
                
    def ivanti_itsm_fetch_customers(self, itsm_url:str, itsm_api_key:str,  client_id:int=None) -> json:
        """
        Fetch ITSM available customers

        :param itsm_url: ITSM Connector URL
        :type itsm_url: str

        :param itsm_api_key: ITSM API Key
        :type itsm_api_key: str

        :param client_id: RS Client Id, defaults to None
        :type client_id: int, optional
        
        :return: Jsonified response
        :rtype: json

        """        
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+f'/api/v1/client/{client_id}/connector/ivanti/fetchCustomers/Frs_CompositeContract_Contacts'

        body = {
            'url': itsm_url,
            'restApiKey' : itsm_api_key
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There was an error fetching ticket information')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response  


    def ivanti_itsm_fetch_fieldValue_wrt_dependentField(self, ticket_type:str, itsm_url:str, itsm_api_key:str, current_field:str, dependent_field:str, dependent_field_value:str, client_id:int=None) -> json:
        """
        Fetch value for a ITSM connector field with respect to dependent field

        :param ticket_type: Ticket type
        :type ticket_type: str

        :param itsm_url: ITSM Connector URL
        :type itsm_url: str

        :param itsm_api_key: ITSM API Key
        :type itsm_api_key: str

        :param current_field: Field that should be queried for available options
        :type current_field: str
        :param dependent_field: Dependent field
        :type dependent_field: str

        :param dependent_field_value: Dependent field value
        :type dependent_field_value: str

        :param client_id: RS Client Id, defaults to None
        :type client_id: int, optional

        :return: Jsonified response
        :rtype: json

        """        
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+f'/api/v1/client/{client_id}/connector/ivanti/{ticket_type}/fetchValidatedFieldValue'

        body = {"connectorCredentials":{"restApiKey":itsm_api_key,"url":itsm_url},"actualField":current_field,"dependentField":dependent_field,"dependentFieldValue":dependent_field_value}

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There was an error fetching ticket information')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response  


    def ivanti_itsm_fetch_validation(self, body:str, ticket_type:str, client_id:int=None) -> json:
        """
        ITSM Connector field form validation

        :param body: Form validation request body
        :type body: str

        :param ticket_type: Ticket type
        :type ticket_type: str

        :param client_id: RS Client Id, defaults to None
        :type client_id: int, optional

        :return: Jsonified response
        :rtype: json

        """        
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+f"/api/v1/client/{client_id}/connector/ivanti/formValidation/ticketType/{ticket_type}"

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There was an error fetching ticket information')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response  


    def ivanti_itsm_fetch_releaseLink(self, itsm_url:str, itsm_api_key:str, client_id:int=None) -> json:
        """
        Fetch available options for Release Link field

        :param itsm_url: ITSM Connector URL
        :type itsm_url: str

        :param itsm_api_key: ITSM API Key
        :type itsm_api_key: str

        :param client_id: RS Client Id, defaults to None
        :type client_id: int, optional

        :return: Jsonified response
        :rtype: json

        """        
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+f'/api/v1/client/{client_id}/connector/ivanti/fetchCustomers/ReleaseProjects'

        body = {"restApiKey":itsm_api_key,"url":itsm_url}

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There was an error fetching ticket information')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response  


    def ivanti_itsm_fetch_requestorLink(self, itsm_url:str, itsm_api_key:str, client_id:int=None) -> json:
        """
        Fetch available options for Requestor Link field

        :param itsm_url: ITSM Connector URL
        :type itsm_url: str

        :param itsm_api_key: ITSM API Key
        :type itsm_api_key: str

        :param client_id: RS Client Id, defaults to None
        :type client_id: int, optional

        :return: Jsonified response
        :rtype: json

        """        
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+f'/api/v1/client/{client_id}/connector/ivanti/fetchCustomers/Employees'

        body = {"restApiKey":itsm_api_key,"url":itsm_url}

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('There was an error fetching ticket information')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response  


    def create_ivanti_itsm_connector(self, body:dict, client_id:int=None) -> json:
        """
        Create ITSM Connector

        :param body: Ticket request body
        :type body: dict

        :param client_id: RS Client Id, defaults to None
        :type client_id: int, optional

        :return: Jsonified response
        :rtype: json
        """        
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
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
