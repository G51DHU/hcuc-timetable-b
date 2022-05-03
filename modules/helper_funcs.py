from bson.json_util import dumps as bson_dumps
from json import loads as json_loads

def BsonToJson(data):
    """Converts data that is of type "BSON" into "Json".

    Args:
        data (bson): Recieves data of type: Bson.

    Returns:
        json : Returns the data in converted form.
    """
    parsed_data =  json_loads(bson_dumps(data))
    for index in range(len(parsed_data)):
        parsed_data[index]["_id"] = parsed_data[index]["_id"]["$oid"]
    return parsed_data
    
