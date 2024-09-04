create database account-service
drop table if exists accounts;
CREATE TABLE "accounts" (
  "account_id" serial PRIMARY KEY,
  "account_name" varchar,
  "username" varchar unique,
  "password" varchar,
  "email_address" varchar,
  "contact_number" varchar,
  "status_id" int,
  "create_date" timestamp,
  "last_update" timestamp
);
CREATE UNIQUE INDEX account_id_account_idx on accounts (account_id);
CREATE UNIQUE INDEX username_account_idx on accounts (username);

drop table if exists users;
CREATE TABLE "users" (
  "user_id" serial PRIMARY KEY,
  "account_id" bigint,
  "first_name" varchar,
  "last_name" varchar,
  "username" varchar unique,
  "password" varchar,
  "email_address" varchar,
  "contact_number" varchar,
  "user_type_id" int,
  "status_id" int,
  "create_date" timestamp,
  "last_update" timestamp
);
CREATE UNIQUE INDEX account_id_user_idx on users (account_id);
CREATE UNIQUE INDEX username_user_idx on users (username);

drop table if exists api_log;
CREATE TABLE "api_log" (
  "id" serial PRIMARY KEY,
  "api_method" varchar,
  "account_id" bigint,
  "request_url" varchar,
  "request_body" text,
  "response_code" int,
  "request_date" timestamp
);

drop table if exists access_controls;
CREATE TABLE "access_controls" (
  "control_id" serial PRIMARY KEY,
  "name" varchar,
  "description" varchar,
  "control_type_id" int,
  "control_level_id" varchar,
  "status_id" int,
  "create_date" timestamp,
  "last_update" timestamp
);
CREATE UNIQUE INDEX control_id_access_idx on access_controls (control_id);

drop table if exists user_access_controls;
CREATE TABLE "user_access_controls" (
  "id" serial PRIMARY KEY,
  "control_id" bigint,
  "user_id" bigint,
  "account_id" bigint,
  "status_id" int,
  "create_date" timestamp,
  "last_update" timestamp
);
CREATE UNIQUE INDEX control_id_user_access_idx on user_access_controls (control_id);
CREATE UNIQUE INDEX user_id_user_access_idx on user_access_controls (user_id);


