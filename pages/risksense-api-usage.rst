.. include:: /main/.special.rst

.. _installation:

======================================
Using Risksense API Library
======================================

To begin make sure you provide the system path to the lib package before importing the script
example 

.. code-block:: console

     >>> sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'lib'))


To use risksense lib package please ensure you import risksense api in your script

.. code-block:: console

     >>> import risksense_api as rsapi


To perform usage of the subject functions you must first create an object and use that object
for subject function definitions. Please ensure you should provide the client id either during function definitions or by setting a default client id using the below function ``set_default_client_id()``

.. code-block:: console

    >>> self.rs=rs_api.RiskSenseApi(self._rs_platform_url, api_key)
        self.rs.set_default_client_id(self.__client_id)

where self._rs_platform_url is the url of the platform and apikey is the user apikey

Now post the risksense object creation, you can use the object ``self.rs`` for using functions in risksense api packages

.. code-block:: console
  
    >>> self.rs.{subjectname}.{functionname}
    where 
        subjectname - The subject module present in the lib package
        functionname - The functionname define for  that particular subject



  