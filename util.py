import pickle
import base64

def object_to_json(object):
	return base64.b64encode(pickle.dumps(object)).decode()

def json_to_object(json_string):
	return pickle.loads(base64.b64decode(json_string))