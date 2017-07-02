"""models for the database"""
# pylint: disable=too-few-public-methods,invalid-name

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Hero(db.Model):
	"""model for hero"""
	__tablename__ = 'hero'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	description = db.Column(db.String)
	affiliation = db.Column(db.String)
	age = db.Column(db.String)
	player_id = db.relationship("db.")

    def __repr__(self):
        return "<Hero(name='%s', description=%s, affiliation=%s, age=%s)>" % (
            self.name, self.description, self.affiliation, self.age)

    def search_result(self):
        """ Returns result format for the hero """
        return {"model": "hero", "id": self.id}

class Player(db.Model):
	"""model for player"""
	__tablename__ = 'player'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	server = db.Column(db.String)
	hero_id = db.Column(db.Integer, db.ForeignKey("hero_id"))
	level = db.Column(db.String)

    def __repr__(self):
        return "<Player(name='%s', server=%s, level=%s, temperature=%s, radius=%s)>" % (
            self.name, self.mass, self.luminosity, self.temperature, self.radius)

    def search_result(self):
        """ Returns result format for the player """
        return {"model": "hero", "id": self.id}

class Reward(db.Model):
	"""model for reward"""
	__tablename__ = 'reward'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	quality = db.Column(db.String)
	cost = db.Column(db.String)
	hero_id = db.relationship("Hero", backref="reward_id")
	achievement_id = db.Column(db.Integer, db.ForeignKey("achievement.id"))

    def __repr__(self):
        return "<Star(name='%s', mass=%s, luminosity=%s, temperature=%s, radius=%s)>" % (
            self.name, self.mass, self.luminosity, self.temperature, self.radius)

    def search_result(self):
        """ Returns result format for the reward """
        return {"model": "hero", "id": self.id}

class Achievement(db.Model):
	"""model for achievement"""
	__tablename__ = 'achievement'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	description = db.Column(db.String)
	type = db.Column(db.String)
	hero_id = db.relationship("Hero", backref="achievement_id")
	reward_id = db.relationship("Reward", backref="achievement_id")

    def __repr__(self):
        return "<Star(name='%s', mass=%s, luminosity=%s, temperature=%s, radius=%s)>" % (
            self.name, self.mass, self.luminosity, self.temperature, self.radius)

    def search_result(self):
        """ Returns result format for the achievement """
        return {"model": "hero", "id": self.id}

