/*
If you are upgrading from Mingus 0.8 version or earlier this is important.

Changes to django-basic-apps added two field to the basic.blog.models.Settings model:
active_editor and excerpt_length. You can migrate something like this:
*/
 
ALTER TABLE blog_settings ADD COLUMN "active_editor" integer NOT NULL DEFAULT 1;
ALTER TABLE blog_settings ADD COLUMN "excerpt_length" integer NOT NULL DEFAULT 500;

