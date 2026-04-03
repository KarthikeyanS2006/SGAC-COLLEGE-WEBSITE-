import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_bcrypt import Bcrypt
from datetime import timedelta
import mysql.connector

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'sgac-secret-2026')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-2026')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

def get_db_config():
    return {
        'host': os.getenv('DB_HOST', 'mysql-3c95dc03-keyan.h.aivencloud.com'),
        'port': int(os.getenv('DB_PORT', 12610)),
        'user': os.getenv('DB_USER', 'avnadmin'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'defaultdb'),
        'charset': 'utf8mb4'
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
            result = [dict(zip(cols, row)) for row in rows]
            cur.close()
            conn.close()
            return result, None
        conn.commit()
        lastid = cur.lastrowid
        cur.close()
        conn.close()
        return lastid, None
    except Exception as e:
        conn.close()
        return None, str(e)

def query_one(sql, params=None):
    result, err = query(sql, params)
    if result:
        return result[0] if result else None, None
    return None, err

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
        conn.close()
        return None, str(e)

TABLES = [
    '''CREATE TABLE IF NOT EXISTS admin_users (id INT AUTO_INCREMENT PRIMARY KEY, email VARCHAR(255) UNIQUE NOT NULL, password_hash VARCHAR(255) NOT NULL, name VARCHAR(255) DEFAULT 'Admin', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''',
    '''CREATE TABLE IF NOT EXISTS news (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(500) NOT NULL, date VARCHAR(100) DEFAULT '', icon VARCHAR(100) DEFAULT 'fa-bullhorn', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''',
    '''CREATE TABLE IF NOT EXISTS events (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(500) NOT NULL, date VARCHAR(100) DEFAULT '', icon VARCHAR(100) DEFAULT 'fa-calendar', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''',
    '''CREATE TABLE IF NOT EXISTS announcements (id INT AUTO_INCREMENT PRIMARY KEY, text TEXT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''',
    '''CREATE TABLE IF NOT EXISTS carousel (id INT AUTO_INCREMENT PRIMARY KEY, img VARCHAR(1000) NOT NULL, alt VARCHAR(500) DEFAULT '', sort_order INT DEFAULT 0, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''',
    '''CREATE TABLE IF NOT EXISTS downloads (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(500) NOT NULL, link VARCHAR(1000) DEFAULT '', icon VARCHAR(100) DEFAULT 'fa-download', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''',
    '''CREATE TABLE IF NOT EXISTS departments (id INT AUTO_INCREMENT PRIMARY KEY, dept_key VARCHAR(100) UNIQUE NOT NULL, name VARCHAR(255) NOT NULL, icon VARCHAR(100) DEFAULT 'fa-book', about TEXT DEFAULT '', vision TEXT DEFAULT '', mission TEXT DEFAULT '', hod_name VARCHAR(255) DEFAULT '', hod_designation VARCHAR(255) DEFAULT '', hod_qualification VARCHAR(255) DEFAULT '', hod_email VARCHAR(255) DEFAULT '', hod_phone VARCHAR(50) DEFAULT '', sort_order INT DEFAULT 0, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''',
    '''CREATE TABLE IF NOT EXISTS faculty (id INT AUTO_INCREMENT PRIMARY KEY, department_id INT NOT NULL, name VARCHAR(255) NOT NULL, designation VARCHAR(255) DEFAULT '', qualification VARCHAR(500) DEFAULT '', email VARCHAR(255) DEFAULT '', phone VARCHAR(50) DEFAULT '', sort_order INT DEFAULT 0, FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE CASCADE)''',
    '''CREATE TABLE IF NOT EXISTS site_config (id INT PRIMARY KEY DEFAULT 1, college_name VARCHAR(500) DEFAULT 'Sethupathy Government Arts College', college_name_tamil VARCHAR(500) DEFAULT '', address VARCHAR(500) DEFAULT 'Ramanathapuram', naac_grade VARCHAR(20) DEFAULT 'B', affiliated_to VARCHAR(500) DEFAULT 'Alagappa University', email VARCHAR(255) DEFAULT 'admin@sgac.edu.in', phone VARCHAR(50) DEFAULT '+91-4567-221343')'''
]

ALTERS = [
    'ALTER TABLE departments ADD COLUMN about TEXT',
    'ALTER TABLE departments ADD COLUMN vision TEXT',
    'ALTER TABLE departments ADD COLUMN mission TEXT',
    'ALTER TABLE departments ADD COLUMN hod_name VARCHAR(255)',
    'ALTER TABLE departments ADD COLUMN hod_designation VARCHAR(255)',
    'ALTER TABLE departments ADD COLUMN hod_qualification VARCHAR(255)',
    'ALTER TABLE departments ADD COLUMN hod_email VARCHAR(255)',
    'ALTER TABLE departments ADD COLUMN hod_phone VARCHAR(50)',
]

for sql in TABLES:
    try:
        execute(sql)
    except:
        pass

for sql in ALTERS:
    try:
        execute(sql)
    except:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/api/health')
def health():
    return jsonify({'status': 'ok'})

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

@app.route('/api/auth/setup', methods=['POST'])
def setup():
    pw = bcrypt.generate_password_hash('sgac2025').decode('utf-8')
    id, err = execute("INSERT INTO admin_users (email, password_hash) VALUES (%s, %s)", ('admin@sgac.edu.in', pw))
    if err:
        if 'Duplicate' in str(err):
            return jsonify({'message': 'Admin already exists'})
        return jsonify({'error': err}), 500
    return jsonify({'message': 'Admin created'})

@app.route('/api/auth/reset-admin', methods=['POST'])
def reset_admin():
    execute("DELETE FROM admin_users WHERE email = %s", ('admin@sgac.edu.in',))
    pw = bcrypt.generate_password_hash('sgac2025').decode('utf-8')
    id, err = execute("INSERT INTO admin_users (email, password_hash) VALUES (%s, %s)", ('admin@sgac.edu.in', pw))
    if err:
        return jsonify({'error': err}), 500
    return jsonify({'message': 'Admin reset successfully', 'email': 'admin@sgac.edu.in', 'password': 'sgac2025'})

@app.route('/api/auth/setup-config', methods=['POST'])
def setup_config():
    _, err = execute("INSERT INTO site_config (id) VALUES (1)")
    if err and 'Duplicate' not in str(err):
        return jsonify({'error': err}), 500
    return jsonify({'message': 'Config created'})

@app.route('/api/auth/seed-full', methods=['POST'])
def seed_full():
    results = []
    execute("DELETE FROM faculty")
    execute("DELETE FROM departments")
    
    dept_data = [
        ('tamil', 'Tamil', 'fa-language', 
         'The Department of Tamil at Sethupathy Government Arts College is dedicated to preserving and promoting the rich heritage of Tamil language and literature.',
         'To be a center of excellence in Tamil language, literature, and cultural studies.',
         'To provide quality education in Tamil and preserve the rich linguistic and cultural heritage.',
         'Dr. M. Senthamarai', 'Assistant Professor & HOD', 'M.A., M.Phil., Ph.D.', 'tamil.hod@sgac.edu.in', '+91-4567-221343'),
        ('english', 'English', 'fa-book-open',
         'The Department of English is dedicated to fostering excellence in English language, literature, and communication skills.',
         'To be a center of excellence in English language and literature studies, nurturing critical thinkers and effective communicators.',
         'To provide quality education in English literature and language, fostering research, creativity, and global perspectives.',
         'Dr. K. Jeyamurugan', 'Assistant Professor & HOD', 'M.A., M.Phil., Ph.D.', 'english.hod@sgac.edu.in', '+91-4567-221343'),
        ('commerce', 'Commerce', 'fa-calculator',
         'Department of Commerce was started in the very first year of inception of the college. The prime motto is to equip students for self-sustainability.',
         'As the destination is beautiful, need not worry about the path.',
         'Walking with the wards - providing quality education and mentorship to shape future commerce professionals.',
         'Dr. K. Muthalagu', 'Head of Department', 'M.Com., M.Phil., Ph.D.', 'commerce.hod@sgac.edu.in', '+91-4567-221343'),
        ('computer-science', 'Computer Science', 'fa-laptop',
         'Learn programming, software development, and IT solutions to excel in the digital technology era.',
         'To be a center of excellence in Computer Science studies, nurturing skilled professionals and researchers.',
         'To provide quality education in Computer Science, fostering research, innovation, and global perspectives.',
         'Dr. K. Rathidevi', 'HOD I/C', 'M.Sc., M.Phil., Ph.D.', 'computerscience.hod@sgac.edu.in', '+91-4567-221343'),
        ('mathematics', 'Mathematics', 'fa-square-root-alt',
         'Develop analytical and problem-solving skills through pure and applied mathematics, preparing for careers in research and industry.',
         'To be a center of excellence in Mathematics studies, nurturing skilled professionals and researchers.',
         'To provide quality education in Mathematics, fostering research, innovation, and global perspectives.',
         'Prof. C. Shanmuga Vadivu', 'Head of Department', 'M.Sc., M.Phil., B.Ed., Ph.D., PGDCA', 'mathematics.hod@sgac.edu.in', '+91-4567-221343'),
        ('physics', 'Physics', 'fa-atom',
         'Understand the fundamental laws of nature and explore the mysteries of the universe through theoretical and experimental physics.',
         'To be a center of excellence in Physics studies, nurturing skilled professionals and researchers.',
         'To provide quality education in Physics, fostering research, innovation, and global perspectives.',
         'B. Senthil', 'Assistant Professor & HOD', 'M.Sc., M.Phil.', 'physics.hod@sgac.edu.in', '+91-4567-221343'),
        ('chemistry', 'Chemistry', 'fa-flask',
         'Explore the composition, structure, properties, and changes of matter through comprehensive chemistry programs.',
         'To be a center of excellence in Chemistry studies, nurturing skilled professionals and researchers.',
         'To provide quality education in Chemistry, fostering research, innovation, and global perspectives.',
         'Dr. N. Uma Sankari', 'Associate Professor & HOD', 'M.Sc., M.Phil., Ph.D.', 'chem.hod@sgac.edu.in', '+91-4567-221343'),
        ('botany', 'Botany', 'fa-leaf',
         'Study plant life, ecology, and environmental sciences for sustainable development and biodiversity conservation.',
         'To be a center of excellence in Botany studies, nurturing skilled professionals and researchers.',
         'To provide quality education in Botany, fostering research, innovation, and global perspectives.',
         'Dr. K. Raveendra Rethnam', 'Assistant Professor & HOD', 'M.Sc., M.Phil., Ph.D.', 'botany.hod@sgac.edu.in', '+91-9442-077661'),
        ('zoology', 'Zoology', 'fa-paw',
         'Discover animal biology, behavior, biodiversity, and conservation through field studies and laboratory research.',
         'To be a center of excellence in Zoology studies, nurturing skilled professionals and researchers.',
         'To provide quality education in Zoology, fostering research, innovation, and global perspectives.',
         'Dr. V. Sivakumaran', 'Assistant Professor & HOD', 'M.Sc.(Zoo), M.Sc.(Micro), Ph.D., M.Ed., D.Sc.', 'zoology.hod@sgac.edu.in', '+91-4567-221343'),
        ('economics', 'Economics', 'fa-chart-line',
         'Study economic theories, policies, and market dynamics to understand global economies and financial systems.',
         'To be a center of excellence in Economics studies, nurturing skilled professionals and researchers.',
         'To provide quality education in Economics, fostering research, innovation, and global perspectives.',
         'Dr. K. Ramakrishnan', 'Associate Professor & HOD', 'M.A., M.Phil., M.B.A., Ph.D., PGDCA', 'economics.hod@sgac.edu.in', '+91-4567-221343'),
        ('history', 'History', 'fa-landmark',
         'Explore historical events, civilizations, and cultural heritage to understand the evolution of human society.',
         'To be a center of excellence in History studies, nurturing skilled professionals and researchers.',
         'To provide quality education in History, fostering research, innovation, and global perspectives.',
         'Dr. R. Murugan', 'Associate Professor & HOD', 'M.A., M.Phil., Ph.D.', 'history.hod@sgac.edu.in', '+91-4567-221343'),
        ('marine-biology', 'Marine Biology', 'fa-fish',
         'Study marine ecosystems, organisms, and oceanography to understand and protect oceanic life.',
         'To be a center of excellence in Marine Biology studies, nurturing skilled professionals and researchers.',
         'To provide quality education in Marine Biology, fostering research, innovation, and global perspectives.',
         'Dr. M.A. Badhul Haq', 'Assistant Professor & HOD', 'M.Sc., Ph.D.', 'marinebiology.hod@sgac.edu.in', '+91-4567-221343'),
        ('commerce-ca', 'Commerce (CA)', 'fa-desktop',
         'Integrate commerce with modern computer applications and technology for the digital business era.',
         'To be a center of excellence in Commerce (Computer Applications) studies.',
         'To provide quality education in Commerce with Computer Applications, fostering research and innovation.',
         'Dr. N. Kesavan', 'Head of Department', 'M.Com., M.B.A., PGDCA., Ph.D.', 'commerceca.hod@sgac.edu.in', '+91-4567-221343'),
    ]
    
    faculty_data = {
        'tamil': [
            ('Dr. M. Senthamarai', 'Head of Department, Assistant Professor', 'M.A., M.Phil., Ph.D.', 'tamil.hod@sgac.edu.in', ''),
            ('Dr. Muthuraman.S', 'Guest Lecturer', 'M.A., M.Phil.', '', ''),
            ('Dr. Poornayogarani.K', 'Guest Lecturer', 'M.A., M.Phil., Ph.D.', '', ''),
            ('Dr. Ramamurthy.S', 'Guest Lecturer', 'M.A., M.Phil., Ph.D.', '', ''),
            ('Dr. Paul Murugan.V', 'Guest Lecturer', 'M.A., M.Phil., Ph.D.', '', ''),
            ('Dr. Rajasekar.A', 'Guest Lecturer', 'M.A., B.Ed., M.Phil., Ph.D.', '', ''),
            ('Dr. Nagapandi.M', 'Guest Lecturer', 'M.A., B.Ed., M.Phil., Ph.D., PGDSA.', '', ''),
            ('Dr. Alagumurugan.M', 'Guest Lecturer', 'M.A., M.Phil., Ph.D.', '', ''),
            ('Dr. Syed Kasim.M', 'Guest Lecturer', 'M.A., M.Phil., Ph.D.', '', ''),
        ],
        'english': [
            ('Dr. K. Jeyamurugan', 'Head of Department, Assistant Professor', 'M.A., M.Phil., Ph.D.', 'english.hod@sgac.edu.in', ''),
            ('Barakkathu Nisha.T.A', 'Guest Lecturer', 'M.A., M.Phil., SET, NET', '', ''),
            ('Dr. Suthanthira Jothi.D', 'Guest Lecturer', 'M.A., M.Phil., B.Ed.', '', ''),
            ('Dr. Nagarajan.K', 'Guest Lecturer', 'M.A., M.Ed., M.Phil.', '', ''),
            ('Dr. Martin Prabahar.J', 'Guest Lecturer', 'M.A., B.Ed., M.Phil., Ph.D.', '', ''),
            ('Dr. Raihana Barvin.A', 'Guest Lecturer', 'M.A., M.Phil., Ph.D.', '', ''),
            ('Dr. Prema Latha.M', 'Guest Lecturer', 'M.A., M.Ed., Ph.D.', '', ''),
            ('Dr. Seeni Sulthan Ibrahim.M', 'Guest Lecturer', 'M.A., M.Phil., B.Ed., Ph.D.', '', ''),
        ],
        'commerce': [
            ('Dr. K. Muthalagu', 'Head of Department', 'M.Com., M.Phil., Ph.D.', 'commerce.hod@sgac.edu.in', ''),
            ('Dr. N. Kesavan', 'Associate Professor', 'M.COM., M.B.A., M.Phil., Ph.D., PGDCA', '', ''),
            ('Dr. Namburajan.N', 'Guest Lecturer', 'M.COM., M.Phil., B.Ed., PGDCS., Ph.D.', '', ''),
            ('Dr. Muneeswaran.K', 'Guest Lecturer', 'M.COM., M.Phil., Ph.D., M.Com(PSTM)., PGDCA., PGDCM., PGDMM', '', ''),
            ('Dr. Ramachandran.R', 'Guest Lecturer', 'M.COM(CA)., MBA., M.Ed., M.Phil., Ph.D.', '', ''),
            ('Dr. Ravi.S', 'Guest Lecturer', 'M.COM(CA), M.Phil., SET., Ph.D., DCBA., DCE', '', ''),
            ('Dr. Vasuki.P', 'Guest Lecturer', 'M.COM., M.Phil., Ph.D.', '', ''),
            ('Dr. Dharmendran', 'Guest Lecturer', 'M.COM., M.COM(CA)., M.Phil., Ph.D.', '', ''),
        ],
        'computer-science': [
            ('Dr. K. Rathidevi', 'HOD I/C', 'M.Sc., M.Phil., Ph.D.', 'computerscience.hod@sgac.edu.in', ''),
            ('Fathima Zahira.M', 'Guest Lecturer', 'M.Sc., M.Phil., Ph.D., B.Ed.', '', ''),
            ('Kalaiselvi.V', 'Guest Lecturer', 'M.Sc., B.Ed., M.Phil., SET', '', ''),
        ],
        'mathematics': [
            ('Prof. C. Shanmuga Vadivu', 'Head of Department', 'M.Sc., M.Phil., B.Ed., Ph.D., PGDCA', 'mathematics.hod@sgac.edu.in', ''),
            ('Prof. G. Chandra Sekaran', 'Associate Professor', 'M.Sc., M.Phil., B.Ed., SET, Ph.D.', '', ''),
            ('Prof. M. Malarvannan', 'Assistant Professor', 'M.Sc., B.Ed., M.Phil.', '', ''),
            ('Dr. G. Bharathi', 'Assistant Professor', 'M.Sc., M.Phil., B.Ed., SET, Ph.D.', '', ''),
            ('Dr. S. Naganathan', 'Assistant Professor', 'M.Sc., M.Phil., Ph.D.', '', ''),
            ('Prof. K. Senthil', 'Assistant Professor', 'M.Sc., M.Phil., Ph.D.', '', ''),
            ('Dr. S. Loganathan', 'Assistant Professor', 'M.Sc., M.Phil., Ph.D., PGDCA.', '', ''),
        ],
        'physics': [
            ('B. Senthil', 'Head of Department, Assistant Professor', 'M.Sc., M.Phil.', 'physics.hod@sgac.edu.in', ''),
            ('Dr. K. Rathidevi', 'Associate Professor', 'M.Sc., M.Phil., Ph.D.', '', ''),
            ('Prof. K. Usha', 'Assistant Professor', 'M.Sc., M.Phil.', '', ''),
            ('Dr. Saravankumar.S.S', 'Guest Lecturer', 'M.Sc., M.Phil., MCA., B.Ed.', '', ''),
            ('Dr. Shanthi.M', 'Guest Lecturer', 'M.Sc., M.Phil.', '', ''),
            ('Dr. Mohandoss.S', 'Guest Lecturer', 'M.Sc., B.Ed., M.Phil., Ph.D.', '', ''),
            ('Dr. Muthukrishnan.U', 'Guest Lecturer', 'M.Sc., M.Phil., M.Ed.', '', ''),
        ],
        'chemistry': [
            ('Dr. N. Uma Sankari', 'Head of Department, Associate Professor', 'M.Sc., M.Phil., Ph.D.', 'chem.hod@sgac.edu.in', ''),
            ('Dr. Paul Pandi.P', 'Guest Lecturer', 'M.Sc., M.Phil., B.Ed., SET', '', ''),
            ('Dr. Rajiv Gandhi.N', 'Guest Lecturer', 'M.Sc., M.Ed., M.Phil.', '', ''),
            ('Dr. Marlin Risana.M', 'Guest Lecturer', 'M.Sc., M.Phil., B.Ed., SET', '', ''),
            ('Dr. Jeya Shree.G', 'Guest Lecturer', 'M.Sc., M.Phil., Ph.D.', '', ''),
            ('Dr. Prakash.S', 'Guest Lecturer', 'M.Sc., M.Phil., Ph.D.', '', ''),
            ('Dr. Sivaranjini.P', 'Guest Lecturer', 'M.Sc., M.Phil., Ph.D.', '', ''),
        ],
        'botany': [
            ('Dr. K. Raveendra Rethnam', 'Head of Department, Assistant Professor', 'M.Sc., M.Phil., Ph.D.', 'botany.hod@sgac.edu.in', '+91-9442-077661'),
            ('Dr. M. Uthiraselvam', 'Assistant Professor', 'M.Sc., M.Phil., Ph.D.', '', ''),
            ('Dr. L. Karikalan', 'Assistant Professor', 'M.Sc., M.Phil., Ph.D., B.Ed., B.L.I.Sc.', '', ''),
            ('Dr. Parvathy.T', 'Guest Lecturer', 'M.Sc., M.Phil., B.Ed., Ph.D.', '', ''),
            ('Dr. Sheik Jahabar Ali.H', 'Guest Lecturer', 'M.Sc., Ph.D., HDCA.', '', ''),
        ],
        'zoology': [
            ('Dr. V. Sivakumaran', 'Head of Department, Assistant Professor', 'M.Sc.(Zoo), M.Sc.(Micro), Ph.D., M.Ed., D.Sc.', 'zoology.hod@sgac.edu.in', ''),
            ('Dr. Viveka.S', 'Assistant Professor', 'M.Sc., M.Tech., Ph.D.', '', ''),
            ('Dr. P. Mayavu', 'Associate Professor', 'M.Sc., M.Phil., Ph.D.', '', ''),
            ('Dr. Maheshkumar.P', 'Guest Lecturer', 'M.Sc., M.Phil., Ph.D.', '', ''),
            ('Dr. Sureshkumar.J', 'Guest Lecturer', 'M.Sc., B.Ed., M.Phil., MCA., SET', '', ''),
            ('Dr. Dinesh Kumar.G', 'Guest Lecturer', 'M.Sc., M.Phil., Ph.D.', '', ''),
        ],
        'economics': [
            ('Dr. K. Ramakrishnan', 'Head of Department, Associate Professor', 'M.A., M.Phil., M.B.A., Ph.D., PGDCA.', 'economics.hod@sgac.edu.in', ''),
            ('Dr. K. Mani Raju', 'Associate Professor', 'M.A., M.Phil., Ph.D., B.Ed.', '', ''),
            ('Dr. A. Logu', 'Assistant Professor', 'M.A., M.Phil., Ph.D.', '', ''),
            ('Dr. G. Kumar', 'Assistant Professor', 'M.A., M.Phil., Ph.D.', '', ''),
            ('Ambedkar.V', 'Guest Lecturer', 'M.A., M.Phil., Ph.D., B.Ed., D.Cop., CGT.', '', ''),
            ('Ilavarasan.R', 'Guest Lecturer', 'M.A., M.Phil., Ph.D., DIT., B.Ed.', '', ''),
            ('Shamsudeen.S', 'Guest Lecturer', 'M.A., M.Phil., Ph.D., B.Ed.', '', ''),
        ],
        'marine-biology': [
            ('Dr. M.A. Badhul Haq', 'Head of Department, Assistant Professor', 'M.Sc., Ph.D.', 'marinebiology.hod@sgac.edu.in', ''),
            ('Dr. Elangovan.M', 'Guest Lecturer', 'M.Sc., Ph.D.', '', ''),
            ('Dr. Kalaiyarasi.M', 'Guest Lecturer', 'M.Sc., M.Phil., Ph.D.', '', ''),
            ('Dr. Santhanakrishnan.M', 'Guest Lecturer', 'M.Sc., Ph.D.', '', ''),
        ],
        'commerce-ca': [
            ('Dr. N. Kesavan', 'Head of Department', 'M.Com., M.B.A., PGDCA., Ph.D.', 'commerceca.hod@sgac.edu.in', ''),
            ('Dr. P. Sundara Pandian', 'Guest Lecturer Shift - I', 'M.COM(CA), M.Phil., SET', '', ''),
            ('Dr. B. Gomathi Jaya', 'Guest Lecturer Shift - II', 'M.COM(CA), M.Phil., B.Ed., Ph.D.', '', ''),
            ('Dr. Kokila Mani Devi', 'PTA Teacher', 'M.Com., M.Phil., Ph.D.', '', ''),
        ],
    }
    
    for d in dept_data:
        dept_key, name, icon, about, vision, mission, hod_name, hod_desig, hod_qual, hod_email, hod_phone = d
        id, err = execute("""INSERT INTO departments (dept_key, name, icon, about, vision, mission, hod_name, hod_designation, hod_qualification, hod_email, hod_phone) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
            (dept_key, name, icon, about, vision, mission, hod_name, hod_desig, hod_qual, hod_email, hod_phone))
        if err:
            results.append(f"Dept {name}: {err}")
        else:
            results.append(f"Dept '{name}': Added with HOD")
            if dept_key in faculty_data:
                for fac in faculty_data[dept_key]:
                    fname, fdesig, fqual, femail, fphone = fac
                    fid, ferr = execute("INSERT INTO faculty (department_id, name, designation, qualification, email, phone) VALUES (%s, %s, %s, %s, %s, %s)",
                        (id, fname, fdesig, fqual, femail, fphone))
                    if ferr:
                        results.append(f"  Faculty {fname}: {ferr}")
                    else:
                        results.append(f"  Faculty '{fname}': Added")
    
    return jsonify({'message': 'Full seed completed', 'results': results})

@app.route('/api/public/all')
def get_all():
    news, _ = query("SELECT * FROM news ORDER BY id DESC")
    events, _ = query("SELECT * FROM events ORDER BY id DESC")
    announcements, _ = query("SELECT * FROM announcements ORDER BY id DESC")
    carousel, _ = query("SELECT * FROM carousel ORDER BY sort_order ASC")
    downloads, _ = query("SELECT * FROM downloads ORDER BY id DESC")
    departments, _ = query("SELECT * FROM departments ORDER BY sort_order ASC")
    site_config, _ = query_one("SELECT * FROM site_config WHERE id = 1")
    return jsonify({
        'news': news or [], 'events': events or [], 'announcements': announcements or [],
        'carousel': carousel or [], 'downloads': downloads or [],
        'departments': departments or [], 'site_config': site_config or {}
    })

@app.route('/api/public/departments/<key>')
def get_department(key):
    dept, _ = query_one("SELECT * FROM departments WHERE dept_key = %s", (key,))
    if not dept:
        return jsonify({'error': 'Department not found'}), 404
    faculty, _ = query("SELECT * FROM faculty WHERE department_id = %s ORDER BY sort_order ASC", (dept['id'],))
    return jsonify({**dept, 'faculty': faculty or []})

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
    cols = ['college_name', 'college_name_tamil', 'address', 'naac_grade', 'affiliated_to', 'email', 'phone']
    sets = ', '.join([f"{c} = %s" for c in cols])
    vals = [data.get(c, '') for c in cols]
    _, err = execute(f"UPDATE site_config SET {sets} WHERE id = 1", vals)
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
    id, err = execute("INSERT INTO news (title, date) VALUES (%s, %s)", (data.get('title',''), data.get('date','')))
    if err:
        return jsonify({'error': err}), 500
    result, _ = query_one("SELECT * FROM news WHERE id = %s", (id,))
    return jsonify(result or {}), 201

@app.route('/api/admin/news/<int:nid>', methods=['PUT', 'DELETE'])
@jwt_required()
def admin_news_item(nid):
    if request.method == 'DELETE':
        _, err = execute("DELETE FROM news WHERE id = %s", (nid,))
        if err:
            return jsonify({'error': err}), 500
        return jsonify({'message': 'Deleted'})
    data = request.get_json() or {}
    _, err = execute("UPDATE news SET title=%s, date=%s WHERE id=%s", (data.get('title'), data.get('date'), nid))
    if err:
        return jsonify({'error': err}), 500
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
    if err:
        return jsonify({'error': err}), 500
    result, _ = query_one("SELECT * FROM events WHERE id = %s", (id,))
    return jsonify(result or {}), 201

@app.route('/api/admin/events/<int:eid>', methods=['PUT', 'DELETE'])
@jwt_required()
def admin_events_item(eid):
    if request.method == 'DELETE':
        _, err = execute("DELETE FROM events WHERE id = %s", (eid,))
        if err:
            return jsonify({'error': err}), 500
        return jsonify({'message': 'Deleted'})
    data = request.get_json() or {}
    _, err = execute("UPDATE events SET title=%s, date=%s WHERE id=%s", (data.get('title'), data.get('date'), eid))
    if err:
        return jsonify({'error': err}), 500
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
    if err:
        return jsonify({'error': err}), 500
    result, _ = query_one("SELECT * FROM announcements WHERE id = %s", (id,))
    return jsonify(result or {}), 201

@app.route('/api/admin/announcements/<int:aid>', methods=['PUT', 'DELETE'])
@jwt_required()
def admin_announcements_item(aid):
    if request.method == 'DELETE':
        _, err = execute("DELETE FROM announcements WHERE id = %s", (aid,))
        if err:
            return jsonify({'error': err}), 500
        return jsonify({'message': 'Deleted'})
    data = request.get_json() or {}
    _, err = execute("UPDATE announcements SET text=%s WHERE id=%s", (data.get('text'), aid))
    if err:
        return jsonify({'error': err}), 500
    result, _ = query_one("SELECT * FROM announcements WHERE id = %s", (aid,))
    return jsonify(result or {})

@app.route('/api/admin/downloads', methods=['GET', 'POST'])
@jwt_required()
def admin_downloads():
    if request.method == 'GET':
        data, _ = query("SELECT * FROM downloads ORDER BY id DESC")
        return jsonify(data or [])
    data = request.get_json() or {}
    id, err = execute("INSERT INTO downloads (title, link) VALUES (%s, %s)", (data.get('title',''), data.get('link','')))
    if err:
        return jsonify({'error': err}), 500
    result, _ = query_one("SELECT * FROM downloads WHERE id = %s", (id,))
    return jsonify(result or {}), 201

@app.route('/api/admin/downloads/<int:did>', methods=['PUT', 'DELETE'])
@jwt_required()
def admin_downloads_item(did):
    if request.method == 'DELETE':
        _, err = execute("DELETE FROM downloads WHERE id = %s", (did,))
        if err:
            return jsonify({'error': err}), 500
        return jsonify({'message': 'Deleted'})
    data = request.get_json() or {}
    _, err = execute("UPDATE downloads SET title=%s, link=%s WHERE id=%s", (data.get('title'), data.get('link'), did))
    if err:
        return jsonify({'error': err}), 500
    result, _ = query_one("SELECT * FROM downloads WHERE id = %s", (did,))
    return jsonify(result or {})

@app.route('/api/admin/carousel', methods=['GET', 'POST'])
@jwt_required()
def admin_carousel():
    if request.method == 'GET':
        data, _ = query("SELECT * FROM carousel ORDER BY sort_order ASC")
        return jsonify(data or [])
    data = request.get_json() or {}
    id, err = execute("INSERT INTO carousel (img, alt) VALUES (%s, %s)", (data.get('img',''), data.get('alt','')))
    if err:
        return jsonify({'error': err}), 500
    result, _ = query_one("SELECT * FROM carousel WHERE id = %s", (id,))
    return jsonify(result or {}), 201

@app.route('/api/admin/carousel/<int:cid>', methods=['PUT', 'DELETE'])
@jwt_required()
def admin_carousel_item(cid):
    if request.method == 'DELETE':
        _, err = execute("DELETE FROM carousel WHERE id = %s", (cid,))
        if err:
            return jsonify({'error': err}), 500
        return jsonify({'message': 'Deleted'})
    data = request.get_json() or {}
    _, err = execute("UPDATE carousel SET img=%s, alt=%s WHERE id=%s", (data.get('img'), data.get('alt'), cid))
    if err:
        return jsonify({'error': err}), 500
    result, _ = query_one("SELECT * FROM carousel WHERE id = %s", (cid,))
    return jsonify(result or {})

@app.route('/api/admin/departments', methods=['GET', 'POST'])
@jwt_required()
def admin_departments():
    if request.method == 'GET':
        data, _ = query("SELECT * FROM departments ORDER BY sort_order ASC")
        return jsonify(data or [])
    data = request.get_json() or {}
    id, err = execute("INSERT INTO departments (dept_key, name, icon) VALUES (%s, %s, %s)", (data.get('dept_key',''), data.get('name',''), data.get('icon','fa-book')))
    if err:
        return jsonify({'error': err}), 500
    result, _ = query_one("SELECT * FROM departments WHERE id = %s", (id,))
    return jsonify(result or {}), 201

@app.route('/api/admin/departments/<int:depid>', methods=['PUT', 'DELETE'])
@jwt_required()
def admin_departments_item(depid):
    if request.method == 'DELETE':
        _, err = execute("DELETE FROM departments WHERE id = %s", (depid,))
        if err:
            return jsonify({'error': err}), 500
        return jsonify({'message': 'Deleted'})
    data = request.get_json() or {}
    cols = ['name', 'icon', 'about', 'vision', 'mission', 'hod_name', 'hod_designation', 'hod_qualification', 'hod_email', 'hod_phone']
    sets = ', '.join([f"{c} = %s" for c in cols])
    vals = [data.get(c, '') for c in cols] + [depid]
    _, err = execute(f"UPDATE departments SET {sets} WHERE id = %s", vals)
    if err:
        return jsonify({'error': err}), 500
    result, _ = query_one("SELECT * FROM departments WHERE id = %s", (depid,))
    return jsonify(result or {})

@app.route('/api/admin/faculty', methods=['GET', 'POST'])
@jwt_required()
def admin_faculty():
    if request.method == 'GET':
        dept_id = request.args.get('department_id')
        if dept_id:
            data, _ = query("SELECT * FROM faculty WHERE department_id = %s ORDER BY sort_order ASC", (dept_id,))
        else:
            data, _ = query("SELECT * FROM faculty ORDER BY department_id, sort_order ASC")
        return jsonify(data or [])
    data = request.get_json() or {}
    id, err = execute("INSERT INTO faculty (department_id, name, designation, qualification, email, phone) VALUES (%s, %s, %s, %s, %s, %s)", 
        (data.get('department_id'), data.get('name',''), data.get('designation',''), data.get('qualification',''), data.get('email',''), data.get('phone','')))
    if err:
        return jsonify({'error': err}), 500
    result, _ = query_one("SELECT * FROM faculty WHERE id = %s", (id,))
    return jsonify(result or {}), 201

@app.route('/api/admin/faculty/<int:fid>', methods=['PUT', 'DELETE'])
@jwt_required()
def admin_faculty_item(fid):
    if request.method == 'DELETE':
        _, err = execute("DELETE FROM faculty WHERE id = %s", (fid,))
        if err:
            return jsonify({'error': err}), 500
        return jsonify({'message': 'Deleted'})
    data = request.get_json() or {}
    _, err = execute("UPDATE faculty SET name=%s, designation=%s, qualification=%s, email=%s, phone=%s WHERE id=%s", 
        (data.get('name'), data.get('designation'), data.get('qualification'), data.get('email'), data.get('phone'), fid))
    if err:
        return jsonify({'error': err}), 500
    result, _ = query_one("SELECT * FROM faculty WHERE id = %s", (fid,))
    return jsonify(result or {})

@app.route('/<path:path>')
def serve_static(path):
    file_path = os.path.join(BASE_DIR, path)
    if os.path.isfile(file_path):
        return send_from_directory(BASE_DIR, path)
    return "Not found", 404

@app.route('/')
def serve_index():
    return send_from_directory(BASE_DIR, 'index.html')

handler = app
