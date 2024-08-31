from avi.sdk.avi_api import ApiSession
from requests.packages import urllib3
urllib3.disable_warnings()
import json
import datetime, time
import pandas as pd


def extract_segroup_data (session_env, source_segroup_name):
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

    # Define GET request parameters
    url_path = "serviceenginegroup"
    query = {
      "skip_default": "true",
      "name": source_segroup_name,
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
    return(resp_data[0])

def extract_se_data_from_segroup (session_env, source_segroup_object):
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

    # GET Service Engine Related Configuration
    # Define GET request parameters
    se_group_uuid=source_segroup_object["uuid"]
    url_path = "serviceengine"
    query = {
      "skip_default": "true",
      "refers_to": f"serviceenginegroup:{se_group_uuid}",
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

def extract_interface_data (session_env, source_se_data, source_if_name):
    
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
    
    output_config={}
    # Extract Interface Information from Source Service Engines
    for i in range(len(source_se_data)):
        config=[]
        print("\033[1mExtracting information from SOURCE SE "+str(i+1)+" interface to migrate "+source_if_name[i]+" \033[0m")
        print("\033[1m----------------------------------------------------------------------------------------------------\033[0m")
        se_data_vnics = source_se_data[i]["data_vnics"]
        se_data_vnic_to_migrate = [ adapter for adapter in se_data_vnics if adapter.get("if_name") == source_if_name[i]]
        #se_data_vnic_to_migrate_df = pd.DataFrame(se_data_vnic_to_migrate)
        time.sleep(1/4)
        #display(se_data_vnic_to_migrate_df)
        se_vnic_to_migrate_config = se_data_vnic_to_migrate[0]["vnic_networks"][0]["ip"]
        se_vnic_to_migrate_config_df = pd.DataFrame(se_vnic_to_migrate_config)

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

        # Writing VNIC extracted variables 
        se_uuid = source_se_data[i]["uuid"]
        ip_addr = se_data_vnic_to_migrate[0]["vnic_networks"][0]["ip"]["ip_addr"]["addr"]
        mask = se_data_vnic_to_migrate[0]["vnic_networks"][0]["ip"]["mask"]
        mac_address = se_data_vnic_to_migrate[0]["mac_address"]
        if_name = source_if_name[i]
        vrf_ref = se_data_vnic_to_migrate[0]["vrf_ref"]

        # Printing Interface configuration
        print("   - Found IP Address "+ip_addr+"/"+str(mask))
        print("   - Found MAC Address "+mac_address)
        print("   - Found VRF Context "+vrf_name)
        print()
      
      
      # Populate a dictionary with extraced data
        config= {
                  "se_uuid": se_uuid,
                  "ip_addr":ip_addr,
                  "mask": mask,
                  "mac_address": mac_address,
                  "if_name": source_if_name[i],
                  "vrf_ref": vrf_ref
                  }
      # Populate a new key SE_n with discovered information for that particular interface
        output_config["SE_"+str(i+1)] = config

    print("\033[1mExtracting IP Routing Information for the VRF Context " +vrf_name+ " where "+source_if_name[i]+" is attached to \033[0m")
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
    
    print("\033[1mExtracting Networservice Information for the VRF Context "+vrf_name+" and Service Engine Group "+source_segroup_name+" \033[0m")
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
        print("Found Network Service for that VRF/SE_GROUP named "+network_service_config["name"])
        output_config["network_service_config"]=network_service_config
        try:
            for i in range(len(network_service_config["routing_service"]["floating_intf_ip"])):
                float_addr = network_service_config["routing_service"]["floating_intf_ip"][i]["addr"]
                float_type = network_service_config["routing_service"]["floating_intf_ip"][i]["type"]
                print("   - Found floating IP"+float_type+" "+float_addr)
        except:
                print("   - No Floating IP Addresses found")
    else:
        print('Error in GET request '+url_path+' :%s' % resp.text)
    
    return(output_config)




def extract_vss_data (session_env, source_se_data, interface_config):    
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
    
    output_config={}
    #extract_vss_info (session_env, source_se_data, interface_config) 
    # Extract related virtual services
    # GET Virtual Services Related Configuration


    #seg_data = source_segroup_data
    # Define GET request parameters
    se_group_uuid=source_se_data[0]["se_group_ref"].split("/")[5].split("#")[0]
    vrf_uuid=interface_config["ip_routing_config"]["vrf_uuid"]
    url_path = "virtualservice"
    query = {
      "skip_default": "true",
      "refers_to": "serviceenginegroup:"+se_group_uuid,
      "include_name": "true",
      "search": "(vrf_context_ref,"+vrf_uuid+")",
      "fields": "se_group_ref,vrf_context_ref,vsvip_ref,pool_ref"
    }

    # Send GET Request
    resp = api.get(url_path, params=query)
    #print(json.dumps(json.loads(resp.text), indent=3))
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
    

def extract_network_vsvip_data (session_env, source_vs_data):    
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
    
    config={}
    source_networks = []
    vsvips_config = []
    for i in range(len(source_vs_data)):
      vsvip_name = source_vs_data[i]["vsvip_ref"].split("#")[1]
      vsvip = api.get_object_by_name("vsvip", vsvip_name)
      placementnetwork_uuid = vsvip["vip"][0]["placement_networks"][0]["network_ref"].split("/")[5].split("#")[0]
      
      query = {
          "uuid": placementnetwork_uuid,
          "include_name": "true"
      }
      resp = api.get("network", params=query)
      
      network_name = json.loads(resp.text)["results"][0]["name"]
      if network_name not in source_networks:
          source_networks.append(network_name)
        
      vip_config = {
          "name": vsvip["name"],
          "vrf_context_ref": vsvip["vrf_context_ref"],
          "ip_address": vsvip["vip"][0]["ip_address"]["addr"],
          "placement_network_ref":  vsvip["vip"][0]["placement_networks"][0]["network_ref"],
          "placement_network":  network_name     
        }
      vsvips_config.append(vip_config)
    # Update information 
    config["network_config"]=source_networks
    config["vsvips_config"]=vsvips_config
    print ("The following placement networks has been found:")
    print(source_networks)
    print()
    print ("The following vsvips networks has been found:")
    vips=[]
    for item in vsvips_config:
        vips.append(item["name"])
    print(vips)
    return(config) 