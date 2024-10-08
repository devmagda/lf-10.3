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

CREATE TABLE tbl_event_subscriptions (
    user_id INT NOT NULL,
    event_id INT NOT NULL,
    PRIMARY KEY (user_id, event_id),
    FOREIGN KEY (user_id) REFERENCES tbl_users(id),
    FOREIGN KEY (event_id) REFERENCES tbl_events(id)
);

-- Insert roles into ref_roles
INSERT INTO ref_roles (id, role) VALUES
(0, 'Guest'),
(1, 'User'),
(2, 'Event-Creator'),
(3, 'Admin');

-- Insert users into tbl_users with the correct role IDs
INSERT INTO tbl_users (username, password, role_id) VALUES
('admin','scrypt:32768:8:1$GL6evrNet9sxTp5Z$34f9b39dcd9925c1e44c802bd2aabda69d5b53fc333a382a9a89a6288b34e71a479cf8ddcaabd252d6ce9d355e08c2e52337d50b3987d3006f5f56a25f7184e6',3),
('anne','scrypt:32768:8:1$fQxPATt0kdWA1Dk5$37dac204e7ad73cd4c4235bc0105800c6fbcc91752c404b4aeed1ec6828099b8a1a8fea527d3121fea0b55f273cbe36509fd703eca0ac6c97bbb26cdb04d3f2b',2),
('magda','scrypt:32768:8:1$3rNfzRdqDCi30vL9$f3fef3a8cb004463e479a2b760068738daad852815ecbf5fe75b88e8f511340496a3142a1a12eb87824eb82fe437e106710eb885ba2c70a9cdc4fb5eeb810307',3),
('user','scrypt:32768:8:1$pO5ia7ZEv3ffbJAc$ba952a6121b1f2bc45c2eae40ccd979cdd61323e9fbfaaab091f770b96d825e5c0d881a3e5967c0a74a140213a6d32432f3a6afe0a7dcea973399d915f58f308',1),
('user1','scrypt:32768:8:1$pO5ia7ZEv3ffbJAc$ba952a6121b1f2bc45c2eae40ccd979cdd61323e9fbfaaab091f770b96d825e5c0d881a3e5967c0a74a140213a6d32432f3a6afe0a7dcea973399d915f58f308',1),
('user2','scrypt:32768:8:1$pO5ia7ZEv3ffbJAc$ba952a6121b1f2bc45c2eae40ccd979cdd61323e9fbfaaab091f770b96d825e5c0d881a3e5967c0a74a140213a6d32432f3a6afe0a7dcea973399d915f58f308',1),
('user3','scrypt:32768:8:1$pO5ia7ZEv3ffbJAc$ba952a6121b1f2bc45c2eae40ccd979cdd61323e9fbfaaab091f770b96d825e5c0d881a3e5967c0a74a140213a6d32432f3a6afe0a7dcea973399d915f58f308',1)
;


-- Insert detailed events into tbl_events
INSERT INTO tbl_events (owner, title_short, title, description) VALUES
-- Event from the creator user
(1, 'Young Clean-Up', 'Urban Clean-Up for Youth',
'Join us for an exciting Urban Clean-Up event specifically designed for young people in our city. This initiative aims to bring together teenagers and young adults to tackle litter in key areas. Not only will you help beautify the city, but you will also have the chance to meet new friends, learn about environmental sustainability, and contribute to a cleaner, greener urban space. This event includes educational workshops on waste management and recycling, making it both fun and informative. Refreshments and cleanup supplies will be provided. Come and be part of a positive change in our community!'),

(1, 'City Tidy', 'Community Cleaning Project',
'Get involved in our City Tidy project, a comprehensive cleaning effort targeting multiple city zones. This event is designed for all age groups and focuses on fostering a strong sense of community. We encourage families, groups, and individuals to participate in various cleaning activities such as litter pick-ups, graffiti removal, and park beautification. The day will include activities for kids, informational booths on environmental stewardship, and a community lunch to celebrate our efforts. Join us to make a significant impact on our city’s cleanliness and enjoy a day of teamwork and community spirit.'),

(1, 'Grandma''s Green Initiative', 'Generations Clean-Up',
'Grandma''s Green Initiative invites people of all ages to participate in an intergenerational clean-up event aimed at bridging gaps between generations. This unique event encourages families and community members of all ages to come together for a day of cleaning and environmental awareness. Activities include neighborhood clean-ups, educational sessions on sustainable living, and interactive games for children and seniors. The event will also feature a storytelling session with our community’s beloved elders sharing their experiences and wisdom. Enjoy a day filled with cooperation, learning, and making a positive impact on our environment.')
;
