from flask import Flask, render_template, request
from werkzeug.middleware.proxy_fix import ProxyFix
import subprocess, sys, os

codeFilePath='/var/www/html/student_code/test.py'
if not os.path.exists(codeFilePath):
    os.mknod(codeFilePath)

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"

def runCode():
    try:
        result = subprocess.check_output("python3 "+codeFilePath, shell = True, executable = "/bin/bash", stderr = subprocess.STDOUT)
    except subprocess.CalledProcessError as cpe:
        result = cpe.output
    finally:
        outList=[]
        for line in result.splitlines():
            outList.append(line.decode())
        print(outList)
        return outList

@app.route("/", methods=['POST','GET'])
def acceptcode():
    if request.method=='POST':
        #print(request.form["code"])
        f = open(codeFilePath, 'w+')  # open file in overwrite mode
        f.write(request.form["code"])
        f.close()
        return runCode()
    elif request.method=='GET':
        return runCode()
    else:
        return "<p>bruh!?</p>"