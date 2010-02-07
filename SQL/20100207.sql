

/*
For anyone who was using a 0.9 version of Mingus prior to 0.9.7 release
you should run the below SQL statements to migrate your database if you
are using django-request.

Database: Postgres
*/

ALTER TABLE request_request
    ADD COLUMN referer_new varchar(255);

update request_request set referer_new = referer;

ALTER TABLE request_request
	DROP COLUMN referer;

ALTER TABLE request_request
	RENAME COLUMN referer_new to referer;
