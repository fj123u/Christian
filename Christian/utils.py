import os
import mysql.connector as mysql
import locale
import time


from datetime import datetime


locale.setlocale(locale.LC_TIME,'')
months = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']


def get_current_time() -> str:
    time_str: str = str(datetime.now())
    return time_str[:time_str.find('.')]


def get_fancy_date(datetime) -> str:
    month_name: str = months[int(time.strftime("%m"))-1]
    string: str = f'{datetime:%A %d {month_name} %Y - %H:%M:%S}'
    return string[0].capitalize() + string[1:]


def get_fancy_date2():
    return get_fancy_date(datetime.now())


class MySQL:
    def __init__(self):
        self.connection = mysql.connect(
            user = '',
            password = '',
            host = '',
            database = 'christian'
        )
        self.cursor = self.connection.cursor()

    def query(self, request, update = False):
        self.cursor.execute(request)
        if update:
            self.connection.commit()
        else:
            return self.cursor.fetchall()


class Database:
    def __init__(self):
        self.con = MySQL()
    
    # TODO : fetch working but not updating after the program started
    def fetch_computers(self):
        data: list[tuple] = self.con.query('SELECT DISTINCT poste FROM registre')
        self.computers = {}
        
        for row in data:
            room: str = row[0][1:5]
            computer: str = row[0]
            
            if room not in list(self.computers):
                self.computers[room] = []
            
            if computer not in self.computers[room]:
                self.computers[room].append(computer)

    def get_rooms(self):
        self.fetch_computers()
        return list(self.computers)
    
    def get_computers(self, room: str):
        self.fetch_computers()
        if room not in self.computers:
            return []
        return self.computers[room]
    
    def get_details(self, poste: str):
        return self.con.query(f'SELECT * FROM registre WHERE poste="{poste}"')
    
    def insert(self, observation: str):
        observation = observation.replace('"',"'")
        poste: str = os.environ['COMPUTERNAME']
        eleve: str = os.getlogin()
        query = f'INSERT INTO registre VALUES("{poste}", NOW(), "{observation}", "{eleve}")'
        
        self.con.query(query, update = True)
    
    def get_last_details(self):
        poste = os.environ['COMPUTERNAME']
        query = f'SELECT observation FROM registre WHERE poste="{poste}" AND NOT(observation LIKE "RAS") ORDER BY horaire DESC LIMIT 1'
        result = self.con.query(query)
        
        if len(result) == 0 or len(result[0]) == 0:
            return 'RAS'
        
        return result[0][0][:-1]
