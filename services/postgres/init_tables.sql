CREATE TABLE groups (
    id varchar(40) PRIMARY KEY,
    name varchar(40),
    description varchar(256),
    group_size integer,
    week_gap integer,
    week_day varchar(40),
    time_of_day time
);

CREATE TABLE user_subscriptions (
    id integer PRIMARY KEY,
    user_id varchar(256),
    group_id integer
);