CREATE TABLE ref_roles (
    id SERIAL PRIMARY KEY,
    role VARCHAR(255) NOT NULL
);

CREATE TABLE tbl_users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role_id INT NOT NULL,
    FOREIGN KEY (role_id) REFERENCES ref_roles(id)
);

CREATE TABLE tbl_events (
    id SERIAL PRIMARY KEY,
    owner INT NOT NULL,
    title_short VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    FOREIGN KEY (owner) REFERENCES tbl_users(id)
);

CREATE TABLE tbl_comments (
    id SERIAL PRIMARY KEY,
    event_id INT NOT NULL,
    owner INT NOT NULL,
    comment VARCHAR(255) NOT NULL,
    FOREIGN KEY (owner) REFERENCES tbl_users(id),
    FOREIGN KEY (event_id) REFERENCES tbl_events(id)
);

CREATE TABLE tbl_event_subscriptions (
    user_id INT NOT NULL,
    event_id INT NOT NULL,
    PRIMARY KEY (user_id, event_id),
    FOREIGN KEY (user_id) REFERENCES tbl_users(id),
    FOREIGN KEY (event_id) REFERENCES tbl_events(id)
);

CREATE VIEW event_subscriptions AS
SELECT
    u.id AS subscription_id,
    es.event_id,
    u.username AS subscribed_username
FROM
    tbl_event_subscriptions es
JOIN
    tbl_users u ON es.user_id = u.id
ORDER BY
    es.event_id, u.username;

CREATE VIEW event_owner_view AS
SELECT
    e.id AS event_id,
    u.id AS user_id,
    e.title_short,
    e.title,
    e.description,
    u.username AS owner_username
FROM
    tbl_events e
JOIN
    tbl_users u
ON
    e.owner = u.id;

CREATE VIEW comment_owner_view AS
SELECT
    c.id AS comment_id,
    c.event_id,
    e.title_short AS event_title,
    c.comment,
    u.username AS owner_username
FROM
    tbl_comments c
JOIN
    tbl_users u
ON
    c.owner = u.id
JOIN
    tbl_events e
ON
    c.event_id = e.id;

CREATE VIEW event_with_comments_view AS
SELECT
    e.id AS event_id,
    e.title_short,
    e.title,
    e.description,
    u.username AS event_owner_username,
    c.id AS comment_id,
    c.comment,
    cu.username AS comment_owner_username
FROM
    tbl_events e
JOIN
    tbl_users u
ON
    e.owner = u.id
LEFT JOIN
    tbl_comments c
ON
    e.id = c.event_id
LEFT JOIN
    tbl_users cu
ON
    c.owner = cu.id;

INSERT INTO ref_roles (id, role) VALUES
(0, 'Guest'),
(1, 'User'),
(2, 'Event-Creator'),
(3, 'Admin');

INSERT INTO tbl_users (username, password, role_id) VALUES
('admin','scrypt:32768:8:1$GL6evrNet9sxTp5Z$34f9b39dcd9925c1e44c802bd2aabda69d5b53fc333a382a9a89a6288b34e71a479cf8ddcaabd252d6ce9d355e08c2e52337d50b3987d3006f5f56a25f7184e6',3),
('anne','scrypt:32768:8:1$fQxPATt0kdWA1Dk5$37dac204e7ad73cd4c4235bc0105800c6fbcc91752c404b4aeed1ec6828099b8a1a8fea527d3121fea0b55f273cbe36509fd703eca0ac6c97bbb26cdb04d3f2b',2),
('magda','scrypt:32768:8:1$3rNfzRdqDCi30vL9$f3fef3a8cb004463e479a2b760068738daad852815ecbf5fe75b88e8f511340496a3142a1a12eb87824eb82fe437e106710eb885ba2c70a9cdc4fb5eeb810307',3),
('user','scrypt:32768:8:1$pO5ia7ZEv3ffbJAc$ba952a6121b1f2bc45c2eae40ccd979cdd61323e9fbfaaab091f770b96d825e5c0d881a3e5967c0a74a140213a6d32432f3a6afe0a7dcea973399d915f58f308',1),
('user1','scrypt:32768:8:1$pO5ia7ZEv3ffbJAc$ba952a6121b1f2bc45c2eae40ccd979cdd61323e9fbfaaab091f770b96d825e5c0d881a3e5967c0a74a140213a6d32432f3a6afe0a7dcea973399d915f58f308',1),
('user2','scrypt:32768:8:1$pO5ia7ZEv3ffbJAc$ba952a6121b1f2bc45c2eae40ccd979cdd61323e9fbfaaab091f770b96d825e5c0d881a3e5967c0a74a140213a6d32432f3a6afe0a7dcea973399d915f58f308',1),
('user3','scrypt:32768:8:1$pO5ia7ZEv3ffbJAc$ba952a6121b1f2bc45c2eae40ccd979cdd61323e9fbfaaab091f770b96d825e5c0d881a3e5967c0a74a140213a6d32432f3a6afe0a7dcea973399d915f58f308',1)
;

INSERT INTO tbl_events (owner, title_short, title, description) VALUES
(1, 'Intro', '🎉 Präsentation: Event-Baukasten',
'<div style="padding: 2em; background: #f0f8ff; border-radius: 16px; margin-bottom: 2em;">
  <h2 style="font-size: 2em; color: #004080;">🎉 Präsentation: Event-Baukasten</h2>
  <p>Heute schauen wir uns folgende Themen an:</p>
  <ul style="line-height: 1.6; font-size: 1.1em;">
    <li>📌 <strong>Abgrenzung</strong> – Was nicht umgesetzt wurde & warum</li>
    <li>🚀 <strong>Zukunft</strong> – Nächste Schritte und Umbau des Projekts</li>
    <li>🌐 <strong>Showcase</strong> – Die Event-Webseite live erleben</li>
    <li>🧠 <strong>Code Deep Dive</strong> – Ein Blick unter die Haube</li>
  </ul>
</div>'),

(1, 'Umsetzung', '🚧 Projektfortschritt',
'<div style="padding: 2em; background: #e6ffe6; border-radius: 16px; margin-bottom: 2em;">
  <h2 style="font-size: 2em; color: #00733e;">🚧 Projektfortschritt</h2>
  <p>Der Event-Baukasten wurde erfolgreich als eigenständiges Modul entwickelt. Highlights:</p>
  <ul style="line-height: 1.6;">
    <li>🔧 Visueller Editor mit Toolbar, Bausteinen & Live-Vorschau</li>
    <li>🧱 Bausteine können einfach per Drag & Drop hinzugefügt werden</li>
    <li>🕒 Undo/Redo durch einfache Änderungshistorie</li>
    <li>📦 Wird später per Build in die Hauptseite integriert</li>
  </ul>
  <p style="margin-top: 1em;">Der Editor ist unabhängig vom Backend und nutzt eine bestehende API zum Speichern.</p>
</div>'),

(1, 'Abgrenzung', '⚠️ Abgrenzung',
'<div style="padding: 2em; background: #fffbe6; border-radius: 16px; margin-bottom: 2em;">
  <h2 style="font-size: 2em; color: #aa8800;">⚠️ Abgrenzung</h2>
  <ul style="line-height: 1.6;">
    <li>❌ <strong>Kein Backend-Modul</strong> – Die nötige Abstraktion für Formularstrukturen hätte eine neue Klasse & DB-Anpassung erfordert</li>
    <li>🧪 <strong>Keine Unit/Integration Tests</strong> – Das Projekt ist aktuell ein JS-Frontend, ohne direkte Anbindung an den Python-Teil</li>
    <li>🖥️ <strong>Keine GUI-Tests</strong> – Zu aufwändig für das aktuelle Zeitfenster</li>
  </ul>
  <p>Die Fokussierung lag auf der Bedienbarkeit & UX des Editors.</p>
</div>'),

(1, 'Zukunft', '🔮 Zukunft & Weiterentwicklung',
'<div style="padding: 2em; background: #f5e6ff; border-radius: 16px;">
  <h2 style="font-size: 2em; color: #800080;">🔮 Zukunft & Weiterentwicklung</h2>
  <ul style="line-height: 1.6;">
    <li>🧭 Umbau zu einem eigenständigen JS-Projekt mit NPM-Setup</li>
    <li>🧪 Einbau von Tests (Unit, Integration) über moderne JS-Testframeworks</li>
    <li>📦 Integration via Build-Prozess in die Hauptseite</li>
    <li>🔗 Eventuelle Erweiterung für dynamische Daten aus dem Backend</li>
  </ul>
  <p style="margin-top: 1em;">Ziel: Der Baukasten wird zu einem wartbaren, testbaren und modularen Bestandteil der Plattform.</p>
</div>');


-- Witzige und thematisch passende Kommentare für Präsentations-Events
INSERT INTO tbl_comments (event_id, owner, comment) VALUES
-- Event 1: Was wird heute passieren?
(1, 4, 'Ich bin nur wegen dem Deep Dive hier. Taucherbrille sitzt! 🏊‍♂️💻'),
(1, 5, 'Wenn heute keine Roadmap kommt, bau ich mir selbst eine aus Post-its.'),
(1, 6, 'Showcase? Mehr wie WOWcase! Zeigt her euren Code-Zauber ✨'),
(1, 7, 'Ich hab meine “Abgrenzungs-Mütze” aufgesetzt. Bereit zum Grenzen ziehen!'),

-- Event 2: Was ist bisher passiert?
(2, 5, 'Ah, der Klassiker: 1 Datei, 1000 Funktionen. Das nenn ich legacy-friendly!'),
(2, 6, 'Ich fühle mich wie Indiana Jones im alten Code-Dschungel. 🏺👨‍💻'),
(2, 7, '“Was bisher geschah” ist mein Lieblingsgenre. Gleich nach “Bugfix RomComs”.'),
(2, 4, 'Das Projekt ist wie ein Sandwich: chaotisch begonnen, aber lecker geworden.'),

-- Event 3: Was nicht passiert ist
(3, 6, 'Unit Tests? Sorry, die wurden von der Deadline überfahren. 🧪🚗💥'),
(3, 7, '“Form-Abstraktion im Backend” klingt wie ein Bossfight, den wir geskippt haben.'),
(3, 5, 'Integrationstests sind wie Socken – immer das Erste, was fehlt. 🧦'),
(3, 4, 'GUI-Tests wurden archiviert im Ordner “vielleicht irgendwann™”.'),

-- Event 4: Wie es weitergeht
(4, 4, 'Neues Projekt, neue Hoffnung! Möge NPM mit dir sein. 🚀'),
(4, 5, 'Von Flask zu JS? Das ist wie von Fahrrad auf Rakete umsteigen.'),
(4, 6, 'Endlich Platz für Tests und Struktur. RIP monolithische Chaos-Datei.'),
(4, 7, 'Ich erwarte mindestens 3 npm-Skripte und 2 Build Errors zum Start!');

