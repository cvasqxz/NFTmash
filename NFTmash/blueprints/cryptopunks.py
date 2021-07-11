from flask import Blueprint, render_template
from random import randint
from uuid import uuid4
from json import dumps
from NFTmash import redis_client
from NFTmash.models.ranking	import Ranking

bp = Blueprint('cryptopunks', __name__, url_prefix='/cryptopunks')
url = "https://www.larvalabs.com/public/images/cryptopunks/punk%s.png"

@bp.route('/')
def index():
	left = {"random": 0, "image": ""}
	right = {"random": 0, "image": ""}

	while left["random"] == right["random"]:
		left["random"] = randint(0, 9999)
		right["random"] = randint(0, 9999)

	left["image"] = url % str(left["random"]).zfill(4)
	right["image"] = url % str(right["random"]).zfill(4)

	candidates = {"left": {"id": left["random"], "image": left["image"]}, 
				  "right": {"id": right["random"], "image": right["image"]},
				  "nft": "cryptopunks"}

	uuid = str(uuid4())
	redis_client.set(uuid, dumps(candidates), 35)

	dbsize = redis_client.dbsize()

	return render_template("index.html", left=left, right=right, id=uuid, dbsize=dbsize, pixelated=True)
