from flask import Flask, render_template, request
from werkzeug.middleware.proxy_fix import ProxyFix
from mylog import log
import subprocess, sys, os
import time, multiprocessing

timeOutSec=60

codeFilePath='/var/www/html/student_code/test.py'
if not os.path.exists(codeFilePath):
    log.warning("path für test code existiert nicht")
    os.mknod(codeFilePath)

codeRunningState=False

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"

def runCode():
    global codeRunningState
    try:
	    result = subprocess.check_output("python3 "+codeFilePath, shell = True, timeout=timeOutSec , executable = "/bin/bash", stderr = subprocess.STDOUT)
    except subprocess.CalledProcessError as cpe:
        result = cpe.output
    except subprocess.timeOutError as toe:
        result = toe.output
    finally:
        outList=[]
        # if result ==  "":
        #     log.error("timeOutError")
        #     return ["timeout-error","your Code is taking too long","please fix it"]
        for line in result.splitlines():
            outList.append(line.decode())
        log.debug(outList)
        codeRunningState=False
        return outList

@app.route("/", methods=['POST','GET'])
def acceptcode():
    if request.method=='POST':
        try:
            with open(codeFilePath, 'w+') as f:  # open file in overwrite mode
                f.write(request.form["code"])
                log.debug(request.form["code"])
            return [True]
        except:
            log.critical(codeFilePath+"not reachable")
            return [False]
    elif request.method=='GET':
        try:
            with open(codeFilePath, 'r') as f:  # open file in read mode
                code=f.read()
                log.debug(code)
            return [True,code.split('\n')]
        except:
            log.critical(codeFilePath+"not reachable")
            return [False,["not found","try uploading first"]]
        return runCode()
    else:
        return [False,["<p>bruh!?</p>"]]

@app.route("/exec", methods=['GET'])
def executecode():  #-Python lässt sich abbrechen wenn der Knopf doppelt gedrückt wird
    global codeRunningState
    if not codeRunningState:
        codeRunningState=True
        return [False,runCode()]
    else:
        return [True,["Code läuft schon"]]