#!/usr/bin/env python3
from flask import Flask

app = Flask(__name__)

@app.route('/')
def help():
    return """
<code>
<h2>Host</h2><br>
POST /createhost<br>
    name: str   VM name<br>
    img: str    VM image<br>
    cpu: int    cpus to attach<br>
    mem: str    amount of memory<br>
    net: dict   new network adapter options<br>
    opti: arr   optical disks to attach<br>
<br>
    ret (hostid: int)<br><br>
<br>


<h2>Tag</h2><br>
POST /createtag<br>
    name: str   tag name<br>
<br><br>
POST /&#60;tagid&#62;/setparent<br>
    parent_tagid: int   tag id of the parent<br><br>
<br>
    ret ()<br>
<br>
    
POST /&#60;tagid&#62;/addhost<br>
    hostid: int     id of host being tagged<br>
<br>
    ret ()<br><br>
<br> 

<h2>Play</h2><br>
POST /createplay<br>
    name: str   play name<br>
<br>
    ret (playid: int)<br><br>
<br>
POST /attachplay<br>
    tagid: int  host tag id<br>

    ret ()<br><br>
<br>
POST /&#60;playid&#62;/addtag<br>
    tagid: int      tag to give action<br>

<h2>Action</h2><br>
POST /createaction<br>
    name: str   Action name<br>
    module: str Action module<br>
    options: arr    array of options<br>
    args:   dict    args to pass to ansible <br> 
<br>
    ret (actionid: int)<br><br>
<br>
    

    
</code>
"""

@app.route('/createhost', methods=["POST"])
def createhost_api():
    ret = createhost(request.form["name"], \
                request.form["img"], \
                request.form["cpu"], \
                request.form["mem"], \
                request.form["net"], \
                request.form["opti"])    
    return ret

@app.route('/<hostid>/destroy', methods=["DELETE"])
def destroyhost_api(hostid):
    ret = destroyhost(hostid)
    return ret

@app.route('/createtag', methods=["POST"])
def createtag_api():
    ret = 

if __name__ == '__main__':
    app.run(debug=True)


'''

    deploy_churchill_play = Play('churchill-deployment')
    deploy_churchill_play.addAction(Action( \
        name='Install prerequiste packages', \
        module='apt', \
        args={'name': ['apt-transport-https', 'ca-certificates', 'curl', 'software-properties-common'], 'update_cache': 'yes'}, \                                                                                                             
        options={'become':'yes'}
    ))


'''
