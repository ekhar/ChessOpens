from flask import flash,render_template, url_for, jsonify, redirect,session, request
from flask_session import Session
from ChessOpens import app, db, oauth, bcrypt
from ChessOpens.models import Opening, User
from ChessOpens.application import change_node, get_all_possible
from ChessOpens.forms import RegistrationForm, LoginForm
import re
import os
from flask_login import login_user, current_user


@app.route('/', methods=["GET", "POST"])
def home():
    #set node_id up with origin's id
    id = 1
    move_number = 0
    pgn = Opening.query.first().pgn
    # all possible moves
    db_moves = get_all_possible(id, move_number, pgn)[0]
    #current node name
    op_name = Opening.query.get(id).name
    openings = Opening.query.all()
    return render_template("home.html",
                           op_data={
                               "op_name": op_name,
                               "db_moves": list(db_moves),
                               "id": id,
                               "parent_id": 0
                           },
                           openings=openings,
                           )


@app.route('/update', methods=["GET", "POST"])
def update_nodes():
    if request.method == "POST":
        #pull info from js query
        pgn = request.get_json()["pgn"]
        id = request.get_json()["id"]
        moves = pgn.split(" ")
        #find the last period in pgn bc move numbers always before period in pgn
        if (len(pgn) == 0):
            move_number = 0
        #black just moved
        elif len(pgn.split(" ")) % 3 <= 1:
            #regex to find third to last number
            move_number = 2 * int(re.findall(r'\d+', pgn)[-3])
        #white just moved
        else:
            #regex to find second to last number
            move_number = 2 *int(re.findall(r'\d+', pgn)[-2])- 1
        
        #gets node_id to properly update
        id = change_node(id, move_number, pgn)
        node = Opening.query.get(id)
        db_moves = get_all_possible(id, move_number, pgn)[0]

        try:
            email = dict(session)['profile']['email']
        except:
            pass

        return jsonify({
            "op_name": node.name,
            "db_moves": list(db_moves),
            "id": id,
            "parent_id": node.parent_id
        })

@app.route('/search', methods=["GET", "POST"])
def search():
    print("hello")
    if request.method == "POST":
        name = request.get_json()["str_name"]
        search1 = "%{0}%".format(name)
        #include () in searches
        search2 = "%({})%".format(name)
        
        name_results = Opening.query.filter(Opening.name.like(search1)).all()
        
        name_results2 = Opening.query.filter(Opening.name.like(search2)).all()
        pgn_results =  Opening.query.filter(Opening.pgn.like(search1)).all()

        openings = name_results+pgn_results + name_results2 
        
        #returns html from boardinfo.html effectivley re instantiating what {{openings}} is
        return jsonify({"data": render_template("/searchop.html",openings = openings)})

@app.route('/logingoogle', methods=["GET"])
def logingoogle():
    print("HELLO")
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scrope
    user_info = resp.json()
    user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
    # Here you use the profile/user data that you got and query your database find/register the user
    # and set ur own data in the session not the profile from google
    print(user_info["email"])
    if not User.query.filter_by(email=user_info["email"]).first():
        user = User(email=user_info["email"], password=bcrypt.generate_password_hash(str(os.urandom(12))).decode('utf-8'))
        db.session.add(user)
        db.session.commit()
    session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed
    return redirect('/')

@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created! You may now login', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessful. Please check email and password.',"danger")
            flash(f'Google accounts must be signed in with Google', 'flash')
    return render_template('login.html', title='Login', form=form)


@app.route("/favorite", methods=['GET', 'POST'])
def favorite():
    if request.method == "POST":
        id = request.get_json()["id"]
        return jsonify({"data": render_template("/searchop.html",openings = openings)})