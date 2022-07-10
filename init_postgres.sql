CREATE DATABASE "appdb"
   WITH OWNER "postgres"
   ENCODING 'UTF8';

-- chose db
\c appdb;

-- trigger for updated_at column
CREATE OR REPLACE FUNCTION trigger_set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- create a toy customer table 
CREATE TABLE IF NOT EXISTS appdb.public.customer(
   id           SERIAL PRIMARY KEY NOT NULL,
   email        VARCHAR(50) NOT NULL,
   phone        VARCHAR(50),
   address      VARCHAR(50),
   name         VARCHAR(50) NOT NULL,
   status       VARCHAR(50) NOT NULL,
   created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   updated_at   TIMESTAMP,
   CONSTRAINT unique_customer_email UNIQUE (email)
);

-- set updated_at trigger for customer table
CREATE TRIGGER set_updated_at
BEFORE UPDATE ON customer
FOR EACH ROW
EXECUTE PROCEDURE trigger_set_updated_at();