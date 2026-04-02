import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask_bcrypt import Bcrypt
from datetime import timedelta
import mysql.connector
from mysql.connector import pooling
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='../static', template_folder='../templates')

CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'sgac-super-secret-key-change-in-production')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-super-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=int(os.getenv('JWT_EXPIRY_HOURS', 24)))

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

db_config = {
    'host': os.getenv('DB_HOST', 'mysql-3c95dc03-keyan.h.aivencloud.com'),
    'port': int(os.getenv('DB_PORT', 12610)),
    'user': os.getenv('DB_USER', 'avnadmin'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'defaultdb'),
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci',
    'ssl_disabled': False,
    'ssl_verify_cert': False
}

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

db_pool = pooling.MySQLConnectionPool(
    pool_name="sgac_pool",
    pool_size=5,
    pool_reset_session=True,
    **db_config
)

def get_db():
    return db_pool.get_connection()

def dict_from_rows(rows, columns):
    result = []
    for row in rows:
        item = {}
        for i, col in enumerate(columns):
            val = row[i]
            if isinstance(val, bytes):
                val = val.decode('utf-8', errors='replace')
            item[col] = val
        result.append(item)
    return result

def dict_from_row(row, columns):
    if not row:
        return None
    item = {}
    for i, col in enumerate(columns):
        val = row[i]
        if isinstance(val, bytes):
            val = val.decode('utf-8', errors='replace')
        item[col] = val
    return item

def init_db():
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS admin_users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            name VARCHAR(255) DEFAULT 'Admin',
            role VARCHAR(50) DEFAULT 'admin',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP NULL
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(500) NOT NULL,
            date VARCHAR(100) DEFAULT '',
            icon VARCHAR(100) DEFAULT 'fa-bullhorn',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(500) NOT NULL,
            date VARCHAR(100) DEFAULT '',
            icon VARCHAR(100) DEFAULT 'fa-calendar',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS announcements (
            id INT AUTO_INCREMENT PRIMARY KEY,
            text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS carousel (
            id INT AUTO_INCREMENT PRIMARY KEY,
            img VARCHAR(1000) NOT NULL,
            alt VARCHAR(500) DEFAULT '',
            sort_order INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS downloads (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(500) NOT NULL,
            link VARCHAR(1000) DEFAULT '',
            icon VARCHAR(100) DEFAULT 'fa-download',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS departments (
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
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS faculty (
            id INT AUTO_INCREMENT PRIMARY KEY,
            department_id INT NOT NULL,
            name VARCHAR(255) NOT NULL,
            designation VARCHAR(255) DEFAULT '',
            qualification VARCHAR(500) DEFAULT '',
            email VARCHAR(255) DEFAULT '',
            phone VARCHAR(50) DEFAULT '',
            sort_order INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE CASCADE
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS gallery (
            id INT AUTO_INCREMENT PRIMARY KEY,
            department_id INT NOT NULL,
            src VARCHAR(1000) NOT NULL,
            caption VARCHAR(500) DEFAULT '',
            sort_order INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE CASCADE
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS activities (
            id INT AUTO_INCREMENT PRIMARY KEY,
            department_id INT NOT NULL,
            title VARCHAR(500) NOT NULL,
            description TEXT DEFAULT '',
            date VARCHAR(100) DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE CASCADE
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS achievements (
            id INT AUTO_INCREMENT PRIMARY KEY,
            department_id INT NOT NULL,
            title VARCHAR(500) NOT NULL,
            description TEXT DEFAULT '',
            student_name VARCHAR(255) DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS econtent (
            id INT AUTO_INCREMENT PRIMARY KEY,
            department_id INT NOT NULL,
            title VARCHAR(500) NOT NULL,
            link VARCHAR(1000) DEFAULT '',
            description TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS site_config (
            id INT PRIMARY KEY DEFAULT 1,
            college_name VARCHAR(500) DEFAULT 'Sethupathy Government Arts College',
            college_name_tamil VARCHAR(500) DEFAULT 'செதுபாதி அரசு கலை கல்லூரி',
            address VARCHAR(500) DEFAULT 'Ramanathapuram-623501',
            naac_grade VARCHAR(20) DEFAULT 'B',
            affiliated_to VARCHAR(500) DEFAULT 'Alagappa University, Karaikudi',
            email VARCHAR(255) DEFAULT 'administration@sgacrmd.edu.in',
            phone VARCHAR(50) DEFAULT '+91-4567-221343',
            principal_name VARCHAR(255) DEFAULT 'Dr. P. Seenuvasa Kumaran',
            principal_qualification VARCHAR(255) DEFAULT 'M.Sc., M.Phil., B.Ed., PGDCA, Ph.D.',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
    ''')
    
    cur.execute("SELECT COUNT(*) FROM site_config")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO site_config (id) VALUES (1)")
    
    cur.execute("SELECT COUNT(*) FROM admin_users WHERE email = %s", ('admin@sgac.edu.in',))
    if cur.fetchone()[0] == 0:
        pw_hash = bcrypt.generate_password_hash('sgac2025').decode('utf-8')
        cur.execute("INSERT INTO admin_users (email, password_hash, name) VALUES (%s, %s, %s)",
                    ('admin@sgac.edu.in', pw_hash, 'Admin'))
    
    conn.commit()
    cur.close()
    conn.close()

with app.app_context():
    try:
        init_db()
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Database initialization error: {e}")

@app.route('/')
def index():
    return jsonify({'message': 'SGAC College API', 'version': '1.0'})

@app.route('/api/health')
def health():
    return jsonify({'status': 'ok'})

@app.route('/api/public/site-config')
def get_site_config():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM site_config WHERE id = 1")
    row = cur.fetchone()
    cols = [d[0] for d in cur.description]
    cur.close()
    conn.close()
    return jsonify(dict_from_row(row, cols) or {})

@app.route('/api/public/news')
def get_news():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM news ORDER BY id DESC")
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    cur.close()
    conn.close()
    return jsonify(dict_from_rows(rows, cols))

@app.route('/api/public/events')
def get_events():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM events ORDER BY id DESC")
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    cur.close()
    conn.close()
    return jsonify(dict_from_rows(rows, cols))

@app.route('/api/public/announcements')
def get_announcements():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM announcements ORDER BY id DESC")
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    cur.close()
    conn.close()
    return jsonify(dict_from_rows(rows, cols))

@app.route('/api/public/carousel')
def get_carousel():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM carousel ORDER BY sort_order ASC, id ASC")
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    cur.close()
    conn.close()
    return jsonify(dict_from_rows(rows, cols))

@app.route('/api/public/downloads')
def get_downloads():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM downloads ORDER BY id DESC")
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    cur.close()
    conn.close()
    return jsonify(dict_from_rows(rows, cols))

@app.route('/api/public/departments')
def get_departments():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM departments ORDER BY sort_order ASC, id ASC")
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    cur.close()
    conn.close()
    return jsonify(dict_from_rows(rows, cols))

@app.route('/api/public/departments/<key>')
def get_department(key):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM departments WHERE dept_key = %s", (key,))
    row = cur.fetchone()
    cols = [d[0] for d in cur.description]
    if not row:
        cur.close()
        conn.close()
        return jsonify({'error': 'Department not found'}), 404
    dept = dict_from_row(row, cols)
    cur.execute("SELECT * FROM faculty WHERE department_id = %s ORDER BY sort_order ASC", (dept['id'],))
    dept['faculty'] = dict_from_rows(cur.fetchall(), [d[0] for d in cur.description])
    cur.execute("SELECT * FROM gallery WHERE department_id = %s ORDER BY sort_order ASC", (dept['id'],))
    dept['gallery'] = dict_from_rows(cur.fetchall(), [d[0] for d in cur.description])
    cur.execute("SELECT * FROM activities WHERE department_id = %s ORDER BY id DESC", (dept['id'],))
    dept['activities'] = dict_from_rows(cur.fetchall(), [d[0] for d in cur.description])
    cur.execute("SELECT * FROM achievements WHERE department_id = %s ORDER BY id DESC", (dept['id'],))
    dept['achievements'] = dict_from_rows(cur.fetchall(), [d[0] for d in cur.description])
    cur.execute("SELECT * FROM econtent WHERE department_id = %s ORDER BY id DESC", (dept['id'],))
    dept['econtent'] = dict_from_rows(cur.fetchall(), [d[0] for d in cur.description])
    cur.close()
    conn.close()
    return jsonify(dept)

@app.route('/api/public/all')
def get_all_public():
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM news ORDER BY id DESC")
    news = dict_from_rows(cur.fetchall(), [d[0] for d in cur.description])
    cur.execute("SELECT * FROM events ORDER BY id DESC")
    events = dict_from_rows(cur.fetchall(), [d[0] for d in cur.description])
    cur.execute("SELECT * FROM announcements ORDER BY id DESC")
    announcements = dict_from_rows(cur.fetchall(), [d[0] for d in cur.description])
    cur.execute("SELECT * FROM carousel ORDER BY sort_order ASC")
    carousel = dict_from_rows(cur.fetchall(), [d[0] for d in cur.description])
    cur.execute("SELECT * FROM downloads ORDER BY id DESC")
    downloads = dict_from_rows(cur.fetchall(), [d[0] for d in cur.description])
    cur.execute("SELECT * FROM departments ORDER BY sort_order ASC")
    departments = dict_from_rows(cur.fetchall(), [d[0] for d in cur.description])
    cur.execute("SELECT * FROM site_config WHERE id = 1")
    site_config = dict_from_row(cur.fetchone(), [d[0] for d in cur.description])
    
    cur.close()
    conn.close()
    
    return jsonify({
        'news': news,
        'events': events,
        'announcements': announcements,
        'carousel': carousel,
        'downloads': downloads,
        'departments': departments,
        'site_config': site_config
    })

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400
    
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, email, password_hash, name FROM admin_users WHERE email = %s", (email,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    
    if not row or not bcrypt.check_password_hash(row[2], password):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    access_token = create_access_token(identity=str(row[0]), additional_claims={'email': row[1], 'name': row[3]})
    return jsonify({
        'access_token': access_token,
        'user': {'id': row[0], 'email': row[1], 'name': row[3]}
    })

@app.route('/api/auth/me', methods=['GET'])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, email, name, role FROM admin_users WHERE id = %s", (user_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'id': row[0], 'email': row[1], 'name': row[2], 'role': row[3]})

def admin_required():
    claims = get_jwt()
    if claims.get('email') != 'admin@sgac.edu.in':
        return jsonify({'error': 'Admin access required'}), 403

@app.route('/api/admin/news', methods=['GET'])
@jwt_required()
def admin_news_list():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM news ORDER BY id DESC")
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    cur.close()
    conn.close()
    return jsonify(dict_from_rows(rows, cols))

@app.route('/api/admin/news', methods=['POST'])
@jwt_required()
def admin_news_create():
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO news (title, date, icon) VALUES (%s, %s, %s)",
                (data.get('title', ''), data.get('date', ''), data.get('icon', 'fa-bullhorn')))
    news_id = cur.lastrowid
    conn.commit()
    cur.execute("SELECT * FROM news WHERE id = %s", (news_id,))
    row = cur.fetchone()
    cols = [d[0] for d in cur.description]
    cur.close()
    conn.close()
    return jsonify(dict_from_row(row, cols)), 201

@app.route('/api/admin/news/<int:news_id>', methods=['PUT'])
@jwt_required()
def admin_news_update(news_id):
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE news SET title=%s, date=%s, icon=%s WHERE id=%s",
                (data.get('title'), data.get('date'), data.get('icon'), news_id))
    conn.commit()
    cur.execute("SELECT * FROM news WHERE id = %s", (news_id,))
    row = cur.fetchone()
    cols = [d[0] for d in cur.description]
    cur.close()
    conn.close()
    return jsonify(dict_from_row(row, cols))

@app.route('/api/admin/news/<int:news_id>', methods=['DELETE'])
@jwt_required()
def admin_news_delete(news_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM news WHERE id = %s", (news_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Deleted'})

@app.route('/api/admin/events', methods=['GET'])
@jwt_required()
def admin_events_list():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM events ORDER BY id DESC")
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    cur.close()
    conn.close()
    return jsonify(dict_from_rows(rows, cols))

@app.route('/api/admin/events', methods=['POST'])
@jwt_required()
def admin_events_create():
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO events (title, date, icon) VALUES (%s, %s, %s)",
                (data.get('title', ''), data.get('date', ''), data.get('icon', 'fa-calendar')))
    event_id = cur.lastrowid
    conn.commit()
    cur.execute("SELECT * FROM events WHERE id = %s", (event_id,))
    row = cur.fetchone()
    cols = [d[0] for d in cur.description]
    cur.close()
    conn.close()
    return jsonify(dict_from_row(row, cols)), 201

@app.route('/api/admin/events/<int:event_id>', methods=['PUT'])
@jwt_required()
def admin_events_update(event_id):
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE events SET title=%s, date=%s, icon=%s WHERE id=%s",
                (data.get('title'), data.get('date'), data.get('icon'), event_id))
    conn.commit()
    cur.execute("SELECT * FROM events WHERE id = %s", (event_id,))
    row = cur.fetchone()
    cols = [d[0] for d in cur.description]
    cur.close()
    conn.close()
    return jsonify(dict_from_row(row, cols))

@app.route('/api/admin/events/<int:event_id>', methods=['DELETE'])
@jwt_required()
def admin_events_delete(event_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM events WHERE id = %s", (event_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Deleted'})

@app.route('/api/admin/announcements', methods=['GET'])
@jwt_required()
def admin_announcements_list():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM announcements ORDER BY id DESC")
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    cur.close()
    conn.close()
    return jsonify(dict_from_rows(rows, cols))

@app.route('/api/admin/announcements', methods=['POST'])
@jwt_required()
def admin_announcements_create():
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO announcements (text) VALUES (%s)", (data.get('text', ''),))
    ann_id = cur.lastrowid
    conn.commit()
    cur.execute("SELECT * FROM announcements WHERE id = %s", (ann_id,))
    row = cur.fetchone()
    cols = [d[0] for d in cur.description]
    cur.close()
    conn.close()
    return jsonify(dict_from_row(row, cols)), 201

@app.route('/api/admin/announcements/<int:ann_id>', methods=['PUT'])
@jwt_required()
def admin_announcements_update(ann_id):
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE announcements SET text=%s WHERE id=%s", (data.get('text'), ann_id))
    conn.commit()
    cur.execute("SELECT * FROM announcements WHERE id = %s", (ann_id,))
    row = cur.fetchone()
    cols = [d[0] for d in cur.description]
    cur.close()
    conn.close()
    return jsonify(dict_from_row(row, cols))

@app.route('/api/admin/announcements/<int:ann_id>', methods=['DELETE'])
@jwt_required()
def admin_announcements_delete(ann_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM announcements WHERE id = %s", (ann_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Deleted'})

@app.route('/api/admin/carousel', methods=['GET'])
@jwt_required()
def admin_carousel_list():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM carousel ORDER BY sort_order ASC, id ASC")
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    cur.close()
    conn.close()
    return jsonify(dict_from_rows(rows, cols))

@app.route('/api/admin/carousel', methods=['POST'])
@jwt_required()
def admin_carousel_create():
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT MAX(sort_order) FROM carousel")
    max_order = cur.fetchone()[0] or 0
    cur.execute("INSERT INTO carousel (img, alt, sort_order) VALUES (%s, %s, %s)",
                (data.get('img', ''), data.get('alt', ''), max_order + 1))
    carousel_id = cur.lastrowid
    conn.commit()
    cur.execute("SELECT * FROM carousel WHERE id = %s", (carousel_id,))
    row = cur.fetchone()
    cols = [d[0] for d in cur.description]
    cur.close()
    conn.close()
    return jsonify(dict_from_row(row, cols)), 201

@app.route('/api/admin/carousel/<int:carousel_id>', methods=['PUT'])
@jwt_required()
def admin_carousel_update(carousel_id):
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE carousel SET img=%s, alt=%s WHERE id=%s",
                (data.get('img'), data.get('alt'), carousel_id))
    conn.commit()
    cur.execute("SELECT * FROM carousel WHERE id = %s", (carousel_id,))
    row = cur.fetchone()
    cols = [d[0] for d in cur.description]
    cur.close()
    conn.close()
    return jsonify(dict_from_row(row, cols))

@app.route('/api/admin/carousel/<int:carousel_id>', methods=['DELETE'])
@jwt_required()
def admin_carousel_delete(carousel_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM carousel WHERE id = %s", (carousel_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Deleted'})

@app.route('/api/admin/downloads', methods=['GET'])
@jwt_required()
def admin_downloads_list():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM downloads ORDER BY id DESC")
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    cur.close()
    conn.close()
    return jsonify(dict_from_rows(rows, cols))

@app.route('/api/admin/downloads', methods=['POST'])
@jwt_required()
def admin_downloads_create():
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO downloads (title, link, icon) VALUES (%s, %s, %s)",
                (data.get('title', ''), data.get('link', ''), data.get('icon', 'fa-download')))
    dl_id = cur.lastrowid
    conn.commit()
    cur.execute("SELECT * FROM downloads WHERE id = %s", (dl_id,))
    row = cur.fetchone()
    cols = [d[0] for d in cur.description]
    cur.close()
    conn.close()
    return jsonify(dict_from_row(row, cols)), 201

@app.route('/api/admin/downloads/<int:dl_id>', methods=['PUT'])
@jwt_required()
def admin_downloads_update(dl_id):
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE downloads SET title=%s, link=%s, icon=%s WHERE id=%s",
                (data.get('title'), data.get('link'), data.get('icon'), dl_id))
    conn.commit()
    cur.execute("SELECT * FROM downloads WHERE id = %s", (dl_id,))
    row = cur.fetchone()
    cols = [d[0] for d in cur.description]
    cur.close()
    conn.close()
    return jsonify(dict_from_row(row, cols))

@app.route('/api/admin/downloads/<int:dl_id>', methods=['DELETE'])
@jwt_required()
def admin_downloads_delete(dl_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM downloads WHERE id = %s", (dl_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Deleted'})

@app.route('/api/admin/departments', methods=['GET'])
@jwt_required()
def admin_departments_list():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM departments ORDER BY sort_order ASC, id ASC")
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    cur.close()
    conn.close()
    return jsonify(dict_from_rows(rows, cols))

@app.route('/api/admin/departments', methods=['POST'])
@jwt_required()
def admin_departments_create():
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT MAX(sort_order) FROM departments")
    max_order = cur.fetchone()[0] or 0
    cur.execute("""INSERT INTO departments (dept_key, name, icon, about, vision, mission, hod_name, hod_designation, hod_qualification, hod_email, hod_phone, sort_order)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (data.get('dept_key', ''), data.get('name', ''), data.get('icon', 'fa-book'),
                 data.get('about', ''), data.get('vision', ''), data.get('mission', ''),
                 data.get('hod_name', ''), data.get('hod_designation', ''), data.get('hod_qualification', ''),
                 data.get('hod_email', ''), data.get('hod_phone', ''), max_order + 1))
    dept_id = cur.lastrowid
    conn.commit()
    cur.execute("SELECT * FROM departments WHERE id = %s", (dept_id,))
    row = cur.fetchone()
    cols = [d[0] for d in cur.description]
    cur.close()
    conn.close()
    return jsonify(dict_from_row(row, cols)), 201

@app.route('/api/admin/departments/<int:dept_id>', methods=['PUT'])
@jwt_required()
def admin_departments_update(dept_id):
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""UPDATE departments SET name=%s, icon=%s, about=%s, vision=%s, mission=%s,
                    hod_name=%s, hod_designation=%s, hod_qualification=%s, hod_email=%s, hod_phone=%s WHERE id=%s""",
                (data.get('name'), data.get('icon'), data.get('about'), data.get('vision'), data.get('mission'),
                 data.get('hod_name'), data.get('hod_designation'), data.get('hod_qualification'),
                 data.get('hod_email'), data.get('hod_phone'), dept_id))
    conn.commit()
    cur.execute("SELECT * FROM departments WHERE id = %s", (dept_id,))
    row = cur.fetchone()
    cols = [d[0] for d in cur.description]
    cur.close()
    conn.close()
    return jsonify(dict_from_row(row, cols))

@app.route('/api/admin/departments/<int:dept_id>', methods=['DELETE'])
@jwt_required()
def admin_departments_delete(dept_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM departments WHERE id = %s", (dept_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Deleted'})

@app.route('/api/admin/departments/<int:dept_id>/faculty', methods=['GET'])
@jwt_required()
def admin_faculty_list(dept_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM faculty WHERE department_id = %s ORDER BY sort_order ASC", (dept_id,))
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    cur.close()
    conn.close()
    return jsonify(dict_from_rows(rows, cols))

@app.route('/api/admin/faculty', methods=['POST'])
@jwt_required()
def admin_faculty_create():
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT MAX(sort_order) FROM faculty WHERE department_id = %s", (data.get('department_id'),))
    max_order = cur.fetchone()[0] or 0
    cur.execute("""INSERT INTO faculty (department_id, name, designation, qualification, email, phone, sort_order)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (data.get('department_id'), data.get('name', ''), data.get('designation', ''),
                 data.get('qualification', ''), data.get('email', ''), data.get('phone', ''), max_order + 1))
    fac_id = cur.lastrowid
    conn.commit()
    cur.execute("SELECT * FROM faculty WHERE id = %s", (fac_id,))
    row = cur.fetchone()
    cols = [d[0] for d in cur.description]
    cur.close()
    conn.close()
    return jsonify(dict_from_row(row, cols)), 201

@app.route('/api/admin/faculty/<int:fac_id>', methods=['PUT'])
@jwt_required()
def admin_faculty_update(fac_id):
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""UPDATE faculty SET name=%s, designation=%s, qualification=%s, email=%s, phone=%s WHERE id=%s""",
                (data.get('name'), data.get('designation'), data.get('qualification'),
                 data.get('email'), data.get('phone'), fac_id))
    conn.commit()
    cur.execute("SELECT * FROM faculty WHERE id = %s", (fac_id,))
    row = cur.fetchone()
    cols = [d[0] for d in cur.description]
    cur.close()
    conn.close()
    return jsonify(dict_from_row(row, cols))

@app.route('/api/admin/faculty/<int:fac_id>', methods=['DELETE'])
@jwt_required()
def admin_faculty_delete(fac_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM faculty WHERE id = %s", (fac_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Deleted'})

@app.route('/api/admin/gallery', methods=['GET'])
@jwt_required()
def admin_gallery_list():
    dept_id = request.args.get('dept')
    conn = get_db()
    cur = conn.cursor()
    if dept_id:
        cur.execute("SELECT * FROM gallery WHERE department_id = %s ORDER BY sort_order ASC", (dept_id,))
    else:
        cur.execute("SELECT * FROM gallery ORDER BY sort_order ASC")
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    cur.close()
    conn.close()
    return jsonify(dict_from_rows(rows, cols))

@app.route('/api/admin/gallery', methods=['POST'])
@jwt_required()
def admin_gallery_create():
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT MAX(sort_order) FROM gallery WHERE department_id = %s", (data.get('department_id'),))
    max_order = cur.fetchone()[0] or 0
    cur.execute("INSERT INTO gallery (department_id, src, caption, sort_order) VALUES (%s, %s, %s, %s)",
                (data.get('department_id'), data.get('src', ''), data.get('caption', ''), max_order + 1))
    gal_id = cur.lastrowid
    conn.commit()
    cur.execute("SELECT * FROM gallery WHERE id = %s", (gal_id,))
    row = cur.fetchone()
    cols = [d[0] for d in cur.description]
    cur.close()
    conn.close()
    return jsonify(dict_from_row(row, cols)), 201

@app.route('/api/admin/gallery/<int:gal_id>', methods=['DELETE'])
@jwt_required()
def admin_gallery_delete(gal_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM gallery WHERE id = %s", (gal_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Deleted'})

@app.route('/api/admin/activities', methods=['POST'])
@jwt_required()
def admin_activities_create():
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO activities (department_id, title, description, date) VALUES (%s, %s, %s, %s)",
                (data.get('department_id'), data.get('title', ''), data.get('description', ''), data.get('date', '')))
    act_id = cur.lastrowid
    conn.commit()
    cur.execute("SELECT * FROM activities WHERE id = %s", (act_id,))
    row = cur.fetchone()
    cols = [d[0] for d in cur.description]
    cur.close()
    conn.close()
    return jsonify(dict_from_row(row, cols)), 201

@app.route('/api/admin/activities/<int:act_id>', methods=['DELETE'])
@jwt_required()
def admin_activities_delete(act_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM activities WHERE id = %s", (act_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Deleted'})

@app.route('/api/admin/achievements', methods=['POST'])
@jwt_required()
def admin_achievements_create():
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO achievements (department_id, title, description, student_name) VALUES (%s, %s, %s, %s)",
                (data.get('department_id'), data.get('title', ''), data.get('description', ''), data.get('student_name', '')))
    ach_id = cur.lastrowid
    conn.commit()
    cur.execute("SELECT * FROM achievements WHERE id = %s", (ach_id,))
    row = cur.fetchone()
    cols = [d[0] for d in cur.description]
    cur.close()
    conn.close()
    return jsonify(dict_from_row(row, cols)), 201

@app.route('/api/admin/achievements/<int:ach_id>', methods=['DELETE'])
@jwt_required()
def admin_achievements_delete(ach_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM achievements WHERE id = %s", (ach_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Deleted'})

@app.route('/api/admin/econtent', methods=['POST'])
@jwt_required()
def admin_econtent_create():
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO econtent (department_id, title, link, description) VALUES (%s, %s, %s, %s)",
                (data.get('department_id'), data.get('title', ''), data.get('link', ''), data.get('description', '')))
    ec_id = cur.lastrowid
    conn.commit()
    cur.execute("SELECT * FROM econtent WHERE id = %s", (ec_id,))
    row = cur.fetchone()
    cols = [d[0] for d in cur.description]
    cur.close()
    conn.close()
    return jsonify(dict_from_row(row, cols)), 201

@app.route('/api/admin/econtent/<int:ec_id>', methods=['DELETE'])
@jwt_required()
def admin_econtent_delete(ec_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM econtent WHERE id = %s", (ec_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Deleted'})

@app.route('/api/admin/site-config', methods=['GET', 'PUT'])
@jwt_required()
def admin_site_config():
    conn = get_db()
    cur = conn.cursor()
    if request.method == 'GET':
        cur.execute("SELECT * FROM site_config WHERE id = 1")
        row = cur.fetchone()
        cols = [d[0] for d in cur.description]
        cur.close()
        conn.close()
        return jsonify(dict_from_row(row, cols) or {})
    else:
        data = request.get_json()
        cur.execute("""UPDATE site_config SET college_name=%s, college_name_tamil=%s, address=%s, naac_grade=%s,
                        affiliated_to=%s, email=%s, phone=%s, principal_name=%s, principal_qualification=%s WHERE id=1""",
                    (data.get('college_name'), data.get('college_name_tamil'), data.get('address'),
                     data.get('naac_grade'), data.get('affiliated_to'), data.get('email'),
                     data.get('phone'), data.get('principal_name'), data.get('principal_qualification')))
        conn.commit()
        cur.execute("SELECT * FROM site_config WHERE id = 1")
        row = cur.fetchone()
        cols = [d[0] for d in cur.description]
        cur.close()
        conn.close()
        return jsonify(dict_from_row(row, cols))

@app.route('/api/admin/stats')
@jwt_required()
def admin_stats():
    conn = get_db()
    cur = conn.cursor()
    stats = {}
    tables = ['news', 'events', 'announcements', 'carousel', 'downloads', 'departments']
    for table in tables:
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        stats[table] = cur.fetchone()[0]
    cur.close()
    conn.close()
    return jsonify(stats)

@app.route('/api/admin/password', methods=['POST'])
@jwt_required()
def change_password():
    data = request.get_json()
    current = data.get('current_password', '')
    new_pw = data.get('new_password', '')
    if not current or not new_pw:
        return jsonify({'error': 'Both passwords required'}), 400
    if len(new_pw) < 6:
        return jsonify({'error': 'New password must be at least 6 characters'}), 400
    user_id = get_jwt_identity()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT password_hash FROM admin_users WHERE id = %s", (user_id,))
    row = cur.fetchone()
    if not row or not bcrypt.check_password_hash(row[0], current):
        cur.close()
        conn.close()
        return jsonify({'error': 'Current password is incorrect'}), 401
    new_hash = bcrypt.generate_password_hash(new_pw).decode('utf-8')
    cur.execute("UPDATE admin_users SET password_hash = %s WHERE id = %s", (new_hash, user_id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Password changed successfully'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
