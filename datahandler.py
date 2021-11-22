from gzip import open as gzipopen
from json import load, dump

def updateusermap(username, map_id, map_data):
    data = load(open("./data.json", "r"))
    data["users"][username]["maps"][str(map_id)] = map_data
    dump(data, open("./data.json", "w"), indent=4)

def saveusermap(username, map_id, map_data):
    print(f"Writing {username}_{map_id}.dat")
    with gzipopen(f"./maps/{username}_{map_id}.dat", "w") as f:
        f.write(map_data)
    f.close()

def getusermaps(username):
    data = load(open("./data.json", "r"))
    map_string = ""
    found_data = False
    for x in data["users"]:
        if x == username:
            found_data = True
            for y in range(5):
                try:
                    map_string += data["users"][username]["maps"][str(y)]["name"]
                except:
                    map_string += "-"
                if y != 4:
                    map_string += ";"
    
    if found_data == False:
        adduserentry(username)
        return "-;-;-;-;-"
    return(map_string)

def getusermapdata(username, map_id):
    with gzipopen(f"./maps/{username}_{map_id}.dat", "rb") as f:
        data = f.read()
    f.close()
    return data

def adduserentry(username):
    data = load(open("./data.json", "r"))
    data["users"].update({f"{username}": {"maps": {}}})
    dump(data, open("./data.json", "w"), indent=4)
