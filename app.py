from flask import Flask, render_template, jsonify, request
from sqlite_manager import SqliteManager
from algorithm import topological_sort

app = Flask(__name__)
db = SqliteManager("database.sqlite")

@app.route("/")
def index():
        return render_template("index.html")


@app.route("/api/graph", methods=["GET"])
def get_graph_data():
        """
        Send the graph data in the format which the Graph visualization
        library will understand
        """

        subjects, topics = db.get_object_lists()
        elements = []

        for sub in subjects:
                elements.append({
                        "data": {"id": f"sub_{sub.id}", "label": sub.name, "type": "SUBJECT"}
                })

        for top in topics:
                elements.append({
                        "data": {"id": f"top_{top.id}", "label": top.name, "type": "TOPIC"}
                })

        # lines between subjects and topics
        for sub in subjects:
                for top in sub.topics:
                        elements.append({
                                "data": {
                                        "id": f"edge_sub_{sub.id}_{top.id}",
                                        "source": f"sub_{sub.id}",
                                        "target": f"top_{top.id}",
                                        "label": "INCLUDES"
                                }
                        })

        # lines between topics and subtopics
        for top in topics:
                for sub_top in top.subtopics:
                        elements.append({
                                "data": {
                                        "id": f"edge_subtop_{top.id}_{sub_top.id}",
                                        "source": f"top_{top.id}",
                                        "target": f"top_{sub_top.id}",
                                        "label": "SUBTOPIC"
                                }
                        })

        # add prerequisites as lines (edges)
        for top in topics:
                for next_top in top.next_topics:
                        elements.append({
                                "data": {
                                        "id": f"edge_{top.id}_{next_top.id}",
                                        "source": f"top_{top.id}",
                                        "target": f"top_{next_top.id}",
                                        "label": "PREREQUISITE"
                                }
                        })
        
        return jsonify(elements), 200

@app.route("/api/sort", methods=["GET"])
def get_study_order():
        """
                Use the topological sort algorithm to obtain a list of subjects to study.
        """
        _, topics = db.get_object_lists()

        topics_suggessted = topological_sort(topics)
        topic_names = [topic.name for topic in topics_suggessted]
        
        return jsonify({"order": topic_names}), 200

if __name__ == "__main__":
        app.run(debug=True)