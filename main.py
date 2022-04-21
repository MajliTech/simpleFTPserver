from plistlib import InvalidFileException
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import TLS_FTPHandler
from pyftpdlib.servers import FTPServer
import elevate
import os
import json



def MainProgram():
    #Config file
    if os.path.isfile("config.json"):
        global config
        tempFile = open("config.json")
        config = json.loads(tempFile.read())
        del tempFile
    authorizer = DummyAuthorizer()

    if config["adminuser"]["enabled"]:
        authorizer.add_user(config["adminuser"]["username"], config["adminuser"]["password"], config["data"], perm='elradfmw')


    for i in list(config["users"]):
        if not i=="forbiden":
            (config["users"][i]["enabled"])
            if config["users"][i]["enabled"]:
                if os.path.exists(config["data"]+"/"+i):
                    authorizer.add_user(i, config["users"][i]["password"], config["data"]+f"/{i}", perm='elradfmw')
                else:
                    print(f"Semms like no folder for {i},creating!")
                    os.mkdir(f"{config['data']}/{i}")
                    f=open(f"{config['data']}/{i}/{config['welcome_message']['filename']}","w")
                    f.close()
                    f=open(f"{config['data']}/{i}/{config['welcome_message']['filename']}","a")
                    for o in config['welcome_message']['file-content']:
                        f.write(o.replace("$USER$",i)+"\n")
                    f.close()
                    
            else:
                if os.path.exists(f"{config['data']}/forbiden"):
                    authorizer.add_user(i, config["users"][i]["password"], config["data"]+f"/forbiden", perm='l')
                else:
                    os.mkdir(f"{config['data']}/forbiden")
                    open(f"{config['data']}/forbiden/Your account has been blocked by an administrator","w").close()
                    authorizer.add_user(i, config["users"][i]["password"], config["data"]+f"/forbiden", perm='l')
        else:
            raise InvalidFileException(f"Invalid name: {i}")
    handler = TLS_FTPHandler
    handler.certfile = 'server.crt'
    handler.keyfile = 'server.key'

    handler.authorizer = authorizer
    handler.banner = "ready"
    address = (config["server"]["bindto"], config["server"]["port"])
    server = FTPServer(address, handler)

    server.max_cons = config["server"]["maxcons"]
    server.max_cons_per_ip = config["server"]["maxipcons"]
    (list(config["users"]))
    server.serve_forever()


if __name__ == '__main__':
    MainProgram()