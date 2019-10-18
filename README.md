# AMAHelper (Android Malware Analysis Helper)

Android Malware analysis helper contains convenience scripts for Android malware analysis.

Currently, AMAHelper contains two scripts:

1. `decompile.py`. This scripts decompiles an apk using jadx and apktool. It also produces a summary of file types in the apk assets.

2. `look-for-sensitive-apis.py`. This script looks for usages of APIs in java code and lists all occurrences of such usages. The script also ignores files under user-defined whitelisted packages (like android/support and com/google).
This helps to narrow down the starting point for reverse engineering.

requirements:

1. python 3.6+

2. jadx

3. apktool

## Usage

``` shell
python3.7 decompile.py app.apk path/for/output/files
```

`app.apk`: the apk
`path/for/output/files` where you want to store the decompiled artifacts. It will be created by the script.

``` shell
python3.7 look-for-sensitive-apis.py sensitive-api-list.txt whitelist.txt matches.txt /path/to/java/directory/
```

`sensitive-api-list.py`: list of APIs that you want to start your analysis from.

`whitelist.txt`: whitelisted packages.

`matches.txt`: the script will create this file and write the search results to it.

`/path/to/java/directory/`: directory of the decompiled apk (in java)

