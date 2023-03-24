import subprocess
import json
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from models import SqliteDB

file_path = "/etc/x-ui/x-ui.db"
# file_path = "x-ui.db"

# file_path = "x-ui-english.db"

app = FastAPI(openapi_url="",)


@app.get("/hacker")
def read_root():
    return {"Hello": "hacker"}


@app.get("/user/{email_uuid_user}")
def read_item(email_uuid_user: str):
    db = SqliteDB(file_path)
    fff = db.all_user_traffic_with_email(email_uuid_user)
    db.close_db()
    return fff


@app.get("/admin/{port}/{uuid}")
def read_item(port: str, uuid: str):
    db = SqliteDB(file_path)
    fff = db.all_admin_traffic_with_uuid(port, uuid)
    db.close_db()
    return fff


class Item(BaseModel):
    port: int
    id: str
    alterId: int | None
    email: str
    limitIp: int | None
    totalGB: int
    expiryTime: str | int


@app.post("/addClients")
def read_add_client(data: Item):
    db = SqliteDB(file_path)
    port = data.port
    all_in_db = db.all_exist_with_port(port)
    user_number = len(json.loads(db.get_settings(port,))["clients"])
    limip = 4
    alter = user_number+1

    if data.limitIp == None:
        pass
    else:
        limip = data.limitIp
    if data.alterId == None:
        pass
    else:
        alter = data.alterId

    if data.expiryTime == "":
        pass
    else:
        data.expiryTime = int(data.expiryTime,)
    d = {
        "id": data.id,
        "alterId": alter,
        "email": data.email,
        "limitIp": limip,
        "totalGB": data.totalGB,
        "expiryTime": data.expiryTime,
    }
    d_vless = {
        "id": data.id,
        "flow": "xtls-rprx-direct",
        "email": data.email,
        "limitIp": limip,
        "totalGB": data.totalGB,
        "expiryTime": data.expiryTime,
    }
    if all_in_db:
        if all_in_db[10] == "vmess":
            db.client_settings_updator(port, d)
        if all_in_db[10] == "vless":
            db.client_settings_updator(port, d_vless)
        db.add_row("client_traffics", (None,
                                       all_in_db[0], True, d["email"], 0,
                                       0, data.expiryTime, d["totalGB"],))
        db.close_db()
        restart_xui()
        d.update({"port": port, "id_in_pan": all_in_db[0],
                  "protocol": all_in_db[10],
                  "streamSettings": all_in_db[12],
                  })
        print("restrat is done")
        return d


def restart_xui() -> None:
    subprocess.run(["x-ui", "restart"])


if __name__ == "__main__":
    db = SqliteDB(file_path)
    # ddd = db.get_settings(443,)
    ddd = len(json.loads(db.get_settings(443,))["clients"])

    # ddd = db.inbound_id_finder(
    #     443, {"id": "1o2o2o1o21o2o1", "alterId": 0})
    print(ddd)
