import datetime
import time

# LOGGER
#
# this utility allows the logging of simple text to a
# file and to the console. can be configured to add
# a timestamp to each statement.
#

log_config = {
    "output_log": "LOG",
    "output_err": "ERR",
    "output_wrn": "WRN",

    "output_end": "\n",
    "output_delimiter": "  ---  ",

    "console_output": True,
    "file_output": True,
    "file_path": "logs/",
    "file_name_format": "log_%y%m%d.log",

    "add_timestamp": True,
    "timestamp_format": "%Y-%m-%d %H:%M:%S",

    "initialized": False,
    "file": None
}

def log (what, log_level="log"):
    # if the log file is not yet initialized, initialize it
    if not log_config["initialized"] and log_config["file_output"]:
        ts = time.time()
        file_name = datetime.datetime.fromtimestamp(ts).strftime(log_config["file_path"] + log_config["file_name_format"])
        log_config["file"] = open(file_name, "a+")
        log_config["initialized"] = True

    # append the proper log level
    level = log_config["output_log"]
    if log_level=="wrn": level = log_config["output_wrn"]
    elif log_level=="err": level = log_config["output_err"]
    what = level + log_config["output_delimiter"] + what + log_config["output_end"]

    # if we want a timestamp, find out the time and write it into the string
    if log_config["add_timestamp"]:
        ts = time.time()
        what = datetime.datetime.fromtimestamp(ts).strftime(log_config["timestamp_format"]) + log_config["output_delimiter"] + what

    # if we want to output to console...
    if log_config["console_output"]:
        print(what[:-1])

    # if we want to output to file...
    if log_config["file_output"]:
        try:
            log_config["file"].write(what)
        except:
            print("Unable to log line '"+what+"' because the log file has been closed!")

def log_err (what):
    log(what,"err")

def log_wrn (what):
    log(what,"wrn")
