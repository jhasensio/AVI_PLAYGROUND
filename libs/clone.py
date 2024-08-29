# Ancillary scripts for cloning existing AVI objects

from avi.sdk.avi_api import ApiSession
from requests.packages import urllib3
urllib3.disable_warnings()
import json

# Creates a NEW VRF named source_vrf-NEW
def clone_vrf (session_env, source_vrf_name):
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
    
    # Get source object 
    # Cloning an object from an exising one after changing required parameters
    api_resource = "vrfcontext"

    # Get the existing Object to be used as template
    body = api.get_object_by_name ("vrfcontext", source_vrf_name) # Response to be used as template
    
    if (body):
      # Update body with new name if exists
      body["name"] = source_vrf_name+"-NEW"
      # Print info
      print("Cloning existing "+api_resource+" "+source_vrf_name+" into "+source_vrf_name+"-NEW" )

      #Send BODY information via POST
      resp = api.post (api_resource, data=json.dumps(body))

      if resp.status_code in range(200, 299):
        print(resp)
        print('- New '+api_resource+' named '+body['name'], resp.reason)#, resp.text)
        return (json.loads(resp.text))
      else:
        print('Error in creating '+api_resource+' :%s' % resp.text)
    else:
      return()


# Creates a NEW NETWORK copied from source_network in vrfcontext vrf_name
def clone_network (session_env, source_network, target_vrf_name):
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
    
    # Get source object 
    # Cloning an object from an exising one after changing required parameters
    api_resource = "network"
    object_name = source_network

    # Get the existing Object to be used as template
    body = api.get_object_by_name (api_resource, object_name) # Response to be used as template

    if (body):
      # Get VRF reference 
      target_vrf = api.get_object_by_name("vrfcontext", target_vrf_name)
      target_vrf_ref = api.get_obj_ref(target_vrf)

      if (target_vrf):
        # Update body with new name 
        body["name"] = source_network+"-NEW"
        body["vrf_context_ref"] = target_vrf_ref
        
        # Print info
        print("Cloning existing "+api_resource+" "+source_network+" into "+source_network+"-NEW at VRF "+target_vrf_name )

        #Send BODY information via POST
        resp = api.post (api_resource, data=json.dumps(body))

        if resp.status_code in range(200, 299):
          print(resp)
          print('- New '+api_resource+' named '+body['name'], resp.reason)#, resp.text)
          return (json.loads(resp.text))
        else:
          print('Error in creating '+api_resource+' :%s' % resp.text)

# Creates a NEW NETWORKSERVICE copied from source_networkservice in vrfcontext vrf_name and serviceenginegroup name new_seg_name
def clone_networkservice (session_env, source_networkservice, target_vrf, target_segroup):
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
    
    # Get source object 
    # Cloning an object from an exising one after changing required parameters
    api_resource = "networkservice"
    object_name = source_networkservice

    # Get the existing Object to be used as template
    body = api.get_object_by_name (api_resource, object_name) # Response to be used as template

    if (body): 
      # Get VRF reference 
      vrfcontext = api.get_object_by_name("vrfcontext", target_vrf)
      vrf_ref = api.get_obj_ref(vrfcontext)

      # Get SEGroup reference 
      segroup = api.get_object_by_name("serviceenginegroup", target_segroup)
      se_group_ref = api.get_obj_ref(segroup)

      # Update body with new name 
      body["name"] = source_networkservice+"-NEW"
      body["se_group_ref"] = se_group_ref
      body["vrf_ref"] = vrf_ref
      
      # Print info
      print("Cloning existing "+api_resource+" "+source_networkservice+" into "+source_networkservice+"-NEW" )

      #Send BODY information via POST
      resp = api.post (api_resource, data=json.dumps(body))

      if resp.status_code in range(200, 299):
        print(resp)
        print('- New '+api_resource+' named '+body['name'], resp.reason)#, resp.text)
        return (json.loads(resp.text))
      else:
        print('Error in creating '+api_resource+' :%s' % resp.text)


# Extract VSVIPS from a given VRF and clone them in a new network and new vrf a NEW NETWORK copied from source_network in vrfcontext vrf_name and serviceenginegroup name new_seg_name
def clone_vsvips (session_env, source_vrf, target_vrf, target_network):
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
    
    # Get SOURCE VRF UUID to create the GET queryeference 
    source_vrfcontext = api.get_object_by_name("vrfcontext", source_vrf)
    if (source_vrfcontext):
      source_vrf_uuid = source_vrfcontext["uuid"]
      # Get NEW network reference 
      network = api.get_object_by_name("network", target_network)
      if (network):
        target_network_ref = api.get_obj_ref(network)
        # Get NEW VRF reference 
        target_vrfcontext = api.get_object_by_name("vrfcontext", target_vrf)
        if (target_vrfcontext):
          target_vrf_ref = api.get_obj_ref(target_vrfcontext)
          target_vrf_uuid = target_vrfcontext["uuid"]

          # Extract all the vsvips that refers to the source VRF
          query = {
         "refers_to": "vrfcontext:"+source_vrf_uuid
          }
          resp = api.get ("vsvip", params=query) 
          if resp.status_code in range(200, 299):
            print ("\033[1mFound "+str(json.loads(resp.text)["count"])+" VSVIP Objects @ source VRF context "+source_vrf+"\033[0m")
            print("\033[1m-------------------------------------------------------------------------------\033[0m")

          else:
              print('Error in getting '+api_resource+' :%s' % resp.text)
    
          #  Convert response JSON into Python Dictionary
          resp = json.loads(resp.text)["results"]  
   
          # Cloning an object from an exising one after changing required parameters
          for body in resp:
            # Print info
            print("Cloning existing vsvip "+body["name"]+" @ VRF context "+source_vrf+" into new vsvip "+body["name"]+"-NEW @ VRF context "+target_vrf )
            # Update body with updated information 
            body["name"] = body["name"]+"-NEW"
            body["vrf_context_ref"] = target_vrf_ref
            body["vip"][0]["placement_networks"][0]["network_ref"] = target_network_ref

            # Cloning an object from an exising one after changing required parameters

            #Send BODY information via POST
            resp = api.post ("vsvip", data=json.dumps(body))

            if resp.status_code in range(200, 299):
              print('- New vsvip named '+body['name'], resp.reason)#, resp.text)
              print()
            else:
              print('Error in creating '+api_resource+' :%s' % resp.text)
            
          # Extract all the created objects
          query = {
              "refers_to": "vrfcontext:"+target_vrf_uuid
          }
          resp = api.get ("vsvip", params=query) 
          if resp.status_code in range(200, 299):
            return(json.loads(resp.text)["results"])


# Extract VSVIPS from a given VRF and clone them in a new network and new vrf a NEW NETWORK copied from source_network in vrfcontext vrf_name and serviceenginegroup name new_seg_name
def clone_pools (session_env, source_vrf, target_vrf):
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
    
    # Set API Resource to be cloned
    api_resource = "pool"

    # Get SOURCE VRF UUID to create the GET queryeference 
    source_vrfcontext = api.get_object_by_name("vrfcontext", source_vrf)
    if (source_vrfcontext):
      vrf_source_uuid = source_vrfcontext["uuid"]
      # Get NEW VRF reference 
      target_vrfcontext = api.get_object_by_name("vrfcontext", target_vrf)
      if (target_vrfcontext):
        target_vrf_ref = api.get_obj_ref(target_vrfcontext)
        target_vrf_uuid = target_vrfcontext["uuid"]
        # Extract all the pools that refers to the source VRF
        query = {
            "refers_to": "vrfcontext:"+vrf_source_uuid
        }
        resp = api.get ("pool", params=query) 
        if resp.status_code in range(200, 299):
          print ("\033[1mFound "+str(json.loads(resp.text)["count"])+" Pools Objects @ source VRF context "+source_vrf+"\033[0m")
          print("\033[1m-------------------------------------------------------------------------------\033[0m")

        else:
          print('Error in getting pools :%s' % resp.text)
        
          # Convert response JSON into Python Dictionary
        resp = json.loads(resp.text)["results"]
      
          # Cloning an object from an exising one after changing required parameters
        for body in resp:
          # Print info
          print("Cloning existing "+api_resource+" named "+body["name"]+" @ VRF context "+source_vrf+" into new "+api_resource+" named "+body["name"]+"-NEW @ VRF context "+target_vrf )
          # Update body with updated information 
          body["name"] = body["name"]+"-NEW"
          body["vrf_ref"] = target_vrf_ref
          #Send BODY information via POST
          resp = api.post (api_resource, data=json.dumps(body))
          if resp.status_code in range(200, 299):
            print('- New pool named '+body['name'], resp.reason)#, resp.text)
            print()
          else:
            print('Error in creating '+api_resource+' :%s' % resp.text)
          
        # Extract all the created objects
        query = {
              "refers_to": "vrfcontext:"+target_vrf_uuid
        }
        resp = api.get ("pool", params=query) 
        if resp.status_code in range(200, 299):
          return(json.loads(resp.text)["results"])


# Extract Virtual Services associated with given VRF and Service Engine Group
# This function assumes you already have cloned VSVIPs and POOLS and reside in target VRF
# The new migrated objects will have a naming as source-name-NEW
def clone_virtualservices (session_env, source_vrf, source_segroup, target_vrf, target_segroup):
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
    
    # Set API Resource to be cloned
    api_resource = "virtualservice"

    # Get SOURCE VRF UUID and SOURCE SEGROUP UUID to create the GET query reference 
    source_vrfcontext = api.get_object_by_name("vrfcontext", source_vrf)
    source_serviceenginegroup = api.get_object_by_name("serviceenginegroup", source_segroup)
    if (source_vrf and source_segroup):
      source_vrf_uuid = source_vrfcontext["uuid"]
      source_segroup_uuid = source_serviceenginegroup["uuid"]
      # Get TARGET VRF and SEGROUP references and UUIDs
      target_vrfcontext = api.get_object_by_name("vrfcontext", target_vrf)
      target_segroup = api.get_object_by_name("serviceenginegroup", target_segroup)
      if (target_vrfcontext and target_segroup):
        target_vrf_ref = api.get_obj_ref(target_vrfcontext)
        target_vrf_uuid = target_vrfcontext["uuid"]
        target_segroup_ref = api.get_obj_ref(target_segroup)
        target_segroup_uuid = target_segroup["uuid"]
        # Extract all the VirtualServices that refers to the source VRF 
        query = {
          "refers_to": "vrfcontext:"+source_vrf_uuid,
          "search": "(se_group_ref,"+source_segroup_uuid+")"
        }
        resp = api.get ("virtualservice", params=query)
        if resp.status_code in range(200, 299):
          print (" - Found "+str(json.loads(resp.text)["count"])+ " VirtualServices at @ source VRF context "+source_vrf+" and SEGroup "+source_segroup)
          print("-------------------------------------------------------------------------------")
        else:
          print('Error in getting virtualservices :%s' % resp.text)
    
    # Convert response JSON into Python Dictionary
    source_vss = json.loads(resp.text)["results"]
    i = 1
    for vs in source_vss:    
      # Extract the name of current VSVIP
      print ("Extracting information for source VS "+ vs["name"]+"....")
      query = {
        "uuid": vs["vsvip_ref"].split("/")[5]
        }
      resp = api.get ("vsvip", params=query) 
      if resp.status_code in range(200, 299):
          #print(resp)
          source_vsvip_name = json.loads(resp.text)["results"][0]["name"]
          print(" - Found source VSVIP "+source_vsvip_name)
      else:
          print('Error in getting virtualservices :%s' % resp.text)

      # Extract the name of current Pool
      query = {
        "uuid": vs["pool_ref"].split("/")[5]
        }
      resp = api.get ("pool", params=query) 
      if resp.status_code in range(200, 299):
          #print(resp)
          source_pool_name = json.loads(resp.text)["results"][0]["name"]
          print(" - Found source POOL "+source_pool_name)
      else:
          print('Error in getting virtualservices :%s' % resp.text)

      # Extract TARGET VSVIP and POOL INFORMATION (it is assumed a previous step to migrate source object into object-NEW has been completed)
      print()
      print("Looking for candidate target objects already cloned")
      target_vsvip_name = source_vsvip_name+"-NEW"
      target_pool_name = source_pool_name+"-NEW"
      target_vsvip = api.get_object_by_name("vsvip", target_vsvip_name)
      target_pool = api.get_object_by_name("pool", target_pool_name)
      if (target_pool and target_vsvip):
          print( " - Found candidate VSVIP "+target_vsvip_name)
          print( " - Found candidate Pool "+target_pool_name)
          target_vsvip_ref = api.get_obj_ref(target_vsvip)
          target_pool_ref = api.get_obj_ref(target_pool)
          target_vsvip_uuid = target_vsvip["uuid"]
          target_pool_ref = target_pool["uuid"]
          
          # Create body with new information
          vs["name"] = vs["name"]+"-NEW"
          vs["vsvip_ref"]= target_vsvip_ref
          vs["pool_ref"]= target_pool_ref
          vs["se_group_ref"] = target_segroup_ref
          vs["vrf_context_ref"] = target_vrf_ref
          print()
          print("Everything looks OK, cloning VS # " + str(i))
          i = i +1
          body = vs
          #Send BODY information via POST
          resp = api.post ("virtualservice", data=json.dumps(body))

          if resp.status_code in range(200, 299):
            print(' - New virtualservice named '+body['name'], resp.reason)#, resp.text)
            print()
          else:
            print('Error in creating '+api_resource+' :%s' % resp.text)
          
    # Extract all the created objects
    query = {
          "name.icontains": "-NEW",
          "include_name": True
    }
    resp = api.get ("virtualservice", params=query) 
    if resp.status_code in range(200, 299):
      return(json.loads(resp.text)["results"])