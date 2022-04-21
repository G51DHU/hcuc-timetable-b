from bson.json_util import dumps as bson_dumps
from json import loads as json_loads

def BsonToJson(data):
    """Converts data that is of type "BSON" into "Json".

    Args:
        data (bson): Recieves data of type: Bson.

    Returns:
        json : Returns the data in converted form.
    """
    try:
        parsed_data =  json_loads(bson_dumps(data))[0]
        parsed_data["_id"] = parsed_data["_id"]["$oid"]
        return parsed_data
    except:
        parsed_data =  json_loads(bson_dumps(data))
        parsed_data["_id"] = parsed_data["$oid"]
        del parsed_data["$oid"]
        return parsed_data
