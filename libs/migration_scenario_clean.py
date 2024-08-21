# Load Scenario

from avi.sdk.avi_api import ApiSession
from requests.packages import urllib3
urllib3.disable_warnings()
import json
import time

def clean_scenario(session_env):
    source_segroup = "SEG-SOURCE-MAD-002"
    target_segroup = "SEG-TARGET-MAD-001"
    network_name = "home-network"

    vs_source_names = ["VS_SOURCE_001", "VS_SOURCE_002", "VS_SOURCE_003"]
    vsvip_source_names = ["vsvip-source-001", "vsvip-source-002", "vsvip-source-003"]
    vs_target_names = ["VS_TARGET_001", "VS_TARGET_002", "VS_TARGET_003"]
    vsvip_target_names = ["vsvip-target-001", "vsvip-target-002", "vsvip-target-003"]

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


    # Delete all VSs from source_segroup
    print("Deleting VSs")
    time.sleep(1/2)
    for i in range(len(vs_source_names)):
      api_resource = "virtualservice"
      object_name = vs_source_names[i]
      object = api.get_object_by_name(api_resource, object_name)

      # Check if a non-empty response was received 
      if object:
        # Extract uuid from response
        object_uuid = object["uuid"]
 
        # Define DELETE parameters
        url_path = api_resource + "/" +object_uuid
        resp = api.delete(url_path)
        if resp.status_code in range(200, 299):
            print('- Object '+url_path+' named '+vs_source_names[i]+ " deleted", resp.reason)#, resp.text)
        else:
            print('Error in deleting '+url_path+' :%s' % resp.text)

    # Delete all VSs from target
    for i in range(len(vs_target_names)):
      api_resource = "virtualservice"
      object_name = vs_target_names[i]
      object = api.get_object_by_name(api_resource, object_name)

      # Check if a non-empty response was received 
      if object:
        # Extract uuid from response
        object_uuid = object["uuid"]
 
        # Define DELETE parameters
        url_path = api_resource + "/" +object_uuid
        resp = api.delete(url_path)
        if resp.status_code in range(200, 299):
            print('- Object '+url_path+' named '+vs_target_names[i]+ " deleted", resp.reason)#, resp.text)
        else:
            print('Error in deleting '+url_path+' :%s' % resp.text)
    
    # Delete all vsvips from source_VS_GROUP
    print("Deleting vsvips")
    time.sleep(1/2)
    for i in range(len(vsvip_source_names)):
      api_resource = "vsvip"
      object_name = vsvip_source_names[i]
      object = api.get_object_by_name(api_resource, object_name)

      # Check if a non-empty response was received 
      if object:
        # Extract uuid from response
        object_uuid = object["uuid"]
 
        # Define DELETE parameters
        url_path = api_resource + "/" +object_uuid
        resp = api.delete(url_path)
        if resp.status_code in range(200, 299):
            print('- Object '+url_path+' named '+vsvip_source_names[i]+ " deleted", resp.reason)#, resp.text)
        else:
            print('Error in deleting '+url_path+' :%s' % resp.text)
  
    # Delete all vsvips from source_segroup
    for i in range(len(vsvip_target_names)):
      api_resource = "vsvip"
      object_name = vsvip_target_names[i]
      object = api.get_object_by_name(api_resource, object_name)

      # Check if a non-empty response was received 
      if object:
        # Extract uuid from response
        object_uuid = object["uuid"]
 
        # Define DELETE parameters
        url_path = api_resource + "/" +object_uuid
        resp = api.delete(url_path)
        if resp.status_code in range(200, 299):
            print('- Object '+url_path+' named '+vsvip_target_names[i]+ " deleted", resp.reason)#, resp.text)
        else:
            print('Error in deleting '+url_path+' :%s' % resp.text)
