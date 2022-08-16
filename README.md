# Shodan Monitor Tool

This was just something quick that I created to automatically set up an alert on Shodan, regardless of my IP address.

- If the IP address changes from the last known IP address, it will delete the alert with the previous IP address, and then create another one for you.
- If you just don't have any alerts, it will create one for you.

## Installation
It should prompt you for everything that you need
```
git clone https://gitea.perfectra1n.com/perf3ct/shodan-monitor-tool
cd shodan-monitor-tool/
pip install -r requirements.txt
python3 main_module.py
```