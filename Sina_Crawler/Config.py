# -*- coding: utf-8 -*-
import re

class Config:

    MYSQL={
        # online
        # '0':{"host":"127.0.0.1","db_name":"joudou_user","uname":"joudou","pwd":"MZrh2sf$6YYa","encoding":"utf8","port":3306},
        # '1':{"host":"127.0.0.1","db_name":"jiudou","uname":"jiudou","pwd":"8682CrWVaXTgChbM","encoding":"utf8","port":3306}
        # local
        '0':{"host":"127.0.0.1","db_name":"test","uname":"kenan","pwd":"tiger","encoding":"utf8","port":3306},
        '1':{"host":"127.0.0.1","db_name":"jiudou","uname":"kenan","pwd":"tiger","encoding":"utf8","port":3306}
       }

    INFLOGGER = "infoLogger"
    ERRLOGGER = "errorLogger"

