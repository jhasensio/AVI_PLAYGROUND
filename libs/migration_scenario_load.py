# Load Scenario

from avi.sdk.avi_api import ApiSession
from requests.packages import urllib3
urllib3.disable_warnings()
import json

def setup_scenario(session_env):
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


    # Create VSVIPs source Objects
    print ("* Creating VSVIPs Source Objects")
    for i in range(len(vsvip_source_names)):
        body = {
          'name': vsvip_source_names[i],
          'vip': [
            {
              'enabled': 'true',
              'auto_allocate_ip': 'true',
              'auto_allocate_ip_type': 'V4_ONLY',
              'ipam_network_subnet': {
                  'network_ref': '/api/network?name='+network_name,
                  'subnet': {
                    'ip_addr': {
                      'addr': '192.168.1.0',
                      'type': 'V4'
                    },
                    'mask': 24
                }
              },
              'vip_id': 1
            }
          ],
        }

        url_path = "vsvip"
        resp = api.post (url_path, data=json.dumps(body))

        if resp.status_code in range(200, 299):
          print('- Object '+url_path+' named '+body['name'], resp.reason)#, resp.text)
          print('   _ Allocated IP address is '+ json.loads(resp.text)["vip"][0]["ip_address"]["addr"])
        else:
          print('Error in creating '+url_path+' :%s' % resp.text)
    
    # Create VS source Objects
    print ("* Creating Source Virtual Service Objects")
    for i in range(len(vs_source_names)):
        body = {
          'name': vs_source_names[i],
          'vsvip_ref': '/api/vsvip?name='+vsvip_source_names[i],
          'se_group_ref': '/api/serviceenginegroup?name='+source_segroup,
          "services": [
             {
              "port": 80,
             }
      ],
          }

        url_path = "virtualservice"
        resp = api.post (url_path, data=json.dumps(body))

        if resp.status_code in range(200, 299):
          print('- Object '+url_path+' named '+body['name'], resp.reason)#, resp.text)
        else:
          print('Error in creating '+url_path+' :%s' % resp.text)

    # Create VSVIPs target Objects
    print ("* Creating VSVIPs Target Objects")
    for i in range(len(vsvip_target_names)):
        body = {
          'name': vsvip_target_names[i],
          'vip': [
            {
              'enabled': 'true',
              'auto_allocate_ip': 'true',
              'auto_allocate_ip_type': 'V4_ONLY',
              'ipam_network_subnet': {
                  'network_ref': '/api/network?name='+network_name,
                  'subnet': {
                    'ip_addr': {
                      'addr': '192.168.1.0',
                      'type': 'V4'
                    },
                    'mask': 24
                }
              },
              'vip_id': 1
            }
          ],
        }

        url_path = "vsvip"
        resp = api.post (url_path, data=json.dumps(body))

        if resp.status_code in range(200, 299):
          print('- Object '+url_path+' named '+body['name'], resp.reason)#, resp.text)
          print('   _ Allocated IP address is '+ json.loads(resp.text)["vip"][0]["ip_address"]["addr"])
        else:
          print('Error in creating '+url_path+' :%s' % resp.text)
    
    # Create VS target Objects
    print ("* Creating target Virtual Service Objects")
    for i in range(len(vs_target_names)):
        body = {
          'name': vs_target_names[i],
          'vsvip_ref': '/api/vsvip?name='+vsvip_target_names[i],
          'se_group_ref': '/api/serviceenginegroup?name='+target_segroup,
          "services": [
             {
              "port": 80,
             }
          ]
          }

        url_path = "virtualservice"
        resp = api.post (url_path, data=json.dumps(body))

        if resp.status_code in range(200, 299):
          print('- Object '+url_path+' named '+body['name'], resp.reason)#, resp.text)
        else:
          print('Error in creating '+url_path+' :%s' % resp.text)         