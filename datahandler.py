from gzip import open as gzipopen
from json import load, dump
from os import path, makedirs

def updateusermap(username, map_id, map_data):
    data = load(open(f"./levels/{username}/data.json", "r"))
    data["levels"][str(map_id)] = map_data
    dump(data, open(f"./levels/{username}/data.json", "w"), indent=4)

def saveusermap(username, map_id, map_data):
    print(f"Writing {username}_{map_id}.dat")
    with gzipopen(f"./levels/{username}/level_{map_id}.dat", "w") as f:
        f.write(map_data)
    f.close()

def getusermaps(username):
    map_string = ""
    try:
        data = load(open(f"./levels/{username}/data.json", "r"))
    except:
        adduserentry(username)
        data = load(open(f"./levels/{username}/data.json", "r"))

    for y in range(5):
        try:
            map_string += data["levels"][str(y)]["name"]
        except:
            map_string += "-"
        if y != 4:
            map_string += ";"

    return(map_string)

def getusermapdata(username, map_id):
    with gzipopen(f"./levels/{username}/level_{map_id}.dat", "rb") as f:
        data = f.read()
    f.close()
    return data

def adduserentry(username):
    if not path.exists(f"./levels/{username}/"):
        makedirs(f"./levels/{username}/")
        data = open(f"./levels/{username}/data.json", 'x')
        data.write("{\"levels\": {}}")
        data.close()
