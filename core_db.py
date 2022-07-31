import mysql.connector
from mysql.connector import Error

import db_config


# Database requests
class db:

    def __init__(self):
        self.connection = mysql.connector.connect(
            host=db_config.server,
            user=db_config.username,
            passwd=db_config.password,
            database=db_config.database
        )
        self.cursor = self.connection.cursor(buffered=True)

    def guilds_get(self):
        for result in self.cursor.execute('select * from guilds where id_guild=' + str(id), multi=True):
            if result.with_rows:
                res = result.fetchall()
        return res

    # def guild_add(self, id, name, status):
    #     for result in self.cursor.execute('select * from guilds where id_guild=' + str(id), multi=True):
    #         if result.with_rows:
    #             check = result.fetchall()
    #     if check:
    #         self.cursor.execute('UPDATE guilds SET status=\'' + str(status) + '\' WHERE id_guild=' + str(id), multi=True)
    #         self.connection.commit()
    #     else:
    #         self.cursor.execute('INSERT INTO guilds (id_guild, name_guild, status) VALUES (' + str(id) + ', \'' + str(name) + '\',\'' + str(status) + '\')', multi=True)
    #         self.connection.commit()
    #
    # def guild_remove(self, id, status):
    #     self.cursor.execute('UPDATE guilds SET status=\'' + str(status) + '\' WHERE id_guild=' + str(id), multi=True)
    #     self.connection.commit()
