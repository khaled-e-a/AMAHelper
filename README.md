### AMAHelper (Android Malware Analysis Helper)

Android Malware analysis helper contains convenience scripts for Android malware analysis.

Currently, AMAHelper contains one script: `look-for-sensitive-apis.py`. This script looks for usages of APIs in java code and lists all occurrences of such usages. The script also ignores files under user-defined whitelisted packages (like android/support and com/google).
This helps to narrow down the starting point for reverse engineering.

## Usage

`look-for-sensitive-apis.py sensitive-api-list.txt whitelist.txt matches.txt /path/to/java/directory/` 

`sensitive-api-list.py`: list of APIs that you want to start your analysis from.

`whitelist.txt`: whitelisted packages.

`matches.txt`: the script will create this file and write the search results to it. 

`/path/to/java/directory/`: directory of the decompiled apk (in java) 


