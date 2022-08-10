""" *******************************************************************************************************************
|
|  Name        :  __sla.py
|  Description :  SLA
|  Project     :  risksense_api
|  Copyright   :  2022 RiskSense, Inc.
|  License     :  Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
******************************************************************************************************************* """

import json
from re import L
import sched
from ..__subject import Subject
from ..._params import *
from ..._api_request_handler import *
import csv
import pandas as pd

class SlaActionType:
    """Types of sla action type"""
    REMEDIATION_SLA= "REMEDIATION_SLA"

class SlaMatrix : 
    """Types of Sla Matrix"""
    STANDARD= {"1":[45,90,90,120,0],"2":[30,90,90,120,0],"3":[21,45,90,120,0],"4":[14,30,90,120,0],"5":[7,21,90,120,0]}
    ACCELERATED= {"1":[30,60,90,90,0],"2":[21,45,90,90,0],"3":[14,30,60,90,0],"4":[7,21,45,90,0],"5":[3,14,30,90,0]}
    AGGRESSIVE= {"1":[14,30,45,60,0],"2":[7,21,30,60,0],"3":[3,14,30,60,0],"4":[2,7,15,60,0],"5":[1,3,15,60,0]}

class SlaDataOperator:
    """Types of sla data operator"""
    MET_SLA="MET_SLA"
    OVERDUE="OVERDUE"
    MISSED_SLA="MISSED_SLA"
    WITHIN_SLA="WITHIN_SLA"

class SlaMatrixProfileType:
    """Types of Sla Matrix Profile Type"""
    STANDARD="STANDARD"
    AGGRESSIVE="AGGRESSIVE"
    ACCELERATED="ACCELERATED"
    CUSTOM="CUSTOM"

class TimeReference:
    """Types of sla time reference"""
    INGESTION_DATE = "INGESTION_DATE"
    DISCOVERED_DATE = "DISCOVERED_DATE"

class offsetbasis:
    VRR       = "VRR"
    SEVERITY  = "SEVERITY"

class Sla(Subject):


    def __init__(self, profile):

        """
        Initialization of sla object.

        :param profile:     Profile Object
        :type  profile:     _profile
        """

        self.subject_name = "sla"
        Subject.__init__(self, profile, self.subject_name)

    def create_sla(self,description:str,schedule_type:str='DAILY',hourofday:int=12,name:str='Remediation SLAs',csvdump:bool=False,client_id:int=None,**kwargs):
        
        """
        Creates an sla

        :param name:                    Name of playbook,note for system sla please mention Remediation SLAs
        :type  name:                    str

        :param description:             Provide description for sla
        :type  description:             str
            
        :param schedule_type:   Schedule Frequency (ScheduleFreq.DAILY, ScheduleFreq.WEEKLY,
                                                    ScheduleFreq.MONTHLY, 'DISABLED')
        :type  schedule_type:   str


        :param hour_of_day:     Hour of the day
        :type  hour_of_day:     str

        :keyword day_of_week:   Day of the week   (str)
        :keyword day_of_month:  Day of the month  (str)

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:       Client ID
        :type  client_id:       int

        :return:    Playbook UUID
        :rtype:     str

        :raises RequestFailed:

        """
        
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))

        day_of_week = kwargs.get("day_of_week", None)
        day_of_month = kwargs.get("day_of_month", None)
        print(type(csvdump))

        body = {
            "name": name,
            "description": description,
            "schedule": {
                "type": schedule_type,
                "hourOfDay": hourofday
            },
            "type":"System"
        }

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()


        elif schedule_type == ScheduleFreq.WEEKLY:
            if int(day_of_week) < 1 or int(day_of_week) > 7:
                raise ValueError("valid day_of_week (1-7) is required for a WEEKLY connector schedule.")
            body['schedule'].update(daysOfWeek=day_of_week)

        elif schedule_type == ScheduleFreq.MONTHLY:
            if int(day_of_month) < 1 or int(day_of_month) > 31:
                raise ValueError("valid day_of_month (1-31) is required for a MONTHLY connector schedule.")
            body['schedule'].update(daysOfMonth=day_of_month)
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
            


        jsonified_response = json.loads(raw_response.text)
        new_playbook_uuid = jsonified_response['uuid']

        if csvdump==True:
            jobid={'playbookuuid':[jsonified_response['uuid']]}
            df=pd.DataFrame(jobid)
            df.to_csv('playbookuuid.csv')

        return new_playbook_uuid

     
    def getslarules(self,playbookuuid:str,csvdump:bool=False,client_id:int=None,):

        """
        Get a list of all sla rules for an sla.

        :param playbookuuid:  Uuid of the playbook to fetch sla
        :type  playbookuuid:     str

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool


        :param client_id:   Client ID, if no client id provided , gets default client id
        :type  client_id:   int

        :return:    Sla rules
        :rtype:     list

        :raises RequestFailed:
        """


        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}/rules".format(playbookuuid)

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)
        if csvdump==True:
            field_names = []
            newdump=[]
            for i in jsonified_response['content']:
                temp={}
                for j,k in i.items():
                    temp[j]=k
                    if j=='filter':
                        temp.pop('filter')
                    if j=='actionConfig':
                        temp.pop('actionConfig')
                    if j=='detailInfo':
                        temp['slatype']=k['type']
                        temp['groupNames']=','.join(k['groupNames'])
                        temp['impacted_asset_count']=k['impactedMetrics']['asset_count']
                        temp['impacted_finding_count']=k['impactedMetrics']['finding_count']
                        temp.pop('detailInfo')
                newdump.append(temp)
            for item in newdump[0]:
                field_names.append(item)
            try:
                with open('slarules.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    for item in newdump:
                        writer.writerow(item)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)

        return jsonified_response

    def getallslas(self,csvdump:bool=False,client_id:int=None):

        """
        Gets all slas for a particular client.

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:   Client ID, if no client id provided , gets default client id
        :type  client_id:   int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/fetch"

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        jsonified_response = json.loads(raw_response.text)

        if csvdump==True:
            newdump=[]
            for i in jsonified_response['content']:
                temp={}
                for j,k in i.items():
                    temp[j]=k
                    if j=='filter':
                        temp.pop('filter')
                    if j=='actionConfig':
                        temp.pop('actionConfig')
                    if j=='detailInfo':
                        temp['slatype']=k['type']
                        temp['groupNames']=','.join(k['groupNames'])
                        temp['impacted_asset_count']=k['impactedMetrics']['asset_count']
                        temp['impacted_finding_count']=k['impactedMetrics']['finding_count']
                        temp.pop('detailInfo')
                newdump.append(temp)
            field_names = []
            for item in newdump[0]:
                field_names.append(item)
            try:
                with open('allslas.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    for item in newdump:
                        writer.writerow(item)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)

        return jsonified_response

    def delete_sla(self,sla_uuid:str,csvdump:bool=False,client_id:int=None):

        """
        Delete a particular sla

        :param sla_uuid:   UUID of sla
        :type  sla_uuid:   str

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:   Client ID, if no client id provided , gets default client id
        :type  client_id:   int

        :return:    Success
        :rtype:     bool

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url  = self.api_base_url.format(str(client_id)) +"/{}".format(sla_uuid)

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        if csvdump==True:
            self.get_specified_sla(playbookuuid=sla_uuid,csvdump=True)

        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.DELETE, url)
            if raw_response.status_code==200:
                success=True
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        return success

    def get_sla_rule(self,playbookrulepairinguuid:str,csvdump=False,client_id=None):

        """
        Gets all sla rules for a particular client.

        :param playbookrulepairinguuid:           Playbook rule pairing uuid
        :type  playbookrulepairinguuid:                str

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:   Client ID, if no client id provided , gets default client id
        :type  client_id:   int

        :return SLA details
        :rtype dict

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        url = self.api_base_url.format(str(client_id)) + "/rule/{}".format(playbookrulepairinguuid)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        jsonified_response = json.loads(raw_response.text)
        if csvdump==True:
            field_names = []
            print(jsonified_response)
            for item in jsonified_response:
                field_names.append(item)
            try:
                with open('sla_rule_data.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    writer.writerow(jsonified_response)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)

        
        return jsonified_response



    def get_specified_sla(self,playbookuuid:str,csvdump=False,client_id:int=None,):

        """
        Gets all slas for a particular client.

        :param playbookuuid:         UUID of playbook
        :type  playbookuuid:         str

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:   Client ID, if no client id provided , gets default client id
        :type  client_id:   int


        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/fetch/{}".format(playbookuuid)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        jsonified_response = json.loads(raw_response.text)

        if csvdump==True:
            print('Sla details saved in the csv file get_specified_sla')
            field_names = []
            print(jsonified_response)
            for item in jsonified_response:
                field_names.append(item)
            try:
                with open('specified_sla.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    writer.writerow(jsonified_response)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)


        return jsonified_response


    def get_sla_details(self,playbookuuid:str,csvdump=False,client_id:int=None,):

        """
        Get details of a particular sla playbook.

        :param playbookuuid:   SLA Playbook uuid
        :type  playbookuuid:       str

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:       Client ID, if no client id provided , gets default client id
        :type  client_id:   int

        :param return:      Returns the sla playbook details
        :type  client_id:   int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))+"/{}".format(playbookuuid)
        print(url)

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()


        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        
        jsonified_response = json.loads(raw_response.text)

        if csvdump==True:
            field_names = []
            for item in jsonified_response:
                field_names.append(item)
            try:
                with open('sladetails.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    writer.writerow(jsonified_response)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)

        return jsonified_response
        
    def add_default_sla_rule(self, sla_uuid:str, description:str, priority:int,
                     timeReference:str=TimeReference.DISCOVERED_DATE, serviceLevelAgreementMatrix:str=SlaMatrix.STANDARD,slaMatrixProfileType:str=SlaMatrixProfileType.STANDARD,offsetBasis:str=offsetbasis.VRR,affectOnlyNewFindings:bool=True,updateSLAIfVRRUpdates:bool=True,inputdata:str="HOST_FINDING",actionType:str=SlaActionType.REMEDIATION_SLA,csvdump:bool=False,client_id:int=None):
        
        """
        Adds default rule to existing sla playbook.Works only if there is no default rule applied to the playbook

        :param sla_uuid:                Sla UUID
        :type  sla_uuid:                str

        :param description:             Provide description for the default sla rule, 
        :type  description:             str

        :param priority:                Priority to be provided to default sla rule , 
                                        note: default sla priority should be a greater number than the group sla rules
        :type  priority:                int

        :param Timereference:           Timereference to be provided to default sla rule , 
        :type  Timereference:           Str

        :param slamatrix:               Provide slamatrix for the particular sla
        :type  slamatrix:               dict

        :param slamatrixprofiletype:    Provide sla matrix type for the sla
        :type  slamatrixprofiletype:    str

        :param offsetbasisc:            Provide offset basis for particular sla
        :type  offset_basis:            str

        :param affectOnlyNewFindings :  Choose whether it affects new findings
        :type affectonlynewfindings:    bool

        :param updateSLAIfVRRUpdates:   Choose if slaupdates with vrr
        :type  updateSLAIfVRRUpdates:   bool

        :param inputdata:               Type of data provided for sla
        :type  inputdata:               str

        :param actionType:              Type of action for particular sla
        :type  actionType:              str

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:               Client ID , if no client id provided , takes default client id
        :type  client_id:               int

        :param action_type:             Action type for the particular sla rule,by default remediation rule is provided
        :type  rule_desc:               str

        :return:                        List containing dict of rule details.
        :rtype:                         list

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}/rule".format(sla_uuid)

        body={"name":'Default SLA',"description":description,"priority":priority,"supplementalFilterRequest":None,"actionType":actionType,"action":{ "isDefaultSLA":True,"targetGroupIds":[],"timeReference":timeReference,"serviceLevelAgreementMatrix":serviceLevelAgreementMatrix,"slaMatrixProfileType":slaMatrixProfileType,"offsetBasis":offsetBasis,"affectOnlyNewFindings":affectOnlyNewFindings,"updateSLAIfVRRUpdates":updateSLAIfVRRUpdates},"outputType":"NO_OUTPUT","output":{},"input":inputdata}

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()


        jsonified_response = json.loads(raw_response.text)
        
        if csvdump==True:
            data={'uuid':jsonified_response[0]['uuid'],'name':jsonified_response[0]['name'],'description':jsonified_response[0]['description']}
            field_names = ['uuid','name','description']
            try:
                with open('defaultslarulecreated.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    writer.writerow(data)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)

        return jsonified_response
    
    def update_default_sla_rule(self, playbookrulepairinguuid:str, description:str, priority:int,
                     timeReference:str=TimeReference.DISCOVERED_DATE, serviceLevelAgreementMatrix:str=SlaMatrix.STANDARD,slaMatrixProfileType:str=SlaMatrixProfileType.STANDARD,offsetBasis:str=offsetbasis.VRR,affectOnlyNewFindings:bool=True,updateSLAIfVRRUpdates:bool=True,inputdata:str="HOST_FINDING",actionType:str=SlaActionType.REMEDIATION_SLA,csvdump:bool=False,client_id:int=None):
        
        """
        Adds default rule to existing sla playbook.Works only if there is no default rule applied to the playbook

        :param sla_uuid:                Sla UUID
        :type  sla_uuid:                str

        :param description:             Provide description for the default sla rule, 
        :type  description:             str

        :param priority:                Priority to be provided to default sla rule , 
                                        note: default sla priority should be a greater number than the group sla rules
        :type  priority:                int

        :param Timereference:           Timereference to be provided to default sla rule , 
        :type  Timereference:           Str

        :param slamatrix:               Provide slamatrix for the particular sla
        :type  slamatrix:               dict

        :param slamatrixprofiletype:    Provide sla matrix type for the sla
        :type  slamatrixprofiletype:    str

        :param offsetbasisc:            Provide offset basis for particular sla
        :type  offset_basis:            str

        :param affectOnlyNewFindings :  Choose whether it affects new findings
        :type affectonlynewfindings:    bool

        :param updateSLAIfVRRUpdates:   Choose if slaupdates with vrr
        :type  updateSLAIfVRRUpdates:   bool

        :param inputdata:               Type of data provided for sla
        :type  inputdata:               str

        :param actionType:              Type of action for particular sla
        :type  actionType:              str

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:               Client ID , if no client id provided , takes default client id
        :type  client_id:               int

        :param action_type:             Action type for the particular sla rule,by default remediation rule is provided
        :type  rule_desc:               str

        :return:                        List containing dict of rule details.
        :rtype:                         list

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url  = self.api_base_url.format(str(client_id)) +"/rule/{}".format(playbookrulepairinguuid)
        print(url)

        body={"name":'Default SLA',"description":description,"priority":priority,"supplementalFilterRequest":None,"actionType":actionType,"action":{ "isDefaultSLA":True,"targetGroupIds":[],"timeReference":timeReference,"serviceLevelAgreementMatrix":serviceLevelAgreementMatrix,"slaMatrixProfileType":slaMatrixProfileType,"offsetBasis":offsetBasis,"affectOnlyNewFindings":affectOnlyNewFindings,"updateSLAIfVRRUpdates":updateSLAIfVRRUpdates},"outputType":"NO_OUTPUT","output":{},"input":inputdata}

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()


        jsonified_response = json.loads(raw_response.text)
        
        if csvdump==True:
            data={'uuid':jsonified_response[0]['uuid'],'name':jsonified_response[0]['name'],'description':jsonified_response[0]['description']}
            field_names = ['uuid','name','description']
            try:
                with open('defaultslaruleupdated.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    writer.writerow(data)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)

        return jsonified_response
    
    def update_group_sla_rule(self, playbookrulepairinguuid:str, name:str, description:str, priority:int, targetgroupids:list,
                     timeReference:str=TimeReference.DISCOVERED_DATE, serviceLevelAgreementMatrix:dict=SlaMatrix.STANDARD,slaMatrixProfileType:str=SlaMatrixProfileType.STANDARD,offsetBasis:str=offsetbasis.VRR,affectOnlyNewFindings:bool=True,updateSLAIfVRRUpdates:bool=True,inputdata:str="HOST_FINDING",actionType:str=SlaActionType.REMEDIATION_SLA,csvdump:bool=False,client_id:int=None):
        
        """
        Updates a group sla rule for an already existing playbook
        :param playbookrulepairinguuid:           Playbook rule pairing uuid
        :type  playbookrulepairinguuid:                str

        :param name:                    Name of the group specific sla rule
        :type  namw:                    str

        :param description:             Provide description for the group specific sla rule, 
        :type  description:             str

        :param priority:                Priority to be provided to group speicifc sla , 
                                        note: group sla priority should be a lesser number than the default sla rule
        :type  priority:                int

        :param targetgroupids:          The groups ids where the sla applies
        :type  targetgroupids:          list

        :param TimeReference:           Timereference to be provided to default sla rule , 
        :type  timeReference:           Str

        :param slamatrix:               Provide slamatrix for the particular sla
        :type  slamatrix:               dict

        :param slamatrixprofiletype:    Provide sla matrix type for the sla
        :type  slamatrixprofiletype:    str

        :param offsetbasisc:            Provide offset basis for particular sla
        :type  offset_basis:            str

        :param affectOnlyNewFindings :  Choose whether it affects new findings
        :type affectonlynewfindings:    bool

        :param updateSLAIfVRRUpdates:   Choose if slaupdates with vrr
        :type  updateSLAIfVRRUpdates:   bool

        :param inputdata:               Type of data provided for sla
        :type  inputdata:               str

        :param actionType:              Type of action for particular sla
        :type  actionType:              str

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:               Client ID , if no client id provided , takes default client id
        :type  client_id:               int

        :param action_type:             Action type for the particular sla rule,by default remediation rule is provided
        :type  rule_desc:               str

        :return:                        List containing dict of rule details.
        :rtype:                         list

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url  = self.api_base_url.format(str(client_id)) +"/rule/{}".format(playbookrulepairinguuid)

        body={"name":name,"description":description,"priority":priority,"supplementalFilterRequest":None,"actionType":actionType,"action":{"isDefaultSLA":False,"targetGroupIds":targetgroupids,"timeReference":timeReference,"serviceLevelAgreementMatrix":serviceLevelAgreementMatrix,"slaMatrixProfileType":slaMatrixProfileType,"offsetBasis":offsetBasis,"affectOnlyNewFindings":affectOnlyNewFindings,"updateSLAIfVRRUpdates":updateSLAIfVRRUpdates},"outputType":"NO_OUTPUT","output":{},"input":inputdata}

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)

        if csvdump==True:
            data={'uuid':jsonified_response[0]['uuid'],'name':jsonified_response[0]['name'],'description':jsonified_response[0]['description']}
            field_names = ['uuid','name','description']
            try:
                with open('groupslaruleupdated.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    writer.writerow(data)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)

        return jsonified_response


    def del_group_sla_rule(self,playbookuuid,client_id=None):
        
        """
        Deletes a particular group sla rule.

        :param client_id:   Client ID, if no client id provided , gets default client id
        :type  client_id:   int

        :param playbookuuid: The playbookuuid that needs to be deleted
        :type  playbookuuid: str

        :return delete_json: Returns json of deleted rule
        :return type:        json

        :raises RequestFailed:
        
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]


        url = self.api_base_url.format(str(client_id)) +"/rule/{}".format(playbookuuid)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.DELETE, url)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response 
    
    def change_order(self,slauuid:str,ruleuuids:list,csvdump:bool=False,client_id:int=None):

        """
        Changes the order of the sla rules

        :param client_id:   Client ID, if no client id provided , gets default client id
        :type  client_id:   int

        :param slauuid: The sla where rules needs to be reordered
        :type  slauuid: str

        :param ruleuuid: The order of rules reordering
        :type  ruleuuid: list
        
        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :return succcess_json: Returns the reordered rule json
        :param  success_json:  json

        :raises RequestFailed:
        
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) +"/{}/rule-reorder".format(slauuid)

        body={"ruleUuids":ruleuuids}
        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
            if raw_response.status_code==200:
                success=True
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)
        if csvdump==True:
            field_names = ['uuid','name']
            data=[]
            for i in jsonified_response:
                data.append({'uuid':i['uuid'],'name':i['name']})
            try:
                with open('rule_reorder.csv', 'w',newline='') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=field_names)
                        writer.writeheader()
                        for item in data:
                            writer.writerow(item)
            except (RequestFailed,Exception) as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        return success
   
    def sla_run(self,slauuid:str,csvdump:bool=False,client_id:int=None):

        """
        Runs the sla

        :param client_id:   Client ID, if no client id provided , gets default client id
        :type  client_id:   int

        :param slauuid: The sla rule that needs to be run
        :type  slauuid: str

        :return jsonified_response: Returns the json of sla
        :param  jsonified_response:  json

        :raises RequestFailed:
        
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) +"/{}/run".format(slauuid)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET,url)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)
        if csvdump==True:
            field_names = []
            print(jsonified_response)
            for item in jsonified_response:
                field_names.append(item)
            try:
                with open('slarun.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    writer.writerow(jsonified_response)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)
        return jsonified_response
   
    def add_group_sla_rule(self, sla_uuid:str, name:str, description:str, priority:int, targetgroupids:list,
                     timeReference:str=TimeReference.DISCOVERED_DATE, serviceLevelAgreementMatrix:dict=SlaMatrix.STANDARD,slaMatrixProfileType:str=SlaMatrixProfileType.STANDARD,offsetBasis:str=offsetbasis.VRR,affectOnlyNewFindings:bool=True,updateSLAIfVRRUpdates:bool=True,inputdata:str="HOST_FINDING",actionType:str=SlaActionType.REMEDIATION_SLA,csvdump:bool=False,client_id:int=None):
        
        """
        Adds group rule to existing sla playbook for the groups specified.
        :param sla_uuid:                Sla UUID
        :type  sla_uuid:                str

        :param name:                    Name of the group specific sla rule
        :type  namw:                    str

        :param description:             Provide description for the group specific sla rule, 
        :type  description:             str

        :param priority:                Priority to be provided to group speicifc sla , 
                                        note: group sla priority should be a lesser number than the default sla rule
        :type  priority:                int

        :param targetgroupids:          The groups ids where the sla applies
        :type  targetgroupids:          list

        :param TimeReference:           Timereference to be provided to default sla rule , 
        :type  timeReference:           Str

        :param slamatrix:               Provide slamatrix for the particular sla
        :type  slamatrix:               dict

        :param slamatrixprofiletype:    Provide sla matrix type for the sla
        :type  slamatrixprofiletype:    str

        :param offsetbasisc:            Provide offset basis for particular sla
        :type  offset_basis:            str

        :param affectOnlyNewFindings :  Choose whether it affects new findings
        :type affectonlynewfindings:    bool

        :param updateSLAIfVRRUpdates:   Choose if slaupdates with vrr
        :type  updateSLAIfVRRUpdates:   bool

        :param inputdata:               Type of data provided for sla
        :type  inputdata:               str

        :param actionType:              Type of action for particular sla
        :type  actionType:              str

        :param client_id:               Client ID , if no client id provided , takes default client id
        :type  client_id:               int

        :param action_type:             Action type for the particular sla rule,by default remediation rule is provided
        :type  rule_desc:               str

        :return:                        List containing dict of rule details.
        :rtype:                         list

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) +"/{}/rule".format(sla_uuid)

        body={"name":name,"description":description,"priority":priority,"supplementalFilterRequest":None,"actionType":actionType,"action":{"isDefaultSLA":False,"targetGroupIds":targetgroupids,"timeReference":timeReference,"serviceLevelAgreementMatrix":serviceLevelAgreementMatrix,"slaMatrixProfileType":slaMatrixProfileType,"offsetBasis":offsetBasis,"affectOnlyNewFindings":affectOnlyNewFindings,"updateSLAIfVRRUpdates":updateSLAIfVRRUpdates},"outputType":"NO_OUTPUT","output":{},"input":inputdata}

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)

        if csvdump==True:
            data={'uuid':jsonified_response[0]['uuid'],'name':jsonified_response[0]['name'],'description':jsonified_response[0]['description']}
            field_names = ['uuid','name','description']
            try:
                with open('groupslarulecreated.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    writer.writerow(data)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)

        return jsonified_response


    def update_sla(self, sla_uuid:str,description:str,schedule_type:str='DAILY',hourofday:int=0,dayofmonth:str='4',dayofweek:str='5',name:str="Remediation SLAs",type:str='System',csvdump:bool=False,client_id=None,**kwargs):
        
        """
        Updates an sla
        
        :param sla_uuid:                Sla UUID
        :type  sla_uuid:                str

        :param name:                    Name of the 
        :type  name:                    str

        :param description:             Provide description for sla 
        :type  description:             str

        :param schedule_type:   Schedule Frequency (ScheduleFreq.DAILY, ScheduleFreq.WEEKLY,
                                                    ScheduleFreq.MONTHLY, 'DISABLED')
        :type  schedule_type:   str


        :param hourofday:     Hour of the day
        :type  hourofday:     int

        :keyword dayofmonth:    Day of month   (str)
        :type    dayofmonth:    Day of the month  (str)

        :keyword dayofweek:    Day of week   (str)
        :type    dayofweek:    Day of week  (str)

        :keyword type:    System   (str)
        :type    type:    System  (str)

        :keyword name:    By default remediation sla   (str)
        :type    name:    str

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:               Client ID , if no client id provided , takes default client id
        :type  client_id:               int

        :return:                        List containing dict of playbook details.
        :rtype:                         list

        :raises RequestFailed:
        """
        if schedule_type.upper()=='DAILY':
            schedule={
                'type':'DAILY',
                "hourOfDay":hourofday
            }
        if schedule_type.upper()=='WEEKLY':
            schedule={
                'type':'WEEKLY',
                "hourOfDay":hourofday,
                'daysOfWeek':dayofweek
            }
        if schedule_type.upper()=='MONTHLY':
            schedule={
                'type':'MONTHLY',
                "hourOfDay":hourofday,
                'daysOfMonth':dayofmonth
            }

        
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) +"/{}".format(sla_uuid)

        body={
                "name": name,
                "description": description,
                "schedule": schedule,
                "type": type
                }


        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)


        if csvdump==True:
            field_names = []
            for item in jsonified_response:
                field_names.append(item)
            try:
                with open('slaupdate.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    writer.writerow(jsonified_response)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)


        return jsonified_response
     
    def disablesla(self,playbookuuid:str,csvdump:bool=False,client_id:int=None):

        """
        Disables a particular sla rule.

        :param playbookuuid: The playbookuuids that needs to be disabled
        :type  playbookuuid: str

        :param csvdump: Dumps data in csv
        :type  csvdump: str

        :param client_id:   Client ID, if no client id provided , gets default client id
        :type  client_id:   int

        :return response: Returns json of disable sla
        :return type:     json

        :raises RequestFailed:
        
        """


        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/toggle-enabled"

        body={"playbookUuids":playbookuuid,"enabled":False}

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def enablesla(self,playbookuuid:list,client_id:int=None):
        """
        Enables a particular sla rule.

        :param playbookuuid: The playbookuuids that needs to be enabled
        :type  playbookuuid: list

        :param client_id:   Client ID, if no client id provided , gets default client id
        :type  client_id:   int

        :return success: success
        :return type:     bool

        :raises RequestFailed:
        
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/toggle-enabled"
        body={"playbookUuids":playbookuuid,"enabled":True}
        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
            if raw_response==200:
                success=True
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)

        return success  

    def getplaybookslarules(self,slaid,client_id=None): 

        """
        Gets sla playbook rules for a particular sla.

        :param slaid:       Slaid to get the sla rules
        :type  slaid:       str

        :param client_id:   Client ID, if no client id provided , gets default client id
        :type  client_id:   int

        :return response: Returns json of playbook rules
        :return type:     json


        :raises RequestFailed:
        """
        

        url = self.api_base_url.format(str(client_id)) + f"/{slaid}"
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def update_slarule(self, playbookrulepairinguuid, name, description, priority, targetgroupids,
                     timeReference=TimeReference.DISCOVERED_DATE, serviceLevelAgreementMatrix=SlaMatrix.STANDARD,slaMatrixProfileType=SlaMatrixProfileType.STANDARD,offsetBasis=offsetbasis.VRR,affectOnlyNewFindings=True,updateSLAIfVRRUpdates=True,inputdata="HOST_FINDING",actionType=SlaActionType.REMEDIATION_SLA,csvdump:bool=False,client_id=None):
        
        """
        Update group rule to existing sla playbook for the groups specified.
        :param sla_uuid:                Sla UUID
        :type  sla_uuid:                str

        :param name:                    Name of the group specific sla rule
        :type  namw:                    str

        :param description:             Provide description for the group specific sla rule, 
        :type  description:             str

        :param priority:                Priority to be provided to group speicifc sla , 
                                        note: group sla priority should be a lesser number than the default sla rule
        :type  priority:                int

        :param targetgroupids:          The groups ids where the sla applies
        :type  targetgroupids:          list

        :param TimeReference:           Timereference to be provided to default sla rule , 
        :type  timeReference:           Str

        :param slamatrix:               Provide slamatrix for the particular sla
        :type  slamatrix:               dict

        :param slamatrixprofiletype:    Provide sla matrix type for the sla
        :type  slamatrixprofiletype:    str

        :param offsetbasisc:            Provide offset basis for particular sla
        :type  offset_basis:            str

        :param affectOnlyNewFindings :  Choose whether it affects new findings
        :type affectonlynewfindings:    bool

        :param updateSLAIfVRRUpdates:   Choose if slaupdates with vrr
        :type  updateSLAIfVRRUpdates:   bool

        :param inputdata:               Type of data provided for sla
        :type  inputdata:               str

        :param actionType:              Type of action for particular sla
        :type  actionType:              str

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:               Client ID , if no client id provided , takes default client id
        :type  client_id:               int

        :param action_type:             Action type for the particular sla rule,by default remediation rule is provided
        :type  rule_desc:               str

        :return:                        List containing dict of rule details.
        :rtype:                         list

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) +"/rule/{}".format(playbookrulepairinguuid)



        body={"name":name,"description":description,"priority":priority,"supplementalFilterRequest":None,"actionType":actionType,"action":{"isDefaultSLA":False,"targetGroupIds":targetgroupids,"timeReference":timeReference,"serviceLevelAgreementMatrix":serviceLevelAgreementMatrix,"slaMatrixProfileType":slaMatrixProfileType,"offsetBasis":offsetBasis,"affectOnlyNewFindings":affectOnlyNewFindings,"updateSLAIfVRRUpdates":updateSLAIfVRRUpdates},"outputType":"NO_OUTPUT","output":{},"input":inputdata}


        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()

        jsonified_response = json.loads(raw_response.text)

        if csvdump==True:
            data={'uuid':jsonified_response[0]['uuid'],'name':jsonified_response[0]['name'],'description':jsonified_response[0]['description']}
            field_names = ['uuid','name','description']
            try:
                with open('defaultslarulecreated.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    writer.writerow(data)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)
        return jsonified_response

    def delete_sla_rule(self,playbookrulepairinguuid,client_id=None):

        """
        Gets all slas for a particular client.

        :param client_id:   Client ID, if no client id provided , gets default client id
        :type  client_id:   int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url  = self.api_base_url.format(str(client_id)) +"/rule/{}".format(playbookrulepairinguuid)

        try:
            success=False
            raw_response = self.request_handler.make_request(ApiRequestHandler.DELETE, url)
            if raw_response.status_code==200:
                success=True
        except RequestFailed as e:
             print()
             print('There seems to be an exception')
             print(e)
             exit()
        return success

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