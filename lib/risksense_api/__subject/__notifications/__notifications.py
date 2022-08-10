""" *******************************************************************************************************************
|
|  Name        :  __notifications.py
|  Module      :  risksense_api
|  Description :  A class to be used for interacting with RiskSense platform notifications.
|  Copyright   :  (c) RiskSense, Inc.
|  License     :  Apache-2.0
|
******************************************************************************************************************* """

import json
from turtle import ontimer
from .. import Subject
from ..._params import *
from ..._api_request_handler import *
import csv


class Notifications(Subject):

    """ Notifications class """

    def __init__(self, profile):

        """
        Initialization of Notifications object.

        :param profile:     Profile Object
        :type  profile:     _profile

        """

        self.subject_name = "rsNotifications"
        Subject.__init__(self, profile, self.subject_name)
    
    def subscribe_notifications(self,notificationtypeid:int,csvdump:bool=False,subscribe=True,client_id=None):

        """
        Subscribe to a notification

        :param notificationtypeid:  The notification id to subscribe.
        :type  notificationtypeid:  int

        :param subscribe:  Whether to subscribe or not
        :type  subscribe:  Bool

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:  The client id , if none will provide the default client id
        :type  client_id:  int

        :return:    Success json
        :rtype:     json

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/subscribe"
        
        body = {"notificationTypeId":notificationtypeid,"subscribe":subscribe}
        
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
            field_names = []
            print(jsonified_response)
            for item in jsonified_response:
                field_names.append(item)
            try:
                with open('subscribenotifications.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    writer.writerow(jsonified_response)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)

        return jsonified_response

    def unsubscribe_notifications(self,notificationtypeid,csvdump:bool=False,subscribe=False,client_id=None):

        """
        Subscribe to a notification

        :param notificationtypeid:  The notification id to subscribe.
        :type  notificationtypeid:  int

        :param subscribe:  Whether to subscribe or not
        :type  subscribe:  Bool

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:  The client id , if none will provide the default client id
        :type  client_id:  int


        :return:    Success json
        :rtype:     json

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/subscribe"
        
        body = {"notificationTypeId":notificationtypeid,"subscribe":subscribe}

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
            field_names = []
            print(jsonified_response)
            for item in jsonified_response:
                field_names.append(item)
            try:
                with open('unsubscribenotifications.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    writer.writerow(jsonified_response)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)

        return jsonified_response


    def listrules(self,csvdump=True, client_id=None):

        """
        In development
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))+"/rules"

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
            print(jsonified_response)
            for item in jsonified_response['_embedded']['networks'][0]:
                field_names.append(item)
            try:
                with open('get_networks.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    for item in jsonified_response['_embedded']['networks']:
                        writer.writerow(item)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)

        return jsonified_response
        
    '''def updatenotifications(self, notificationtypeid,subject,operators,frequency,whiteListed,blackListed,deliveryChannel,targetCount,subscribe,notificationRuleGroupId="null",client_id=None):

        """
        In development
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/rules"

        body = {"notificationTypeId":notificationtypeid,"subject":subject,"configs":{"notificationRuleGroupId":"null","subscribe":subscribe,"operators":[],"frequency":"INSTANT","whiteListed":[],"blackListed":[],"deliveryChannel":"In Platform Only","targetCount":27001},"subscribe":subscribe}

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except RequestFailed as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        jsonified_response = json.loads(raw_response)

        return jsonified_response'''

    def markasread(self,notificationids:list,markasread:bool=False,client_id:int=None):

        """
        Mark as read/unread notifications

        :param notificationtypeid:  The notification id to subscribe.
        :type  notificationtypeid:  list

        :param markasread:  Whether to markread or not
        :type  subscribe:   Bool

        :param client_id:  The client id , if none will provide the default client id
        :type  client_id:  int

        :return:    Success json
        :rtype:     json
        
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]


        try:
            body = {
                "notificationIds": notificationids,
                "markAsRead": markasread
                }

        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        try:
            url = self.api_base_url.format(str(client_id)) + "/mark-as-read"
            raw_response=self.request_handler.make_request(ApiRequestHandler.PUT, url,body=body)
            if raw_response.status_code==200:
                return True
        except (RequestFailed,Exception) as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()


    def create_delivery_channel(self, channelname:str, channeltype:str,
                               address:str,verificationcode:str,webhookcontenttype=None,client_id=None):

        """
        Creates delivery channel for the user

        :param channelname: Name of channel
        :type channelname: str

        :param channeltype: Type of channel
        :type channeltype: str

        :param webhookcontenttype: Webhook content type
        :type webhookcontenttype:  None

        :param address:  Address
        :type address:  str

        :param verificationcode:  Verification code of user
        :type verificationcode:  str

        :param client_id:  The client id , if none will provide the default client id
        :type  client_id:  int

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]
        addressDetails=[{
            "address":address,"verification_code":verificationcode
        }]

        url = self.api_base_url.format(str(client_id)) + "/channel"

        body = {
                "channelName": channelname,
                "channelType": channeltype,
                "webhookContentType": webhookcontenttype,
                "addressDetails": addressDetails
                }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except RequestFailed as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response['status']

    def edit_delivery_channel(self,channelid:int, channelname:str, channeltype:str,addressDetails:str,verificationcode:int,webhookcontenttype=None,disabled:bool=False,shared:bool=False,client_id:int=None):
        """
        Edits delivery channel for the user

        :param channelid: Channel id
        :type channelid: int

        :param channelname: Name of channel
        :type channelname: str

        :param channeltype: Type of channel
        :type channeltype: str

        :param webhookcontenttype: Webhook content type
        :type webhookcontenttype:  None

        :param address:  Address
        :type address:  str

        :param verificationcode:  Verification code of user
        :type verificationcode:  str

        :param webhookcontenttype:  Webhook content type
        :type webhookcontenttype:  None

        :param disabled:  Enable/disable notifications
        :type disabled:  bool

        :param shared:  Shared
        :type shared:  bool

        :param client_id:  The client id , if none will provide the default client id
        :type  client_id:  int

        :return status
        :rtype str

        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        addressDetails=[{
            "address":addressDetails,"verification_code":verificationcode
        }]

        url = self.api_base_url.format(str(client_id)) + "/channel"

        body = {
                "id": channelid,
                "channelName": channelname,
                "channelType": channeltype,
                "webhookContentType": webhookcontenttype,
                "disabled": disabled,
                "shared": shared,
                "addressDetails": addressDetails
                }
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except RequestFailed as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response['status']

    def delete_delivery_channel(self,channelids:list,client_id:int=None):
        """
        Deletes delivery channels

        :param channelids: Channel ids
        :type channelids: list

        :param client_id:  The client id , if none will provide the default client id
        :type  client_id:  int

        :return status
        :rtype str

        """
        if client_id is None:
            client_id= self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/channel"

        body ={
                "channelIds": channelids
                }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.DELETE, url, body=body)
        except RequestFailed as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response['status']
    
    def list_channel(self,order='ASC',csvdump=False,client_id=None):
        
        if client_id is None:
            client_id= self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + f"/admin/channel/{order}"

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except RequestFailed as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def list_channel_user(self,order='ASC',csvdump=False,client_id=None):

        """
        List delivery channels

        :param order: Sort order
        :type order: str

        :param csvdump:  csvdump
        :type  csvdump:  bool

        :param client_id:  The client id , if none will provide the default client id
        :type  client_id:  int

        :return status
        :rtype str

        """
        
        if client_id is None:
            client_id= self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + f"/channel/{order}"

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()


        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
            jsonified_response = json.loads(raw_response.text)
            if csvdump==True:
                field_names = []
                deliverychanneldetails=jsonified_response["deliveryChannelDetails"]
                for item in deliverychanneldetails[0].keys():
                    field_names.append(item)
                try:
                    with open('channels.csv', 'w') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=field_names)
                        writer.writeheader()
                        for item in deliverychanneldetails:
                            writer.writerow(item)
                except FileNotFoundError as fnfe:
                    print("An exception has occurred while attempting to write the .csv file.")
                    print()
                    print(fnfe)

        except RequestFailed as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        


        return jsonified_response

    def send_verification_code(self,channelname:str,channeladdress:str,channeltype:str,client_id:int=None):
        """
        Sends verification code to the user 

        :param channelname: Name of the channel.
        :type  channelname:  str

        :param channeladdress: Address of the channel.
        :type  channeladdress:  str
        
        :param channeltype: TYPE of channel
        :type channeltype: str

        :param client_id:  The client id , if none will provide the default client id
        :type  client_id:  int

        """
        if client_id is None:
            client_id= self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + f"/sendverificationcode"

        body={
                "channelName": channelname,
                "channelDetails": [
                    {
                    "channelAddress": channeladdress,
                    "channelType": channeltype
                    }
                ]
                }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response['status']

    def get_model(self, client_id:int=None):

        """
        List projections and their models that can be requested from the search endpoint.

        :param client_id:  The client id , if none will provide the default client id
        :type  client_id:  int

        """

        if client_id is None:
            client_id= self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + f"/model"
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except RequestFailed as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def search_filters(self, client_id:int=None):


        """
        List fields that can be filtered by in the search endpoint

        :param client_id:  The client id , if none will provide the default client id
        :type  client_id:  int

        """

        if client_id is None:
            client_id= self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/filter"

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except RequestFailed as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def notification_search(self,filters:list,csvdump:bool=False,client_id:int=None):

        """
        Search for notifications

        :param filters:  Search filters
        :type  filters:  list

        :param csvdump:  csvdump
        :type  csvdump:  bool

        :param client_id:  The client id , if none will provide the default client id
        :type  client_id:  int

        :return:    Success json
        :rtype:     json

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id= self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + f"/search"
        body={
                "filters": filters,
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
            exit()

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body) 
            jsonified_response = json.loads(raw_response.text)

            if csvdump==True:
                print('Saving the notifications search data in a csv called notifications.csv')
                field_names = []
                for item in jsonified_response['_embedded']['notificationAlertEvents'][0]:
                    field_names.append(item)
                try:
                    with open('notifications.csv', 'w',newline='') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=field_names)
                        writer.writeheader()
                        for item in jsonified_response['_embedded']['notificationAlertEvents']:
                            writer.writerow(item)
                except FileNotFoundError as fnfe:
                    print("An exception has occurred while attempting to write the .csv file.")
                    print()
                    print(fnfe)

            return jsonified_response
        except RequestFailed as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()

    def quickfilters_count(self,client_id=None):

        """"
        in development

        """

        """
        Get quickfilters dara

        :param client_id:  The client id , if none will provide the default client id
        :type  client_id:  int

        :return:    Success json
        :rtype:     json

        :raises RequestFailed:
        :raises ValueError:
        """
        
        if client_id is None:
            client_id= self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + f"/quick-filters/count"
        body={
                "subject": "rsNotifications",
                "filterRequest": {
                    "filters": [
                    {
                        "field": "subject",
                        "exclusive": False,
                        "operator": "IN",
                        "value": "groups"
                    }
                    ]
                }
                }
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        jsonified_response = json.loads(raw_response.text)
        return jsonified_response
    
    def enablenotification(self,id,channelname,channeltype,client_id=None):
        if client_id is None:
            client_id= self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/admin/channel"
        body= {"id":id,"channelName":channelname,"channelType":channeltype,"disabled":False}
        print(body)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url,body=body)
        except RequestFailed as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response
    
    def disablenotification(self,id,channelname,channeltype,client_id=None):
        if client_id is None:
            client_id= self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/admin/channel"
        body= {"id":id,"channelName":channelname,"channelType":channeltype,"disabled":True}

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url,body=body)
        except RequestFailed as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def edit_delivery_channel_admin(self,id:int,channelname:str,channeltype:str,address:str,verification_code:str,webhookcontenttype:str=None,disabled:bool=False,shared:bool=False,client_id:bool=None):

        """
        Edits delivery channel for the admin

        :param id: Channel id
        :type id: int

        :param channelname: Name of channel
        :type channelname: str

        :param channeltype: Type of channel
        :type channeltype: str

        :param webhookcontenttype: Webhook content type
        :type webhookcontenttype:  str

        :param address:  Address
        :type address:  str

        :param verificationcode:  Verification code of user
        :type verificationcode:  str

        :param disabled:  Enable/disable notifications
        :type disabled:  bool

        :param shared:  Shared
        :type shared:  bool

        :param client_id:  The client id , if none will provide the default client id
        :type  client_id:  int

        :return status
        :rtype str

        """

        if client_id is None:
            client_id= self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/channel/admin"
        body={
                "id": id,
                "channelName": channelname,
                "channelType": channeltype,
                "webhookContentType": webhookcontenttype,
                "disabled": disabled,
                "shared": shared,
                "addressDetails": [
                    {
                    "address": address,
                    "verification_code": verification_code
                    }
                ]
                }
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url,body=body)
        except RequestFailed as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response
    
    def get_notifications(self,client_id=None):
        if client_id is None:
            client_id= self._use_default_client_id()[0]
        
        url = self.api_base_url.format(str(client_id)) + "/page?page=0&size=50&order=desc"
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except RequestFailed as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        jsonified_response = json.loads(raw_response.text)
        return jsonified_response
    
    def list_channel_admin(self,order:str='ASC',client_id:int=None):
        
        """
        In development


        List channels from admin

        :param order:  The sort order
        :type  order:  str

        :param client_id:  The client id , if none will provide the default client id
        :type  client_id:  int

        :return:    Success json
        :rtype:     json

        :raises RequestFailed:
        :raises ValueError:
        """

        if client_id is None:
            client_id= self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + f"/channel/admin/{order}"
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except RequestFailed as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        
        jsonified_response = json.loads(raw_response.text)

        return jsonified_response
  
    def get_detailpane(self,notification_id:int,csvdump:bool=False,client_id:int=None):

        """
        Get details pane

        :param notificationid:  The notiifcation id to get details of
        :type  notificationid:  int

        :param csvdump:         dumps the data in csv
        :type  csvdump:         bool

        :param client_id:  The client id , if none will provide the default client id
        :type  client_id:  int

        :return:    Notifications detail
        :rtype:     list

        :raises RequestFailed:
        :raises ValueError:
        """
        if client_id is None:
            client_id= self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + f"/detail?notification_id={notification_id}"
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except RequestFailed as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        
        jsonified_response = json.loads(raw_response.text)

        if type(csvdump)!=bool:
            print('Error in csvdump value,Please provide either true or false')
            exit()


        if csvdump==True:
            field_names = []
            print(jsonified_response)
            for item in jsonified_response[0]:
                field_names.append(item)
            try:
                with open('notificationsdetails.csv', 'w',newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    for item in jsonified_response:
                        writer.writerow(item)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)

        return jsonified_response

    def get_delivery_channel_template(self,client_id:int=None):

        """
        Get delivery channel template

        :param client_id:  The client id , if none will provide the default client id
        :type  client_id:  int

        :return:    Delivery channel template
        :rtype:     list

        :raises RequestFailed:
        :raises ValueError:
        """


        if client_id is None:
            client_id= self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + f"/delivery-channel-template"


        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except RequestFailed as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        
        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def trigger_systemfilter(self,filterid,subject,description,client_id=None):
        
        if client_id is None:
            client_id= self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/trigger-systemfilter"
        body={
            "filterId": filterid,
            "subject": subject,
            "description": description
            }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed as e:
                        print()
                        print('There seems to be an exception')
                        print(e)
                        exit()
        

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response
 
    
    

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
