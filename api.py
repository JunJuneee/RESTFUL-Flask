from flask import Flask
from flask_restful import abort, Api, fields, marshal_with, reqparse, Resource
from datetime import datetime
from models import MessageModel
import status
from pytz import utc

class MessageManager():
  last_id =0
  def __init__(self):
    self.messages = {}
  
  def insert_message(self, message):
    self.__class__ .last_id +=1
    message.id = self.__class__.last_id
    self.messages[self.__class__.lastid] = message

  def get_message(self, id):
    return self.messages[id]
  
  def delete_message(self, id):
    del self.messages[id]

message_fields = {
  'id' : fields.Integer,
  'uri' : fields.Url('message_endpoint')
  'message' : fields.String,
  'duration' : fields.Integer,
  'creation_date' : fields.DateTime,
  'message_category' : fields.String,
  'printed_time' : fields.Integer,
  'printed_once' : fields.Boolean
}

message_manager = MessageManager()

class Message(Resource):
  def abort_if_message_doesnt_exist(self, id):
    if id not in message_manager.messages:
      abort(
        status.HTTP_404_NOT_FOUND,
        message="Massage {0} doesn't exist".format(id))
  
  @marshal_with(message_fields)
  def get(self, id):
    self.abort_if_message_doesnt_exist(id)
    return message_manager.get_message(id)
  
  def delete(self, id):
    self.abort_if_message_doesnt_exist(id)
    message_manager.delete_message(id)
    return '', status.HTTP_204_NO_CONTENT
  
  @marshal_with(message_fields)
  def patch(self, id):
    self.abort_if_message_doesnt_exist(id)
    message = message_manager.get_message(id)
    parser = reqparse.RequestParser()
    parser.add_argument('message',type=str)
    parser.add_argument('duration',type=int)
    parser.add_argument('printed_times',type=int)
    parser.add_argument('printed_once',type=bool)
    args = parser.parse_args()
    if 'message' in args:
      message.message = args['message']
    if 'duration' in args:
      message.duration = args['duration']
    if 'printed_times' in args:
      message.printed_times = args['printed_times']
    if 'printed_once' in args:
      message.printed_once = args['printed_once']
    return message
    