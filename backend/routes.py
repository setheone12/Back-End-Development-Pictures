from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))



######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data)

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    picture = next((pic for pic in data if pic['id'] == id), None)
    if picture:
        return jsonify(picture)
    else:
        return jsonify(error='Picture not found'), 404
    pass


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    data_list = request.get_json()
    new_picture = {
        "id": data_list['id'],
        "pic_url": data_list['pic_url'],
        "event_country": data_list['event_country'],
        "event_state": data_list['event_state'],
        "event_city": data_list['event_city'],
        "event_date": data_list['event_date']
    }
    if new_picture in data:
        return jsonify({"Message": "picture with id {} already present".format(data_list['id'])}), 302
    else:
        data.append(new_picture)
        return jsonify(new_picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture = next((pic for pic in data if pic['id'] == id), None)
    if picture:
        data_list = request.get_json()
        picture['id'] = data_list['id']
        picture['pic_url'] = data_list['pic_url']
        picture['event_country'] = data_list['event_country']
        picture['event_state'] = data_list['event_state']
        picture['event_city'] = data_list['event_city']
        picture['event_date'] = data_list['event_date']
        return jsonify(picture)
    else:
        return jsonify({"message": "picture not found"}), 404
    pass

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    picture = next((pic for pic in data if pic["id"] == id), None)
    if picture:
        data.remove(picture)
        return jsonify(), 204  # HTTP_204_NO_CONTENT
    else:
        return jsonify({"message": "picture not found"}), 404
