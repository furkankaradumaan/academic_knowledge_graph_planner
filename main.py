from model import *
from sqlite_manager import SqliteManager

def topological_sort(topics):
        WHITE = 0
        GRAY = 1
        BLACK = 2

        color = { topic : WHITE for topic in topics }
        ordering = []

        def dfs(topic, visited):
                if color[topic] == GRAY:
                        raise ValueError("Error: Cycle detected")
                
                color[topic] = GRAY

                for next_topic in topic.next_topics:
                        if color[next_topic] != BLACK:
                                dfs(next_topic, visited)
                
                for subtopic in topic.subtopics:
                        if color[subtopic] != BLACK:
                                dfs(subtopic, visited)

                
                if len(topic.subtopics) == 0:
                        visited.append(topic)
                color[topic] = BLACK

        for topic in topics:
                if color[topic] != WHITE: # skip topics that has subtopics
                        continue
                visited = []
                dfs(topic, visited)
                ordering += visited
        
        ordering.reverse()
        return ordering

def main():
        manager = SqliteManager("database.sqlite")

        subject_list, topic_list = manager.get_object_lists()

        ordering = topological_sort(topic_list)
        print(f"Suggested topic order for you:\n{' -> '.join(map(str, ordering))}\n")          

main()