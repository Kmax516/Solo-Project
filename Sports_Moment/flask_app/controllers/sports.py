from flask import render_template,redirect,request,session
from flask_app import app
# ...server.py
from flask_app.models import user, sport    





@app.route('/new/moment')
def bands():
    if 'user_num' in session:
        data ={
    'id': session['user_num']
    }
        return render_template('new.html',user=user.User.get_by_id(data))
      
    return redirect('/new/moment')

@app.route('/create/moment',methods=['POST'])
def create_band():
    if 'user_num' in session:
        print(request.form)
      
    if not sport.Sport.validate_band(request.form):
    
          return redirect('/new/moment')
    
    data = {
          'Player_Name' : request.form['Player_Name'],
          'Sport' : request.form['Sport'],
          'Team' : request.form['Team'],
          'Description' : request.form['Description'],
          'Image' : request.form['Image'],
          'Video' : request.form['Video'],
          'user_id'  : session ['user_num'],
        }
    sport.Sport.save(data)
    return redirect('/dashboard')

@app.route('/bands/delete/<int:id>')
def delete(id):
     if 'user_num' not in session:
         return redirect('/logout')
        
     data ={
        'id': id
      }
     sport.Sport.delete(data)
    
     return redirect('/dashboard')

@app.route('/edit/<int:id>')
def edit_page(id):
    data = {
        'id': id
    }
    data1 ={
    'id': session['user_num'] 
    }
    return render_template("edit.html", sport = sport.Sport.get_by_id(data), user=user.User.get_by_id(data1))

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
   
     if 'user_num' in session:
        print(request.form)
      
     if not sport.Sport.validate_band(request.form):
    
          return redirect ( f'/edit/{id}')
     data = {
        'id': id,
        'Player_Name' : request.form['Player_Name'],
        'Sport' : request.form['Sport'],
        'Team' : request.form['Team'],
        'Description' : request.form['Description'],
        'Image' : request.form['Image'],
        'Video' : request.form['Video'],
    }
     sport.Sport.update(data)
     return redirect('/dashboard')

@app.route('/moment/<int:id>')
def display(id):
    data = {
        'id': id
    }
    return render_template("display.html",sport1 = sport.Sport.get_by_id(data) )