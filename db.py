from peewee import *
import logging
import datetime

logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


db_file = "./database.db"
conn = SqliteDatabase(db_file, pragmas={
    'journal_mode': 'wal',
    'cache_size': -1024 * 64})


class BaseModel(Model):
    class Meta:
        database = conn


# History table
""" '''CREATE TABLE IF NOT EXISTS history (chat_id integer PRIMARY KEY, 
        message text NOT NULL, 
        message_author_id int,
        date text, 
        result_SEVERE_TOXICITY int, 
        result_THREAT int, 
        result_INSULT int, 
        result_PROFANITY int, 
        result_IDENTITY_ATTACK int, 
        result_TOXICITY int);'''
"""


class GlobalHistory(BaseModel):
    chat_id = IntegerField(index=True, help_text="Telegram Chat Id")
    message_text = TextField(help_text="Message text, that was tested")
    message_author_id = IntegerField(index=True, help_text="Telegram ID of the message author")
    message_author_name = TextField(help_text="Author name aka @username")
    timestamp = TimestampField(help_text="Timestamp of message", default=datetime.datetime.now)
    result_toxicity = IntegerField(help_text="TOXICITY score of this message")

    class Meta:
        table_name = 'GlobalHistory'


'''CREATE TABLE IF NOT EXISTS chats (chat_id integer PRIMARY KEY, 
        allowed_SEVERE_TOXICITY_level int, 
        allowed_THREAT_level int, 
        allowed_INSULT_level int, 
        allowed_PROFANITY_level int, 
        allowed_IDENTITY_ATTACK_level int, 
        allowed_TOXICITY_level int,
        warn_SEVERE_TOXICITY_level int, 
        warn_THREAT_level int, 
        warn_INSULT_level int, 
        warn_PROFANITY_level int, 
        warn_IDENTITY_ATTACK_level int, 
        warn_TOXICITY_level int,
        try_mode int,
        debug_mode int,
        admin_list text,
        immune_list text);'''

class Artist(BaseModel):
    artist_id = AutoField(column_name='ArtistId')
    name = TextField(column_name='Name', null=True)

    class Meta:
        table_name = 'Artist'



