import os
import json
from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from datetime import timedelta
import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)
CORS(app)

BASE = os.path.dirname(os.path.abspath(__file__))
STATIC_DIRS = ['css', 'js', 'Activities', 'Courses', 'img']

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'sgac-secret-2026')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-2026')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=int(os.getenv('JWT_EXPIRY_HOURS', 24)))

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

def get_db_config():
    return {
        'host': os.getenv('DB_HOST', 'mysql-3c95dc03-keyan.h.aivencloud.com'),
        'port': int(os.getenv('DB_PORT', 12610)),
        'user': os.getenv('DB_USER', 'avnadmin'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'defaultdb'),
        'charset': 'utf8mb4',
        'ssl_disabled': False
    }

def get_conn():
    try:
        return mysql.connector.connect(**get_db_config())
    except Exception as e:
        print(f"DB Error: {e}")
        return None

def query(sql, params=None):
    conn = get_conn()
    if not conn:
        return None, "Database connection failed"
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        if cur.description:
            rows = cur.fetchall()
            cols = [d[0] for d in cur.description]
            result = []
            for row in rows:
                item = {}
                for i, c in enumerate(cols):
                    v = row[i]
                    if isinstance(v, bytes):
                        v = v.decode('utf-8', errors='replace')
                    item[c] = v
                result.append(item)
            cur.close()
            conn.close()
            return result, None
        else:
            conn.commit()
            lastid = cur.lastrowid
            cur.close()
            conn.close()
            return lastid, None
    except Exception as e:
        if conn:
            conn.close()
        return None, str(e)

def query_one(sql, params=None):
    conn = get_conn()
    if not conn:
        return None, "Database connection failed"
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        row = cur.fetchone()
        if row:
            cols = [d[0] for d in cur.description]
            item = {}
            for i, c in enumerate(cols):
                v = row[i]
                if isinstance(v, bytes):
                    v = v.decode('utf-8', errors='replace')
                item[c] = v
            cur.close()
            conn.close()
            return item, None
        cur.close()
        conn.close()
        return None, None
    except Exception as e:
        if conn:
            conn.close()
        return None, str(e)

def execute(sql, params=None):
    conn = get_conn()
    if not conn:
        return None, "Database connection failed"
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        lastid = cur.lastrowid
        conn.commit()
        cur.close()
        conn.close()
        return lastid, None
    except Exception as e:
        if conn:
            conn.close()
        return None, str(e)

TABLES = [
    '''CREATE TABLE IF NOT EXISTS admin_users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        name VARCHAR(255) DEFAULT 'Admin',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''',
    '''CREATE TABLE IF NOT EXISTS news (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(500) NOT NULL,
        date VARCHAR(100) DEFAULT '',
        icon VARCHAR(100) DEFAULT 'fa-bullhorn',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''',
    '''CREATE TABLE IF NOT EXISTS events (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(500) NOT NULL,
        date VARCHAR(100) DEFAULT '',
        icon VARCHAR(100) DEFAULT 'fa-calendar',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''',
    '''CREATE TABLE IF NOT EXISTS announcements (
        id INT AUTO_INCREMENT PRIMARY KEY,
        text TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''',
    '''CREATE TABLE IF NOT EXISTS carousel (
        id INT AUTO_INCREMENT PRIMARY KEY,
        img VARCHAR(1000) NOT NULL,
        alt VARCHAR(500) DEFAULT '',
        sort_order INT DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''',
    '''CREATE TABLE IF NOT EXISTS downloads (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(500) NOT NULL,
        link VARCHAR(1000) DEFAULT '',
        icon VARCHAR(100) DEFAULT 'fa-download',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''',
    '''CREATE TABLE IF NOT EXISTS departments (
        id INT AUTO_INCREMENT PRIMARY KEY,
        dept_key VARCHAR(100) UNIQUE NOT NULL,
        name VARCHAR(255) NOT NULL,
        icon VARCHAR(100) DEFAULT 'fa-book',
        about TEXT DEFAULT '',
        vision TEXT DEFAULT '',
        mission TEXT DEFAULT '',
        hod_name VARCHAR(255) DEFAULT '',
        hod_designation VARCHAR(255) DEFAULT '',
        hod_qualification VARCHAR(255) DEFAULT '',
        hod_email VARCHAR(255) DEFAULT '',
        hod_phone VARCHAR(50) DEFAULT '',
        sort_order INT DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''',
    '''CREATE TABLE IF NOT EXISTS faculty (
        id INT AUTO_INCREMENT PRIMARY KEY,
        department_id INT NOT NULL,
        name VARCHAR(255) NOT NULL,
        designation VARCHAR(255) DEFAULT '',
        qualification VARCHAR(500) DEFAULT '',
        email VARCHAR(255) DEFAULT '',
        phone VARCHAR(50) DEFAULT '',
        sort_order INT DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE CASCADE
    )''',
    '''CREATE TABLE IF NOT EXISTS site_config (
        id INT PRIMARY KEY DEFAULT 1,
        college_name VARCHAR(500) DEFAULT 'Sethupathy Government Arts College',
        college_name_tamil VARCHAR(500) DEFAULT 'SGAC',
        address VARCHAR(500) DEFAULT 'Ramanathapuram',
        naac_grade VARCHAR(20) DEFAULT 'B',
        affiliated_to VARCHAR(500) DEFAULT 'Alagappa University',
        email VARCHAR(255) DEFAULT 'admin@sgac.edu.in',
        phone VARCHAR(50) DEFAULT '+91-4567-221343',
        principal_name VARCHAR(255) DEFAULT 'Dr. P. Seenuvasa Kumaran',
        principal_qualification VARCHAR(255) DEFAULT 'Ph.D.'
    )'''
]

def init_tables():
    for sql in TABLES:
        try:
            execute(sql)
        except:
            pass
    result, _ = query("SELECT COUNT(*) as c FROM admin_users WHERE email = %s", ('admin@sgac.edu.in',))
    if result and result[0]['c'] == 0:
        pw = bcrypt.generate_password_hash('sgac2025').decode('utf-8')
        execute("INSERT INTO admin_users (email, password_hash) VALUES (%s, %s)", ('admin@sgac.edu.in', pw))
    result, _ = query("SELECT COUNT(*) as c FROM site_config WHERE id = 1")
    if result and result[0]['c'] == 0:
        execute("INSERT INTO site_config (id) VALUES (1)")

try:
    init_tables()
except Exception as e:
    print(f"Init error: {e}")

@app.route('/api/health')
def health():
    return jsonify({'status': 'ok'})

@app.route('/')
def serve_index():
    return render_template('index.html')

@app.route('/admin-login.html')
def serve_admin_login():
    return render_template('admin-login.html')

@app.route('/admin.html')
def serve_admin():
    return render_template('admin.html')

@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory(os.path.join(BASE, 'css'), filename)

@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory(os.path.join(BASE, 'js'), filename)

@app.route('/Activities/<path:filename>')
def serve_activities(filename):
    return send_from_directory(os.path.join(BASE, 'Activities'), filename)

@app.route('/Courses/<path:filename>')
def serve_courses(filename):
    return send_from_directory(os.path.join(BASE, 'Courses'), filename)

@app.route('/img/<path:filename>')
def serve_img(filename):
    return send_from_directory(os.path.join(BASE, 'img'), filename)

@app.route('/Courses/<path:filename>')
def serve_courses_html(filename):
    path = os.path.join(BASE, 'Courses', filename)
    if os.path.exists(path):
        return send_from_directory(os.path.join(BASE, 'Courses'), filename)
    return "Not found", 404

@app.route('/Activities/<path:filename>')
def serve_activities_html(filename):
    path = os.path.join(BASE, 'Activities', filename)
    if os.path.exists(path):
        return send_from_directory(os.path.join(BASE, 'Activities'), filename)
    return "Not found", 404

@app.route('/<path:filename>')
def serve_any(filename):
    for d in STATIC_DIRS:
        path = os.path.join(BASE, d, filename)
        if os.path.exists(path):
            return send_from_directory(os.path.join(BASE, d), filename)
    root_html = os.path.join(BASE, filename)
    if os.path.exists(root_html):
        return send_from_directory(BASE, filename)
    tpl_path = os.path.join(BASE, 'templates', filename)
    if os.path.exists(tpl_path):
        return render_template(filename)
    return "Not found", 404

@app.route('/api/auth/setup', methods=['POST'])
def setup():
    pw = bcrypt.generate_password_hash('sgac2025').decode('utf-8')
    id, err = execute("INSERT INTO admin_users (email, password_hash) VALUES (%s, %s)", ('admin@sgac.edu.in', pw))
    if err:
        if 'Duplicate' in str(err) or 'duplicate' in str(err).lower():
            return jsonify({'message': 'Admin already exists. Try login.'})
        return jsonify({'error': err}), 500
    return jsonify({'message': 'Admin created. You can now login.'})

@app.route('/api/auth/setup-config', methods=['POST'])
def setup_config():
    cols = ['college_name','college_name_tamil','address','naac_grade','affiliated_to','email','phone','principal_name','principal_qualification']
    vals = ['Sethupathy Government Arts College','செதுபாதி அரசு கலை கல்லூரி','Ramanathapuram-623501','B','Alagappa University, Karaikudi','administration@sgacrmd.edu.in','+91-4567-221343','Dr. P. Seenuvasa Kumaran','M.Sc., M.Phil., B.Ed., PGDCA, Ph.D.']
    _, err = execute("INSERT INTO site_config (id, college_name, college_name_tamil, address, naac_grade, affiliated_to, email, phone, principal_name, principal_qualification) VALUES (1, %s, %s, %s, %s, %s, %s, %s, %s, %s)", vals)
    if err:
        if 'Duplicate' in str(err) or 'duplicate' in str(err).lower():
            return jsonify({'message': 'Config already exists.'})
        return jsonify({'error': err}), 500
    return jsonify({'message': 'Site config created.'})

@app.route('/api/public/all')
def get_all():
    news, _ = query("SELECT * FROM news ORDER BY id DESC")
    events, _ = query("SELECT * FROM events ORDER BY id DESC")
    announcements, _ = query("SELECT * FROM announcements ORDER BY id DESC")
    carousel, _ = query("SELECT * FROM carousel ORDER BY sort_order ASC, id ASC")
    downloads, _ = query("SELECT * FROM downloads ORDER BY id DESC")
    departments, _ = query("SELECT * FROM departments ORDER BY sort_order ASC, id ASC")
    site_config, _ = query_one("SELECT * FROM site_config WHERE id = 1")
    return jsonify({
        'news': news or [], 'events': events or [], 'announcements': announcements or [],
        'carousel': carousel or [], 'downloads': downloads or [],
        'departments': departments or [], 'site_config': site_config or {}
    })

@app.route('/api/public/site-config')
def get_site_config():
    data, _ = query_one("SELECT * FROM site_config WHERE id = 1")
    return jsonify(data or {})

@app.route('/api/public/news')
def get_news():
    data, _ = query("SELECT * FROM news ORDER BY id DESC")
    return jsonify(data or [])

@app.route('/api/public/events')
def get_events():
    data, _ = query("SELECT * FROM events ORDER BY id DESC")
    return jsonify(data or [])

@app.route('/api/public/announcements')
def get_announcements():
    data, _ = query("SELECT * FROM announcements ORDER BY id DESC")
    return jsonify(data or [])

@app.route('/api/public/carousel')
def get_carousel():
    data, _ = query("SELECT * FROM carousel ORDER BY sort_order ASC, id ASC")
    return jsonify(data or [])

@app.route('/api/public/departments')
def get_departments():
    data, _ = query("SELECT * FROM departments ORDER BY sort_order ASC, id ASC")
    return jsonify(data or [])

@app.route('/api/public/departments/<key>')
def get_dept(key):
    dept, err = query_one("SELECT * FROM departments WHERE dept_key = %s", (key,))
    if err or not dept:
        return jsonify({'error': 'Not found'}), 404
    faculty, _ = query("SELECT * FROM faculty WHERE department_id = %s ORDER BY sort_order ASC", (dept['id'],))
    dept['faculty'] = faculty or []
    return jsonify(dept)

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email', '').strip()
    password = data.get('password', '')
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400
    user, _ = query_one("SELECT id, email, password_hash, name FROM admin_users WHERE email = %s", (email,))
    if not user or not bcrypt.check_password_hash(user['password_hash'], password):
        return jsonify({'error': 'Invalid credentials'}), 401
    token = create_access_token(identity=str(user['id']), additional_claims={'email': user['email'], 'name': user['name']})
    return jsonify({'access_token': token, 'user': {'id': user['id'], 'email': user['email'], 'name': user['name']}})

def admin_endpoints():
    @app.route('/api/admin/stats')
    @jwt_required()
    def admin_stats():
        results = {}
        for table in ['news', 'events', 'announcements', 'carousel', 'downloads', 'departments']:
            r, _ = query(f"SELECT COUNT(*) as c FROM {table}")
            results[table] = r[0]['c'] if r else 0
        return jsonify(results)

    @app.route('/api/admin/site-config', methods=['GET', 'PUT'])
    @jwt_required()
    def admin_site_config():
        if request.method == 'GET':
            data, _ = query_one("SELECT * FROM site_config WHERE id = 1")
            return jsonify(data or {})
        data = request.get_json() or {}
        cols = ['college_name', 'college_name_tamil', 'address', 'naac_grade', 'affiliated_to', 'email', 'phone', 'principal_name', 'principal_qualification']
        sets = ', '.join([f"{c} = %s" for c in cols])
        vals = [data.get(c, '') for c in cols]
        id, err = execute(f"UPDATE site_config SET {sets} WHERE id = 1", vals)
        if err:
            return jsonify({'error': err}), 500
        data, _ = query_one("SELECT * FROM site_config WHERE id = 1")
        return jsonify(data or {})

    @app.route('/api/admin/news', methods=['GET', 'POST'])
    @jwt_required()
    def admin_news():
        if request.method == 'GET':
            data, _ = query("SELECT * FROM news ORDER BY id DESC")
            return jsonify(data or [])
        data = request.get_json() or {}
        id, err = execute("INSERT INTO news (title, date, icon) VALUES (%s, %s, %s)", (data.get('title',''), data.get('date',''), data.get('icon','fa-bullhorn')))
        if err: return jsonify({'error': err}), 500
        result, _ = query_one("SELECT * FROM news WHERE id = %s", (id,))
        return jsonify(result or {}), 201

    @app.route('/api/admin/news/<int:nid>', methods=['PUT', 'DELETE'])
    @jwt_required()
    def admin_news_item(nid):
        if request.method == 'DELETE':
            _, err = execute("DELETE FROM news WHERE id = %s", (nid,))
            return jsonify({'message': 'Deleted'}) if not err else jsonify({'error': err}), 500
        data = request.get_json() or {}
        _, err = execute("UPDATE news SET title=%s, date=%s, icon=%s WHERE id=%s", (data.get('title'), data.get('date'), data.get('icon'), nid))
        if err: return jsonify({'error': err}), 500
        result, _ = query_one("SELECT * FROM news WHERE id = %s", (nid,))
        return jsonify(result or {})

    @app.route('/api/admin/events', methods=['GET', 'POST'])
    @jwt_required()
    def admin_events():
        if request.method == 'GET':
            data, _ = query("SELECT * FROM events ORDER BY id DESC")
            return jsonify(data or [])
        data = request.get_json() or {}
        id, err = execute("INSERT INTO events (title, date) VALUES (%s, %s)", (data.get('title',''), data.get('date','')))
        if err: return jsonify({'error': err}), 500
        result, _ = query_one("SELECT * FROM events WHERE id = %s", (id,))
        return jsonify(result or {}), 201

    @app.route('/api/admin/events/<int:eid>', methods=['PUT', 'DELETE'])
    @jwt_required()
    def admin_events_item(eid):
        if request.method == 'DELETE':
            _, err = execute("DELETE FROM events WHERE id = %s", (eid,))
            return jsonify({'message': 'Deleted'}) if not err else jsonify({'error': err}), 500
        data = request.get_json() or {}
        _, err = execute("UPDATE events SET title=%s, date=%s WHERE id=%s", (data.get('title'), data.get('date'), eid))
        if err: return jsonify({'error': err}), 500
        result, _ = query_one("SELECT * FROM events WHERE id = %s", (eid,))
        return jsonify(result or {})

    @app.route('/api/admin/announcements', methods=['GET', 'POST'])
    @jwt_required()
    def admin_announcements():
        if request.method == 'GET':
            data, _ = query("SELECT * FROM announcements ORDER BY id DESC")
            return jsonify(data or [])
        data = request.get_json() or {}
        id, err = execute("INSERT INTO announcements (text) VALUES (%s)", (data.get('text',''),))
        if err: return jsonify({'error': err}), 500
        result, _ = query_one("SELECT * FROM announcements WHERE id = %s", (id,))
        return jsonify(result or {}), 201

    @app.route('/api/admin/announcements/<int:aid>', methods=['PUT', 'DELETE'])
    @jwt_required()
    def admin_announcements_item(aid):
        if request.method == 'DELETE':
            _, err = execute("DELETE FROM announcements WHERE id = %s", (aid,))
            return jsonify({'message': 'Deleted'}) if not err else jsonify({'error': err}), 500
        data = request.get_json() or {}
        _, err = execute("UPDATE announcements SET text=%s WHERE id=%s", (data.get('text'), aid))
        if err: return jsonify({'error': err}), 500
        result, _ = query_one("SELECT * FROM announcements WHERE id = %s", (aid,))
        return jsonify(result or {})

    @app.route('/api/admin/carousel', methods=['GET', 'POST'])
    @jwt_required()
    def admin_carousel():
        if request.method == 'GET':
            data, _ = query("SELECT * FROM carousel ORDER BY sort_order ASC, id ASC")
            return jsonify(data or [])
        data = request.get_json() or {}
        id, err = execute("INSERT INTO carousel (img, alt) VALUES (%s, %s)", (data.get('img',''), data.get('alt','')))
        if err: return jsonify({'error': err}), 500
        result, _ = query_one("SELECT * FROM carousel WHERE id = %s", (id,))
        return jsonify(result or {}), 201

    @app.route('/api/admin/carousel/<int:cid>', methods=['PUT', 'DELETE'])
    @jwt_required()
    def admin_carousel_item(cid):
        if request.method == 'DELETE':
            _, err = execute("DELETE FROM carousel WHERE id = %s", (cid,))
            return jsonify({'message': 'Deleted'}) if not err else jsonify({'error': err}), 500
        data = request.get_json() or {}
        _, err = execute("UPDATE carousel SET img=%s, alt=%s WHERE id=%s", (data.get('img'), data.get('alt'), cid))
        if err: return jsonify({'error': err}), 500
        result, _ = query_one("SELECT * FROM carousel WHERE id = %s", (cid,))
        return jsonify(result or {})

    @app.route('/api/admin/downloads', methods=['GET', 'POST'])
    @jwt_required()
    def admin_downloads():
        if request.method == 'GET':
            data, _ = query("SELECT * FROM downloads ORDER BY id DESC")
            return jsonify(data or [])
        data = request.get_json() or {}
        id, err = execute("INSERT INTO downloads (title, link) VALUES (%s, %s)", (data.get('title',''), data.get('link','')))
        if err: return jsonify({'error': err}), 500
        result, _ = query_one("SELECT * FROM downloads WHERE id = %s", (id,))
        return jsonify(result or {}), 201

    @app.route('/api/admin/downloads/<int:did>', methods=['PUT', 'DELETE'])
    @jwt_required()
    def admin_downloads_item(did):
        if request.method == 'DELETE':
            _, err = execute("DELETE FROM downloads WHERE id = %s", (did,))
            return jsonify({'message': 'Deleted'}) if not err else jsonify({'error': err}), 500
        data = request.get_json() or {}
        _, err = execute("UPDATE downloads SET title=%s, link=%s WHERE id=%s", (data.get('title'), data.get('link'), did))
        if err: return jsonify({'error': err}), 500
        result, _ = query_one("SELECT * FROM downloads WHERE id = %s", (did,))
        return jsonify(result or {})

    @app.route('/api/admin/departments', methods=['GET', 'POST'])
    @jwt_required()
    def admin_departments():
        if request.method == 'GET':
            data, _ = query("SELECT * FROM departments ORDER BY sort_order ASC, id ASC")
            return jsonify(data or [])
        data = request.get_json() or {}
        id, err = execute("INSERT INTO departments (dept_key, name, icon) VALUES (%s, %s, %s)", (data.get('dept_key',''), data.get('name',''), data.get('icon','fa-book')))
        if err: return jsonify({'error': err}), 500
        result, _ = query_one("SELECT * FROM departments WHERE id = %s", (id,))
        return jsonify(result or {}), 201

    @app.route('/api/admin/departments/<int:depid>', methods=['PUT', 'DELETE'])
    @jwt_required()
    def admin_departments_item(depid):
        if request.method == 'DELETE':
            _, err = execute("DELETE FROM departments WHERE id = %s", (depid,))
            return jsonify({'message': 'Deleted'}) if not err else jsonify({'error': err}), 500
        data = request.get_json() or {}
        cols = ['name','icon','about','vision','mission','hod_name','hod_designation','hod_qualification','hod_email','hod_phone']
        sets = ', '.join([f"{c} = %s" for c in cols])
        vals = [data.get(c, '') for c in cols] + [depid]
        _, err = execute(f"UPDATE departments SET {sets} WHERE id=%s", vals)
        if err: return jsonify({'error': err}), 500
        result, _ = query_one("SELECT * FROM departments WHERE id = %s", (depid,))
        return jsonify(result or {})

    @app.route('/api/admin/departments/<int:depid>/faculty')
    @jwt_required()
    def admin_faculty_list(depid):
        data, _ = query("SELECT * FROM faculty WHERE department_id = %s ORDER BY sort_order ASC", (depid,))
        return jsonify(data or [])

    @app.route('/api/admin/faculty', methods=['POST'])
    @jwt_required()
    def admin_faculty_create():
        data = request.get_json() or {}
        id, err = execute("INSERT INTO faculty (department_id, name, designation, qualification, email, phone) VALUES (%s, %s, %s, %s, %s, %s)",
                          (data.get('department_id'), data.get('name',''), data.get('designation',''), data.get('qualification',''), data.get('email',''), data.get('phone','')))
        if err: return jsonify({'error': err}), 500
        result, _ = query_one("SELECT * FROM faculty WHERE id = %s", (id,))
        return jsonify(result or {}), 201

    @app.route('/api/admin/faculty/<int:fid>', methods=['PUT', 'DELETE'])
    @jwt_required()
    def admin_faculty_item(fid):
        if request.method == 'DELETE':
            _, err = execute("DELETE FROM faculty WHERE id = %s", (fid,))
            return jsonify({'message': 'Deleted'}) if not err else jsonify({'error': err}), 500
        data = request.get_json() or {}
        _, err = execute("UPDATE faculty SET name=%s, designation=%s, qualification=%s, email=%s, phone=%s WHERE id=%s",
                         (data.get('name'), data.get('designation'), data.get('qualification'), data.get('email'), data.get('phone'), fid))
        if err: return jsonify({'error': err}), 500
        result, _ = query_one("SELECT * FROM faculty WHERE id = %s", (fid,))
        return jsonify(result or {})

admin_endpoints()

handler = app
