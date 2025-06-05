
import logging
import os
import sys

log=logging.getLogger("myLog")
log.setLevel(logging.DEBUG)
formatter=logging.Formatter('%(asctime)s;%(levelname)s;%(module)s;%(funcName)s;%(message)s')
formatter2=logging.Formatter('%(levelname)s - %(funcName)s: %(message)s')

#https://stackoverflow.com/questions/35807605/create-a-file-if-it-doesnt-exist
logFilePath = os.path.join(".","log_data","flask.log")
if not os.path.isfile(logFilePath):
    os.mknod(logFilePath)
    log.warning("path für log code existiert nicht")

logFileHandler=logging.FileHandler(logFilePath)
logFileHandler.setFormatter(formatter)
logFileHandler.setLevel(logging.DEBUG)

logTerminalHandler=logging.StreamHandler(sys.stdout)
logTerminalHandler.setFormatter(formatter2)
logTerminalHandler.setLevel(logging.DEBUG)

log.addHandler(logFileHandler)
log.addHandler(logTerminalHandler)
