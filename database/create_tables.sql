-- =====================================================================
-- PaletteVault - database schema
-- PostgreSQL 18.6
-- Creates the four tables from the ERD (Submission 2) with their
-- primary keys, foreign keys (relationships) and field constraints.
-- Safe to re-run: existing tables are dropped first.
-- =====================================================================

DROP TABLE IF EXISTS usage_logs CASCADE;
DROP TABLE IF EXISTS wishlist_items CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- ---------------------------------------------------------------------
-- users: one row per registered PaletteVault user
-- ---------------------------------------------------------------------
CREATE TABLE users (
    user_id        SERIAL        PRIMARY KEY,
    username       VARCHAR(50)   NOT NULL UNIQUE,
    email          VARCHAR(120)  NOT NULL UNIQUE,
    password_hash  VARCHAR(255)  NOT NULL,
    created_at     TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ---------------------------------------------------------------------
-- products: makeup items in a user's vault
-- Relationship: one user OWNS many products (1 : 0..*)
-- ---------------------------------------------------------------------
CREATE TABLE products (
    product_id     SERIAL        PRIMARY KEY,
    user_id        INTEGER       NOT NULL
                   REFERENCES users (user_id) ON DELETE CASCADE,
    brand          VARCHAR(60)   NOT NULL,
    product_name   VARCHAR(100)  NOT NULL,
    shade          VARCHAR(50),
    category       VARCHAR(30)   NOT NULL
                   CHECK (category IN ('Face', 'Eyes', 'Lips', 'Cheeks', 'Brows')),
    barcode        VARCHAR(13)
                   CHECK (barcode ~ '^[0-9]{8,13}$'),
    opened_date    DATE          NOT NULL,
    pao_months     INTEGER       NOT NULL
                   CHECK (pao_months BETWEEN 1 AND 60),
    expiry_date    DATE          NOT NULL,
    pan_progress   INTEGER       NOT NULL DEFAULT 0
                   CHECK (pan_progress BETWEEN 0 AND 100),
    status         VARCHAR(20)   NOT NULL DEFAULT 'Fresh'
                   CHECK (status IN ('Fresh', 'Expiring Soon', 'Expired')),
    CHECK (expiry_date > opened_date)
);

-- ---------------------------------------------------------------------
-- usage_logs: dated pan-progress history for a product
-- Relationship: one product is LOGGED IN many usage logs (1 : 0..*)
-- ---------------------------------------------------------------------
CREATE TABLE usage_logs (
    log_id         SERIAL        PRIMARY KEY,
    product_id     INTEGER       NOT NULL
                   REFERENCES products (product_id) ON DELETE CASCADE,
    log_date       DATE          NOT NULL DEFAULT CURRENT_DATE,
    pan_progress   INTEGER       NOT NULL
                   CHECK (pan_progress BETWEEN 0 AND 100),
    notes          VARCHAR(255)
);

-- ---------------------------------------------------------------------
-- wishlist_items: products a user WANTS to buy
-- Relationship: one user wants many wishlist items (1 : 0..*)
-- ---------------------------------------------------------------------
CREATE TABLE wishlist_items (
    wishlist_id    SERIAL        PRIMARY KEY,
    user_id        INTEGER       NOT NULL
                   REFERENCES users (user_id) ON DELETE CASCADE,
    brand          VARCHAR(60)   NOT NULL,
    product_name   VARCHAR(100)  NOT NULL,
    shade          VARCHAR(50),
    category       VARCHAR(30)   NOT NULL
                   CHECK (category IN ('Face', 'Eyes', 'Lips', 'Cheeks', 'Brows')),
    added_date     DATE          NOT NULL DEFAULT CURRENT_DATE
);

-- Indexes on the foreign keys and barcode (used by the barcode lookup)
CREATE INDEX idx_products_user_id   ON products (user_id);
CREATE INDEX idx_products_barcode   ON products (barcode);
CREATE INDEX idx_usage_logs_product ON usage_logs (product_id);
CREATE INDEX idx_wishlist_user_id   ON wishlist_items (user_id);
