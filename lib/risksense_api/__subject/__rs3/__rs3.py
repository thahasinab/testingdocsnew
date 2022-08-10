""" *******************************************************************************************************************
|
|  Name        :  Rs3.py
|  Module      :  risksense_api
|  Description :  A class to be used for getting information on rs3 endpoint
|  Copyright   : (c) RiskSense, Inc.
|  License     : Apache-2.0 (http://www.apache.org/licenses/LICENSE-2.0)
|
******************************************************************************************************************* """

from http import client
import json
from .. import Subject
from ..._params import *
from ..._api_request_handler import *
import csv


class Rs3(Subject):

    """ Rs3 Class """

    def __init__(self, profile):

        """
        Initialization of Rs3 object.

        :param profile:     Profile Object
        :type  profile:     _profile

        """
        Subject.__init__(self, profile)
        self.rs3aggregate = self.profile.platform_url + "/api/v1/client/{}/rs3V11OverTime/aggregate"
        self.rs3simulate = self.profile.platform_url + "/api/v1/client/{}/simulate/rs3"


    def get_rs3overtimeaggregate(self,startdate:str,enddate:str,filters:list,csvdump:bool=False,client_id:int=None):
        """
        Gets rs3 aggregate score between dates

        param startdate: The start date from when rs3 score is needed,please mention date
        in YYY-MM-DD format
        type  startdate: date

        param enddate:  The end date till when rs3 score is needed,please mention date
        in YYY-MM-DD format
        type  enddate:  date

        param filters: filters to define for the rs3
        type  filters: list



        param client_id: client id , if none takes default client_id
        type client_id: int

        :return jsonified_response: The jsonified response from the platform
        :type  jsonified_response : dict

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.rs3aggregate.format(str(client_id))

        body = {
                    "startDate": startdate,
                    "endDate": enddate,
                    "filters": filters
                    }
        
        
        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')


        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,
        Exception) as  e:
            print('There seems to be an exception')
            print(e)
            exit()
    


        jsonified_response = json.loads(raw_response.text)

        if csvdump==True:
            field_names = []
            for item in jsonified_response['dataPoints'][0]:
                field_names.append(item)

            try:
                with open('rs3overtime.csv', 'w',newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    for item in jsonified_response['dataPoints']:
                        writer.writerow(item)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)
        
        return jsonified_response

    def get_rs3aggregate(self,search_filter:list,applymecheck:bool=True,csvdump:bool=False,client_id:int=None):
        """
        Gets rs3 aggregate score 

        param search_filter: Search filters for rs3 aggregate
        type  search_filter: list

        param applymecheck:  Apply manual exploit check for client rs3 with default value true
        type  applymecheck:  bool

        param csvdump: Dump the data in csv
        type  csvdump: bool

        param client_id: client id , if none takes default client_id
        type client_id: int

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url + "/api/v1/client/{}/rs3/aggregate?applyMeCheck={}".format(str(client_id),applymecheck)
        print(url)

        body = {
                "filters": search_filter,
                "projection": "basic",
                "sort": [
                    {
                    "field": "id",
                    "direction": "ASC"
                    }
                ],
                "page": 0,
                "size": 20
                }

        
        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')


        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,
        Exception) as  e:
            print('There seems to be an exception')
            print(e)
            exit()


        jsonified_response = json.loads(raw_response.text)

        if csvdump==True:
            field_names = []
            for item in jsonified_response.keys():
                field_names.append(item)
            try:
                with open('aggregate.csv', 'w',newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    for item,value in jsonified_response.items():
                        jsonified_response[item]=str(value) 
                    writer.writerow(jsonified_response)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)
        
        return jsonified_response

    def get_rs3historyaggregate(self,startdate:str,enddate:str,search_filter:list,csvdump:bool=False,client_id:int=None):
        """
        Gets rs3 aggregate history between dates

        param startdate: The start date from when rs3 score is needed
        type  startdate: date

        param enddate:  The end date till when rs3 score is needed
        type  enddate:  date

        param filters: filters to define for the rs3
        type  filters: list

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        param client_id: client id , if none takes default client_id
        type client_id: int

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url + "/api/v1/client/{}/rs3History/aggregate".format(str(client_id))

        body = {
                "startDate": startdate,
                "endDate": enddate,
                "filters": search_filter
                }
        
        
        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
    
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,
        Exception) as  e:
            print('There seems to be an exception')
            print(e)
            exit()


        jsonified_response = json.loads(raw_response.text)

        if csvdump==True:
            field_names = []
            for item in jsonified_response[0]:
                field_names.append(item)

            try:
                with open('rs3history.csv', 'w',newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    for item in jsonified_response:
                        writer.writerow(item)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)
        
        return jsonified_response

    def simulate_rs3(self,vrrCriticalMax:float,vrrHighMax:float,vrrMediumMax:float,vrrLowMax:float,findingCount:int,assetType:str,assetCriticality:int,assetCategory:str,client_id:int=None):
    
            """
            Simulate rs3 score based on the vrr,findingcount,asset data

            param vrrCriticalMax: The vrrCriticalMax info
            type  vrrCriticalMax: float

            param vrrHighMax:     The vrrhighmax info
            type  vrrHighMax:     float

            param vrrMediumMax:   The vrrMediumMax info
            type  vrrMediumMax:   float

            param vrrLowMax:     The vrrLowMax info
            type  vrrLowMax:     float

            param findingCount:     The number of findings
            type  findingCount:     int
            
            param assetType:     The type of asset either external or internal
            type  assetType:     str

            param assetCriticality:     The asset criticality
            type  assetType:            int

            param assetCategory:     The asset category
            type  assetCategory:     str

            param client_id: client id , if none takes default client_id
            type client_id: int

            """
            if client_id is None:
                client_id = self._use_default_client_id()[0]

            url = self.rs3simulate.format(str(client_id))

            body = {
                    "vrrCriticalMax": vrrCriticalMax,
                    "vrrHighMax": vrrHighMax,
                    "vrrMediumMax": vrrMediumMax,
                    "vrrLowMax": vrrLowMax,
                    "findingCount": findingCount,
                    "assetType": assetType,
                    "assetCriticality": assetCriticality,
                    "assetCategory": assetCategory
                    }
            try:
                raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
            except (RequestFailed,
            Exception) as  e:
                print('There seems to be an exception')
                print(e)
                exit()


            jsonified_response = json.loads(raw_response.text)

            
            return jsonified_response['rs3']

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