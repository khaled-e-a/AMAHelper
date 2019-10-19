import os
import subprocess


def get_all_files(directory: str) -> list:
    # Get all files in the given directory
    # https://thispointer.com/python-how-to-get-list-of-files-in-directory-and-sub-directories/
    if not os.path.isdir(directory):
        raise ValueError(directory+" is not a directory")
    files = list()
    for (dirpath, dirnames, filenames) in os.walk(directory):
        files += [os.path.join(dirpath, file) for file in filenames]
    return files


def shell_command_stdout(args: list) -> str:
    # https://stackoverflow.com/a/4760517
    result = subprocess.run(args, stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8')


def shell_command(args: list) -> str:
    # https://stackoverflow.com/a/4760517
    result = subprocess.run(args, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    return result.stdout.decode('utf-8')


def append_to_file(file_name: str, line: str) -> None:
    with open(file_name, "a+") as f:
        f.write(line)
        f.write("\n")
