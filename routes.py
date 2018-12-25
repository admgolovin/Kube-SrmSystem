from flask import render_template,request,Flask,jsonify, make_response
# from app.forms import DepForm
import json
import psycopg2
from psycopg2.extras import RealDictCursor
import requests
import ConfigParser, os

app = Flask(__name__)



###############################################################################################################################
### Connection to the database:

class BaseConnector(object):
    
    def __init__(self):
        configParser = ConfigParser.RawConfigParser()
        configFilePath = os.path.join(os.path.dirname(__file__), 'Config.cfg')
        configParser.read(configFilePath)
        self.host = configParser.get("base","host")
        self.user  = configParser.get("base","user")
        self.password = configParser.get("base","password")
        self.dbname = configParser.get("base","dbname")

    def connector(self):
        conn =  psycopg2.connect(host = self.host, user = self.user, password = self.password, dbname = self.dbname, cursor_factory=RealDictCursor)       
        return conn



base = BaseConnector()
conn = base.connector()
cur = conn.cursor()
print(cur)

##################################################################################################################################

### GET BEGINS HERE: 
@app.route("/get-dep", methods=['GET'])
def get():
    cur.execute("select name from depart")
    result = cur.fetchall()
    result2 = {"department":[]}
    for i in result:
        result2["department"].append(i)
    # print(result2)
    return jsonify(result2)

@app.route("/get-empl", methods=['GET'])
def get2():     
    cur.execute("select team_id,name,surname,experience,position,salary,coef from employee")
    result = cur.fetchall()
    result2 = {"Employee":[]}
    for i in result:
        result2["Employee"].append(i)
    print(type(jsonify(result2)))
    return jsonify(result2)

@app.route("/get-team", methods=['GET'])
def get3():
    cur.execute("select iddepart,name,id_manager,id  from team")
    result = cur.fetchall()
    result3 = {"Team":[]}
    for i in result:
        result3["Team"].append(i)
    # print(result3)
    return jsonify(result3)


##################################################################################################################################

### Test URLs:

@app.route('/new', methods=['GET'])
def sent():
    sender = {"depart_id":1,"name":"developers","manager_id":"1"}
    result = json.dumps(sender)
    r = requests.post("http://127.0.0.1:5000/teams", data=result)
    return result

@app.route("/department", methods=['GET', 'POST'])
def department():
    form1 = DepForm()
    if form1.validate_on_submit():
        print(form1.DepName.data)
        id_="Type"
        sender = {id_: form1.DepName.data}
        url = "http://127.0.0.1:5000/depart"
        r = requests.post(url, data=json.dumps(sender))
    return render_template("index.html", title="Department", form=form1)

####################################################################################################################################

### POST STARTS HERE:

@app.route("/depart", methods=['POST'])
def writer():
    if request.get_json(force=True):
        print("Ok")
        result = request.get_json(force=True)
        print(result)
    else: print("Empty")
    for i in result:
        print(i)
    cur.execute("select name from Depart where name ='" + str(result[i])+"'")
    results = cur.fetchall()
    if results:
        print("Data exist")
        return make_response("Department is already exist", 500)

    else:
        print("Data not presented in the database")
        cur.execute("insert into Depart (Name) values ('"+ str(result[i])+"')")
        conn.commit()
    return make_response("Department has been created", 200)


@app.route("/users", methods=['POST'])
def writer2():
    if request.get_json(force=True):
        print("Ok")
        result = request.get_json(force=True)
    else: print("Empty")
    cur.execute("select count(*) from employee where name ='"+ str(result['name'])+"' and surname = '" + str(result['sname']) + "'")
    results = cur.fetchall()
    print(results)
    print(type(results[0]['count']))
    if int(results[0]['count']) == 0:
        print("Data not presented in the database")
        for i in result:
            if result[i] == None:
                task = "dont write"
                return make_response("Not all fields are filled in", 500)
                break
            else: task = "write"
        if task == "write":
            cur.execute("insert into employee (team_id,name,surname,experience,position,salary,coef) values ('"+ str(result["team_id"])+"','"+ str(result["name"])+"','"+ str(result["sname"])+"','"+ str(result["exp"])+"','"+ str(result["position"])+"','"+ str(result["salary"])+"','"+ str(result["coefficient"])+"')")
            conn.commit()
            return make_response("Employee has been created", 200)
    else:
        return make_response("Employee is already exist", 500)


@app.route("/team", methods=["POST"])
def writer3():
    if request.get_json(force=True):
        print("Ok")
        result = request.get_json(force=True)
    else: print("Empty")
    cur.execute("select count(*) from team where name ='" + str(result["name"])+"' and id_manager = '" + str(result["manager_id"]) + "'")
    results = cur.fetchall()
    print(results)
    if int(results[0]['count']) != 0:
        print("Data exist")
        return make_response("Team is already exist", 500)
    else:
        print("Data not presented in the database")
        for i in result:
            if result[i] == None:
                task = "dont write"
                return make_response("Not all fields are filled in", 500)
                break
            else: task = "write"
        if task == "write":
            cur.execute("insert into team (iddepart,name,id_manager ) values ('"+ str(result["depart_id"])+"','"+ str(result["name"])+"','"+ str(result["manager_id"])+"')")
            conn.commit()
            return make_response("New team has been created", 200)

if __name__ == "__main__":
    app.run()




