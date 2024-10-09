# Archived this Repository

I've decided to archive this repo because GoDaddy quietly changed the policy for using their API.  They no longer allow users with only a few domains to have free access to their API.  I moved all my domains to Cloudflare and forked this into a new script called [CloudflareDynDNS](https://github.com/rjgura/CloudflareDynDNS) to use Cloudflare's API to update their nameservers.

# GoDaddyDynDNS

Script to keep GoDaddy's DNS records updated with your current external IP address.  This creates a Dynamic DNS solution for domain names registered with GoDaddy and using their nameservers.

## Getting Started

This script assumes that you have registered a domain with GoDaddy and use their nameservers. 

### Prerequisites

   1. Domain name registered with GoDaddy
   2. GoDaddy API key and secret requested from to https://developer.godaddy.com/keys/
   3. Python 3.7.4 64 bit
   4. GoDaddyPy 2.2.7 module for Python
   5. pif 0.8.2 module for Python

Note: Sometimes the production API keys don't seem to work correctly. Just delete it and request another one.
  

### Installing

1. Download and install Python
2. Install the GoDaddyPy module for Python
3. Install the pif module for Python
4. Copy GoDaddyDynDNS.py to the system you will run from (only one system per network is needed)
5. Copy and modify the GoDaddyDynDNS.ini
6. Edit GoDaddyDynDNS.py to point to your GoDaddyDynDNS.ini and select a location for the log file
7. Schedule a recurring job to run GoDaddyDynDNS.py

## Built With

* [Python](https://www.python.org/) - Python is a programming language that lets you work quickly and integrate systems more effectively.

* [PyCharm](https://www.jetbrains.com/pycharm/) - The Python IDE for Professional Developers

* [GoDaddyPy](https://www.github.com/eXamadeus/godaddypy/) - Python library useful for updating DNS settings through the GoDaddy v1 API

* [pif](https://github.com/barseghyanartur/pif) - Public IP address checker 
