# Introduction
Lucy is a pentesting script for information collection using an existing arbitrary file download vulnerability.

# Installation
Please read install.txt for prerequisites and how to run.

# Useful information
Script uses Tor and a list of pre-defined user agents to set up identity. User agents are in /templates/template.useragent file. Identity will change after 50 to 100 requests by default. You may change these limits by modifying rnd_min, rnd_max values in lucy.py. You may change sleep value between requests by modifying sleep_req value, in case of multiple requests. Files to be scanned are grouped by functionality (eg. os, network, processes) and are under /mods folder. Script /various/usergen.py may use /templates/template.userprofile with one more file to create a list of user profile files to scan. Target url should be in uri file, please check the example uri file. Tool saves collected information under /downloads folder.

# Feedback
Code and file lists can always be improved. Feel free to contact me should you have ideas, suggestions or comments for improvement.

# Disclaimer
All information and software available on this site are for educational purposes only. Use these at your own discretion, the site owner cannot be held responsible for any damages caused. The views expressed on this site are my own and do not necessarily reflect those of my employer.

Usage of the tool for attacking targets without prior mutual consent is illegal. It is the end user’s responsibility to obey all applicable local, state and federal laws. I assume no liability and I am not responsible for any misuse or damage caused by this tool.
