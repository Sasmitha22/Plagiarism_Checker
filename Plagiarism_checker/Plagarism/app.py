from flask import Flask,session,render_template,request,redirect,g,url_for
from pymongo import MongoClient
import urllib.request
import math
import re
import datetime 
from fpdf import FPDF
 

pdf = FPDF()
 

pdf.add_page()
 

pdf.set_font("Arial", size = 15)


app = Flask(__name__)
client=MongoClient()
client=MongoClient('mongodb://localhost:27017/')

db=client['Plagarism']
app.secret_key = 'password'
users=db['users']

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method=='POST':
        session.pop('user',None)


    if request.method=='POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['email']
        password = request.form['password']
        hist1=[]
        hist2=[]
        hist3=[]

        if db.users.find_one({'username': username}):
            return render_template('signup.html', result="Username already exists")
        
        user_data = {'username': username, 'password': password,
                     'firstname': firstname, 'lastname': lastname,
                     'history1':hist1,'history2':hist2, 'history3':hist3}
        db.users.insert_one(user_data)

        session['user'] = username
        
        return success()
    return render_template('signup.html')

@app.route('/signin', methods=['GET','POST'])
def signin():
    if request.method=='POST':
        session.pop('user',None)

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = db.users.find_one(
            {'username': username, 'password': password})
        if user:
            
            session['user'] = user['username']
            return success()
        else:
            return render_template('signin.html', result="Invalid username or password")

    return render_template('signin.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/home')
def success():
    if g.user:
        return render_template('home1.html')
    return redirect(url_for('home'))

@app.route('/plagiarism')
def mainn():
    if g.user:

        return render_template('plagarism.html')
    
    return redirect(url_for('signin'))

@app.before_request
def before_request():
    g.user=None

    if 'user' in session:
        g.user=session['user']

@app.route('/depression')
def depression():
    session.pop('user',None)
    return render_template('home.html')

@app.route('/history')
def history():
    user = db.users.find_one({'username': session['user']})
    if user:
        hist1=user.get('history1')
        hist2=user.get('history2')
        hist3=user.get('history3')
        no_of_box=len(hist1)
    return render_template('history.html',no_of_box=no_of_box,hist1=hist1,hist2=hist2,hist3=hist3)

@app.route('/plagiarism', methods=['POST'])
def upload_file():
    
    file = request.files['file1']
    file.save('check1.txt')    
    file1 = request.files['file2']
    
    file1.save('check2.txt')

    with open ("check1.txt","r") as h1:
        set1=h1.read()
    with open ("check2.txt","r") as h2:
        set2=h2.read()
    
    if set1=="" and set2=="":
        text1=request.form['doc1']
        text2=request.form['doc2']
        with open ("check1.txt","w") as c1:
            c1.write(text1)
        with open ("check2.txt","w") as c2:
            c2.write(text2)

    with open ("check1.txt","r") as h1:
        set1=h1.read()
    with open ("check2.txt","r") as h2:
        set2=h2.read()

    if set1=="" and set2=="":
        weburl11=urllib.request.urlopen(request.form['url1'])
        ("result: "+str(weburl11.getcode()))
        htmldata1=weburl11.read()
        htmldata1=str(htmldata1)
        weburl12=urllib.request.urlopen(request.form['url2'])
        ("result: "+str(weburl12.getcode()))
        htmldata2=weburl12.read()
        htmldata2=str(htmldata2)
        with open ("check1.txt","w") as c1:
            c1.write(htmldata1)
        with open ("check2.txt","w") as c2:
            c2.write(htmldata2)
        


    def rephrase(phrase):
        return re.sub(r"(\s+|[@$&*%#:;'.,!]*)","",phrase.lower())
    
    class Node:
        def __init__(self, order):
            self.order = order
            self.values = []
            self.keys = []
            self.nextKey = None
            self.parent = None
            self.check_leaf = False

    class Bplustree():
        def __init__(self, order,length):
            self.order = order
            self.length = length
            self.root = None
            self.con=[]
            self.ans=[]
            self.f_w=""
            self.s=''
            self.li=[",","!",".","_",";",")","}","]"]
        def ins(self, value, key):
            value = str(value)
            old_node = self.search(value)
            old_node.insert_at_leaf(old_node, value, key)

            if (len(old_node.values) == old_node.order):
                node1 = Node(old_node.order)
                node1.check_leaf = True
                node1.parent = old_node.parent
                mid = int(math.ceil(old_node.order / 2)) - 1
                node1.values = old_node.values[mid + 1:]
                node1.keys = old_node.keys[mid + 1:]
                node1.nextKey = old_node.nextKey
                old_node.values = old_node.values[:mid + 1]
                old_node.keys = old_node.keys[:mid + 1]
                old_node.nextKey = node1
                self.insert_in_parent(old_node, node1.values[0], node1)

        def srch(self, value):
            current_node = self.root
            while(current_node.check_leaf == False):
                temp2 = current_node.values
                for i in range(len(temp2)):
                    if (value == temp2[i]):
                        current_node = current_node.keys[i + 1]
                        break
                    elif (value < temp2[i]):
                        current_node = current_node.keys[i]
                        break
                    elif (i + 1 == len(current_node.values)):
                        current_node = current_node.keys[i + 1]
                        break
            return current_node

        def find(self, value, key):
            l = self.search(value)
            for i, item in enumerate(l.values):
                if item == value:
                    if key in l.keys[i]:
                        return True
                    else:
                        return False
            return False

        def insert_in_parent(self, n, value, ndash):
            if (self.root == n):
                rootNode = Node(n.order)
                rootNode.values = [value]
                rootNode.keys = [n, ndash]
                self.root = rootNode
                n.parent = rootNode
                ndash.parent = rootNode
                return

            parentNode = n.parent
            temp3 = parentNode.keys
            for i in range(len(temp3)):
                if (temp3[i] == n):
                    parentNode.values = parentNode.values[:i] + \
                        [value] + parentNode.values[i:]
                    parentNode.keys = parentNode.keys[:i +
                                                    1] + [ndash] + parentNode.keys[i + 1:]
                    if (len(parentNode.keys) > parentNode.order):
                        parentdash = Node(parentNode.order)
                        parentdash.parent = parentNode.parent
                        mid = int(math.ceil(parentNode.order / 2)) - 1
                        parentdash.values = parentNode.values[mid + 1:]
                        parentdash.keys = parentNode.keys[mid + 1:]
                        value_ = parentNode.values[mid]
                        if (mid == 0):
                            parentNode.values = parentNode.values[:mid + 1]
                        else:
                            parentNode.values = parentNode.values[:mid]
                        parentNode.keys = parentNode.keys[:mid + 1]
                        for j in parentNode.keys:
                            j.parent = parentNode
                        for j in parentdash.keys:
                            j.parent = parentdash
                        self.insert_in_parent(parentNode, value_, parentdash)
        def insert(self):
            with open ("check1.txt","r") as f:
                self.f_w1= (f.read ())
            for i in self.f_w1:
                self.s+=i
                if i in self.li:
                    self.s=self.s.lower()
                    p=rephrase(self.s)
                    self.con.append(p)
                    self.s=''
            #print(self.con)
        def search(self,given):
            if (given in self.con):
                return True
            else:
                return False
        def printtree(self):
            return self.con
        def sec_part(self):
            with open ("check2.txt","r") as f:
                self.f_w2= (f.read ())
            for i in self.f_w2:
                self.s+=i
                if i in self.li:
                    self.s=self.s.lower()
                    p=rephrase(self.s)
                    self.ans.append (p)
                    self.s=''
            #print(self.ans)
        def li_to_b(self):
            if len(self.ans)==0:
                return 0
            match=0
            for i in self.ans:
                #print(i)
                if self.search(i):
                    match+=1
            self.ann= (match/len(self.ans))*100
            return self.ann
        def b_to_li(self):
            if len(self.con)==0:
                return 0
            match=0
            for i in self.con:
                #print(i)
                if i in self.ans:
                    match+=1
            self.bnn= (match/len(self.con))*100
            return self.bnn
        def dbb(self):
            user = db.users.find_one({'username': session['user']})
            if user:
                hist1=user.get('history1')
                hist2=user.get('history2')
                hist3=user.get('history3')
                hist1.append(self.ann)
                hist2.append(self.bnn)
                hist3.append(datetime.datetime.now())
                db.users.update_one({'username':session['user']},{'$set':{'history1':hist1}})
                db.users.update_one({'username':session['user']},{'$set':{'history2':hist2}})
                db.users.update_one({'username':session['user']},{'$set':{'history3':hist3}})

    bplustree = Bplustree("file",10)
    bplustree.insert()
    bplustree.sec_part()
    sol1=bplustree.li_to_b()
    sol2=bplustree.b_to_li()
    bplustree.dbb()

    return render_template('result.html',ans1=sol1,ans2=sol2,txt1=bplustree.f_w1,txt2=bplustree.f_w2)

@app.route('/result')
def result():
    pass

    
if __name__ == '__main__':
    app.run(debug=True)
