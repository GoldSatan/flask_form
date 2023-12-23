from flask import Flask, render_template, session, redirect, request
from flask_sqlalchemy import SQLAlchemy
# pip install flask_sqlalchemy
# pip install pymysql

app = Flask(__name__)

app.config['SECRET_KEY'] = 'ASDASD!_)!@KD_!D@'
app.config['PERMANENT_SESSION_LIFETIME'] = 1800
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:0000@localhost/flask_form'


db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    
    id 			= db.Column(db.Integer, 	primary_key=True)
    username 	= db.Column(db.String(30), nullable=False)
    name 		= db.Column(db.String(20), nullable=False)
    surname 	= db.Column(db.String(20), nullable=False)
    email 		= db.Column(db.String(255), nullable=False)
    password 	= db.Column(db.String(30), nullable=False)
    
    
    def __repr__(self):
        return self.username


@app.route('/', methods=['GET', 'POST'])
def indexView():
	if request.method == 'POST':
		data = {}

		data['username'] = request.form.get('username')
		data['name'] = request.form.get('name')
		data['surname'] = request.form.get('surname')
		data['email'] = request.form.get('email')
		data['password'] = request.form.get('password')

		data_users = User.query.all()
  
		for item in data_users:
			if data['username'] == item.username:
				print('Користувач існує!!!!')
				return redirect('/login_success')

		try:
			new_user = User(
				username	=data['username'],
				name		=data['name'],
				surname		=data['surname'],
				email		=data['email'],
				password	=data['password'],
			) 
			db.session.add(new_user)
			db.session.commit()
		except:
			print('Error, add new user to database')
  
		return redirect('/login_success')

	else:
		return render_template('index.html')


@app.route('/login_success')
def successView():
    return render_template('success.html')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='8080')