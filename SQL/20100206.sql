

/*
For anyone who was using a 0.9 version of Mingus prior to 0.9.6 release
you should run the below SQL statements to migrate your database if you
are using django-request.

Database: Postgres
*/

ALTER TABLE request_request
    ADD COLUMN language_new varchar(255);

update request_request set language_new = language;

ALTER TABLE request_request
	DROP COLUMN language;

ALTER TABLE request_request
	RENAME COLUMN language_new to language;
