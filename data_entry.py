from bson import ObjectId
from flask import Flask, Response, json, request, Blueprint
from main import DataslateDBContext

data_entry = Blueprint('data_entry', __name__)

data_entry_collection = DataslateDBContext("data_entry")
