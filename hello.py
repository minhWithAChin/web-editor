from flask import Flask, render_template, request
from werkzeug.middleware.proxy_fix import ProxyFix
from mylog import log
import subprocess, sys, os
import time

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
	except BaseException as e:
		log.critical(e)
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

def cancelSubProc():
	global proc
	if checkSubProc():
		proc.terminate()
		proc.kill()
		#codeRunningState=Fals
		time.sleep(0.1)
		subprocess.run(["/var/www/html/.venv/bin/python3","/var/www/html/student_code/reset.py"])
		return not checkSubProc()

@app.route("/", methods=['POST','GET'])
def acceptcode():
    if request.method=='POST':
        try:
            with open(codeFilePath, 'w+') as f:  # open file in overwrite mode
                f.write(request.form["code"])
                log.debug(request.form["code"])
            return [True,False]
        except:
            log.critical(codeFilePath+"not reachable")
            return [False,False]
    elif request.method=='GET':
        try:
            with open(codeFilePath, 'r') as f:  # open file in read mode
                code=f.read()
                log.debug(code)
            return [True,False,code.split('\n')]
        except:
            log.critical(codeFilePath+"not reachable")
            return [False,False,["not found","try uploading first"]]
        return runCode()
    else:
        return [False,False,["<p>bruh!?</p>"]]

@app.route("/exec", methods=['POST','GET'])
def executecode():  #-Python lässt sich abbrechen wenn der Knopf doppelt gedrückt wird
    global codeRunningState
    if request.method=='GET':
	    if not codeRunningState:
                codeRunningState=startSubProc()
                log.debug(f"proc gestartet: {codeRunningState}")
                if codeRunningState:
                    outStr="Code gestartet"
                else:
                    outStr="Etwas ist schiefgelaufen"
                return [False,True,[outStr]]
	    else:
	        return [False,True,["Code läuft schon"]]
    elif request.method=='POST':
        codeRunningState=checkSubProc()
        if not codeRunningState:
            output=extractSubProc()
            log.debug(output) #___hier heartbeat abbr
            return [True,True,[output]]
        else:
            if request.form["cancelled"]=="true":
                cancelSuccess=cancelSubProc()
                if cancelSuccess:
                    outStr="Abgebrochen"
                else:
                    outStr="Abbruch im Gange. Bitte warten"
                log.debug(outStr)
                return [cancelSuccess,True,[outStr]] #___hier heartbeat abbr
            else:
                 return [False,True,["Warten..."]]
    else:
        return [False,True,["<p>bruh!?</p>"]]

if __name__ == "__main__":
    app.run(host='0.0.0.0')

