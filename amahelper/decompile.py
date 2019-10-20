import os
import sys
from .util import Util
import collections

if __name__ == "__main__":
    # apk name to decompile
    apk_name = sys.argv[1]
    # output directory to place decompiled artifacts
    output_directory = sys.argv[2]
    os.mkdir(output_directory)

    # prepare directories
    jadx_directory = os.path.join(output_directory, "jadx-out")
    apktool_directory = os.path.join(output_directory, "apktool-out")
    unzip_directory = os.path.join(output_directory, "unzip-out")
    report_file = os.path.join(output_directory, "report.txt")

    # extract the malware
    os.system("jadx --deobf " + apk_name + " -d " + jadx_directory)
    os.system("mv " + apk_name.replace(".apk", ".jobf") + " " +
              jadx_directory)
    os.system("apktool d " + apk_name + " -o " + apktool_directory)
    os.system("unzip " + apk_name + " -d " + unzip_directory)

    # summarize the malware assets types
    asset_types = collections.defaultdict(list)
    assets_directory = os.path.join(unzip_directory, "assets")
    for file in Util.get_all_files(assets_directory):
        t = Util.shell_command(["file", file]) \
                               .split(": ")[1].split(",")[0]
        asset_types[t].append(file)

    Util.append_to_file(report_file, "File types in assets:")
    for t in asset_types:
        Util.append_to_file(report_file, "|   Type: " + t)
        Util.append_to_file(report_file, "|   |   File list: ")
        for f in asset_types[t]:
            Util.append_to_file(report_file, "|   |   |   " + f)
