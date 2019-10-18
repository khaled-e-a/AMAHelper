import os
import sys
import re
import util
import collections

if __name__ == "__main__":
    # file containing sensitive APIs (sensitive-api-list.txt)
    apis_file_name = sys.argv[1]
    # file containing white listed packages (whitelist.txt)
    whitelist_file_name = sys.argv[2]
    # output file, will be created if non-existing
    log_file = sys.argv[3]
    # the directory containing the java files
    directory_to_scan = sys.argv[4]

    # Get sensitvie apis
    sensitive_apis_set = set()
    with open(apis_file_name, 'r') as f:
        for l in f:
            if l.startswith("<"):
                sensitive_apis_set.add(l.strip())

    # Get whitelist libraries
    whitelist_libraries = set()
    with open(whitelist_file_name, 'r') as f:
        for l in f:
            whitelist_libraries.add(l.strip())

    # Get method names only
    sensitive_apis_methods = collections.defaultdict(list)
    for s in sensitive_apis_set:
        method = s.split(" ", 2)[2].split("(")[0]
        sensitive_apis_methods[method].append(s)

    # Get all files in the given directory
    # https://thispointer.com/python-how-to-get-list-of-files-in-directory-and-sub-directories/
    files = list()
    for (dirpath, dirnames, filenames) in os.walk(directory_to_scan):
        files += [os.path.join(dirpath, file) for file in filenames]

    # Filter by .java extension
    files = [x for x in files if x.endswith(".java")]

    # Remove whitelisted packages
    files = \
        [x for x in files if not any([w in x for w in whitelist_libraries])]

    # Scan the java for usages of these sensitive methods
    malicious_files = set()
    util.append_to_file(log_file, "Sensitive api search results")
    for method in sensitive_apis_methods:
        wrote_sensitive_api = False
        for f in files:
            with open(f, 'r') as targetFile:
                lines_to_write = list()
                for line_num, line in enumerate(targetFile):
                    line = line.rstrip()
                    if re.search("\\."+method+"\\(", line):
                        lines_to_write.append(str(line_num) + ":" + line)
                if lines_to_write:
                    if not wrote_sensitive_api:
                        message = "Looking for method: " + method
                        util.append_to_file(log_file, message)
                        message = "This method is possibly a sensitive API" + \
                                  "from this list: " + \
                                  str(sensitive_apis_methods[method])
                        util.append_to_file(log_file, message)
                        wrote_sensitive_api = True
                    malicious_files.add(f)
                    util.append_to_file(log_file, "File: " + f)
                    for l in lines_to_write:
                        util.append_to_file(log_file, l)

    # Summarize possibly malicious files
    if malicious_files:
        util.append_to_file(log_file, "Summary of possible malicious files:")
        for f in malicious_files:
            util.append_to_file(log_file, f)
