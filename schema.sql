CREATE TABLE user_table (
	user_id SERIAL PRIMARY KEY,
    username TEXT,
	password TEXT,
	"session" varchar(40)
	);

CREATE TABLE post_table (
	post_id SERIAL PRIMARY KEY,
	post TEXT,
	posted TIMESTAMP,
	user_id INTEGER REFERENCES "user_table"
	);

CREATE TABLE access_table (
	post_id INTEGER REFERENCES "post_table",
	user_id INTEGER REFERENCES "user_table"
	);

CREATE FUNCTION get_posts(fromuser TEXT, asuser TEXT)
RETURNS SETOF text
AS $$
	WITH help AS (SELECT user_id FROM user_table WHERE asuser = username)
	SELECT format(' (%s)  (%s) ', post, posted)
	FROM help, post_table INNER JOIN user_table USING (user_id) INNER JOIN access_table USING (post_id)
	WHERE user_table.username = fromuser AND access_table.user_id = help.user_id;
$$
LANGUAGE sql;

CREATE FUNCTION get_friends(fromuser TEXT)
RETURNS SETOF text
AS $$
	WITH help AS (SELECT user_id FROM user_table WHERE fromuser = username)
	SELECT DISTINCT format(' (%s)  (%s) ', post_table.user_id, username)
	FROM help, post_table INNER JOIN user_table USING (user_id) INNER JOIN access_table USING (post_id)
	WHERE access_table.user_id = help.user_id
$$
LANGUAGE sql;
