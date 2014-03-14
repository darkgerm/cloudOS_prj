#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import hcc
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp/'
app.config['DOWNLOAD_FOLDER'] = '/tmp/'
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'cpp', 'c'])

users = {
    'dkg': 'abc',
    'gxlkhhc': '123',
    'demo': 'gg'
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        if password != users[username]:
            return redirect(url_for('login'))
        return render_template('index.html', username=username)
    else:
        return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/un/<username>')
def list(username):
    resp = hcc.fs_list(username)
    return json.dumps(resp)

@app.route('/fsupload', methods=['POST'])
def upload():
    file = request.files['file']
    if file and allowed_file(file.filename):
        username = request.form["username"]
        filename = file.filename
        tmpname = secure_filename(filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], tmpname)

        file.save(filepath)
        resp = hcc.fs_upload(username, filepath, filename)

        return json.dumps(resp)

@app.route('/un/<username>/fn/<filename>', methods=['GET', 'DELETE'])
def fileRD(username, filename):
    if request.method == 'GET':
        filepath = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
        resp = hcc.fs_download(username, filename, filepath)
        print resp["status"]
        return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)
    else:
        resp = hcc.fs_delete(username, filename)
        return json.dumps(resp)

@app.route('/c/un/<username>/fn/<filename>', methods=['POST'])
def compile(username, filename):
    data = request.get_json()
    filetype = data["filetype"]
    exename = data["exename"]

    if exename == "":
        resp = hcc.mpi_compile(username, filetype, filename, u'a.out')
    else:
        resp = hcc.mpi_compile(username, filetype, filename, exename)

    return json.dumps(resp)

@app.route('/r/un/<username>/fn/<filename>', methods=['POST'])
def run(username, filename):
    data = request.get_json()
    print data
    hosts = int(data["hosts"])
    np = int(data["np"])
    #args = data["args"]

    resp = hcc.mpi_run(username, filename, hosts, np, u'')
    #if args == "":
    #    resp = hcc.mpi_run(username, filename, hosts, np, u'')
    #else:
    #    resp = hcc.mpi_run(username, filename, hosts, np, args)

    return json.dumps(resp)

if __name__ == '__main__':
    app.run(host='xxx.xxx.xxx.xxx',
            port=5566,
            debug=True,
            threaded=True)
