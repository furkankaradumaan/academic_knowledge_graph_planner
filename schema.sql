CREATE TABLE subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
);

CREATE TABLE topics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        main_topic_id INTEGER,
        subject_id INTEGER,
        FOREIGN KEY (main_topic_id) REFERENCES topics(id) ON DELETE CASCADE,
        FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
);

CREATE TABLE prerequisites (
        id_first INTEGER,
        id_next INTEGER,
        FOREIGN KEY (id_first) REFERENCES topics(id) ON DELETE CASCADE,
        FOREIGN KEY (id_next) REFERENCES topics(id) ON DELETE CASCADE
);
