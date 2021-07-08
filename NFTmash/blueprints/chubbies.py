from flask import Blueprint, render_template
from random import randint
from uuid import uuid4
from json import dumps
from NFTmash import redis_client

bp = Blueprint('chubbies', __name__, url_prefix='/chubbies')
db = Redis('localhost')

@bp.route('/')
def index():
	left = {"random": 0, "image": ""}
	right = {"random": 0, "image": ""}

	while left["random"] == right["random"]:
		left["random"] = randint(0, 9999)
		right["random"] = randint(0, 9999)

	api = "https://ipfs.io/ipfs/QmNdNTQVE4BUpERFwVTxX2RwZNbTCSwQr5pZ83EJJsBfWW/%i.gif"

	left["image"] = api % left["random"]
	right["image"] = api % right["random"]

	candidates = {"left": left["random"], "right": right["random"], "nft": "chubbies"}

	uuid = str(uuid4())
	db.set(uuid, dumps(candidates), 35)

	dbsize = db.dbsize()

	return render_template("index.html", left=left, right=right, id=uuid, dbsize=dbsize)


@bp.route("/ranking")
def ranking():
	return "hi"