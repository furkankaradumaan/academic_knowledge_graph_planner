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
                self.conn = sqlite3.connect(self.file_name, check_same_thread=False)
                self.cursor = self.conn.cursor() # necessary to execute commands

        def __get_id(self, name, table):
                if self.conn is None:
                        self.create_connection()
                self.cursor.execute(f"SELECT id FROM {table} WHERE name=? LIMIT 1", (name, ))
                id = self.cursor.fetchone()
                if id:
                        return id[0]
                else:
                        raise ValueError(f"Error: {name} couldn't found in database")

        def __name_exists(self, name, table):
                if self.conn is None:
                        self.create_connection()
                self.cursor.execute(f"SELECT 1 FROM {table} WHERE name=? LIMIT 1", (name, ))
                result = self.cursor.fetchone()
                if result:
                        return True
                else:
                        return False
                
        def is_prerequisite(self, id_first, id_next):
                if self.conn is None:
                        self.create_connection()
                self.cursor.execute("SELECT 1 FROM prerequisites WHERE id_first=? AND id_next=? LIMIT 1", (id_first, id_next))
                result = self.cursor.fetchone()
                if result:
                        return True
                else:
                        return False

        def add_new_subject(self, subject_name):
                if self.conn is None:
                        self.create_connection()
                if self.__name_exists(subject_name, "subjects"):
                        raise ValueError("Error: This subject already exists")
                self.cursor.execute("INSERT INTO subjects (name) VALUES (?)", (subject_name, ))
                self.conn.commit()

        def add_new_topic(self, topic_name, main_topic_name=None, subject_name=None):
                if self.conn is None:
                        self.create_connection()

                if self.__name_exists(topic_name, "topics"):
                        raise ValueError("Error: This topic name is already exists")
                
                main_topic_id = self.__get_id(main_topic_name, "topics") if main_topic_name else None
                subject_id = self.__get_id(subject_name, "subjects") if subject_name else None

                self.cursor.execute("INSERT INTO topics (name, main_topic_id, subject_id) VALUES (?, ?, ?)",
                                    (topic_name, main_topic_id, subject_id))
                self.conn.commit()

        def add_new_prerequisite(self, name_first, name_next):
                if self.conn is None:
                        self.create_connection()
                
                id_first = self.__get_id(name_first, "topics")
                id_next = self.__get_id(name_next, "topics")

                if self.is_prerequisite(id_first, id_next):
                        raise ValueError("Error: Same prerequisition already exists")
                self.cursor.execute("INSERT INTO prerequisites (id_first, id_next) VALUES(?, ?)", (id_first, id_next))
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
                for id, name, _, _ in topics:
                        topic_dict[id] = Topic(id, name)
                
                for id, _, main_topic_id, subject_id in topics:
                        if main_topic_id is not None:
                                topic_dict[main_topic_id].add_subtopic(topic_dict[id])
                        elif subject_id is not None:
                                subject_dict[subject_id].add_topic(topic_dict[id])
                
                self.cursor.execute("SELECT * FROM prerequisites")
                prerequisites = self.cursor.fetchall()
                for first_topic_id, next_topic_id in prerequisites:
                        topic_dict[first_topic_id].add_next_topic(topic_dict[next_topic_id])
                
                return list(subject_dict.values()), list(topic_dict.values())