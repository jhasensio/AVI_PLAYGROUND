from avi.sdk.avi_api import ApiSession
from requests.packages import urllib3
urllib3.disable_warnings()
import json
import pandas as pd

def extract_segroup_data (api: object, segroup_name: dict) -> dict:
    """
    Extract information of a given Service Engine Group
    
    Parameters:
    -----------
    api : avi.sdk.avi_api.ApiSession
      The AVI ApiSession object containing session paramenters to use AVI API
    
    segroup_name : string
      The service group name of interest
    
    Returns:
    --------
    dict
      Dictionary containing serviceenginegroup object output

    """ 

    # Define GET request parameters
    url_path = "serviceenginegroup"
    query = {
      "skip_default": "true",
      "name": segroup_name,
      "include_name": "true"
    }
    # Send GET Request
    resp = api.get(url_path, params=query)


    # Control Response Status Code
    if resp.status_code in range(200, 299):
        
      # Convert response JSON into Python Dictionary
      resp_data = json.loads(resp.text)

      # Extract Result
      resp_data = resp_data["results"]
      resp_names = [resp_name["name"] for resp_name in resp_data]
      print("The following " + url_path + " names has been found:")
      print(resp_names)
      print()
    else:
        print('Error in GET request '+url_path+' :%s' % resp.text)

    # Save Result
    return(resp_data[0])

def extract_se_data_from_segroup (api: object, segroup: dict) -> list:
    """
    Extract Service Engines information of a given Service Engine Group
    
    Parameters:
    -----------
    api : object
      The avi.sdk.avi_api.ApiSession object containing session paramenters to use AVI API
    
    segroup : dict
      The dictionary containing service engine group information
    
    Returns:
    --------
    list
      Dictionary containing service engine configuration output

    """ 

    # GET Service Engine Related Configuration
    # Define GET request parameters
    segroup_uuid=segroup["uuid"]
    url_path = "serviceengine"
    query = {
      "skip_default": "true",
      "refers_to": "serviceenginegroup:"+segroup_uuid,
      "include_name": "true"
    }

    # Send GET Request
    resp = api.get(url_path, params=query)
    #print ("Request sent to URL: " + resp.url)

    # Control Response Status Code
    if resp.status_code in range(200, 299):
      #print(resp)
      #print(resp.reason)
        
      # Convert response JSON into Python Dictionary
      resp_data = json.loads(resp.text)

      # Extract Result
      resp_data = resp_data["results"]
      resp_names = [resp_name["name"] for resp_name in resp_data]
      print("The following " + url_path + " names has been found:")
      print(resp_names)
      print()
    else:
        print('Error in GET request '+url_path+' :%s' % resp.text)

    # Save Result
    return(resp_data)

def extract_interface_data (api: object, source_se_data: list, source_if_names: list, target_se_data: list, target_if_names: list) -> dict:
    """
    Extract relevant network and interface configuration for migration purposes from source to target  
    
    Parameters:
    -----------
    api : object
      The avi.sdk.avi_api.ApiSession object containing session paramenters to use AVI API
    
    source_se_data : list
      A list containing source service engine group information
    
    source_if_name : list
      A list with source if name, e.g ["eth1", "eth1"]
    
    source_se_data : list
      A dictionary containing source service engine group information
    
    target_if_name : list
      A string with target if name, e.g e.g ["eth2", "eth2"]
    
    Returns:
    --------
    list
      Dictionary containing service engine configuration output
    """ 
    output_config={}
    se_config=[]
    # Extract Interface Information from Source Service Engines
    for i in range(len(source_se_data)):
        print("\033[1mExtracting information from SOURCE SE "+str(i+1)+" interface to migrate "+source_if_names[i]+" \033[0m")
        print("\033[1m----------------------------------------------------------------------------------------------------\033[0m")
        se_data_vnics = source_se_data[i]["data_vnics"]
        se_data_vnic_to_migrate = [ adapter for adapter in se_data_vnics if adapter.get("if_name") == source_if_names[i]]

        # Extract VRF UUID from the vrf_ref
        
        vrf_ref = se_data_vnic_to_migrate[0]['vrf_ref']
        vrf_uuid = vrf_ref.split("/")[5].split("#")[0]
        vrf_name = vrf_ref.split("#")[1]
        
        vrf_config = {  "vrfcontext": vrf_name,
                        "vrf_ref": vrf_ref,
                        "vrf_uuid": vrf_uuid
                     }

        # Insert information into output_config dictionary
        output_config["ip_routing_config"] = vrf_config

        # Writing SOURCE VNIC extracted variables 
        src_se_uuid = source_se_data[i]["uuid"]
        src_se_name = source_se_data[i]["name"]
        src_ip_addr = se_data_vnic_to_migrate[0]["vnic_networks"][0]["ip"]["ip_addr"]["addr"]
        src_mask = se_data_vnic_to_migrate[0]["vnic_networks"][0]["ip"]["mask"]
        src_mac_address = se_data_vnic_to_migrate[0]["mac_address"]
        src_if_name = source_if_names[i]
        src_vrf_ref = se_data_vnic_to_migrate[0]["vrf_ref"]

        # Writing TARGET VNIC extracted variables 
        target_se_uuid = target_se_data[i]["uuid"]
        target_se_name = target_se_data[i]["name"]
        target_intf_name = target_if_names[i]
        target_if_ip_addr = src_ip_addr
        target_if_mask = src_mask

        # Printing Interface configuration
        print("   - Found IP Address "+src_ip_addr+"/"+str(src_mask))
        print("   - Found MAC Address "+src_mac_address)
        print("   - Found VRF Context "+vrf_name)
        print()
      
        
      # Populate a dictionary with extraced data
        se_pair_config= {
                  "source_se": {
                     "se_uuid": src_se_uuid,
                     "se_name": src_se_name,
                     "if_name": src_if_name,
                     "if_vrf_ref": src_vrf_ref,
                     "if_ip_addr": src_ip_addr,
                     "if_mask": src_mask,
                     "if_mac_address": src_mac_address,
                  },
                   "target_se": {
                       "se_uuid": target_se_uuid,
                       "se_name": target_se_name,
                       "if_name": target_intf_name,
                       "if_ip_addr": target_if_ip_addr,
                       "if_mask": target_if_mask
                   }
        } 
        se_config.append(se_pair_config)
      # Populate a new key SE_n with discovered information for that particular interface
        output_config["se_pairs"] = se_config

    print("\033[1mExtracting IP Routing Information for the VRF Context " +vrf_name+ " where "+source_if_names[i]+" is attached to \033[0m")
    print("\033[1m----------------------------------------------------------------------------------------------------\033[0m")

    resp = api.get_object_by_name("vrfcontext", vrf_name)
    # Extracting IP Static Route information
    try:
      static_routes =[]
      for i in range(len(resp["static_routes"])):
        route_type = resp["static_routes"][i]["prefix"]["ip_addr"]["type"]
        route_prefix = resp["static_routes"][i]["prefix"]["ip_addr"]["addr"]
        route_mask = resp["static_routes"][i]["prefix"]["mask"]
        route_next_hop = resp["static_routes"][i]["next_hop"]["addr"]
        print("   - Found static IP"+route_type+" route prefix "+route_prefix+"/"+str(route_mask)+" pointing to next-hop --> "+route_next_hop)
        static_routes.insert(i, {
            "route_type": route_type,
            "route_prefix": route_prefix,
            "route_mask": route_mask,
            "route_next_hop": route_next_hop
        })
    except:
        print("   - No Static routes found")
    print()

    # Add Extracted routing information to the dictionary
    output_config["ip_routing_config"]["static_routes"]=static_routes
    source_segroup_name = source_se_data[0]["se_group_ref"].split("#")[1]
    se_group_uuid = source_se_data[0]["se_group_ref"].split("/")[5].split("#")[0]
    
    print("\033[1mExtracting Networkservice Information for the VRF Context "+vrf_name+" and Service Engine Group "+source_segroup_name+" \033[0m")
    print("\033[1m----------------------------------------------------------------------------------------------------\033[0m")

    # Read Network Service attached to the VRF and Source SEGroup 
    query = {
      "refers_to": "vrfcontext:"+vrf_uuid,
      "search": "(se_group_ref,"+se_group_uuid+")"
    }
    resp = api.get('networkservice', params=query)
    if resp.status_code in range(200, 299):
      # Convert response JSON into Python Dictionary
      if json.loads(resp.text)["count"] == 0:
        print("No Network Service Found for that particular VRF/SE_GROUP")
      else:
        network_service_config = json.loads(resp.text)["results"][0]
        print("   - Found Network Service for that VRF/SE_GROUP named "+network_service_config["name"])
        output_config["network_service_config"]=network_service_config
        try:
            for i in range(len(network_service_config["routing_service"]["floating_intf_ip"])):
                float_addr = network_service_config["routing_service"]["floating_intf_ip"][i]["addr"]
                float_type = network_service_config["routing_service"]["floating_intf_ip"][i]["type"]
                print("      - Found floating IP"+float_type+" "+float_addr)
        except:
                print("      - No Floating IP Addresses found")
    else:
        print('Error in GET request networkservice:%s' % resp.text)
    
    return(output_config)

def extract_vss_data (api: object, source_se_data: list, interface_config: dict) -> list:   
    """
    Extract relevant Virtual Services information from a given source_se_data and interface_config extracted previously using 
    extract_se_data_from_se_group and extract_interface_data functions
    
    Parameters:
    -----------
    api : object
      The avi.sdk.avi_api.ApiSession object containing session paramenters to use AVI API
    
    source_se_data : list
      A list containing source service engine group information
    
    interface_config : dictionary
      A dictionary with interface config output from extract_interface_data function
    
    Returns:
    --------
    list
      Dictionary containing Virtual Services Configuration 
    """ 
    
    se_group_uuid=source_se_data[0]["se_group_ref"].split("/")[5].split("#")[0]
    vrf_uuid=interface_config["ip_routing_config"]["vrf_uuid"]

    query = {
      "skip_default": "true",
      "refers_to": "serviceenginegroup:"+se_group_uuid,
      "include_name": "true",
      "search": "(vrf_context_ref,"+vrf_uuid+")",
      "fields": "se_group_ref,vrf_context_ref,vsvip_ref,pool_ref"
    }

    # Send GET Request
    resp = api.get("virtualservice", params=query)
  
    # Control Response Status Code
    if resp.status_code in range(200, 299):
        
      # Convert response JSON into Python Dictionary
      resp_data = json.loads(resp.text)

      # Extract Result
      resp_data = resp_data["results"]
      for vs in resp_data:
         print("   - Found virtualservice named "+vs["name"]+" at VRF "+ vs["vrf_context_ref"].split("#")[1]+" associated with VSVIP "+vs["vsvip_ref"].split("#")[1])
      print()
    else:
        print('Error in GET request virtualservice :%s' % resp.text)

    # Save Result
    return(resp_data)
    
def extract_network_vsvip_data (api: object, source_vs_data: list) -> list:    
    """
    Extract relevant VSVIP and Network Placement information from previously collected Virtual Services information using extract_vss_data function 
    
    Parameters:
    -----------
    api : object
      The avi.sdk.avi_api.ApiSession object containing session paramenters to use AVI API
    
    source_vs_data : list
      A list containing relevant virtual service information extracted using extract_vss_data function
    
    Returns:
    --------
    list
      Dictionary containing Virtual Services Configuration 
    """ 
    
    config={}
    source_networks = []
    vsvips_config = []
    for i in range(len(source_vs_data)):
      vsvip_name = source_vs_data[i]["vsvip_ref"].split("#")[1]
      vsvip = api.get_object_by_name("vsvip", vsvip_name, params={"include_name": "true"})
      placement_network_name = vsvip["vip"][0]["placement_networks"][0]["network_ref"].split("#")[1]
      placement_network_ref = vsvip["vip"][0]["placement_networks"][0]["network_ref"]
      
      
      if placement_network_name not in source_networks:
          source_networks.append(placement_network_name)
        
      vip_config = {
          "name": vsvip["name"],
          "vrf_context_ref": vsvip["vrf_context_ref"],
          "vrf_context_name": vsvip["vrf_context_ref"].split("#")[1],
          "ip_address": vsvip["vip"][0]["ip_address"]["addr"],
          "placement_network_ref":  placement_network_ref,
          "placement_network":  placement_network_name     
        }
      vsvips_config.append(vip_config)
    # Update information 
    config["network_config"]=source_networks
    config["vsvips_config"]=vsvips_config
    for net in source_networks:
      print ("   - Found placement network "+ net)
    for vip in vsvips_config:
      print ("   - Found vsvip named "+vip["name"]+ " at VRF "+ vip["vrf_context_name"] + " with IP Address " + vip["ip_address"] + " placed at network " + vip["placement_network"])
    return(config) 