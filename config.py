
TOKEN = "767660137:AAE6WBNx8BCd0uCKBl0tOGo-6IxvYPMtQ_k"

view_sport = ['Футбол']
view_commands = ['/help - список команд', '/list - список подписок', '/add - добавить подписку',
                 '/remove - удалить подписку']

user_dict = {}

link_db = "dbname='Bot' user='postgres' password='0122' host='localhost' port='5432'"


class User:
    def __init__(self, sport):
        self.sport = sport
        self.chat_id = None
        self.gg = None


request_to_bd = """with
                    t1 as (
                        select 
                        football.id_game,
                        coeff_home,
                        score,
                        play_time
                        from football
                        join football_live on football.id_game=football_live.id_game 
                        where coeff_home<1.5 and score in ('0 - 0','0 - 1') and play_time in ('24 ','60 ')
                    ),
                    t2 as (
                        select 
                        football.id_game,
                        coeff_home,
                        score,
                        play_time
                        from football
                        join football_live on football.id_game=football_live.id_game 
                        where coeff_guest<1.5 and score in ('0 - 0','1 - 0') and play_time in ('24 ','60 ')
                    ),
                    t3 as (
                        select * from t1
                        union
                        select * from t2
                    )
                    select id_game,play_time from t3
                    """
