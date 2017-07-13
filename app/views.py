from flask import Blueprint, render_template, jsonify, request, session, redirect, url_for
import json
import traceback
import models as models
from models import *
from sqlalchemy import or_

from forms import SignupForm, LoginForm, HeroForm

views = Blueprint('views', __name__)

@views.route('/') 
def index():
    """ Returns Welcome Page """
    return render_template('index.html')


@views.route('/tests/run')
def run_tests():
    """ Runs all the unittests and returns the text result with verbosity 2 """
    import overwatchdb.test_runner as test_runner
    return test_runner.run_tests()


@views.route('/api/players', methods=['GET'])
def players():
    """ Returns Players Page """
    data = models.Player.query.all()
    if not data:
        return render_template('404.html', thing='Players')
   
    return render_template('players.html', data=data)

@views.route('/api/players/asc', methods=['GET'])
def players_asc():
    """ Returns Heroes Page """
    data = models.Player.query.order_by(models.Player.name.asc()).all()
    if not data:
        return render_template('404.html', thing='Heroes')
    return render_template('players.html', data=data)

@views.route('/api/players/desc', methods=['GET'])
def players_desc():
    """ Returns Heroes Page """
    data = models.Player.query.order_by(models.Player.name.desc()).all()
    if not data:
        return render_template('404.html', thing='Heroes')
    
    return render_template('players.html', data=data)

@views.route('/api/players/<int:player_id>', methods=['GET'])
def player(player_id):
    """ Returns Page for a single Player """
    data = models.Player.query.get(player_id)
    if not data:
        return render_template('404.html', thing='Player')

    return render_template('players_instance.html', data=data)


@views.route('/api/heroes', methods=['GET'])
def heroes():
    if ("hero page" not in session):
        session["hero page"] = 1
    if ("hero order" not in session):
        session["hero order"] = "ascending"
    if ("hero filter" not in session):
        session["hero filter"] = "non"
    
    if type(request.args.get('page')) is unicode:
        session["hero page"] = int(request.args.get('page'))
    if type(request.args.get('order')) is unicode:
        session["hero order"] = str(request.args.get('order'))
    if type(request.args.get('filter')) is unicode:
        session["hero filter"] = str(request.args.get('filter'))

    """ Returns Heroes Page """
    if session["hero order"] == "ascending":
        if session["hero filter"] == "non":
            data = models.Hero.query.order_by(models.Hero.name.asc()).all()
        elif session["hero filter"] == "Overwatch":
            data = models.Hero.query.order_by(models.Hero.name.asc()).filter(Hero.affiliation == 'Overwatch').all()
        else:
            data = models.Hero.query.order_by(models.Hero.name.asc()).filter(Hero.affiliation != 'Overwatch').all()
    else:
        if session["hero filter"] == "non":
            data = models.Hero.query.order_by(models.Hero.name.desc()).all()
        elif session["hero filter"] == "Overwatch":
            data = models.Hero.query.order_by(models.Hero.name.desc()).filter(Hero.affiliation == 'Overwatch').all()
        else:
            data = models.Hero.query.order_by(models.Hero.name.desc()).filter(Hero.affiliation != 'Overwatch').all()
        
    
    if not data:
        return render_template('404.html', thing='Heroes')
    output = data[9 * (session["hero page"] - 1): 9 * session["hero page"]]

    return render_template('heroes.html', data=data, output=output)


@views.route('/api/heroes/<int:hero_id>', methods=['GET'])
def hero(hero_id):
    """ Returns Page for a single Hero """
    data = models.Hero.query.get(hero_id)
    if not data:
        return render_template('404.html', thing='Hero')
    
    return render_template('heroes_instance.html', data=data)


@views.route('/api/rewards', methods=['GET'])
def rewards():
    if ("reward page" not in session):
        session["reward page"] = 1
    if ("reward order" not in session):
        session["reward order"] = "Low Cost"
    if ("reward filter" not in session):
        session["reward filter"] = "non"
    
    if type(request.args.get('page')) is unicode:
        session["reward page"] = int(request.args.get('page'))
    if type(request.args.get('order')) is unicode:
        session["reward order"] = str(request.args.get('order'))
    if type(request.args.get('filter')) is unicode:
        session["reward filter"] = str(request.args.get('filter'))

    """ Returns Heroes Page """
    if session["reward order"] == "Low Cost":
        if session["reward filter"] == "non":
            data = models.Reward.query.order_by(models.Reward.cost.asc()).all()
        elif session["reward filter"] == "From Achievements":
            data = models.Reward.query.order_by(models.Reward.cost.asc()).filter(Reward.achievement_id != None).all()
        else:
            data = models.Reward.query.order_by(models.Reward.cost.asc()).filter(Reward.achievement_id == None).all()
    else:
        if session["reward filter"] == "non":
            data = models.Reward.query.order_by(models.Reward.cost.desc()).all()
        elif session["reward filter"] == "From Achievements":
            data = models.Reward.query.order_by(models.Reward.cost.desc()).filter(Reward.achievement_id != None).all()
        else:
            data = models.Reward.query.order_by(models.Reward.cost.desc()).filter(Reward.achievement_id == None).all()
    
    if not data:
        return render_template('404.html', thing='Rewards')
    output = data[54 * (session["reward page"] - 1): 54 * session["reward page"]]

    return render_template('rewards.html', data=data, output=output)


@views.route('/api/rewards/<int:reward_id>', methods=['GET'])
def reward(reward_id):
    """ Returns Page for a single Reward """
    data = models.Reward.query.get(reward_id)
    if not data:
        return render_template('404.html', thing='Reward')
    
    return render_template('rewards_instance.html', data=data)



@views.route('/api/achievements', methods=['GET'])
def achievements():
    """ Returns Achievements Page """
    if ("achievement page" not in session):
        session["achievement page"] = 1
    if ("achievement order" not in session):
        session["achievement order"] = "ascending"
    if ("achievement filter" not in session):
        session["achievement filter"] = "non"
    
    if type(request.args.get('page')) is unicode:
        session["achievement page"] = int(request.args.get('page'))
    if type(request.args.get('order')) is unicode:
        session["achievement order"] = str(request.args.get('order'))
    if type(request.args.get('filter')) is unicode:
        session["achievement filter"] = str(request.args.get('filter'))

    """ Returns Heroes Page """
    if session["achievement order"] == "ascending":
        if session["achievement filter"] == "non":
            data = models.Achievement.query.order_by(models.Achievement.name.asc()).all()
        elif session["achievement filter"] == "Linked to Hero":
            data = models.Achievement.query.order_by(models.Achievement.name.asc()).filter(Achievement.hero_id != None).all()
        else:
            data = models.Achievement.query.order_by(models.Achievement.name.asc()).filter(Achievement.hero_id == None).all()
    else:
        if session["achievement filter"] == "non":
            data = models.Achievement.query.order_by(models.Achievement.name.desc()).all()
        elif session["achievement filter"] == "Linked to Hero":
            data = models.Achievement.query.order_by(models.Achievement.name.desc()).filter(Achievement.hero_id != None).all()
        else:
            data = models.Achievement.query.order_by(models.Achievement.name.desc()).filter(Achievement.hero_id == None).all()
    
    if not data:
        return render_template('404.html', thing='Rewards')
    output = data[12 * (session["achievement page"] - 1): 12 * session["achievement page"]]

    return render_template('achievements.html', data=data, output=output)

@views.route('/api/achievements/<int:achievement_id>', methods=['GET'])
def achievement(achievement_id):
    """ Returns Page for a single Achievement """
    data = models.Achievement.query.get(achievement_id)
    if not data:
        return render_template('404.html', thing='Reward')
    
    return render_template('achievements_instance.html', data=data)



@views.route('/about/')
def about():
    """ Returns Heroes Page """
    return render_template('about.html')

# Usage example: "http://127.0.0.1:5000/api/search?search_string=her&page=1"
@views.route('/api/search', methods=['GET'])
def search(search_string="", page=1):
    if request.form.get('search_string') is not None :
        search_string = request.form.get('search_string') 
    else:
        search_string = request.args.get('search_string')
    print(search_string)
    # Disabling because of switch to client-side pagination
    # if request.form.get('page') is not None :
    #     page = request.form.get('page')
    # else :
    #     page = int(request.args.get('page'))
    page = 1
    if not search_string :
        return render_template('search.html', data=[[], []])

    # Find the AND search matches in the tables
    like_search_string = "%" + search_string + "%"
    data = [[], []]
    data[0] += models.Achievement.query.filter(or_(Achievement.name.like(like_search_string),
                                               Achievement.description.like(like_search_string))).all()
    data[0] += models.Reward.query.filter(or_(Reward.name.like(like_search_string),
                                           Reward.quality.like(like_search_string))).all()
    data[0] += models.Player.query.filter(or_(Player.name.like(like_search_string),
                                           Player.server.like(like_search_string),
                                           Player.level.like(like_search_string),
                                           Player.server.like(like_search_string))).all()
    data[0] += models.Hero.query.filter(or_(Hero.name.like(like_search_string),
                                         Hero.age.like(like_search_string),
                                         Hero.description.like(like_search_string),
                                         Hero.affiliation.like(like_search_string))).all()

    # Find the OR search matches in the tables
    for word in search_string.split():
        word = "%" + word + "%"
        data[1] += models.Achievement.query.filter(or_(Achievement.name.like(word),
                                                   Achievement.description.like(word))).all()
        data[1] += models.Reward.query.filter(or_(Reward.name.like(word),
                                               Reward.quality.like(word))).all()
        data[1] += models.Player.query.filter(or_(Player.name.like(word),
                                               Player.server.like(word),
                                               Player.level.like(word),
                                               Player.server.like(word))).all()
        data[1] += models.Hero.query.filter(or_(Hero.name.like(word),
                                             Hero.age.like(word),
                                             Hero.description.like(word),
                                             Hero.affiliation.like(word))).all()

    # Get the data into usable dicts
    data = [[d.serialize() for d in data[0]], [d.serialize() for d in data[1]]]

    search_results = [[], []]
    # Search through the results for the context of search terms as well as format the search results into usable values
    for result in data[0]:
        context = []
        for value in [getContext(val, search_string) for val in result.values()]:
            if (value != []):
                context += value
        search_results[0].append({"name": result["name"], "search_url": result["search_url"], "matches": context})
    for result in data[1]:
        context = []
        for word in search_string.split():
            for value in [getContext(val, word) for val in result.values()]:
                if (value != []):
                    context += value
        search_results[1].append({"name": result["name"], "search_url": result["search_url"], "matches": context})

    # Get the results for the specified page
    # search_results = [search_results[0][10 * (page - 1):10 * page], search_results[1][10 * (page - 1):10 * page]]
    return render_template('search.html', data=search_results)

# Method to find context in the values of the table entries
def getContext(val, search):
    context_amount = 5
    results = []
    if (type(val) is int):
        try:
            if (val == int(search)):
                return [val]
        except Exception:
            return results
    if (type(val) is unicode):
        index = val.find(search)
        while (index != -1):
            front = index
            back = index
            frontCount = context_amount + 1
            backCount = context_amount + 1
            while (frontCount > 0 or backCount > 0):
                if (front > 0 and frontCount > 0):
                    front -= 1
                if (back < len(val) and backCount > 0):
                    back += 1
                if (val[front] == ' ' or front == 0):
                    frontCount -= 1
                if (back == len(val) or val[back] == ' '):
                    backCount -= 1
            results.append(val[front:back].encode('utf-8'))
            frontCount = context_amount + 1
            backCount = context_amount + 1
            val = val[back::]
            index = val.find(search)
    return results



@views.route("/createHero", methods=["GET", "POST"])
def createHero():
  form = HeroForm()

  if request.method == "POST":
    if form.validate() == False:
      return render_template('createHero.html', form=form)
    else:
      hero = Hero(form.name.data, form.description.data, form.affiliation.data, form.age.data, form.url.data)
      db.session.add(hero)
      db.session.commit()
      return redirect(url_for('views.index'))

  elif request.method == "GET":
    return render_template('createHero.html', form=form)

#Signup, Login, Logout ------

@views.route("/signup", methods=["GET", "POST"])
def signup():
  form = SignupForm()

  if request.method == "POST":
    if form.validate() == False:
      return render_template('signup.html', form=form)
    else:
      newuser = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
      db.session.add(newuser)
      db.session.commit()

      session['email'] = newuser.email
      return redirect(url_for('views.index'))

  elif request.method == "GET":
    return render_template('signup.html', form=form)


@views.route("/login", methods=["GET","POST"])
def login():
  form = LoginForm()

  if request.method == "POST":
    if form.validate() == False:
        return render_template("login.html", form=form)
    else:
      email = form.email.data
      password = form.password.data

      user = User.query.filter_by(email=email).first()
      if user is not None and user.check_password(password):
        session['email'] = form.email.data
        return redirect(url_for('views.index'))
      else:
        return redirect(url_for('views.login'))

  elif request.method == "GET":
    return render_template('login.html', form=form)


@views.route("/logout")
def logout():
  session.pop('email', None)
  return redirect(url_for('views.index'))




