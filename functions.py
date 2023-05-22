import pymongo
import dns
import os
from bson.objectid import ObjectId


clientm = pymongo.MongoClient(os.getenv("clientm"))
notesdb = clientm.Notes
notescol = notesdb.Notes

def get_notes(user_id):
  myquery = {"UserId": int(user_id)}
  mydoc = notescol.find(myquery)
  notes = []
  for x in mydoc:
    notes.append(x)
  return notes

def get_note(note_id):
  myquery = {"_id": ObjectId(note_id)}
  mydoc = notescol.find(myquery)
  for x in mydoc:
    return x
  return False

def add_note(user_id, note):
  document = [{
    "Desc": note, 
    "UserId": int(user_id)
  }]
  notescol.insert_many(document)
  return True

def delete_note(user_id, note_id):
  note = get_note(note_id)
  if note == False:
    return "That note doesn't exist!"
  if note['UserId'] != int(user_id):
    return "You cannot delete someone else's note!"
  notescol.delete_one({"_id": note['_id']})
  return True