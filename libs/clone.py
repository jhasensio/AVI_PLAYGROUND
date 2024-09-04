# Ancillary scripts for cloning existing AVI objects

#from avi.sdk.avi_api import ApiSession
from requests.packages import urllib3
urllib3.disable_warnings()
import json

# Creates a NEW VRF named source_vrf-NEW
def clone_vrf (api: object, source_vrf_name: str) -> dict:
    """
    Clone a VRF from a given name appending suffix -NEW
    
    Parameters:
    -----------
    api : avi.sdk.avi_api.ApiSession
      The AVI ApiSession object containing session paramenters to use AVI API
    
    source_vrf_name : str
      The name of the VRF to clone
    
    Returns:
    --------
    dict
      Dictionary containing cloned vrf object output
    """ 
    
    # Cloning an object from an exising one after changing required parameters
    api_resource = "vrfcontext"

    # Get the existing Object to be used as template
    body = api.get_object_by_name ("vrfcontext", source_vrf_name, params={"include_name": "true"}) # Response to be used as template
    
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
def clone_network (api: object, source_network: list, target_vrf_name: str) -> dict:
    """
    Clone a network object with suffix -NEW from a given source network dictionary object on a give target vrf name
    
    Parameters:
    -----------
    api : avi.sdk.avi_api.ApiSession
      The AVI ApiSession object containing session paramenters to use AVI API
    
    source_network : list
      The name of the VRF to clone
    
    target_vrf_name : str
      The name of the VRF to attach the new created network
    
    Returns:
    --------
    dict
      Dictionary containing cloned vrf object output

    """ 
    
    # Get source object 
    # Cloning an object from an exising one after changing required parameters
    api_resource = "network"
    object_name = source_network

    # Get the existing Object to be used as template
    body = api.get_object_by_name (api_resource, object_name, params={"include_name": "true"}) # Response to be used as template

    if (body):
      # Get VRF reference 
      target_vrf = api.get_object_by_name("vrfcontext", target_vrf_name, params={"include_name": "true"})

      if (target_vrf):
        # Update body with new name
        target_vrf_ref = api.get_obj_ref(target_vrf)
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
def clone_networkservice (api: object, source_networkservice_name: str, target_vrf_name: str, target_segroup_name: str) -> dict:
    """
    Clone a networkservice object with suffix -NEW from a given source network service on a given target vrf and target service engine group 
    
    Parameters:
    -----------
    api : avi.sdk.avi_api.ApiSession
      The AVI ApiSession object containing session paramenters to use AVI API
    
    source_networkservice_name : str
      The name of the networkservice to clone
    
    target_vrf_name : str
      The name of the VRF to attach the new created networkservice
    
    target_segroup_name : str
      The name of the service engine group to attach new create networkservice
    
    Returns:
    --------
    dict
      Dictionary containing cloned network object output

    """ 
    
    # Get source object 
    # Cloning an object from an exising one after changing required parameters
    api_resource = "networkservice"

    # Get the existing Object to be used as template
    body = api.get_object_by_name (api_resource, source_networkservice_name) # Response to be used as template

    if (body): 
      # Get VRF reference 
      vrfcontext = api.get_object_by_name("vrfcontext", target_vrf_name)
      if vrfcontext:
         vrf_ref = api.get_obj_ref(vrfcontext)

      # Get SEGroup reference 
      segroup = api.get_object_by_name("serviceenginegroup", target_segroup_name)
      if segroup:
         se_group_ref = api.get_obj_ref(segroup)

      # Update body with new name 
      body["name"] = source_networkservice_name+"-NEW"
      body["se_group_ref"] = se_group_ref
      body["vrf_ref"] = vrf_ref
      
      # Print info
      print("Cloning existing "+api_resource+" "+source_networkservice_name+" into "+source_networkservice_name+"-NEW" )

      #Send BODY information via POST
      resp = api.post (api_resource, data=json.dumps(body))

      if resp.status_code in range(200, 299):
        print(resp)
        print('- New '+api_resource+' named '+body['name'], resp.reason)#, resp.text)
        return (json.loads(resp.text))
      else:
        print('Error in creating '+api_resource+' :%s' % resp.text)

# Clone existing VSVIP to a given target_vrf and target_placement_network 
def clone_vsvips (api: object, source_vsvip_name: str, target_vrf_name: str, target_network_name: str) -> dict:
    """
    Clone a vsvip object with suffix -NEW from a given vsvip on a given target vrf and target network
    
    Parameters:
    -----------
    api : avi.sdk.avi_api.ApiSession
      The AVI ApiSession object containing session paramenters to use AVI API
    
    vsvip_name : str
      The name of the vsvip to clone
    
    target_vrf_name : str
      The name of the VRF to attach the new created networkservice
    
    target_network_name : str
      The name of the network where to place the new vsvip
    
    Returns:
    --------
    dict
      Dictionary containing cloned vsvip object output

    """ 
  
    # Get NEW network reference 
    network = api.get_object_by_name("network", target_network_name)
    if (network):
      target_network_ref = api.get_obj_ref(network)
      # Get NEW VRF reference 
      target_vrfcontext = api.get_object_by_name("vrfcontext", target_vrf_name)
      if (target_vrfcontext):
        target_vrf_ref = api.get_obj_ref(target_vrfcontext)

        # Extract source vsvip object that will be used as body template for new object creation
        vsvip = api.get_object_by_name("vsvip", source_vsvip_name)
        print("Cloning existing vsvip "+vsvip["name"]+" into new vsvip "+vsvip["name"]+"-NEW @ VRF context "+target_vrf_name )
        # Update body with updated information
        body = vsvip
        body["name"] = vsvip["name"]+"-NEW"
        body["vrf_context_ref"] = target_vrf_ref
        body["vip"][0]["placement_networks"][0]["network_ref"] = target_network_ref

        # Cloning an object from an exising one after changing required parameters

        #Send BODY information via POST
        resp = api.post ("vsvip", data=json.dumps(body))

        if resp.status_code in range(200, 299):
          print('- New vsvip named '+body['name'], resp.reason)#, resp.text)
          print()
          return(json.loads(resp.text))
        else:
          print('Error in creating vsvip :%s' % resp.text)
          
# Clone Pools
def clone_pools (api: object, source_vs_name: str, target_vrf_name: str) -> dict:
    """
    Clone a pool object with suffix -NEW from a given vs on a given target vrf
    
    Parameters:
    -----------
    api : avi.sdk.avi_api.ApiSession
      The AVI ApiSession object containing session paramenters to use AVI API
    
    source_vs_name : str
      The name of the vs to clone
    
    target_vrf_name : str
      The name of the VRF to attach the new created virtualservice
    
    Returns:
    --------
    dict
      Dictionary containing cloned pool object output

    """ 
    
    target_vrfcontext = api.get_object_by_name("vrfcontext", target_vrf_name)
    if (target_vrfcontext):
      target_vrf_ref = api.get_obj_ref(target_vrfcontext)
      # Extract pool  associated to the source vs
      vs = api.get_object_by_name("virtualservice", source_vs_name, params={"include_name":"true"})
      if vs:
        pool_name = vs["pool_ref"].split("/")[5].split("#")[1]
        print ("\033[1mFound Pool Name "+pool_name+"\033[0m")
        print("\033[1m------------------------------\033[0m")
      
      pool=api.get_object_by_name("pool", pool_name, params={"include_name":"true"})
      body = pool
      print("Cloning existing POOL named "+body["name"]+" attached to VS " + source_vs_name+ " into new POOL named "+body["name"]+"-NEW @ VRF context "+target_vrf_name )
      # Update body with updated information 
      body["name"] = body["name"]+"-NEW"
      body["vrf_ref"] = target_vrf_ref
      
      #Send BODY information via POST
      resp = api.post ("pool", data=json.dumps(body))
      if resp.status_code in range(200, 299):
         print('- New pool named '+body['name'], resp.reason)#, resp.text)
         print()
         return(json.loads(resp.text))
      else:
          print('Error in creating Pool :%s' % resp.text)
        


# Clone VS
def clone_virtualservices (api:object, source_vs_name: str, target_vrf_name: str, target_segroup_name: str) -> dict:
    """
    Clone a pool object with suffix -NEW from a given vs on a given target vrf
    
    Parameters:
    -----------
    api : avi.sdk.avi_api.ApiSession
      The AVI ApiSession object containing session paramenters to use AVI API
    
    source_vs_name : str
      The name of the vs to clone
    
    target_vrf_name : str
      The name of the VRF to attach the new created virtualservice

    target_segroup_name : str
      The name of the segroup to to attach the new created virtualservice
    
    Returns:
    --------
    dict
      Dictionary containing cloned pool object output

    """ 
    # Set API Resource to be cloned
    api_resource = "virtualservice"

    # Get TARGET VRF and SEGROUP references and UUIDs
    target_vrfcontext = api.get_object_by_name("vrfcontext", target_vrf_name)
    target_segroup = api.get_object_by_name("serviceenginegroup", target_segroup_name)
    if (target_vrfcontext and target_segroup):
      target_vrf_ref = api.get_obj_ref(target_vrfcontext)
      target_segroup_ref = api.get_obj_ref(target_segroup)
      vs = api.get_object_by_name ("virtualservice", source_vs_name, params={"include_name": "true"})
      if vs:
        print (" - Found virtual service "+ vs["name"])
        print("-------------------------------------------------------------------------------")
      i = 1    
      # Extract the name of current VSVIP
      print ("Extracting information for source VS "+ vs["name"] +"....")
      source_vsvip_name = vs["vsvip_ref"].split("/")[5].split("#")[1]
      print("    - Found source VSVIP "+source_vsvip_name)
      
      # Extract the name of current Pool
      source_pool_name = vs["pool_ref"].split("/")[5].split("#")[1]
      print("    - Found source POOL "+source_pool_name)

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
          target_pool_ref = target_pool["uuid"]
          
          # Create body with new information
          vs["name"] = vs["name"]+"-NEW"
          vs["vsvip_ref"]= target_vsvip_ref
          vs["pool_ref"]= target_pool_ref
          vs["se_group_ref"] = target_segroup_ref
          vs["vrf_context_ref"] = target_vrf_ref
          vs["enabled"] = False
          print()
          print("Everything looks OK, cloning VS")
          body = vs
          #Send BODY information via POST
          resp = api.post ("virtualservice", data=json.dumps(body))

          if resp.status_code in range(200, 299):
            print(' - New virtualservice named '+body['name'], resp.reason)#, resp.text)
            print()
            return(json.loads(resp.text))
          else:
            print('Error in creating '+api_resource+' :%s' % resp.text)
