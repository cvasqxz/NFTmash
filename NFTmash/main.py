from flask import Blueprint, render_template, request, Response
from NFTmash.models.ranking	 import Ranking
from NFTmash import redis_client, db
from json import loads

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route("/ranking/<collection>/")
def ranking(collection):
	full_ranking = Ranking.query.filter_by(collection=collection).limit(9)
	return render_template("ranking.html", collection=collection, full_ranking=full_ranking)


@bp.route("/vote", methods=["POST"])
def vote():
	assert request.method == 'POST'

	vote = request.form["vote"]
	uuid = request.form["uuid"]

	candidates = loads(redis_client.get(uuid))
	redis_client.delete(uuid)

	nft_id = int(candidates[vote]["id"])
	collection = candidates["nft"]
	image_url = candidates[vote]["image"]

	exists = Ranking.query.filter_by(id=nft_id, collection=collection).first()

	if exists == None:
		new_vote = Ranking(id=nft_id, collection=collection, votes=1, image=image_url)
		db.session.add(new_vote)
	else:
		exists.votes += 1

	db.session.commit()

	return Response(status=200)