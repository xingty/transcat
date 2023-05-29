DROP TABLE IF EXISTS translate_history;
DROP TABLE IF EXISTS service_usage;

CREATE TABLE "translate_history" (
	"id" integer,
	"sid" varchar NOT NULL DEFAULT NULL,
	"src" varchar NOT NULL DEFAULT '',
	"dst" varchar NOT NULL,
	"source_text" text NOT NULL,
	"target_text" text NOT NULL,
	"hash_id" varchar NOT NULL,
	"engine" varchar NOT NULL,
	"text_length" integer NOT NULL,
	"create_time" datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (id)
);

CREATE INDEX idx_hash_id ON translate_history (hash_id);
CREATE INDEX idx_create_time ON translate_history (create_time);

CREATE TABLE "service_usage" (
	"id" integer,
	"service_id" varchar NOT NULL,
	"name" varchar NOT NULL,
	"engine" varchar NOT NULL,
	"usage" bigint DEFAULT '0',
	"month_key" varchar NOT NULL,
	"create_time" datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (id)
);

CREATE UNIQUE INDEX uk_service_id ON service_usage (service_id);
CREATE INDEX idx_screate_time ON service_usage (create_time);