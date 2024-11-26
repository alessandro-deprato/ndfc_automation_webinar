import os
import sys
import ndfc
import logging
from webexteamssdk import WebexTeamsAPI

logging.basicConfig(level=logging.INFO,format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s")

##
api_key = {"api_key": "4b725bc0297d4491a79af60494080e967651427bc6b54d02bc671d0792e570d5", "username": "admin"}
aggressive = False
##

def send_webex_message(message):
    # Import the webext token from an environment variable for security
    # Personal Access Token can be generated from https://developer.webex.com/docs/api/getting-started
    webex_token = os.environ.get("WEBEX_TEAMS_ACCESS_TOKEN")
    
    # Import the webex room id from an environment variable for security
    # Room ID can be found in the webex API reference documentation
    # https://developer.webex.com/docs/api/v1/rooms
    webex_room_id = os.environ.get("WEBEX_TEAMS_ROOM_ID")
    webex_connection = WebexTeamsAPI(webex_token)
    if webex_connection.messages.create(roomId=webex_room_id, text=f"\n{message}\n"):
        return True
    else:
        return False

def main():
    # GOAL: Check the status of all the devices in all the fabrics 
    # If the device is not in sync, send a message to the Webex Teams Room
    
    # Create a new NDFC object
    ndfc_obj = ndfc.Ndfc("10.58.31.9", api_key=api_key)

    # Get a list of all the fabrics
    fabrics = [fabric['fabricName'] for fabric in ndfc_obj.get_all_the_fabrics() if not fabric['templateFabricType'] == "VXLAN EVPN Multi-Site"]
    logging.info(f"Found {len(fabrics)} fabrics")
    #Fabrics will look like  ['MIL1-PHY-VXLAN-1', 'MIL-PHY-CORE', 'MIL-PHY-IXN', 'MIL2-PHY-VXLAN-2']
    
    for fabric in fabrics:
        devices = ndfc_obj.get_all_the_devices(fabric)
        logging.info(f"Found {len(devices)} devices in Fabric {fabric}")
        if aggressive:
            serials = ",".join([device['serialNumber'] for device in devices])
            # This will return a list of devices serials
            # FDO281108X8,FDO28320USZ,FDO28260ZA8,FDO270907B2,FDO27090FK6,FDO28270F1X,FDO28270EAW

            # We now trigger a full sync on the devices, NDFC will request the latest running-config
            report = ndfc_obj.force_calculate_device_diff(fabric, serials)
            if not report:
                # That means an namanaged Fabric
                continue
            for device in report:
                if device['pendingConfig']:
                    # pendingConfig is a list of commands that are missing on the device
                    # We will joing the list in a unique string to send it to the Webex Teams Room
                    logging.info(f"Device {device['switchName']} in Fabric {fabric} is not in sync")
                    commands = "\n".join(device['pendingConfig'])
                    # Send a message to the Webex Teams Room
                    send_webex_message(f"The device {device['switchName']} in Fabric {fabric} is not in sync. \n\n {commands}")
        else:
            for device in devices:
                # Now we will check the status of all the devices
                if device['hostName'] and not device['ccStatus'] == "In-Sync":
                    # If the device is not in sync, we will find out what is missing
                    logging.info(f"Device {device['hostName']} in Fabric {fabric} is not in sync")
                    out_of_sync = ndfc_obj.get_device_missing_configs(fabric, device['serialNumber'])
                    # Out of sync is a list of commands that are missing on the device
                    # We will join the list in a unique string to send it to the Webex Teams Room
                    # Every command will be separated by a new line
                    commands = "\n".join(out_of_sync['pendingConfig'])
                    # Send a message to the Webex Teams Room
                    send_webex_message(f"The device {device['hostName']} in Fabric {fabric} is not in sync. \n\n {commands}")
    logging.info("Script completed")

if __name__ == "__main__":
    main()

