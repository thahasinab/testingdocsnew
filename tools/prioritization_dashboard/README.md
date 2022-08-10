+-----------------------------------------------------------+
|                                                           |
|                  Prioritization Dashboard                    |
|                                                           |
+-----------------------------------------------------------+

This script will display data from theprioritization 
dashboard based on the input provided by you in the terminal


+--------------------+---------------------------------------
|    Requirements    |
+--------------------+

This script requires a working installation of Python3 and the
ability to install Python packages.



+--------------------+---------------------------------------
|    Installation    |
+--------------------+

Copy the zip file to your desired location and unzip it.
Using your terminal, navigate to the folder that you just
unzipped. Run the main.py file in the terminal


+---------------------+--------------------------------------
|    Configuration    |
+---------------------+

The configuration file is found at conf/config.toml. This
file is formatted using TOML formatting. Using your preferred
text editor, open this file.


Update the platform URL field to reflect the URL of the
RiskSense platform you use. Update the API key field to
reflect an API key generated by your user. You may also
specify the name of the .CSV file the script should read in
the Qualys filename field.

The remaining fields in the configuration file should be
configured to reflect your desired values.



+-------------+----------------------------------------------
|    Usage    |
+-------------+

To execute the script, using your terminal, navigate to the
unzipped folder containing the script. Issue the following
command:

    python3 prioritization.py

       --- OR (depending on your install) ---

    python prioritization.py
Fill the necessary data input in the terminal prompts and the
dashboard data will be shown in the terminal

+-------------+----------------------------------------------
|    NOTE    |
+-------------+

1. Please check Prioritization.log for the log of the script for 
   more information of any errors or info while running the script