"""
Assessments
"""
""" *******************************************************************************************************************
|
|  Name        :  __assessments.py
|  Module      :  risksense_api
|  Description :  A class to be used for interacting with RiskSense platform assessments.
|  Copyright   :  (c) RiskSense, Inc.
|  License     :  Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
******************************************************************************************************************* """

from ftplib import all_errors
import json
from ...__subject import Subject
from ..._params import *
from ..._api_request_handler import *
import csv


class Assessments(Subject):

    """ Assessments Class """

    def __init__(self, profile):

        """
        Initialization of Assessments object.

        :param profile:     Profile Object
        :type  profile:     _profile

        """

        self.subject_name = "assessment"
        Subject.__init__(self, profile, self.subject_name)
        self.al_base_url = self.profile.platform_url + "/api/v1/client/{}/reportingChecklist/assessment/{}"


    def create(self, name, start_date, notes="", client_id=None):

        """
        Create an Assessment

        :param name:        The name for new assessment.
        :type  name:        str

        :param start_date:  The date for the new assessment.  Should be in "YYYY-MM-DD" format.
        :type  start_date:  str

        :param notes:       Any notes to associated with the assessment.
        :type  notes:       str

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The new assessment ID is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))

        body = {
            "name": name,
            "startDate": start_date,
            "notes": notes
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed,Exception) as e:
            print('Error in creating assessment')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)
        assessment_id = jsonified_response['id']

        return assessment_id

    def update(self, assessment_id, client_id=None, **kwargs):

        """
        Update an assessment

        :param assessment_id:   The assessment ID
        :type  assessment_id:   int

        :keyword name:          The name to assign to the assessment.  String.
        :keyword start_date:    The start date to assign to the assessment.  String.  Should be in "YYYY-MM-DD" format.
        :keyword notes:         Notes to assign to the assessment.  String.

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The job ID is returned.
        :rtype:     int

        :raises ValueError:
        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        name = kwargs.get('name', None)
        start_date = kwargs.get('start_date', None)
        notes = kwargs.get('notes', None)

        url = self.api_base_url.format(str(client_id)) + "/" + str(assessment_id)

        body = {}

        if name is not None:
            body.update(name=name)

        if start_date is not None:
            body.update(startDate=start_date)

        if notes is not None:
            body.update(notes=notes)

        if body == {}:
            raise ValueError("Body is empty. At least one of these fields is required: name, start_date, notes")

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except (RequestFailed,Exception) as e:
            print('Error in updating assessment')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)
        returned_id = jsonified_response['id']

        return returned_id

    def delete(self, assessment_id, client_id=None,csvdump=False):

        """
        Deletes an assessment.

        :param assessment_id:   Assessment ID.
        :type  assessment_id:   int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The job ID is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/" + str(assessment_id)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.DELETE, url)
        except (RequestFailed,Exception) as e:
            print('Error in deleting assessment')
            print(e)
            exit()

        if csvdump==True:
            all_findings=self.search([{"field":"id","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":f"{assessment_id}"}])
            field_names = []

            for item in all_findings[0]:
                field_names.append(item)
            try:
                with open('assessmentdetails.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    for item in all_findings:
                        writer.writerow(item)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def get_model(self, client_id=None):

        """
        Get available projections and models for Assessments.

        :param client_id:   Client ID
        :type  client_id:   int

        :return:    Assessment projections and models are returned.
        :rtype:     dict

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            response = self._model(self.subject_name, client_id)
        except (RequestFailed,Exception) as e:
            print('Error in getting model')
            print(e)
            exit()

        return response

    def list_assessment_filter_fields(self,client_id=None):

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
            print('Error in suggesting for filter fields')
            print(e)
            exit()

        return response
        
    def get_single_search_page(self, search_filters, page_num=0, page_size=150,
                               sort_field=SortField.ID, sort_dir=SortDirection.ASC, client_id=None):

        """
        Searches for and returns assessments based on the provided filter(s) and other parameters.

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

        :return:    The paginated JSON response from the platform is returned.
        :rtype:     dict

        :raises RequestFailed:
        """

        func_args = locals()
        func_args.pop('self')

        if client_id is None:
            client_id, func_args['client_id'] = self._use_default_client_id()

        try:
            response = self._get_single_search_page(self.subject_name, **func_args)
        except (RequestFailed,Exception) as e:
            print('Error in searching for assessments')
            print(e)
            exit()

        return response

    def search(self, search_filters, page_size=150, sort_field=SortField.ID, sort_dir=SortDirection.ASC, client_id=None,csvdump=False):

        """
        Searches for and returns assessments based on the provided filter(s) and other parameters.  Rather
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
        :raises Exception:
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
        except (RequestFailed,Exception) as e:
            print('Error in searching for assessments')
            print(e)
            exit()

        page_range = range(0, num_pages)

        try:
            all_results = self._search(self.subject_name, self.get_single_search_page, page_range, **func_args)
        except (RequestFailed, Exception) as e:
            print('Error in searching for assessments')
            print(e)
            exit()

        if csvdump==True:
            field_names = []

            for item in all_results[0]:
                field_names.append(item)
            try:
                with open('assessmentdetailssearch.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    for item in all_results:
                        writer.writerow(item)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)

        return all_results
        
    def update_assessment_status(self, assessment_id,status, client_id=None):

        """
        Update the status of the assessment

        :param assessment_id:       The assessment ID.
        :type  assessment_id:       int

        :param status:       Update the status either "LOCKED" or "UNLOCKED"
        :type  status:       str

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The jsonified data of the status
        :rtype:     dict

        :raises RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/" + str(assessment_id) + "/status"

        body= {
                 "status": status.upper()
              }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except (RequestFailed,Exception) as e:
            print('Error in updating assessment status')
            print(e)
            exit()

        jsonified_data = json.loads(raw_response.text)

        return jsonified_data

    def get_assessment_history(self, assessment_id,csvdump=False,client_id=None):

        """
        Get history of assessments

        :param assessment_id:       The assessment ID.
        :type  assessment_id:       int

        :param csvdump:             Whether to dump the assessment history in a csv, true to dump and false to not dump
        :type  csvdump:             bool


        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The jsonified data of the status
        :rtype:     dict

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/" + str(assessment_id) + "/history"

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('Error in getting assessment history')
            print(e)
            exit()

        jsonified_data = json.loads(raw_response.text)
        if csvdump==True:
            field_names = []

            for item in jsonified_data[0]:
                field_names.append(item)
            try:
                with open('assessmenthistory.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    for item in jsonified_data:
                        writer.writerow(item)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)

        return jsonified_data
        
    def list_attachments(self, assessment_id,csvdump=False,client_id=None):

        """
        Lists attachments associated with an assessment.

        :param assessment_id:       The assessment ID
        :type  assessment_id:       int

        :param csvdump:             Whether to dump the attachment data in a csv, true to dump and false to not dump
        :type  csvdump:             bool

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    A list of attachments associated with the assessment is returned.
        :rtype:     list

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/" + str(assessment_id) + "/attachment"

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('Error in listing attachments')
            print(e)
            exit()

        jsonified_response = json.loads(raw_response.text)

        if csvdump==True:
            field_names = []

            for item in jsonified_response[0]:
                field_names.append(item)
            try:
                with open('attachmentofassessment.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    for item in jsonified_response:
                        writer.writerow(item)
            except FileNotFoundError as fnfe:
                print("An exception has occurred while attempting to write the .csv file.")
                print()
                print(fnfe)

        return jsonified_response

    def get_attachment(self, assessment_id, attachment_uuid, filename, client_id=None):

        """
        Download an attachment associated with an assessment.

        :param assessment_id:       The assessment ID.
        :type  assessment_id:       int

        :param attachment_uuid:     The unique ID associated with the attachment.
        :type  attachment_uuid:     str

        :param filename:            The filename to be used for the downloaded file.
        :type  filename:            str

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    True/False indicating whether or not the operation was successful.
        :rtype:     bool

        :raises RequestFailed:
        :raises FileNotFoundError:
        :raises Exception:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/" + str(assessment_id) + "/attachment/" + str(attachment_uuid)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('Error in getting attachment')
            print(e)
            exit()

        try:
            open(filename, "wb").write(raw_response.content)
        except (FileNotFoundError, Exception):
            print('Error in getting downloading attachment')
            print(e)
            exit()

        print("Done.")
        success = True

        return success

    def get_attachment_metadata(self, assessment_id, attachment_uuid, client_id=None):

        """
        Get the metadata associated with an assessment's attachment.

        :param assessment_id:       The assessment ID.
        :type  assessment_id:       int

        :param attachment_uuid:     The unique ID associated with the attachment.
        :type  attachment_uuid:     str

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    A dictionary containing the metadata for the attachment is returned.
        :rtype:     dict

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/" + str(assessment_id) + "/attachment/" + str(attachment_uuid) + "/meta"

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('Error in getting attachment metada')
            print(e)
            exit()

        jsonified_data = json.loads(raw_response.text)

        return jsonified_data


### PRIVATE FUNCTIONS ##

    def edit_network_internalreport(self,assessment_id,conclusion,constraints,client_id=None):

        """
        Edit network internal report for an assessment

        :param assessment_id:       The assessment ID.
        :type  assessment_id:       int

        :param conclusion:          Conclusion statement for internal report
        :type  conclusion:          str

        :param conclusion:          Constraints statement for internal report
        :type  conclusion:          str

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:                Jsonified data of the response
        :rtype:     dict

        :raises RequestFailed:
        """
        
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.al_base_url.format(str(client_id),str(assessment_id))+'/NETWORK_INTERNAL'

        body= {"conclusion":conclusion,"constraints":constraints}

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url,body=body)
        except (RequestFailed,Exception) as e:
            print('Error in editing network internal report')
            print(e)
            exit()

        jsonified_data = json.loads(raw_response.text)

        return jsonified_data

    def edit_application_report(self,assessment_id,conclusion,constraints,client_id=None):

        """
        Edit application report for an assessment

        :param assessment_id:       The assessment ID.
        :type  assessment_id:       int

        :param conclusion:          Conclusion statement for internal report
        :type  conclusion:          str

        :param conclusion:          Constraints statement for internal report
        :type  conclusion:          str

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:                Jsonified data of the response
        :rtype:     dict

        :raises RequestFailed:
        """
        
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.al_base_url.format(str(client_id),str(assessment_id))+'/APPLICATION'

        body= {"conclusion":conclusion,"constraints":constraints}

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url,body=body)
        except (RequestFailed,Exception) as e:
            print('Error in editing application report')
            print(e)

        jsonified_data = json.loads(raw_response.text)

        return jsonified_data
    
    def edit_networkexternal_report(self,assessment_id,conclusion,constraints,client_id=None):

        """
        Edit network external report for an assessment

        :param assessment_id:       The assessment ID.
        :type  assessment_id:       int

        :param conclusion:          Conclusion statement for internal report
        :type  conclusion:          str

        :param conclusion:          Constraints statement for internal report
        :type  conclusion:          str

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:                Jsonified data of the response
        :rtype:     dict

        :raises RequestFailed:
        """
        
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.al_base_url.format(str(client_id),str(assessment_id))+'/NETWORK_EXTERNAL'

        body= {"conclusion":conclusion,"constraints":constraints}

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url,body=body)
        except (RequestFailed,Exception) as e:
            print('Error in editing network external report')
            print(e)
            exit()

        jsonified_data = json.loads(raw_response.text)

        return jsonified_data

    def lock_assessment(self, assessment_id, client_id=None):

        """
        Lock an assessment

        :param assessment_id:       The assessment ID.
        :type  assessment_id:       int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The jsonified data of the status
        :rtype:     dict

        :raises RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/" + str(assessment_id) + "/status"


        body= {
                 "status": "LOCKED"
              }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except (RequestFailed,Exception) as e:
            print()
            print('Error in locking assessment')
            print(e)
            exit()

        jsonified_data = json.loads(raw_response.text)

        return jsonified_data

    def unlock_assessment(self, assessment_id, client_id=None):

        """
        Unlock an assessment

        :param assessment_id:       The assessment ID.
        :type  assessment_id:       int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The jsonified data of the status
        :rtype:     dict

        :raises RequestFailed:
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/" + str(assessment_id) + "/status"

        body= {
                 "status": "UNLOCKED"
              }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except (RequestFailed,Exception) as e:
            print()
            print('Error in unlocking assessment')
            print(e)
            exit()
        jsonified_data = json.loads(raw_response.text)

        return jsonified_data  

    def get_assessment_filterfields(self, client_id=None):

        """
        List fields that can be filtered by in the search endpoint

        :param assessment_id:       The assessment ID.
        :type  assessment_id:       int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The jsonified data of the status
        :rtype:     dict

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/filter"

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed,Exception) as e:
            print('Error in getting assessment filter fields')
            print(e)
            exit()

        jsonified_data = json.loads(raw_response.text)

        return jsonified_data


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
