-- ============================================================
-- STEP 1: Create all tables
-- Run this FIRST in Supabase SQL Editor
-- ============================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- NEWS TABLE
CREATE TABLE IF NOT EXISTS news (
    id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    date TEXT DEFAULT '',
    icon TEXT DEFAULT 'fa-bullhorn',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- EVENTS TABLE
CREATE TABLE IF NOT EXISTS events (
    id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    date TEXT DEFAULT '',
    icon TEXT DEFAULT 'fa-calendar',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- DOWNLOADS TABLE
CREATE TABLE IF NOT EXISTS downloads (
    id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    link TEXT DEFAULT '',
    icon TEXT DEFAULT 'fa-download',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- CAROUSEL TABLE
CREATE TABLE IF NOT EXISTS carousel (
    id BIGSERIAL PRIMARY KEY,
    img TEXT NOT NULL,
    alt TEXT DEFAULT '',
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ANNOUNCEMENTS TABLE
CREATE TABLE IF NOT EXISTS announcements (
    id BIGSERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- DEPARTMENTS TABLE
CREATE TABLE IF NOT EXISTS departments (
    id BIGSERIAL PRIMARY KEY,
    dept_key TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    icon TEXT DEFAULT 'fa-book',
    about TEXT DEFAULT '',
    vision TEXT DEFAULT '',
    mission TEXT DEFAULT '',
    hod_name TEXT DEFAULT '',
    hod_designation TEXT DEFAULT '',
    hod_qualification TEXT DEFAULT '',
    hod_email TEXT DEFAULT '',
    hod_phone TEXT DEFAULT '',
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- FACULTY TABLE
CREATE TABLE IF NOT EXISTS faculty (
    id BIGSERIAL PRIMARY KEY,
    department_id BIGINT REFERENCES departments(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    designation TEXT DEFAULT '',
    qualification TEXT DEFAULT '',
    email TEXT DEFAULT '',
    phone TEXT DEFAULT '',
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- GALLERY TABLE
CREATE TABLE IF NOT EXISTS gallery (
    id BIGSERIAL PRIMARY KEY,
    department_id BIGINT REFERENCES departments(id) ON DELETE CASCADE,
    src TEXT NOT NULL,
    caption TEXT DEFAULT '',
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ACTIVITIES TABLE
CREATE TABLE IF NOT EXISTS activities (
    id BIGSERIAL PRIMARY KEY,
    department_id BIGINT REFERENCES departments(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    description TEXT DEFAULT '',
    date TEXT DEFAULT '',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ACHIEVEMENTS TABLE
CREATE TABLE IF NOT EXISTS achievements (
    id BIGSERIAL PRIMARY KEY,
    department_id BIGINT REFERENCES departments(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    description TEXT DEFAULT '',
    student_name TEXT DEFAULT '',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ECONTENT TABLE
CREATE TABLE IF NOT EXISTS econtent (
    id BIGSERIAL PRIMARY KEY,
    department_id BIGINT REFERENCES departments(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    link TEXT DEFAULT '',
    description TEXT DEFAULT '',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- SITE CONFIG TABLE
CREATE TABLE IF NOT EXISTS site_config (
    id SERIAL PRIMARY KEY,
    college_name TEXT DEFAULT 'Sethupathy Government Arts College',
    college_name_tamil TEXT DEFAULT 'செதுபாதி அரசு கலை கல்லூரி',
    address TEXT DEFAULT 'Ramanathapuram-623501',
    naac_grade TEXT DEFAULT 'B',
    affiliated_to TEXT DEFAULT 'Alagappa University, Karaikudi',
    email TEXT DEFAULT 'administration@sgacrmd.edu.in',
    phone TEXT DEFAULT '+91-4567-221343',
    principal_name TEXT DEFAULT 'Dr. P. Seenuvasa Kumaran',
    principal_qualification TEXT DEFAULT 'M.Sc., M.Phil., B.Ed., PGDCA, Ph.D.',
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(id)
);
