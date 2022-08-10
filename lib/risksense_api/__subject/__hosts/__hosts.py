""" *******************************************************************************************************************
|
|  Name        :  __hosts.py
|  Module      :  risksense_api
|  Description :  A class to be used for searching for and updating Hosts on the RiskSense Platform.
|  Copyright   :  (c) RiskSense, Inc.
|  License     :  Apache-2.0 (http://www.apache.org/licenses/LICENSE-2.0)
|
******************************************************************************************************************* """

import json
from re import I

from risksense_api import FilterSubject
from ..__exports import ExportFileType
from ..__exports import ExportRowNumbers
from ...__subject import Subject
from ..._params import *
from ..._api_request_handler import *
from ..__filters import Filters
from ..__exports import Exports
import zipfile
import sys
import csv
import pandas as pd



class Hosts(Subject):

    """ Hosts class """

    def __init__(self, profile):

        """
        Initialization of Hosts object.

        :param profile:     Profile Object
        :type  profile:     _profile

        """

        self.subject_name = "host"
        Subject.__init__(self, profile, self.subject_name)
        self.alt_base_api_url=self.profile.platform_url + "/api/v1/client/{}/search/{}"

    def downloadfilterinexport(self,filename,filters,client_id=None):
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
                self.exports.download_export(exportid,f"{filename}.csv")
        except(RequestFailed,MaxRetryError,StatusCodeError, ValueError):
                    print(ex)
                    print()
                    print("Unable to retrieve file. Exiting.")
                    sys.exit(1)
  


    def create(self, group_id:int, assessment_id:int, network_id:int, ip_address:str, hostname:str, subnet:str, disc_date:str, client_id:int=None, **kwargs):

        """
        Create a new host.

        :param group_id:        Group ID
        :type  group_id:        int

        :param assessment_id:   Assessment ID
        :type  assessment_id:   int

        :param network_id:      Network ID
        :type  network_id:      int

        :param ip_address:      IP Address of host
        :type  ip_address:      str

        :param hostname:        Hostname
        :type  hostname:        str

        :param subnet:          Subnet host belongs to
        :type  subnet:          str

        :param disc_date:       Discovered Date (Date formatted as "YYYY-MM-DD")
        :type  disc_date:       str

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :keyword manufactured_by:   str
        :keyword model:             str
        :keyword mac_address:       str
        :keyword location:          str
        :keyword managed_by:        str
        :keyword owned_by:          str
        :keyword supported_by:      str
        :keyword support_group:     str
        :keyword sys_id:            str
        :keyword operating_system:  str
        :keyword last_scan_date:    str     Date formatted as "YYYY-MM-DD"
        :keyword ferpa:             bool
        :keyword hipaa:             bool
        :keyword pci:               bool
        :keyword criticality:       int     1-5
        :keyword services:          list    A list of dicts, each dict containing "portNumber" (int), and "name" (str)
        :keyword os_scanner:        dict    A dict containing "name" (str), "family" (str), "class" (str),
                                            "vendor" (str), "product" (str), and "certainty" (int)
        :keyword cf_1:              str
        :keyword cf_2:              str
        :keyword cf_3:              str
        :keyword cf_4:              str
        :keyword cf_5:              str
        :keyword cf_6:              str
        :keyword cf_7:              str
        :keyword cf_8:              str
        :keyword cf_9:              str
        :keyword cf_10:             str
        :keyword am_1:              str
        :keyword am_2:              str
        :keyword am_3:              str
        :return:    The host ID on the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))

        manufactured_by = kwargs.get("manufactured_by", None)
        model = kwargs.get("model", None)
        scannerFirstDiscoveredOn=kwargs.get('scanner_first_discovered_on',None)
        scannerlastDiscoveredOn=kwargs.get('scanner_last_discovered_on',None)
        mac_address = kwargs.get("mac_address", None)
        location = kwargs.get("location", None)
        managed_by = kwargs.get("managed_by", None)
        owned_by = kwargs.get("owned_by", None)
        supported_by = kwargs.get("supported_by", None)
        support_group = kwargs.get("support_group", None)
        sys_id = kwargs.get("sys_id", None)
        operating_system = kwargs.get("operating_system", None)
        last_scan_date = kwargs.get("last_scan_date", None)
        ferpa_compliance = kwargs.get("ferpa_compliance", None)
        hipaa_compliance = kwargs.get("hipaa_compliance", None)
        pci_compliance = kwargs.get("pci_compliance", None)
        criticality = kwargs.get("criticality", None)
        services = kwargs.get("services", None)
        os_scanner = kwargs.get("os_scanner", None)
        cf_1 = kwargs.get("cf_1", None)
        cf_2 = kwargs.get("cf_2", None)
        cf_3 = kwargs.get("cf_3", None)
        cf_4 = kwargs.get("cf_4", None)
        cf_5 = kwargs.get("cf_5", None)
        cf_6 = kwargs.get("cf_6", None)
        cf_7 = kwargs.get("cf_7", None)
        cf_8 = kwargs.get("cf_8", None)
        cf_9 = kwargs.get("cf_9", None)
        cf_10 = kwargs.get("cf_10", None)
        am_1 = kwargs.get("am_1", None)
        am_2 = kwargs.get("am_2", None)
        am_3 = kwargs.get("am_3", None)
        lockCmdb=kwargs.get("lock_cmdb",None)
        body = {
            "groupId": group_id,
            "assessmentId": assessment_id,
            "networkId": network_id,
            "ipAddress": ip_address,
            "subnet": subnet,
            "hostName": hostname,
            "discoveredDate": disc_date,
            "scannerFirstDiscoveredOn":scannerFirstDiscoveredOn,
            "scannerLastDiscoveredOn":scannerlastDiscoveredOn,
            "services": services,
            "criticality": criticality,
            "operatingSystemScanner": os_scanner,
            "createCmdb": {
                "manufacturer": manufactured_by,
                "model_id": model,
                "mac_address": mac_address,
                "location": location,
                "managed_by": managed_by,
                "owned_by": owned_by,
                "supported_by": supported_by,
                "support_group": support_group,
                "sys_id": sys_id,
                "os": operating_system,
                "sys_updated_on": last_scan_date,
                "ferpa": ferpa_compliance,
                "hipaa": hipaa_compliance,
                "pci": pci_compliance,
                "cf_1": cf_1,
                "cf_2": cf_2,
                "cf_3": cf_3,
                "cf_4": cf_4,
                "cf_5": cf_5,
                "cf_6": cf_6,
                "cf_7": cf_7,
                "cf_8": cf_8,
                "cf_9": cf_9,
                "cf_10": cf_10,
                "am_1": am_1,
                "am_2": am_2,
                "am_3": am_3
            },
            "lockCmdb":lockCmdb
        }

        body = self._strip_nones_from_dict(body)
        body['createCmdb'] = self._strip_nones_from_dict(body['createCmdb'])

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
    
    def getdynamiccolumns(self,client_id:int=None):
        
        """
        Gets Dynamic columns for the hosts.

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

    def list_host_filter_fields(self,client_id:int=None):

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


    def delete(self, search_filters:list,csvdump:bool=False, client_id:int=None):

        """
        Delete hosts based on provided filters.

        :param search_filters:      A list of dictionaries containing filter parameters.
        :type  search_filters:      list

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The delete Job ID
        :rtype:     int

        :raises RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/delete"

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        body = {
            "filterRequest": {
                "filters": search_filters
            }
        }

        if csvdump==True:
            self.downloadfilterinexport('hostexportbeforedeletion',search_filters) 
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

    def get_groupby_host(self,client_id=None):

        """
        Get groupby values for app finding

        :param hostkey: The main key where other metric fields depend on
        :type  hostkey: Str

        :param metricfields:   The fields that will be populated,choose one or many of the following "App Finding Assessment Date","App Finding Apps Count","App Finding Open Count","App Finding Closed Count","App Finding VRR Critical Count","App Finding VRR High Count","App Finding VRR Medium Count","App Finding VRR Low Count","App Finding VRR Info Count","App Finding With Threat Count","App Finding Threat Count","App Finding CVE Count"
        :type  metricfields:   list
        
        :param filters:        The filters which will populate in groupby
        :type filters:         list

        :param sortorderfield: The order to sort the groupby values, please choose ASC for ascending and DESC for descending
        :type sortorderfield:  str

        :param client_id:      The client id , if none, default client id is taken
        :type  client_id:       int
        
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

        hostgroupbykeymetrics={}

        for i in range(len(jsonified_response['groupByFields'])):
            hostgroupbykeymetrics[jsonified_response['groupByFields'][i]['key']]=[jsonified_response['groupByFields'][i]['groupMetrics'][j]['key'] for j in range(len(jsonified_response['groupByFields'][i]['groupMetrics']))]

            
        return hostgroupbykeymetrics


    def post_groupby_host(self,filters:list=[],sortorder:str=None,csvdump:bool=False,client_id:int=None):

        """
        Get groupby values for app finding
        
        :param filters:        The filters which will populate in groupby
        :type filters:         list

        :param sortorderfield: The order to sort the groupby values, please choose ASC for ascending and DESC for descending
        :type sortorderfield:  str

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:      The client id , if none, default client id is taken
        :type  client_id:       int
        
        """
        if client_id is None:
                client_id = self._use_default_client_id()[0]

        url = url = self.api_base_url.format(str(client_id)) + "/group-by"

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

        hostslist=self.get_groupby_host()

        hostskeys=list(hostslist.keys())
        

        try:
            for i in range(len(hostskeys)):
                print(f'Index-{i},Key:{hostskeys[i]}')
            keymetric=hostskeys[int(input('Please enter the key for group by parameter:'))]
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
                "metricFields": hostslist[keymetric],
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
                with open('hostgroupby.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    for item in jsonified_response['data']:
                        writer.writerow(item)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)    
        return jsonified_response




    def update_hosts_attrs(self, search_filters:list,csvdump:bool=False, client_id:int=None, **kwargs):

        """
        Update an existing host.

        :param search_filters:      A list of dictionaries containing filter parameters.
        :type  search_filters:      list

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :keyword ip_address:        str     IP Address of host
        :keyword hostname:          str     Hostname
        :keyword subnet:            str     Subnet host belongs to
        :keyword discovered_date:   str     Date formatted as "YYYY-MM-DD"
        :keyword criticality:       int     1-5
        :keyword services:          list    A list of dicts, each dict containing "portNumber" (int), and "name" (str)
        :keyword os_scanner:        dict    A dict containing "name" (str), "family" (str), "class" (str),
                                            "vendor" (str), "product" (str), and "certainty" (int)

        :return:    The host ID on the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/update"

        ip_address = kwargs.get("ip_address", None)
        hostname = kwargs.get("hostname", None)
        subnet = kwargs.get("subnet", None)
        discovered_date = kwargs.get("discovered_date", None)
        criticality = kwargs.get("criticality", None)
        services = kwargs.get("services", None)
        os_scanner = kwargs.get("os_scanner", None)
        edit_cmdb= kwargs.get('edit_cmdb',None)


        body = {
            "filterRequest": {
                "filters": search_filters
            },
            "ipAddress": ip_address,
            "hostname": hostname,
            "subnet": subnet,
            "discoveredDate": discovered_date,
            "criticality": criticality,
            "services": services,
            "operatingSystemScanner": os_scanner,
            "editCmdb": edit_cmdb
             
            }
        body = self._strip_nones_from_dict(body)

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
            hostid={'jobid':[jsonified_response['id']]}
            df = pd.DataFrame(hostid)
            df.to_csv('hostupdated.csv',index=False)

        return job_id

    def update_hosts_cmdb(self, search_filters:list, client_id:int=None, **kwargs):

        """

        Updates host cmdb

        :param search_filters:      A list of dictionaries containing filter parameters.
        :type  search_filters:      list

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :keyword manufacturer:      str
        :keyword model_id:          str
        :keyword mac_address:       str
        :keyword location:          str
        :keyword managed_by:        str
        :keyword owned_by:          str
        :keyword supported_by:      str
        :keyword support_group:     str
        :keyword sys_id:            str
        :keyword os:                str
        :keyword last_scan_date:    str     Date formatted as "YYYY-MM-DD"
        :keyword asset_tag:         str
        :keyword ferpa:             bool
        :keyword hipaa:             bool
        :keyword pci:               bool
        :keyword cf_1:              str
        :keyword cf_2:              str
        :keyword cf_3:              str
        :keyword cf_4:              str
        :keyword cf_5:              str
        :keyword cf_6:              str
        :keyword cf_7:              str
        :keyword cf_8:              str
        :keyword cf_9:              str
        :keyword cf_10:             str
        :keyword am_1:              str
        :keyword am_2:              str
        :keyword am_3:              str

        :return:    The job ID
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/update"

        o_s = kwargs.get("os", None)
        manufacturer = kwargs.get("manufacturer", None)
        model_id = kwargs.get("model_id", None)
        location = kwargs.get("location", None)
        managed_by = kwargs.get("managed_by", None)
        owned_by = kwargs.get("owned_by", None)
        supported_by = kwargs.get("supported_by", None)
        support_group = kwargs.get("support_group", None)
        sys_id = kwargs.get('sys_id', None)
        mac_address = kwargs.get("mac_address", None)
        last_scan_date = kwargs.get("last_scan_date", None)
        asset_tag = kwargs.get("asset_tags", None)
        ferpa = kwargs.get("ferpa", None)
        hipaa = kwargs.get("hipaa", None)
        pci = kwargs.get("pci", None)
        cf_1 = kwargs.get("cf_1", None)
        cf_2 = kwargs.get("cf_2", None)
        cf_3 = kwargs.get("cf_3", None)
        cf_4 = kwargs.get("cf_4", None)
        cf_5 = kwargs.get("cf_5", None)
        cf_6 = kwargs.get("cf_6", None)
        cf_7 = kwargs.get("cf_7", None)
        cf_8 = kwargs.get("cf_8", None)
        cf_9 = kwargs.get("cf_9", None)
        cf_10 = kwargs.get("cf_10", None)
        am_1 = kwargs.get("am_1", None)
        am_2 = kwargs.get("am_2", None)
        am_3 = kwargs.get("am_3", None)   

        body = {
            "filterRequest": {
                "filters": search_filters
            },
            "editCmdb": {
                "manufacturer": manufacturer,
                "model_id": model_id,
                "location": location,
                "managed_by": managed_by,
                "owned_by": owned_by,
                "supported_by": supported_by,
                "support_group": support_group,
                "sys_id": sys_id,
                "mac_address": mac_address,
                "os": o_s,
                "sys_updated_on": last_scan_date,
                "asset_tag": asset_tag,
                "ferpa": ferpa,
                "hipaa": hipaa,
                "pci": pci,
                "cf_1": cf_1,
                "cf_2": cf_2,
                "cf_3": cf_3,
                "cf_4": cf_4,
                "cf_5": cf_5,
                "cf_6": cf_6,
                "cf_7": cf_7,
                "cf_8": cf_8,
                "cf_9": cf_9,
                "cf_10": cf_10,
                "am_1": am_1,
                "am_2": am_2,
                "am_3": am_3 
            }
        }

        body['editCmdb'] = self._strip_nones_from_dict(body['editCmdb'])

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

    def lock_hosts_cmdb(self, search_filters:list, client_id:int=None, **kwargs):

        """
        Locks hosts cmdb

        :param search_filters:      A list of dictionaries containing filter parameters.
        :type  search_filters:      list

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :keyword manufacturer:      str
        :keyword model_id:          str
        :keyword mac_address:       str
        :keyword location:          str
        :keyword managed_by:        str
        :keyword owned_by:          str
        :keyword supported_by:      str
        :keyword support_group:     str
        :keyword sys_id:            str
        :keyword os:                str
        :keyword last_scan_date:    str     Date formatted as "YYYY-MM-DD"
        :keyword asset_tag:         str
        :keyword ferpa:             bool
        :keyword hipaa:             bool
        :keyword pci:               bool
        :keyword cf_1:              str
        :keyword cf_2:              str
        :keyword cf_3:              str
        :keyword cf_4:              str
        :keyword cf_5:              str
        :keyword cf_6:              str
        :keyword cf_7:              str
        :keyword cf_8:              str
        :keyword cf_9:              str
        :keyword cf_10:             str
        :keyword am_1:              str
        :keyword am_2:              str
        :keyword am_3:              str

        :return:    The job ID
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/update"

        os = kwargs.get("os", None)
        manufacturer = kwargs.get("manufacturer", None)
        model_id = kwargs.get("model_id", None)
        location = kwargs.get("location", None)
        managed_by = kwargs.get("managed_by", None)
        owned_by = kwargs.get("owned_by", None)
        supported_by = kwargs.get("supported_by", None)
        support_group = kwargs.get("support_group", None)
        sys_id = kwargs.get('sys_id', None)
        mac_address = kwargs.get("mac_address", None)
        last_scan_date = kwargs.get("last_scan_date", None)
        asset_tag = kwargs.get("asset_tags", None)
        ferpa = kwargs.get("ferpa", None)
        hipaa = kwargs.get("hipaa", None)
        pci = kwargs.get("pci", None)
        cf_1 = kwargs.get("cf_1", None)
        cf_2 = kwargs.get("cf_2", None)
        cf_3 = kwargs.get("cf_3", None)
        cf_4 = kwargs.get("cf_4", None)
        cf_5 = kwargs.get("cf_5", None)
        cf_6 = kwargs.get("cf_6", None)
        cf_7 = kwargs.get("cf_7", None)
        cf_8 = kwargs.get("cf_8", None)
        cf_9 = kwargs.get("cf_9", None)
        cf_10 = kwargs.get("cf_10", None)
        am_1 = kwargs.get("am_1", None)
        am_2 = kwargs.get("am_2", None)
        am_3 = kwargs.get("am_3", None)   

        body = {
            "filterRequest": {
                "filters": search_filters
            },
            "lockCmdb": {
                "manufacturer": manufacturer,
                "model_id": model_id,
                "location": location,
                "managed_by": managed_by,
                "owned_by": owned_by,
                "supported_by": supported_by,
                "support_group": support_group,
                "sys_id": sys_id,
                "mac_address": mac_address,
                "os": os,
                "sys_updated_on": last_scan_date,
                "asset_tag": asset_tag,
                "ferpa": ferpa,
                "hipaa": hipaa,
                "pci": pci,
                "cf_1": cf_1,
                "cf_2": cf_2,
                "cf_3": cf_3,
                "cf_4": cf_4,
                "cf_5": cf_5,
                "cf_6": cf_6,
                "cf_7": cf_7,
                "cf_8": cf_8,
                "cf_9": cf_9,
                "cf_10": cf_10,
                "am_1": am_1,
                "am_2": am_2,
                "am_3": am_3 
            }
        }

        body['lockCmdb'] = self._strip_nones_from_dict(body['lockCmdb'])

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

    def get_single_search_page(self, search_filters, projection=Projection.BASIC, page_num=0, page_size=150,
                               sort_field=SortField.ID, sort_dir=SortDirection.ASC, client_id=None,csvdump=False):

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
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def search(self, search_filters:list, projection=Projection.BASIC, page_size=150,
               sort_field=SortField.ID, sort_dir=SortDirection.ASC, csvdump=False,client_id=None):

        """
        Searches for and returns hosts based on the provided filter(s) and other parameters.  Rather
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
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        page_range = range(0, num_pages)

        try:
            all_results = self._search(self.subject_name, self.get_single_search_page, page_range, **func_args)
        except (RequestFailed, Exception):
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

        if csvdump==True:
            self.downloadfilterinexport('hostdata',search_filters) 

        return all_results

    def get_count(self, search_filters, client_id=None):

        """
        Gets a count of hosts identified using the provided filter(s).

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The number of hosts identified using the provided filter(s).
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
    
    def add_tag(self, search_filters:list, tag_id:int,csvdump:bool=False, client_id:int=None):

        """
        Adds a tag to host(s).

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param tag_id:          ID of tag to tbe added to host(s).
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

        body = {
            "tagId": tag_id,
            "isRemove": False,
            "filterRequest": {
                "filters": search_filters
            }
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
        

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        if csvdump==True:
                self.downloadfilterinexport('addtag',search_filters) 
        return job_id

    def apply_system_filters(self, client_id=None,csvdump=False):

        """
        Adds a tag to host(s).

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param tag_id:          ID of tag to tbe added to host(s).
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
            for hostsystemfilter in filter['subjectFilters']:
                if hostsystemfilter['subject']=="host":
                    systemfilters[filter['name']]=hostsystemfilter["filterRequest"]
    
        systemfilterkeys=list(systemfilters.keys())
        i=0
        for key in systemfilterkeys:
            print(f'Index-{i},Key:{key}')
            i=i+1
        try:
            actualfilter=systemfilters[ systemfilterkeys[int(input('Please enter the key for group by parameter:'))]]
        except IndexError as ex:
                print()
                print('Please enter an index number from the above list')
                print(ex)
                exit()
        except (Exception) as e:
                print('There was an error fetching group by data')
                print(e)
                exit()


        response=self.search(actualfilter['filters'])

        if csvdump==False:
            self.downloadfilterinexport('hostsystemfilter',actualfilter['filters']) 

        return response

    def remove_tag(self, search_filters, tag_id, client_id=None,csvdump=False):

        """
        Removes a tag from host(s).

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param tag_id:          ID of tag to tbe removed from host(s).
        :type  tag_id:          int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The job ID is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/tag"

        if csvdump==True:
            self.downloadfilterinexport('hostremovetag',search_filters) 

        body = {
            "tagId": tag_id,
            "isRemove": True,
            "filterRequest": {
                "filters": search_filters
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


    def getexporttemplate(self,client_id:int=None):
        
        """
        Gets configurable export template for Hosts.

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

    def merge_host(self, search_filter,host_id_to_merge_to, client_id=None,csvdump=False):

        """
        Removes a tag from host(s).

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param tag_id:          ID of tag to tbe removed from host(s).
        :type  tag_id:          int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The job ID is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url+'/api/v1/client/{}/search/host/job/merge'.format(str(client_id))

        body = {"filterRequest":{"filters":search_filter},"sourceId":host_id_to_merge_to}


        if csvdump==True:
            self.downloadfilterinexport('hostmerge',search_filter) 

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

    def set_asset_criticality(self, filter:list,assetcriticality:int, csvdump:bool=False,client_id:int=None):

        """
        Sets asset criticality of the host.

        :param filter:  Search filters
        :type  filter:  list

        :param assetcriticality:  The asset criticality to provide.
        :type  assetcriticality:  int

        :param csvdump:  Dump the csv data.
        :type  csvdump:  bool

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The job ID is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/update"

        body = {"filterRequest":{"filters":filter},"criticality":assetcriticality}

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')

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
            self.downloadfilterinexport('assetcriticalityhost',filter) 

        return job_id

    def set_address_type(self, filter:list,addresstype:str,csvdump:bool=False, client_id:int=None):

        """
        Sets address type of the host.

        :param filter:  Search filters
        :type  filter:  list

        :param addresstype:  Provide external for external address and internal for internal
        :type  addresstype:  str

        :param csvdump:  Dump the csv data.
        :type  csvdump:  bool

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
            setaddresstype=False
        if addresstype.lower()=='external':
            setaddresstype=True

        body = {"filterRequest":{"filters":filter},"isExternal":setaddresstype}

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        
        
        if csvdump==True:
            self.downloadfilterinexport('addresstypessethost',filter) 
        
        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id



    def export(self, search_filters:list, file_name:str, row_count=ExportRowNumbers.ROW_ALL,file_type=ExportFileType.CSV, client_id:int=None):

        """
        Initiates an export job on the platform for host(s) based on the
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

    def network_move(self, search_filters, network_identifier, is_force_merge=False, client_id=None,csvdump=False):

        """
        Moves host(s) into a new network as specified.

        :param search_filters:      A list of dictionaries containing filter parameters.
        :type  search_filters:      list

        :param network_identifier:  Network ID
        :type  network_identifier:  int

        :param is_force_merge:      Force merge of hosts?
        :type  is_force_merge:      bool

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

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
            "targetNetworkId": network_identifier,
            "isForceMerge": is_force_merge
        }

        if csvdump==True:
            self.downloadfilterinexport('hostnetworkmove',search_filters) 

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

    def run_urba(self, search_filters:list, client_id:int=None):

        """
        Initiates the update of remediation by assessment for hosts specified in filter(s).

        :param search_filters:      A list of dictionaries containing filter parameters.
        :type  search_filters:      list

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

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

    def add_note(self, search_filters:list, new_note:str,csvdump:bool=False, client_id:int=None):

        """
        Adds a note to host(s) based on the filter(s) provided.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param new_note:        The note to be added to the host(s).
        :type  new_note:        str

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
            self.downloadfilterinexport('hostnotesadded',search_filters) 

        return job_id

    def get_model(self, client_id:int=None):

        """
        Get available projections and models for Hosts.

        :param client_id:   Client ID
        :type  client_id:   int

        :return:    Hosts projections and models are returned.
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

    def add_group(self, search_filter:list, group_ids:list,csvdump:bool=False, client_id:int=None):

        """
        Add host(s) to one or more groups.

        :param search_filter:   Search filter
        :type  search_filter:   list

        :param group_ids:       List of Group IDs to add to host(s).
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

        try:
            response = self._add_group(self.subject_name, search_filter, group_ids, client_id)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        if csvdump==True:
            self.downloadfilterinexport('hostgroupadd',search_filter) 

        return response

    def remove_group(self, search_filter:list, group_ids:list,csvdump:bool=False, client_id:int=None):

        """
        Remove host(s) from one or more groups.

        :param search_filter:   Search filter
        :type  search_filter:   list

        :param group_ids:       List of Group IDs to add to host(s).
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
        
        if csvdump==True:
            self.downloadfilterinexport('removegrouphost',search_filter) 

        try:
            response = self._remove_group(self.subject_name, search_filter, group_ids, client_id)
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()


        return response


"""
   Copyright 2021 RiskSense, Inc.
   
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
