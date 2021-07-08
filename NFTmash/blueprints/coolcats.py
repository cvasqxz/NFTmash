from flask import Blueprint, render_template
from random import randint
from requests import get
from uuid import uuid4
from json import dumps
from NFTmash import redis_client
from NFTmash.models.ranking	import Ranking

bp = Blueprint('coolcats', __name__, url_prefix='/coolcats')
url = "https://api.coolcatsnft.com/cat/%i"

@bp.route('/')
def index():
	left = {"random": 0, "image": ""}
	right = {"random": 0, "image": ""}

	while left["random"] == right["random"]:
		left["random"] = randint(0, 9907)
		right["random"] = randint(0, 9907)

	left["image"] = get(url % left["random"]).json()["image"]
	right["image"] = get(url % right["random"]).json()["image"]

	candidates = {"left": {"id": left["random"], "image": left["image"]}, 
				  "right": {"id": right["random"], "image": right["image"]},
				  "nft": "coolcats"}

	uuid = str(uuid4())
	redis_client.set(uuid, dumps(candidates), 35)

	dbsize = redis_client.dbsize()

	return render_template("index.html", left=left, right=right, id=uuid, dbsize=dbsize)
