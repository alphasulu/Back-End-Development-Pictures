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
    return data

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    item = list(filter(lambda x: x['id']==id, data))
    if(len(item)>0):
        return item[0]
    else:
        return {"message": "Item not found"}, 404


# {'id': 200, 'pic_url': 'http://dummyimage.com/230x100.png/dddddd/000000', 'event_country': 'United States', 'event_state': 'California', 'event_city': 'Fremont', 'event_date': '11/2/2030'}
######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    arg = request.get_json()
    idd = arg['id']
    foundItem = list(filter(lambda x: x['id']==idd, data))
    if len(foundItem)>0:
        return {"Message": f"picture with id {idd} already present"}, 302
    else:
        data.append(arg)
        return {"id": idd}, 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    arg = request.get_json()
    id = arg['id']
    foundItem = list(filter(lambda x: x['id']==id, data))
    if len(foundItem)>0:
        data.remove(foundItem[0])
        data.append(arg)
        return {"id": id}, 201
    else:
        return {"message": "picture not found"}, 404
######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    foundItem = list(filter(lambda x: x['id']==id, data))
    if len(foundItem)>0:
        data.remove(foundItem[0])
        return {"id": id}, 204
    else:
        return {"message": "picture not found"}, 404
