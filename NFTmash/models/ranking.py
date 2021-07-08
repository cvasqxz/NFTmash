from NFTmash import db

class Ranking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    votes = db.Column(db.Integer, nullable=False)
    collection = db.Column(db.String(80), nullable=False)
    image = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return "Rank %i: %i votes" % (self.id, self.votes)