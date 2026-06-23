from model import *
from db_manager import DatabaseManager
import sqlite3

class SqliteManager(DatabaseManager):
        def __init__(self, file_name):
                self.file_name = file_name
                self.conn = None
                self.cursor = None
        
        def create_connection(self):
                if self.conn is not None:
                        return
                self.conn = sqlite3.connect(self.file_name)
                self.cursor = self.conn.cursor() # necessary to execute commands

        def add_new_subject(self, subject_name):
                if self.conn is None:
                        self.create_connection()
                self.cursor.execute("INSERT INTO subjects (name) VALUES (?)", (subject_name, ))
                self.conn.commit()

        def add_new_topic(self, topic_name, main_topic_id=None, subject_id=None):
                if self.conn is None:
                        self.create_connection()

                self.cursor.execute("INSERT INTO topics (name, main_topic_id, subject_id) VALUES (?, ?, ?)",
                                    (topic_name, main_topic_id, subject_id))
                self.conn.commit()

        def add_new_prerequisite(self, first_topic_id, next_topic_id):
                if self.conn is None:
                        self.create_connection()
                
                self.cursor.execute("INSERT INTO prerequisites (id_first, id_next) VALUES(?, ?)", (first_topic_id, next_topic_id))
                self.conn.commit()
        
        def get_object_lists(self):
                if self.conn is None:
                        self.create_connection()

                subject_dict = {}
                topic_dict = {}

                self.cursor.execute("SELECT * FROM subjects")
                subjects = self.cursor.fetchall()
                for id, name in subjects:
                        subject_dict[id] = Subject(id, name)
                
                self.cursor.execute("SELECT * FROM topics")
                topics = self.cursor.fetchall()
                for id, name, _, subject_id in topics:
                        topic_dict[id] = Topic(id, name)
                        subject_dict[subject_id].add_topic(topic_dict[id]) # link topic and its subject
                
                for id, _, main_topic_id, _ in topics:
                        if main_topic_id is not None:
                                topic_dict[main_topic_id].add_subtopic(topic_dict[id])
                
                self.cursor.execute("SELECT * FROM prerequisites")
                prerequisites = self.cursor.fetchall()
                for first_topic_id, next_topic_id in prerequisites:
                        topic_dict[first_topic_id].add_next_topic(topic_dict[next_topic_id])
                
                return list(subject_dict.values()), list(topic_dict.values())