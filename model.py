class Subject:
        def __init__(self, id, name):
                self.id = id
                self.name = name

                self.topics = []
        def add_topic(self, topic):
                self.topics.append(topic)

class Topic:
        def __init__(self, id, name, difficulty_level):
                self.id = id
                self.name = name
                self.difficulty_level = difficulty_level
        
                self.next_topics = [] # topics which this topic is a prerequisite for
                self.subtopics = []

        def add_next_topic(self, topic):
                self.next_topics.append(topic)
        
        def add_subtopic(self, topic):
                self.subtopics.append(topic)

        def __str__(self):
                return self.name