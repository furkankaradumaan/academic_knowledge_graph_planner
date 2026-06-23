from abc import ABC, abstractmethod

class DatabaseManager(ABC):
        @abstractmethod
        def create_connection(self):
                pass

        @abstractmethod
        def add_new_subject(self, subject_name):
                pass

        @abstractmethod
        def add_new_topic(self, topic_name, main_topic_id, subject_id):
                pass

        @abstractmethod
        def add_new_prerequisite(self, first_topic_id, next_topic_id):
                pass
