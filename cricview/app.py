from flask import Flask, request, render_template, url_for
from flask_socketio import SocketIO
from dataclasses import dataclass
import json
import uuid

atlasite    = json.load(open('atlassite.json'  ,'r'))
pandaqueue  = json.load(open('pandaqueue.json' ,'r'))
ddmendpoint = json.load(open('ddmendpoint.json','r'))

app = Flask(__name__)
app.config['SECRET_KEY'] = str(uuid.uuid4())
socketio = SocketIO(app)

hc_days = 'http://hammercloud.cern.ch/hc/app/atlas/siteoverview/?site={site}&days={days}&templateType=isGolden'

@dataclass
class SiteOverview():
    name: str
    url_hc: str
    url_cric: str
    url_panda: str  

@app.route("/", methods=['GET','POST'])
def hello_world():

    sites = []  
    for site_name in sorted(atlasite.keys()): 
        s = SiteOverview(
          site_name,
          f'https://atlas-cric.cern.ch/core/experimentsite/detail/{site_name}/',
          hc_days.format(site=site_name,days=7),
          f'https://bigpanda.cern.ch/site/{site_name}/',
        )
        sites.append(s)
    return render_template("overview.jinja2",
                            sites = sites)
  

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']): 
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)



@app.route('/ddm')
def ddmdata():
    return ddmendpoint

@app.route('/pq')
def pqdata():
    return pandaqueue

@app.route('/as')
def asdata():
    return atlasite



if __name__ == '__main__':
    socketio.run(app)

