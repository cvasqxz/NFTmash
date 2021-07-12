from flask import Blueprint, render_template, request, Response
from NFTmash.models.ranking	 import Ranking
from NFTmash import redis_client, db
from json import loads

bp = Blueprint('ranking', __name__, url_prefix='/ranking')


@bp.route("/<collection>")
def vote_results(collection):
	current_page = request.args.get("page")
	current_page = 1 if current_page == None else int(current_page)

	count = Ranking.query.filter_by(collection=collection).count()
	max_pages = int(count/12) + 1

	full_ranking = Ranking.query.filter_by(collection=collection).order_by(Ranking.votes.desc()).limit(12).offset(12*(current_page-1))

	is_pixelated = True if collection == "cryptopunks" else False

	return render_template("ranking.html", 
		collection=collection, 
		full_ranking=full_ranking,
		current_page=current_page,
		max_pages=max_pages,
		pixelated=is_pixelated)


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