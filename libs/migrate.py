# Other scripts for migration
from avi.sdk.avi_api import ApiSession
from requests.packages import urllib3
urllib3.disable_warnings()
import json


# Disable interface if_name of service engine se_name 
def disable_interface (api: object, se_name: str, if_name: str):  
# Establish a first session with AVI Controller
    """
    Disable a interface named if_name of a servive engine name (Default-Cloud is assumed) 
    
    Parameters:
    -----------
    api : avi.sdk.avi_api.ApiSession
      The AVI ApiSession object containing session paramenters to use AVI API
    
    se_name : str
      The name of the Service Engine where the interface belong to
    
    if_name : str
      The name of the Service Engine where the interface belong to
    
    """ 
    # Read 
    se = api.get_object_by_name("serviceengine", se_name)
    se_uuid = se["uuid"]
    
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
      print(" - Interface "+if_name+" set to DISABLED at SE "+ se["name"])
    else:
      print('Error in modifying '+url_path+' :%s' % resp.text)

# Enable interface if_name of service engine se_name 
def enable_interface (api: object, se_name: str, if_name: str):  
    # Establish a first session with AVI Controller
    """
    Disable a interface named if_name of a servive engine name (Default-Cloud is assumed) 
    
    Parameters:
    -----------
    api : avi.sdk.avi_api.ApiSession
      The AVI ApiSession object containing session paramenters to use AVI API
    
    se_name : str
      The name of the Service Engine where the interface belong to
    
    if_name : str
      The name of the Service Engine where the interface belong to
    
    """ 
    # Read 
    se = api.get_object_by_name("serviceengine", se_name)
    se_uuid = se["uuid"]
    
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
      print(" - Interface "+if_name+" set to ENABLED at SE "+ se["name"])
    else:
      print('Error in modifying '+url_path+' :%s' % resp.text)

# Configure interface if_name of service engine se_name 
def configure_interface (api, target_se_data, target_vrf_name):
    """
    :param api: apisession object 
    :param target_se: dictionary that must containing following keys(
         se_name
         if_name,
         if_ip_addr,
         if_mask,
         vrf_name) 
    """
    """
    Configure the IP  a interface named if_name of a servive engine name (Default-Cloud is assumed) 
    
    Parameters:
    -----------
    api : avi.sdk.avi_api.ApiSession
      The AVI ApiSession object containing session paramenters to use AVI API
    
    target_se: dict
      A variable that must containing following keys(
         se_name
         if_name,
         if_ip_addr,
         if_mask,
         vrf_name)

    target_vrf_name: str
      A string containing the name of the VRF attached to interface to configure  
    
    """ 
    # Read 
    se = api.get_object_by_name("serviceengine", target_se_data["se_name"], params={"include_name": "true"})
    se_uuid = se["uuid"]
    vrf = api.get_object_by_name("vrfcontext", target_vrf_name, params={"include_name": "true"})
    vrf_ref = api.get_obj_ref(vrf)

    # Loop through each adapter in the list
    for adapter in se["data_vnics"]:
        # Update config for matching interface
        if adapter.get("if_name") == target_se_data["if_name"]:
            # Update the value of keys to modify with new config
            vnic_network = [{
                "ip": {
                  "ip_addr": {
                      "addr": target_se_data["if_ip_addr"],
                      "type": "V4"
                    },
                  "mask": target_se_data["if_mask"]
                  },
                  "mode": "STATIC"
                }]
            adapter["vnic_networks"]= vnic_network
            adapter["enabled"] = False
            adapter["vrf_ref"] = vrf_ref
      
    body = se

    # Define PUT parameters
    url_path="serviceengine/"+se_uuid

    #Send BODY information via PUT
    resp = api.put (url_path, data=json.dumps(body))

    if resp.status_code in range(200, 299):
      print(" - Interface "+target_se_data["if_name"]+" of Service Engine "+target_se_data["se_name"]+" configured with IP Address "+target_se_data["if_ip_addr"]+"/"+str(target_se_data["if_mask"])+" at VRF "+target_vrf_name)
    else:
      print('Error in modifying '+url_path+' :%s' % resp.text)


def disable_vs (api: object, vs_name: str):  
    """
    Disable a interface named if_name of a servive engine name (Default-Cloud is assumed) 
    
    Parameters:
    -----------
    api : avi.sdk.avi_api.ApiSession
      The AVI ApiSession object containing session paramenters to use AVI API
    
    vs_name : str
      The name of the VS to disable 
    
    """ 
    # Read 
    vs = api.get_object_by_name("virtualservice", vs_name)
    vs_uuid = vs["uuid"]
    

    body = vs
    body["enabled"] = False

    # Define PUT parameters
    url_path="virtualservice/"+vs_uuid

    #Send BODY information via PUT
    resp = api.put (url_path, data=json.dumps(body))

    if resp.status_code in range(200, 299):
      print(" - VirtualService "+vs_name+" set to DISABLED")
    else:
      print('Error in modifying '+url_path+' :%s' % resp.text)

def enable_vs (api: object, vs_name: str):  
    """
    Disable a Virtual service named if_name of a servive engine name (Default-Cloud is assumed) 
    
    Parameters:
    -----------
    api : avi.sdk.avi_api.ApiSession
      The AVI ApiSession object containing session paramenters to use AVI API
    
    vs_name : str
      The name of the VS to enable 
    
    """ 
    # Read 
    vs = api.get_object_by_name("virtualservice", vs_name)
    vs_uuid = vs["uuid"]
    

    body = vs
    body["enabled"] = True

    # Define PUT parameters
    url_path="virtualservice/"+vs_uuid

    #Send BODY information via PUT
    resp = api.put (url_path, data=json.dumps(body))

    if resp.status_code in range(200, 299):
      print(" - VirtualService "+vs_name+" set to ENABLED")
    else:
      print('Error in modifying '+url_path+' :%s' % resp.text)

def adjust_max_vs_per_se (api: object, source_seg_name: str, target_seg_name: str) -> int:
    """
    Function to acommodate migrated Vs from source seg into target seg
    
    Parameters:
    -----------
    api : avi.sdk.avi_api.ApiSession
      The AVI ApiSession object containing session paramenters to use AVI API
    
    vs_name : str
      The name of the VS to enable 
    
    """ 
    # Increase the number of VS per SE to acommodate imported VS
    source_seg = api.get_object_by_name("serviceenginegroup", source_seg_name)
    source_seg_uuid = source_seg["uuid"]

    target_seg = api.get_object_by_name("serviceenginegroup", target_seg_name)
    target_seg_uuid = target_seg["uuid"]
    target_max_vs_per_se = target_seg["max_vs_per_se"]
    
    # Get Source VS Count
    query = {
       "include_name": "true",
       "refers_to": "serviceenginegroup:"+source_seg_uuid
    }

    resp = api.get("virtualservice", params=query)
    if resp.status_code in range(200, 299):
        source_vs_count = json.loads(resp.text)["count"]
        print(" - Found "+str(source_vs_count)+" virtual services at source Service Engine group "+ source_seg_name)
    else:
      print('Error in getting virtualservices information :%s' % resp.text)
    
    # Get Source VS Count
    query = {
       "include_name": "true",
       "refers_to": "serviceenginegroup:"+target_seg_uuid
    }
     
    resp = api.get("virtualservice", params=query)
    if resp.status_code in range(200, 299):
        target_vs_count = json.loads(resp.text)["count"]
        print(" - Found "+str(target_vs_count)+" virtual services at target Service Engine group "+ source_seg_name)
    else:
      print('Error in getting virtualservices information :%s' % resp.text)
    
    body = target_seg

    if ((source_vs_count + target_vs_count) >= (target_max_vs_per_se - 5)):
        body["max_vs_per_se"] = source_vs_count + target_vs_count + 5
        
        # Remove _last_modified key to avoid concurrent update error
        body.pop("_last_modified", None)

        url_path = "serviceenginegroup/"+target_seg_uuid
        resp = api.put (url_path, data=json.dumps(body))

        if resp.status_code in range(200, 299):
          return(json.loads(resp.text)["max_vs_per_se"])
        else:
          print('Error in modifying '+url_path+' :%s' % resp.text)
    else:
       return(target_max_vs_per_se)