ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS users_pkey CASCADE;

DROP TABLE IF EXISTS public.users;
DROP SEQUENCE IF EXISTS public.users_id_seq;

CREATE TABLE users (
    id serial PRIMARY KEY,
    username varchar UNIQUE,
    password varchar
)
