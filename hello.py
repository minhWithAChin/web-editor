from flask import Flask, render_template, request
from werkzeug.middleware.proxy_fix import ProxyFix
from mylog import log
import subprocess, sys, os
import time, multiprocessing
app = Flask(__name__)

timeOutSec=60
cancelled=True
proc=0

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

#def runCode():
#    global codeRunningState
#    try:
#	    result = subprocess.check_output("python3 "+codeFilePath, shell = True, timeout=timeOutSec , executable = "/bin/bash", stderr = subprocess.STDOUT)
#    except subprocess.CalledProcessError as cpe:
#        result = cpe.output
#    except subprocess.timeOutError as toe:
#        result = toe.output
#    finally:
#        outList=[]
#        # if result ==  "":
#        #     log.error("timeOutError")
#        #     return ["timeout-error","your Code is taking too long","please fix it"]
#        for line in result.splitlines():
#            outList.append(line.decode())
#        log.debug(outList)
#        codeRunningState=False
#        return outList

def startSubProc():
	global proc
	try:
		proc=subprocess.Popen(["/var/www/html/.venv/bin/python3",codeFilePath],stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
		#codeRunningState=True
		return True
	except:
		return False;

def checkSubProc():
	global proc
	time.sleep(0.1)
	if proc.poll() is None:
		#codeRunningState=True
		return True
	else:
		return False

def extractSubProc():
	global proc
	(stdOut,stdErr)= proc.communicate()
	#codeRunningState=False
	if stdErr:
		return stdErr
	return stdOut

def cancelSupProc():
	global proc
	if checkSubProc():
		proc.kill
		#codeRunningState=False
		return  [proc.poll < 0]
	else:
		return [False,["execute some Code first"]]

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

@app.route("/exec", methods=['POST','GET'])
def executecode():  #-Python lässt sich abbrechen wenn der Knopf doppelt gedrückt wird
    global codeRunningState
    if request.method=='GET':
	    if not codeRunningState:
                codeRunningState=startSubProc()
                log.debug(f"proc gestartet: {codeRunningState}")
                time.sleep(1)
                return [False,[codeRunningState]]
	    else:
	        return [False,["Code läuft schon"]]
    elif request.method=='POST':
        codeRunningState=checkSubProc()
        if not codeRunningState:
            output=extractSubProc()
            log.debug(output) #___hier heartbeat abbr
            return [True,[output]]
        else:
            if request.form["cancelled"]=="true":
                return cancelSubProc() #___hier heartbeat abbr
            else:
                 return [False,["Warten..."]]
    else:
        return [False,["<p>bruh!?</p>"]]

if __name__ == "__main__":
    app.run(host='0.0.0.0')
