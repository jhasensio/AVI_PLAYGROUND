# Other scripts for migration
from avi.sdk.avi_api import ApiSession
from requests.packages import urllib3
urllib3.disable_warnings()
import json


# Disable interface if_name of service engine se_name 
def disable_interface (session_env, se_name, if_name):  
# Establish a first session with AVI Controller
    api = ApiSession(
        controller_ip=session_env['controller_ip'],
        username=session_env['controller_username'],
        password=session_env['controller_password'],
        tenant=session_env['tenant'],
        api_version=session_env['api_version']
        )
    # Update headers and api version imported from demo env file with controller version (ensure actual API Version is uses in subsequent requests
    session_env['headers']['X-Avi-Version'] = api.remote_api_version['Version']
    session_env['api_version'] = api.remote_api_version['Version']

    # Create a new session with received AVI API Version
    api = ApiSession(
        controller_ip=session_env['controller_ip'],
        username=session_env['controller_username'],
        password=session_env['controller_password'],
        tenant=session_env['tenant'],
        api_version=session_env['api_version']
        )
    # Read 
    se = api.get_object_by_name("serviceengine", se_name)
    se_uuid = se["uuid"]

    #adapter_config = [ data_vnic for data_vnic in se["data_vnics"] if data_vnic.get("if_name") == if_name ]
    
    # Loop through each adapter in the list
    for adapter in se["data_vnics"]:
        # Check if the key_to_check matches the value_to_match
        if adapter.get("if_name") == if_name:
            # Update the value of key_to_modify
            adapter["enabled"] = False
     
    body = se

    # Define PUT parameters
    url_path="serviceengine/"+se_uuid

    #Send BODY information via PUT
    resp = api.put (url_path, data=json.dumps(body))

    if resp.status_code in range(200, 299):
      print(resp)
      print("- Object "+url_path+" modified", resp.reason)#, resp.text)
      print()
    else:
      print('Error in modifying '+url_path+' :%s' % resp.text)

# Enable interface if_name of service engine se_name 
def enable_interface (session_env, se_name, if_name):  
# Establish a first session with AVI Controller
    api = ApiSession(
        controller_ip=session_env['controller_ip'],
        username=session_env['controller_username'],
        password=session_env['controller_password'],
        tenant=session_env['tenant'],
        api_version=session_env['api_version']
        )
    # Update headers and api version imported from demo env file with controller version (ensure actual API Version is uses in subsequent requests
    session_env['headers']['X-Avi-Version'] = api.remote_api_version['Version']
    session_env['api_version'] = api.remote_api_version['Version']

    # Create a new session with received AVI API Version
    api = ApiSession(
        controller_ip=session_env['controller_ip'],
        username=session_env['controller_username'],
        password=session_env['controller_password'],
        tenant=session_env['tenant'],
        api_version=session_env['api_version']
        )
    # Read 
    se = api.get_object_by_name("serviceengine", se_name)
    se_uuid = se["uuid"]

    #adapter_config = [ data_vnic for data_vnic in se["data_vnics"] if data_vnic.get("if_name") == if_name ]
    
    # Loop through each adapter in the list
    for adapter in se["data_vnics"]:
        # Check if the key_to_check matches the value_to_match
        if adapter.get("if_name") == if_name:
            # Update the value of key_to_modify
            adapter["enabled"] = True
      
    body = se

    # Define PUT parameters
    url_path="serviceengine/"+se_uuid

    #Send BODY information via PUT
    resp = api.put (url_path, data=json.dumps(body))

    if resp.status_code in range(200, 299):
      print(resp)
      print("- Object "+url_path+" modified", resp.reason)#, resp.text)
      print()
    else:
      print('Error in modifying '+url_path+' :%s' % resp.text)


    


