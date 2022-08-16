import argparse
import traceback
import questionary
import shodan
import json

# Local import
import log
from cli_color import Color
import quickmailer

def get_api_key():
    try:
        with open("secrets.json", "r") as f:
            secrets = json.load(f)
            return secrets["shodan_api_key"]
    except:
        print("Shodan API Key not found in secrets.json")
        api_key = questionary.password("Enter your Shodan API key:").ask()
        with open("secrets.json", "w") as f:
            json.dump({"shodan_api_key": api_key}, f)
    return api_key

def get_last_ip():
    with open("secrets.json") as f:
        secrets = json.load(f)
        
        try:
            return secrets["last_ip"]
        except:
            return None

def main():
    shodan_api = shodan.Shodan(get_api_key())
    last_ip = get_last_ip()
    
    
    my_ip = shodan_api.tools.myip()
    all_shodan_alerts = shodan_api.alerts() 
    
    # See if our IP address is in any of the alerts.
    alert_exists = False
    for alert in all_shodan_alerts:
        # Need to make sure it's our IP plus /32.
        if my_ip+"/32" in alert["filters"]["ip"]:
            alert_exists = True
            logger.info(f"Shodan alert already exists for IP address: {my_ip}, with alert ID: {alert['id']}")
            logger.info(f"This alert will send an email to the email address associated with the Shodan account.")
    
    # If the alert doesn't exist, check if our last known IP address is in the alerts.
    # If it is, then we can delete it.
    if not alert_exists and last_ip:
        for alert in all_shodan_alerts:
            if last_ip in alert["filters"]["ip"] and alert["name"] == "Personal Network Monitor":
                shodan_api.delete_alert(alert["id"])
                logger.info(f"Deleted Shodan alert for IP address: {last_ip}, with alert ID: {alert['id']}")
    
    # If the alert doesn't exist, create it.
    if not alert_exists:
        create_alert_response = shodan_api.create_alert("Personal Network Monitor", my_ip+"/32")
        logger.info(f"Created Shodan alert for IP address: {my_ip}, with alert ID: {create_alert_response['id']}")        
        logger.info(f"This alert will send an email to the email address associated with the Shodan account.")

        # Then set it to alert on anything?
        shodan_api.enable_alert_trigger(create_alert_response["id"], "any")

    return

if __name__ == "__main__":

    try:
        parser = argparse.ArgumentParser(
            description="This is the description for the main parser!"
        )
        parser.add_argument(
            "--debug",
            action="store_true",
            help="Optional. Use this argument if you are debugging any errors.",
        )

        args = parser.parse_args()

        logger = log.get_logger(logger_name=__file__ + "Logger", log_file_name=__file__ + ".log", debug=args.debug)

        logger.debug("This is the debug logger!")

        main()

    except Exception:
        logger.error("Unhandled Exception!")
        logger.error(traceback.format_exc())
