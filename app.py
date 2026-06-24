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

@app.route("/api/subject", methods=["POST"])
def add_new_subject():
        data = request.get_json()
        subject_name = data.get("name")
        if subject_name is None or len(subject_name) == 0:
                return jsonify({"error": "You need to enter a subject name"}), 500

        try:
                db.add_new_subject(subject_name)
                return jsonify({"message": f"'{subject_name}' added successfully"}), 201
        except ValueError as e:
                return jsonify({"error": str(e)}), 500

@app.route("/api/topic", methods=["POST"])
def add_new_topic():
        data = request.get_json()
        name = data.get("name")
        subject_name = data.get("subject_name")
        main_top_name = data.get("main_topic_name")

        if name is None or len(name) == 0:
                return jsonify({"error": "You need to enter a topic name"}), 500

        if subject_name and main_topic_name:
                return jsonify({"error": "You cannot enter both main topic name and subject name"}), 500
        elif subject_name:
                main_topic_name = None
        elif main_topic_name:
                subject_name = None
        else:
                return jsonify({"error": "You need to enter a main topic name or a subject name"}), 500

        try:
                db.add_new_topic(name, main_top_name, subject_name)
                return jsonify({"message": f"'{name}' added successfully"}), 201
        except ValueError as e:
                return jsonify({"error": str(e)}), 500
        
@app.route("/api/prerequisite", methods=["POST"])
def add_new_prerequisite():
        data = request.get_json()

        name_first = data.get("name_first")
        name_next = data.get("name_next")

        if name_first is None or name_next is None:
                return jsonify({"error": "You need to enter first topic name and next topic name"}), 500

        try:
                db.add_new_prerequisite(name_first, name_next)
                return jsonify({"message": "Prerequisite added successfully"}), 201
        except ValueError as e:
                return jsonify({"error": str(e)}), 500
        
if __name__ == "__main__":
        app.run(debug=True)
