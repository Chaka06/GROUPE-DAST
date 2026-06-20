-- ══════════════════════════════════════════════════════════════════
--  DAST NEWGEN'SPARK — Script d'initialisation Supabase
--  À coller dans : Supabase → SQL Editor → New query → Run
--  Crée toutes les tables nécessaires pour Django
-- ══════════════════════════════════════════════════════════════════

-- ── 1. Tables système Django ─────────────────────────────────────

CREATE TABLE IF NOT EXISTS django_migrations (
    id          BIGSERIAL PRIMARY KEY,
    app         VARCHAR(255) NOT NULL,
    name        VARCHAR(255) NOT NULL,
    applied     TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS django_content_type (
    id        SERIAL PRIMARY KEY,
    app_label VARCHAR(100) NOT NULL,
    model     VARCHAR(100) NOT NULL,
    UNIQUE (app_label, model)
);

CREATE TABLE IF NOT EXISTS auth_permission (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(255) NOT NULL,
    content_type_id INTEGER NOT NULL REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED,
    codename        VARCHAR(100) NOT NULL,
    UNIQUE (content_type_id, codename)
);

CREATE TABLE IF NOT EXISTS auth_group (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS auth_group_permissions (
    id            BIGSERIAL PRIMARY KEY,
    group_id      INTEGER NOT NULL REFERENCES auth_group(id) ON DELETE CASCADE,
    permission_id INTEGER NOT NULL REFERENCES auth_permission(id) ON DELETE CASCADE,
    UNIQUE (group_id, permission_id)
);

CREATE TABLE IF NOT EXISTS django_session (
    session_key  VARCHAR(40)  PRIMARY KEY,
    session_data TEXT         NOT NULL,
    expire_date  TIMESTAMPTZ  NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_django_session_expire ON django_session(expire_date);

-- ── 2. Utilisateurs (Custom AbstractUser) ───────────────────────

CREATE TABLE IF NOT EXISTS accounts_user (
    id                  BIGSERIAL    PRIMARY KEY,
    password            VARCHAR(128) NOT NULL,
    last_login          TIMESTAMPTZ  NULL,
    is_superuser        BOOLEAN      NOT NULL DEFAULT FALSE,
    username            VARCHAR(150) NOT NULL UNIQUE,
    first_name          VARCHAR(150) NOT NULL DEFAULT '',
    last_name           VARCHAR(150) NOT NULL DEFAULT '',
    email               VARCHAR(254) NOT NULL DEFAULT '',
    is_staff            BOOLEAN      NOT NULL DEFAULT FALSE,
    is_active           BOOLEAN      NOT NULL DEFAULT TRUE,
    date_joined         TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    -- Champs personnalisés DAST
    is_owner            BOOLEAN      NOT NULL DEFAULT FALSE,
    avatar              VARCHAR(200) NULL,
    role_title          VARCHAR(100) NOT NULL DEFAULT '',
    bio                 TEXT         NOT NULL DEFAULT '',
    linkedin_url        VARCHAR(200) NOT NULL DEFAULT '',
    twitter_url         VARCHAR(200) NOT NULL DEFAULT '',
    github_url          VARCHAR(200) NOT NULL DEFAULT '',
    show_on_team_page   BOOLEAN      NOT NULL DEFAULT FALSE,
    team_order          INTEGER      NOT NULL DEFAULT 0 CHECK (team_order >= 0),
    created_at          TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_accounts_user_username ON accounts_user(username);

CREATE TABLE IF NOT EXISTS accounts_user_groups (
    id       BIGSERIAL PRIMARY KEY,
    user_id  BIGINT    NOT NULL REFERENCES accounts_user(id) ON DELETE CASCADE,
    group_id INTEGER   NOT NULL REFERENCES auth_group(id) ON DELETE CASCADE,
    UNIQUE (user_id, group_id)
);

CREATE TABLE IF NOT EXISTS accounts_user_user_permissions (
    id            BIGSERIAL PRIMARY KEY,
    user_id       BIGINT  NOT NULL REFERENCES accounts_user(id) ON DELETE CASCADE,
    permission_id INTEGER NOT NULL REFERENCES auth_permission(id) ON DELETE CASCADE,
    UNIQUE (user_id, permission_id)
);

-- ── 3. Admin Log (Django) ────────────────────────────────────────

CREATE TABLE IF NOT EXISTS django_admin_log (
    id             SERIAL       PRIMARY KEY,
    action_time    TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    object_id      TEXT         NULL,
    object_repr    VARCHAR(200) NOT NULL,
    action_flag    SMALLINT     NOT NULL CHECK (action_flag > 0),
    change_message TEXT         NOT NULL,
    content_type_id INTEGER     NULL REFERENCES django_content_type(id) ON DELETE SET NULL,
    user_id        BIGINT       NOT NULL REFERENCES accounts_user(id) ON DELETE CASCADE
);

-- ── 4. Summernote (éditeur blog) ─────────────────────────────────

CREATE TABLE IF NOT EXISTS django_summernote_attachment (
    id       SERIAL       PRIMARY KEY,
    name     VARCHAR(255) NOT NULL,
    file     VARCHAR(200) NOT NULL,
    uploaded TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

-- ── 5. Core — Paramètres site (singleton) ───────────────────────

CREATE TABLE IF NOT EXISTS core_sitesettings (
    id                      SERIAL       PRIMARY KEY,
    site_name               VARCHAR(100) NOT NULL DEFAULT 'DAST NEWGEN''SPARK',
    tagline                 VARCHAR(200) NOT NULL DEFAULT '',
    tagline_sub             VARCHAR(300) NOT NULL DEFAULT '',
    about_short             TEXT         NOT NULL DEFAULT '',
    about_long              TEXT         NOT NULL DEFAULT '',
    logo                    VARCHAR(200) NULL,
    logo_white              VARCHAR(200) NULL,
    favicon                 VARCHAR(200) NULL,
    og_image                VARCHAR(200) NULL,
    email_main              VARCHAR(254) NOT NULL DEFAULT '',
    email_secondary         VARCHAR(254) NOT NULL DEFAULT '',
    phone_main              VARCHAR(30)  NOT NULL DEFAULT '',
    phone_secondary         VARCHAR(30)  NOT NULL DEFAULT '',
    whatsapp                VARCHAR(30)  NOT NULL DEFAULT '',
    address                 TEXT         NOT NULL DEFAULT '',
    google_maps_url         VARCHAR(200) NOT NULL DEFAULT '',
    google_maps_embed       TEXT         NOT NULL DEFAULT '',
    facebook_url            VARCHAR(200) NOT NULL DEFAULT '',
    instagram_url           VARCHAR(200) NOT NULL DEFAULT '',
    linkedin_url            VARCHAR(200) NOT NULL DEFAULT '',
    tiktok_url              VARCHAR(200) NOT NULL DEFAULT '',
    youtube_url             VARCHAR(200) NOT NULL DEFAULT '',
    twitter_url             VARCHAR(200) NOT NULL DEFAULT '',
    github_url              VARCHAR(200) NOT NULL DEFAULT '',
    meta_description        VARCHAR(300) NOT NULL DEFAULT '',
    meta_keywords           TEXT         NOT NULL DEFAULT '',
    google_analytics_id     VARCHAR(50)  NOT NULL DEFAULT '',
    google_tag_manager_id   VARCHAR(50)  NOT NULL DEFAULT '',
    stat_projects           INTEGER      NOT NULL DEFAULT 0 CHECK (stat_projects >= 0),
    stat_clients            INTEGER      NOT NULL DEFAULT 0 CHECK (stat_clients >= 0),
    stat_years              INTEGER      NOT NULL DEFAULT 0 CHECK (stat_years >= 0),
    stat_team               INTEGER      NOT NULL DEFAULT 0 CHECK (stat_team >= 0)
);

-- ── 6. Core — Partenaires ────────────────────────────────────────

CREATE TABLE IF NOT EXISTS core_partner (
    id          BIGSERIAL    PRIMARY KEY,
    name        VARCHAR(150) NOT NULL,
    logo        VARCHAR(200) NOT NULL,
    website_url VARCHAR(200) NOT NULL DEFAULT '',
    "order"     INTEGER      NOT NULL DEFAULT 0 CHECK ("order" >= 0),
    is_active   BOOLEAN      NOT NULL DEFAULT TRUE
);

-- ── 7. Core — Témoignages ────────────────────────────────────────

CREATE TABLE IF NOT EXISTS core_testimonial (
    id           BIGSERIAL    PRIMARY KEY,
    client_name  VARCHAR(150) NOT NULL,
    client_role  VARCHAR(150) NOT NULL DEFAULT '',
    client_photo VARCHAR(200) NULL,
    content      TEXT         NOT NULL,
    rating       SMALLINT     NOT NULL DEFAULT 5 CHECK (rating BETWEEN 1 AND 5),
    "order"      INTEGER      NOT NULL DEFAULT 0 CHECK ("order" >= 0),
    is_active    BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at   TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

-- ── 8. Core — FAQ ────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS core_faq (
    id        BIGSERIAL    PRIMARY KEY,
    question  VARCHAR(300) NOT NULL,
    answer    TEXT         NOT NULL,
    category  VARCHAR(100) NOT NULL DEFAULT '',
    "order"   INTEGER      NOT NULL DEFAULT 0 CHECK ("order" >= 0),
    is_active BOOLEAN      NOT NULL DEFAULT TRUE
);

-- ── 9. Home — Hero Slides ────────────────────────────────────────

CREATE TABLE IF NOT EXISTS home_heroslide (
    id                  BIGSERIAL    PRIMARY KEY,
    title               VARCHAR(150) NOT NULL,
    subtitle            VARCHAR(250) NOT NULL DEFAULT '',
    description         TEXT         NOT NULL DEFAULT '',
    cta_primary_text    VARCHAR(60)  NOT NULL DEFAULT '',
    cta_primary_url     VARCHAR(200) NOT NULL DEFAULT '',
    cta_secondary_text  VARCHAR(60)  NOT NULL DEFAULT '',
    cta_secondary_url   VARCHAR(200) NOT NULL DEFAULT '',
    background_image    VARCHAR(200) NULL,
    "order"             INTEGER      NOT NULL DEFAULT 0 CHECK ("order" >= 0),
    is_active           BOOLEAN      NOT NULL DEFAULT TRUE
);

-- ── 10. Home — Valeurs DAST ──────────────────────────────────────

CREATE TABLE IF NOT EXISTS home_valueproposition (
    id          BIGSERIAL    PRIMARY KEY,
    icon_class  VARCHAR(80)  NOT NULL DEFAULT '',
    title       VARCHAR(100) NOT NULL,
    description TEXT         NOT NULL,
    "order"     INTEGER      NOT NULL DEFAULT 0 CHECK ("order" >= 0),
    is_active   BOOLEAN      NOT NULL DEFAULT TRUE
);

-- ── 11. Services ─────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS services_service (
    id                BIGSERIAL    PRIMARY KEY,
    title             VARCHAR(150) NOT NULL,
    slug              VARCHAR(160) NOT NULL UNIQUE,
    icon_class        VARCHAR(80)  NOT NULL DEFAULT '',
    short_description VARCHAR(250) NOT NULL,
    description       TEXT         NOT NULL,
    cover_image       VARCHAR(200) NULL,
    color_accent      VARCHAR(7)   NOT NULL DEFAULT '#2B7FD4',
    featured          BOOLEAN      NOT NULL DEFAULT FALSE,
    "order"           INTEGER      NOT NULL DEFAULT 0 CHECK ("order" >= 0),
    is_active         BOOLEAN      NOT NULL DEFAULT TRUE,
    meta_description  VARCHAR(300) NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS services_servicefeature (
    id          BIGSERIAL    PRIMARY KEY,
    service_id  BIGINT       NOT NULL REFERENCES services_service(id) ON DELETE CASCADE,
    icon_class  VARCHAR(80)  NOT NULL DEFAULT '',
    title       VARCHAR(150) NOT NULL,
    description TEXT         NOT NULL DEFAULT '',
    "order"     INTEGER      NOT NULL DEFAULT 0 CHECK ("order" >= 0)
);

-- ── 12. Portfolio ─────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS portfolio_technology (
    id         BIGSERIAL   PRIMARY KEY,
    name       VARCHAR(80) NOT NULL,
    icon_class VARCHAR(80) NOT NULL DEFAULT '',
    color      VARCHAR(7)  NOT NULL DEFAULT '#2B7FD4'
);

CREATE TABLE IF NOT EXISTS portfolio_projectcategory (
    id   BIGSERIAL    PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(50)  NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS portfolio_project (
    id                BIGSERIAL    PRIMARY KEY,
    title             VARCHAR(200) NOT NULL,
    slug              VARCHAR(220) NOT NULL UNIQUE,
    category_id       BIGINT       NULL REFERENCES portfolio_projectcategory(id) ON DELETE SET NULL,
    short_description VARCHAR(280) NOT NULL,
    description       TEXT         NOT NULL,
    cover_image       VARCHAR(200) NOT NULL,
    client_name       VARCHAR(150) NOT NULL DEFAULT '',
    project_url       VARCHAR(200) NOT NULL DEFAULT '',
    github_url        VARCHAR(200) NOT NULL DEFAULT '',
    featured          BOOLEAN      NOT NULL DEFAULT FALSE,
    "order"           INTEGER      NOT NULL DEFAULT 0 CHECK ("order" >= 0),
    is_active         BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at        TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS portfolio_project_technologies (
    id            BIGSERIAL PRIMARY KEY,
    project_id    BIGINT    NOT NULL REFERENCES portfolio_project(id) ON DELETE CASCADE,
    technology_id BIGINT    NOT NULL REFERENCES portfolio_technology(id) ON DELETE CASCADE,
    UNIQUE (project_id, technology_id)
);

CREATE TABLE IF NOT EXISTS portfolio_projectimage (
    id         BIGSERIAL    PRIMARY KEY,
    project_id BIGINT       NOT NULL REFERENCES portfolio_project(id) ON DELETE CASCADE,
    image      VARCHAR(200) NOT NULL,
    caption    VARCHAR(200) NOT NULL DEFAULT '',
    "order"    INTEGER      NOT NULL DEFAULT 0 CHECK ("order" >= 0)
);

-- ── 13. Blog ─────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS blog_category (
    id          BIGSERIAL    PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    slug        VARCHAR(110) NOT NULL UNIQUE,
    description TEXT         NOT NULL DEFAULT '',
    cover_image VARCHAR(200) NULL,
    "order"     INTEGER      NOT NULL DEFAULT 0 CHECK ("order" >= 0)
);

CREATE TABLE IF NOT EXISTS blog_tag (
    id   BIGSERIAL   PRIMARY KEY,
    name VARCHAR(80) NOT NULL,
    slug VARCHAR(90) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS blog_post (
    id               BIGSERIAL    PRIMARY KEY,
    title            VARCHAR(250) NOT NULL,
    slug             VARCHAR(270) NOT NULL UNIQUE,
    author_id        BIGINT       NULL REFERENCES accounts_user(id) ON DELETE SET NULL,
    category_id      BIGINT       NULL REFERENCES blog_category(id) ON DELETE SET NULL,
    cover_image      VARCHAR(200) NULL,
    excerpt          VARCHAR(400) NOT NULL DEFAULT '',
    content          TEXT         NOT NULL,
    status           VARCHAR(20)  NOT NULL DEFAULT 'draft',
    featured         BOOLEAN      NOT NULL DEFAULT FALSE,
    published_at     TIMESTAMPTZ  NULL,
    meta_description VARCHAR(300) NOT NULL DEFAULT '',
    views_count      INTEGER      NOT NULL DEFAULT 0 CHECK (views_count >= 0),
    created_at       TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS blog_post_tags (
    id      BIGSERIAL PRIMARY KEY,
    post_id BIGINT    NOT NULL REFERENCES blog_post(id) ON DELETE CASCADE,
    tag_id  BIGINT    NOT NULL REFERENCES blog_tag(id) ON DELETE CASCADE,
    UNIQUE (post_id, tag_id)
);

-- ── 14. Contact ───────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS contact_contactmessage (
    id         BIGSERIAL    PRIMARY KEY,
    full_name  VARCHAR(200) NOT NULL,
    email      VARCHAR(254) NOT NULL,
    phone      VARCHAR(30)  NOT NULL DEFAULT '',
    company    VARCHAR(150) NOT NULL DEFAULT '',
    subject    VARCHAR(30)  NOT NULL DEFAULT 'other',
    message    TEXT         NOT NULL,
    is_read    BOOLEAN      NOT NULL DEFAULT FALSE,
    replied_at TIMESTAMPTZ  NULL,
    ip_address INET         NULL,
    created_at TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

-- ══════════════════════════════════════════════════════════════════
--  Enregistrement des migrations Django (pour éviter les doublons)
--  Django saura que les tables existent déjà
-- ══════════════════════════════════════════════════════════════════

INSERT INTO django_migrations (app, name, applied) VALUES
  ('contenttypes',    '0001_initial',                        NOW()),
  ('contenttypes',    '0002_remove_content_type_name',       NOW()),
  ('auth',            '0001_initial',                        NOW()),
  ('auth',            '0002_alter_permission_name_max_length',NOW()),
  ('auth',            '0003_alter_user_email_max_length',    NOW()),
  ('auth',            '0004_alter_user_username_opts',       NOW()),
  ('auth',            '0005_alter_user_last_login_null',     NOW()),
  ('auth',            '0006_require_contenttypes_0002',      NOW()),
  ('auth',            '0007_alter_validators_add_error_messages', NOW()),
  ('auth',            '0008_alter_user_username_max_length', NOW()),
  ('auth',            '0009_alter_user_last_name_max_length',NOW()),
  ('auth',            '0010_alter_group_name_max_length',    NOW()),
  ('auth',            '0011_update_proxy_permissions',       NOW()),
  ('auth',            '0012_alter_user_first_name_max_length',NOW()),
  ('accounts',        '0001_initial',                        NOW()),
  ('admin',           '0001_initial',                        NOW()),
  ('admin',           '0002_logentry_remove_auto_add',       NOW()),
  ('admin',           '0003_logentry_add_action_flag_choices',NOW()),
  ('sessions',        '0001_initial',                        NOW()),
  ('django_summernote','0001_initial',                       NOW()),
  ('django_summernote','0002_auto_20141027_1013',            NOW()),
  ('core',            '0001_initial',                        NOW()),
  ('home',            '0001_initial',                        NOW()),
  ('services',        '0001_initial',                        NOW()),
  ('portfolio',       '0001_initial',                        NOW()),
  ('blog',            '0001_initial',                        NOW()),
  ('contact',         '0001_initial',                        NOW())
ON CONFLICT DO NOTHING;
