-- Database generated with pgModeler (PostgreSQL Database Modeler).
-- pgModeler version: 1.1.4
-- PostgreSQL version: 16.0
-- Project Site: pgmodeler.io
-- Model Author: ---

-- Database creation must be performed outside a multi lined SQL file. 
-- These commands were put in this file only as a convenience.
-- 
-- object: "accident-manager-db" | type: DATABASE --
-- DROP DATABASE IF EXISTS "accident-manager-db";
-- CREATE DATABASE "accident-manager-db";
-- ddl-end --


-- object: postgis | type: EXTENSION --
-- DROP EXTENSION IF EXISTS postgis CASCADE;
CREATE EXTENSION postgis
WITH SCHEMA public;
-- ddl-end --

-- object: public.user_role | type: TYPE --
-- DROP TYPE IF EXISTS public.user_role CASCADE;
CREATE TYPE public.user_role AS
ENUM ('admin','user');
-- ddl-end --

-- object: public.accident_status | type: TYPE --
-- DROP TYPE IF EXISTS public.accident_status CASCADE;
CREATE TYPE public.accident_status AS
ENUM ('pending','in_progress','resolved');
-- ddl-end --

-- object: public.users | type: TABLE --
-- DROP TABLE IF EXISTS public.users CASCADE;
CREATE TABLE public.users (
	user_id uuid NOT NULL DEFAULT gen_random_uuid(),
	email varchar NOT NULL,
	password_hash varchar NOT NULL,
	role public.user_role DEFAULT 'user',
	is_active boolean DEFAULT true,
	created_at timestamptz DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT users_pk PRIMARY KEY (user_id),
	CONSTRAINT email_uq UNIQUE (email)
);
-- ddl-end --

-- object: public.accidents | type: TABLE --
-- DROP TABLE IF EXISTS public.accidents CASCADE;
CREATE TABLE public.accidents (
	accident_id uuid NOT NULL DEFAULT gen_random_uuid(),
	reporter_id uuid NOT NULL,
	title varchar NOT NULL,
	description text,
	status public.accident_status DEFAULT 'pending',
	is_deleted boolean DEFAULT false,
	location geometry(POINT, 4326) NOT NULL,
	created_at timestamptz DEFAULT CURRENT_TIMESTAMP,
	updated_at timestamptz DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT accidents_pk PRIMARY KEY (accident_id)
);
-- ddl-end --

-- object: public.comments | type: TABLE --
-- DROP TABLE IF EXISTS public.comments CASCADE;
CREATE TABLE public.comments (
	comment_id uuid NOT NULL DEFAULT gen_random_uuid(),
	author_id uuid NOT NULL,
	accident_id uuid NOT NULL,
	content text NOT NULL,
	is_deleted boolean DEFAULT false,
	created_at timestamptz DEFAULT CURRENT_TIMESTAMP,
	updated_at timestamptz DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT comments_pk PRIMARY KEY (comment_id)
);
-- ddl-end --

-- object: accident_location_idx | type: INDEX --
-- DROP INDEX IF EXISTS public.accident_location_idx CASCADE;
CREATE INDEX accident_location_idx ON public.accidents
USING gist
(
	location
);
-- ddl-end --

-- object: reporter_id_fk | type: CONSTRAINT --
-- ALTER TABLE public.accidents DROP CONSTRAINT IF EXISTS reporter_id_fk CASCADE;
ALTER TABLE public.accidents ADD CONSTRAINT reporter_id_fk FOREIGN KEY (reporter_id)
REFERENCES public.users (user_id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: author_id_fk | type: CONSTRAINT --
-- ALTER TABLE public.comments DROP CONSTRAINT IF EXISTS author_id_fk CASCADE;
ALTER TABLE public.comments ADD CONSTRAINT author_id_fk FOREIGN KEY (author_id)
REFERENCES public.users (user_id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: accident_id_fk | type: CONSTRAINT --
-- ALTER TABLE public.comments DROP CONSTRAINT IF EXISTS accident_id_fk CASCADE;
ALTER TABLE public.comments ADD CONSTRAINT accident_id_fk FOREIGN KEY (accident_id)
REFERENCES public.accidents (accident_id) MATCH SIMPLE
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --


