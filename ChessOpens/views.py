from flask import flash,render_template, url_for, jsonify, redirect,session, request, g
from sqlalchemy import or_
from functools import wraps
from flask_session import Session
from ChessOpens import app, db, oauth, bcrypt
from ChessOpens.models import Opening, User, addOpening
from ChessOpens.application import change_node, get_all_possible
from ChessOpens.forms import RegistrationForm, LoginForm
import re
import os
from flask_login import login_user, current_user, login_required



@app.route('/', methods=["GET", "POST"])
def home():
    #set node_id up with origin's id
    id = 1
    move_number = 1 
    pgn = "" 
    # all possible moves
    db_moves = get_all_possible(id, move_number, pgn)[0]
    #current node name
    op_name = Opening.query.get(id).name
    if current_user.is_authenticated:
        openings = Opening.query.filter(Opening.user_id==None, Opening.user_id==current_user.id).all()
    else:
        openings = Opening.query.filter(Opening.user_id==None).all()

    return render_template("home.html",
                           op_data={
                               "op_name": op_name,
                               "db_moves": list(db_moves),
                               "id": id,
                               "parent_id": 0
                           },
                           openings=openings,
                           op = Opening
                           )


@app.route('/update_specific', methods=["GET", "POST"])
def update_nodes_specific():
    if request.method == "POST":
        #pull info from js query
        pgn = request.get_json()["pgn"]
        if pgn=="":
            pgn = "1."
        fen = request.get_json()["fen"]
        moves = pgn.split(" ")
        #find the last period in pgn bc move numbers always before period in pgn
        if (len(pgn) == 0):
            move_number = 0
        #black just moved
        elif len(pgn.split(" ")) % 3 <= 1:
            #regex to find third to last number
            move_number = 2 * (int(fen.split()[-1]))-1
        #white just moved
        else:
            #regex to find second to last number
            move_number = 2 *(int(fen.split()[-1]))
        
        if current_user.is_authenticated:
            id = change_node(pgn, id, current_user.id)
        else:
            id = change_node(pgn,id)
        node = Opening.query.get(id)
        db_moves = moves[move_number]
        print("DB MOVES")
        print(db_moves)
        return jsonify({
            "op_name": node.name,
            "db_moves": list(db_moves),
            "id": id,
            "parent_id": node.parent_id
        })

@app.route('/update', methods=["GET", "POST"])
def update_nodes():
    if request.method == "POST":
        #pull info from js query
        pgn = request.get_json()["pgn"]
        if pgn=="":
            pgn = "1."
        id = request.get_json()["id"]
        fen = request.get_json()["fen"]
        moves = pgn.split(" ")
        #find the last period in pgn bc move numbers always before period in pgn
        if (len(pgn) == 0):
            move_number = 0
        #black just moved
        elif len(pgn.split(" ")) % 3 <= 1:
            #regex to find third to last number
            move_number = 2 * (int(fen.split()[-1]))-1
        #white just moved
        else:
            #regex to find second to last number
            move_number = 2 *(int(fen.split()[-1]))
        
        #gets node_id to properly update
        if current_user.is_authenticated:
            id = change_node(pgn, id, current_user.id)
        else:
            id = change_node(pgn,id)
        node = Opening.query.get(id)
        if current_user.is_authenticated:
            db_moves = get_all_possible(id, move_number, pgn, current_user.id)[0]
        else:
            db_moves = get_all_possible(id,move_number,pgn)[0]

        return jsonify({
            "op_name": node.name,
            "db_moves": list(db_moves),
            "id": id,
            "parent_id": node.parent_id
        })

@app.route('/search', methods=["GET", "POST"])
def search():
    if request.method == "POST":
        name = request.get_json()["str_name"]
        search1 = "%{0}%".format(name)
        #include () in searches
        search2 = "%({})%".format(name)
        
        if current_user.is_authenticated:

            name_results = Opening.query.filter(Opening.name.like(search1), or_(Opening.user_id==None, Opening.user_id==current_user.id) ).all()
            name_results2 = Opening.query.filter(Opening.name.like(search2), or_(Opening.user_id==None, Opening.user_id==current_user.id)).all()
            pgn_results =  Opening.query.filter(Opening.pgn.like(search1), or_(Opening.user_id==None, Opening.user_id==current_user.id)).all()

        else:
            name_results = Opening.query.filter(Opening.name.like(search1)).all()
            name_results2 = Opening.query.filter(Opening.name.like(search2)).all()
            pgn_results =  Opening.query.filter(Opening.pgn.like(search1)).all()

        openings = name_results+pgn_results + name_results2 
        
        #returns html from boardinfo.html effectivley re instantiating what {{openings}} is
        return jsonify({"data": render_template("/searchop.html",openings = openings)})

@app.route('/logingoogle', methods=["GET"])
def logingoogle():
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
    if not User.query.filter_by(email=user_info["email"]).first():
        user = User(email=user_info["email"], password=bcrypt.generate_password_hash(str(os.urandom(12))).decode('utf-8'))
        db.session.add(user)
        db.session.commit()
    session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed
    user = User.query.filter_by(email=user_info['email']).first()
    if user:
        login_user(user)
    return redirect('/')

@app.route('/logout')
@login_required
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
@login_required
def favorite():
    if request.method == "POST":
        opening_id = request.get_json()["opening_id"]
        user_id = current_user.id
        opening = Opening.query.get(opening_id)
        if current_user.favorites.filter_by(id=opening_id).first() is None:
            User.query.get(user_id).favorites.append(opening)
            db.session.commit()
            return jsonify({"id": opening.id, "status": "Unfavorite"})


@app.route("/unfavorite", methods=['GET', 'POST'])
@login_required
def unfavorite():
    if request.method == "POST":
        opening_id = request.get_json()["opening_id"]
        user_id = current_user.id
        opening = Opening.query.get(opening_id)
        User.query.get(user_id).favorites.remove(opening)
        db.session.commit()
        return jsonify({"id": opening.id, "status": "Favorite"})


@app.route("/view_favorites", methods=['GET', 'POST'])
@login_required
def view_favorites():
    fav_list = current_user.favorites.all()
    return jsonify({"data": render_template("/searchop.html",openings = fav_list)})

@app.route("/view_all", methods=['GET', 'POST'])
def view_all():
    openings = Opening.query.filter_by(user_id=None).all()
    if current_user.is_authenticated:
        openings += Opening.query.filter_by(user_id=current_user.id).all()
    return jsonify({"data": render_template("/searchop.html",openings = openings)})

@app.route("/view_custom", methods=['GET', 'POST'])
@login_required
def view_custom():
    user_id = current_user.id
    openings = User.query.get(user_id).custom_op
    return jsonify({"data": render_template("/searchop.html",openings = openings)})


@app.route("/create", methods=["GET", "POST"])
@login_required
def create_page():
    #set node_id up with origin's id
    id = 1
    move_number = 0
    pgn = Opening.query.first().pgn
    # all possible moves
    db_moves = get_all_possible(id, move_number, pgn)[0]
    #current node name
    op_name = Opening.query.get(id).name
    openings = Opening.query.filter_by(user_id=None)
    return render_template("create.html",
                           op_data={
                               "op_name": op_name,
                               "db_moves": list(db_moves),
                               "id": id,
                               "parent_id": 0
                           },
                           openings=openings,
                           op = Opening
                           )

@app.route("/create_op", methods=["GET", "POST"])
@login_required
def create_op():
    user_id = current_user.id
    name = request.get_json()["name"]
    pgn = request.get_json()["pgn"]
    if(Opening.query.filter_by(name=name, user_id=user_id).first() is None and Opening.query.filter_by(pgn=pgn, user_id=user_id).first() is None and name.strip() != ""):
        addOpening(name=name,pgn=pgn, user_id=user_id)
        return jsonify({"status": " has been added to your account!"})
    else:
        return jsonify({"status": " is already on your account with either a matching pgn or name (or blank name) as the one you tried to submit."})

@app.route("/delete_op", methods=["GET", "POST"])
@login_required
def delete_op():
    id = request.get_json()["id"]
    if Opening.query.get(id).user_id == current_user.id:
        Opening.query.filter_by(id=id).delete()
        db.session.commit()
    return redirect(url_for('view_custom'))
    #user_id = current_user.id
    #Opening.query.filter_by(user_id=user_id,name=name).remove()


@app.route("/random", methods=["GET", "POST"])
def random():
    if current_user.is_authenticated:
        openings = Opening.query.filter(Opening.user_id==None, Opening.user_id==current_user.id).all()
    else:
        openings = Opening.query.filter(Opening.user_id==None).all()
    
    id=1
    move_number=0
    op_name = Opening.query.get(id).name
    pgn = Opening.query.first().pgn
    db_moves = get_all_possible(id, move_number, pgn)[0]
    return render_template("/random.html",
                           op_data={
                               "op_name": op_name,
                               "db_moves": list(db_moves),
                               "id": id,
                               "parent_id": 0
                           },
                           openings=openings,
                           op = Opening
                           )
                           

@app.route("/specific", methods=["GET", "POST"])
def specific():
    if current_user.is_authenticated:
        openings = Opening.query.filter(Opening.user_id==None, Opening.user_id==current_user.id).all()
    else:
        openings = Opening.query.filter(Opening.user_id==None).all()
    
    id=1
    move_number=0
    op_name = Opening.query.get(id).name
    pgn = Opening.query.first().pgn
    db_moves = get_all_possible(id, move_number, pgn)[0]
    return render_template("/specific.html",
                           op_data={
                               "op_name": op_name,
                               "db_moves": list(db_moves),
                               "id": id,
                               "parent_id": 0
                           },
                           openings=openings,
                           op = Opening
                           )


@app.route('/undo', methods=["GET", "POST"])
def undo():
    if request.method == "POST":
        #pull info from js query
        pgn = request.get_json()["pgn"]
        opening = Opening.query.filter_by(pgn=pgn).first()
        name = opening.name
        id = opening.id
        parent_id = opening.parent_id
        
        fen = request.get_json()["fen"]
        moves = pgn.split(" ")

        #black just moved
        if len(pgn.split(" ")) % 3 <= 1:
            #regex to find third to last number
            move_number = 2 * (int(fen.split()[-1]))-1
        #white just moved
        else:
            #regex to find second to last number
            move_number = 2 *(int(fen.split()[-1]))

        if current_user.is_authenticated:
            db_moves = get_all_possible(id, move_number, pgn, current_user.id)[0]
        else:
            db_moves = get_all_possible(id,move_number,pgn)[0]

        return jsonify({
            "op_name": opening.name,
            "db_moves": list(db_moves),
            "id": id,
            "parent_id": parent_id
        })