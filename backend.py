from flask import Flask, render_template, request, redirect, jsonify, session
app = Flask(__name__)
app.secret_key = 'Tarbiyah23'

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/api/mhs')
def api_mahasiswa():
  mhs=[]
  docs = db.collection('mahasiswa').stream()
  for doc in docs:
    mahasiswa = doc.to_dict()
    mahasiswa['id'] = doc.id
    mhs.append(mahasiswa)
  return jsonify(mhs)

@app.route('/')
def index():
  if 'login' not in session:
      return redirect('/login')    
  mhs=[]
  docs = db.collection('mahasiswa').stream()
  for doc in docs:
    mahasiswa = doc.to_dict()
    mahasiswa['id'] = doc.id
    mhs.append(mahasiswa)
  return render_template("index.html", mhs=mhs)

@app.route('/regis')
def regis():
	return render_template("regis.html")

@app.route('/prosesregis',methods=["POST"])
def prosesregis():
  username  = request.form.get("username")
  password = request.form.get("password")
  admin = {
    'username'  : username,
    'password'  : password
  }
  db.collection('admin').document().set(admin)
  return redirect('/')

@app.route('/login')
def login():
  if 'login'  in session:
  # if session['login'] == True:
    return redirect('/')
  return render_template("login.html")

@app.route('/proseslogin', methods=["POST"])
def proseslogin():
  username  = request.form.get("username")
  password = request.form.get("password")
  # docs = db.collection('admin').stream()
  # for d in docs:
  #   admin = d.to_dict()
  #   login = None
  #   if admin['username'] == username and admin['password'] == password :
  #     print("Berhasil Login")
  #     login = "ok"
  #     break
  #   else:
  #     # print("Login Gagal")
  #   # print(d)
  
  docs = db.collection('admin').where('username', '==', username).where('password', '==', password).stream()
  for d in docs:
    admin = d.to_dict()
    if admin['password'] == password :
      session['login'] = True
      return redirect('/')
  return render_template("login.html")

@app.route('/logout')
def logout():
	session.clear()
	# session.pop('login', None)
	return redirect('/')



@app.route('/detail/<id>')
def detail(id):
  d = db.collection(u'mahasiswa').document(id).get().to_dict()
  return render_template("detail.html", d=d)

@app.route('/edit/<id>')
def edit(id):
  # d = db.collection(u'mahasiswa').document(id).get().to_dict()
  d = db.collection(u'mahasiswa').document(id).get()
  mahasiswa = d.to_dict()
  mahasiswa['id'] = d.id
  return render_template("edit.html", d=mahasiswa)

@app.route('/update/<id>',methods=["POST"])
def update(id):
  nama  = request.form.get("nama")
  email = request.form.get("email")
  foto = request.form.get("foto")
  nilai = request.form.get("nilai")
  alamat = request.form.get("alamat")
  no_hp = request.form.get("no_hp")
  
  db.collection(u'mahasiswa').document(id).update({
    'nama'  : nama,
    'email'  : email,
    'foto'  : foto,
    'nilai'  : int(nilai),
    'alamat'  : alamat,
    'no_hp'  : no_hp
  })
  return redirect('/')

@app.route('/delete/<id>',methods=["GET"])
def delete(id):
  db.collection(u'mahasiswa').document(id).delete()
  return redirect('/')


@app.route('/add',methods=["POST"])
def add_data():
  nama  = request.form.get("nama")
  email = request.form.get("email")
  nilai = request.form.get("nilai")
  alamat = request.form.get("alamat")
  no_hp = request.form.get("no_hp")

  mahasiswa = {
    'nama'  : nama,
    'email'  : email,
    'nilai'  : int(nilai),
    'alamat'  : alamat,
    'no_hp'  : no_hp
  }
  db.collection('mahasiswa').document().set(mahasiswa)
  return redirect('/')

if __name__ == "__main__":
  app.run(debug=True)