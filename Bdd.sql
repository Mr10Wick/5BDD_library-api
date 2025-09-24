SET SERVEROUTPUT ON
WHENEVER SQLERROR CONTINUE

-- -----------------------------
-- Drop TRIGGERS (if exist)
-- -----------------------------
BEGIN EXECUTE IMMEDIATE 'DROP TRIGGER users_bi'; EXCEPTION WHEN OTHERS THEN IF SQLCODE != -4080 THEN RAISE; END IF; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TRIGGER books_bi'; EXCEPTION WHEN OTHERS THEN IF SQLCODE != -4080 THEN RAISE; END IF; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TRIGGER loans_bi'; EXCEPTION WHEN OTHERS THEN IF SQLCODE != -4080 THEN RAISE; END IF; END;
/

-- -----------------------------
-- Drop SEQUENCES (if exist)
-- -----------------------------
BEGIN EXECUTE IMMEDIATE 'DROP SEQUENCE users_seq'; EXCEPTION WHEN OTHERS THEN IF SQLCODE != -2289 THEN RAISE; END IF; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP SEQUENCE books_seq'; EXCEPTION WHEN OTHERS THEN IF SQLCODE != -2289 THEN RAISE; END IF; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP SEQUENCE loans_seq'; EXCEPTION WHEN OTHERS THEN IF SQLCODE != -2289 THEN RAISE; END IF; END;
/

-- -----------------------------
-- Drop TABLES (if exist)
-- -----------------------------
BEGIN EXECUTE IMMEDIATE 'DROP TABLE loans CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN IF SQLCODE != -942 THEN RAISE; END IF; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE books CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN IF SQLCODE != -942 THEN RAISE; END IF; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE users CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN IF SQLCODE != -942 THEN RAISE; END IF; END;
/

-- ============================================================
-- USERS
-- ============================================================
CREATE TABLE users (
  id              NUMBER(10)           PRIMARY KEY,
  name            VARCHAR2(120 CHAR)   NOT NULL,
  email           VARCHAR2(255 CHAR)   NOT NULL,
  phone           VARCHAR2(30 CHAR),
  hashed_password VARCHAR2(255 CHAR)   NOT NULL,
  created_at      TIMESTAMP            DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Unicité de l'email
CREATE UNIQUE INDEX ux_users_email ON users(email);

-- ============================================================
-- BOOKS
-- ============================================================
CREATE TABLE books (
  id              NUMBER(10)           PRIMARY KEY,
  title           VARCHAR2(255 CHAR)   NOT NULL,
  author          VARCHAR2(255 CHAR)   NOT NULL,
  genre           VARCHAR2(120 CHAR),
  published_date  DATE,
  available       NUMBER(1)            DEFAULT 1 NOT NULL,   -- 1 = disponible, 0 = indisponible
  created_at      TIMESTAMP            DEFAULT CURRENT_TIMESTAMP NOT NULL,
  CONSTRAINT ck_books_available CHECK (available IN (0,1))
);

-- Index utiles pour la recherche
CREATE INDEX ix_books_title  ON books(title);
CREATE INDEX ix_books_author ON books(author);
CREATE INDEX ix_books_genre  ON books(genre);

-- ============================================================
-- LOANS
-- ============================================================
CREATE TABLE loans (
  id           NUMBER(10)  PRIMARY KEY,
  user_id      NUMBER(10)  NOT NULL,
  book_id      NUMBER(10)  NOT NULL,
  borrowed_at  TIMESTAMP   DEFAULT CURRENT_TIMESTAMP NOT NULL,
  returned_at  TIMESTAMP   NULL,
  CONSTRAINT fk_loans_user FOREIGN KEY (user_id) REFERENCES users(id),
  CONSTRAINT fk_loans_book FOREIGN KEY (book_id) REFERENCES books(id)
);

-- Index de jointure
CREATE INDEX ix_loans_user ON loans(user_id);
CREATE INDEX ix_loans_book ON loans(book_id);

-- ============================================================
-- SEQUENCES
-- ============================================================
CREATE SEQUENCE users_seq START WITH 1 INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE books_seq START WITH 1 INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE loans_seq START WITH 1 INCREMENT BY 1 NOCACHE;

-- ============================================================
-- TRIGGERS (auto-increment)
-- ============================================================
CREATE OR REPLACE TRIGGER users_bi
BEFORE INSERT ON users
FOR EACH ROW
WHEN (NEW.id IS NULL)
BEGIN
  SELECT users_seq.NEXTVAL INTO :NEW.id FROM dual;
END;
/
CREATE OR REPLACE TRIGGER books_bi
BEFORE INSERT ON books
FOR EACH ROW
WHEN (NEW.id IS NULL)
BEGIN
  SELECT books_seq.NEXTVAL INTO :NEW.id FROM dual;
END;
/
CREATE OR REPLACE TRIGGER loans_bi
BEFORE INSERT ON loans
FOR EACH ROW
WHEN (NEW.id IS NULL)
BEGIN
  SELECT loans_seq.NEXTVAL INTO :NEW.id FROM dual;
END;
/

BEGIN
  DBMS_OUTPUT.PUT_LINE('USERS columns:');
  FOR r IN (SELECT column_name, nullable FROM user_tab_columns WHERE table_name='USERS' ORDER BY column_id) LOOP
    DBMS_OUTPUT.PUT_LINE('  '||r.column_name||'  nullable='||r.nullable);
  END LOOP;

  DBMS_OUTPUT.PUT_LINE('BOOKS columns:');
  FOR r IN (SELECT column_name, nullable FROM user_tab_columns WHERE table_name='BOOKS' ORDER BY column_id) LOOP
    DBMS_OUTPUT.PUT_LINE('  '||r.column_name||'  nullable='||r.nullable);
  END LOOP;

  DBMS_OUTPUT.PUT_LINE('LOANS columns:');
  FOR r IN (SELECT column_name, nullable FROM user_tab_columns WHERE table_name='LOANS' ORDER BY column_id) LOOP
    DBMS_OUTPUT.PUT_LINE('  '||r.column_name||'  nullable='||r.nullable);
  END LOOP;
END;
/
