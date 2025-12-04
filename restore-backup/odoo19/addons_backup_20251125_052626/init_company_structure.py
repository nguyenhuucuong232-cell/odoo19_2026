import odoo
from odoo import api, SUPERUSER_ID
import random
import base64
import os

# ------------------------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------------------------
DB_NAME = 'odoo19'
COMPANY_NAME = 'CÔNG TY CỔ PHẦN DỊCH VỤ CÔNG NGHỆ SÀI GÒN'
COMPANY_SHORT = 'SGC'
PASSWORD_DEFAULT = '1'

# Logo path (Placeholder - user needs to verify path)
LOGO_PATH = '/mnt/extra-addons/logo.png' 

# Vietnamese Name Data
HO = ['Nguyễn', 'Trần', 'Lê', 'Phạm', 'Huỳnh', 'Hoàng', 'Phan', 'Vũ', 'Võ', 'Đặng', 'Bùi', 'Đỗ', 'Hồ', 'Ngô', 'Dương', 'Lý']
DEM = ['Văn', 'Thị', 'Hữu', 'Minh', 'Ngọc', 'Thanh', 'Gia', 'Bảo', 'Đức', 'Thùy', 'Kim', 'Quang', 'Hải', 'Tuấn', 'Hoài', 'Xuân', 'Thu']
TEN = ['An', 'Bình', 'Cường', 'Dung', 'Giang', 'Hải', 'Hương', 'Hùng', 'Khánh', 'Lan', 'Linh', 'Minh', 'Nam', 'Nga', 'Oanh', 'Phúc', 'Quân', 'Quang', 'Sơn', 'Tâm', 'Thảo', 'Trang', 'Tú', 'Uyên', 'Vinh', 'Yến', 'Vy', 'Châu', 'Kiệt', 'Thắng', 'Nhi', 'Tùng']

def get_random_name():
    return f"{random.choice(HO)} {random.choice(DEM)} {random.choice(TEN)}"

def generate_login(full_name):
    # Create login: sonnh54, minhv99...
    clean_name = remove_accents(full_name).lower().split()
    if not clean_name: return "user"
    # Last name + first letter of other names
    short_name = clean_name[-1] + "".join([w[0] for w in clean_name[:-1]])
    return f"{short_name}{random.randint(1,99)}"

def remove_accents(input_str):
    s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
    s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'
    s = ''
    for c in input_str:
        if c in s1:
            s += s0[s1.index(c)]
        else:
            s += c
    return s

# ------------------------------------------------------------------------------
# DATA STRUCTURE
# ------------------------------------------------------------------------------
# Define the structure exactly as requested
DEPARTMENTS = [
    {
        'name': 'Ban Giám Đốc',
        'code': 'BGD',
        'manager': None, # CEO will be created separately or assigned
        'staff_count': 0 # Only CEO
    },
    {
        'name': 'Phòng Kinh Doanh',
        'code': 'PKD',
        'manager': {'name': 'Trần Văn Minh', 'role': 'Trưởng phòng'},
        'teams': [
            {
                'lead': {'name': 'Lê Thùy Linh', 'role': 'Trưởng nhóm'},
                'members': [{'name': 'Phạm Thị Vân', 'role': 'Chuyên viên'}],
                'extra_staff': 10 # Fill to reach target
            }
        ]
    },
    {
        'name': 'Phòng Quan Trắc',
        'code': 'PQT',
        'manager': {'name': 'Nguyễn Thanh Hùng', 'role': 'Trưởng phòng'},
        'members': [{'name': 'Nguyễn Văn An', 'role': 'Chuyên viên'}],
        'extra_staff': 10
    },
    {
        'name': 'Phòng Thí Nghiệm',
        'code': 'PTN',
        'manager': {'name': 'Nguyễn Trần Minh Toàn', 'role': 'Trưởng phòng'},
        'sub_depts': [
            {'name': 'Phòng Hóa & Sinh', 'code': 'PHS', 'extra_staff': 8}
        ],
        'extra_staff': 2
    },
    {
        'name': 'Phòng Kế Toán',
        'code': 'PKT',
        'manager': {'name': 'Hoàng Thị Kế Toán', 'role': 'Trưởng phòng'}, # Funny name kept as requested
        'extra_staff': 5
    }
]

def main():
    print("="*80)
    print("🚀 BẮT ĐẦU KHỞI TẠO HỆ THỐNG SGC (PHASE 1, 2, 3)")
    print("="*80)

    # 1. Connect DB
    try:
        # Setup config from Env
        db_host = os.environ.get('HOST', 'db')
        db_port = os.environ.get('PORT', '5432')
        db_user = os.environ.get('USER', 'odoo')
        db_password = os.environ.get('PASSWORD', 'odoo19@2025')
        
        odoo.tools.config.parse_config([
            '--db_host', db_host,
            '--db_port', db_port,
            '--db_user', db_user,
            '--db_password', db_password,
        ])
        odoo.tools.config['db_name'] = DB_NAME
        registry = odoo.modules.registry.Registry.new(DB_NAME)
    except Exception as e:
        print(f"❌ CRITICAL ERROR: Không thể kết nối DB. {e}")
        return

    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        
        # ---------------------------------------------------------
        # PHASE 1: COMPANY INFO
        # ---------------------------------------------------------
        print("\n🏢 CẤU HÌNH CÔNG TY...")
        company = env.user.company_id
        company.write({
            'name': COMPANY_NAME,
            'street': 'TP. Hồ Chí Minh, Việt Nam',
            'currency_id': env.ref('base.VND').id,
        })
        
        # Try load logo
        if os.path.exists(LOGO_PATH):
            with open(LOGO_PATH, "rb") as image_file:
                company.logo = base64.b64encode(image_file.read())
                print("   ✅ Đã cập nhật Logo")
        else:
            print(f"   ⚠️ Không tìm thấy file logo tại {LOGO_PATH}")

        # ---------------------------------------------------------
        # PHASE 2 & 3: DEPARTMENTS & EMPLOYEES
        # ---------------------------------------------------------
        print("\n👥 THIẾT LẬP PHÒNG BAN & NHÂN SỰ...")
        
        total_created = 0
        
        # --- 1. Ban Giám Đốc ---
        bgd = env['hr.department'].create({'name': 'Ban Giám Đốc', 'company_id': company.id})
        
        # Create CEO (Optional, assume user Admin is CEO or create new)
        # Let's create a formal CEO
        ceo_user = create_user(env, 'Tổng Giám Đốc', 'ceo', company)
        ceo_emp = create_employee(env, ceo_user, 'Tổng Giám Đốc', bgd, None)
        bgd.manager_id = ceo_emp.id
        print(f"   ✅ [Ban Giám Đốc] CEO: Tổng Giám Đốc")

        # --- 2. Process Other Departments ---
        for dept_data in DEPARTMENTS:
            if dept_data['name'] == 'Ban Giám Đốc': continue # Skip, already done

            print(f"   📂 Xử lý: {dept_data['name']}")
            dept = env['hr.department'].create({
                'name': dept_data['name'],
                'parent_id': bgd.id, # All departments report to Board
                'company_id': company.id
            })

            # Create Manager
            manager_emp = None
            if dept_data.get('manager'):
                m_name = dept_data['manager']['name']
                m_role = dept_data['manager']['role']
                m_user = create_user(env, m_name, generate_login(m_name), company)
                manager_emp = create_employee(env, m_user, m_role, dept, ceo_emp)
                dept.manager_id = manager_emp.id
                print(f"      👤 Trưởng phòng: {m_name}")
                total_created += 1

            # Handle Teams (Sales)
            if 'teams' in dept_data:
                for team in dept_data['teams']:
                    # Team Lead reports to Manager
                    lead_name = team['lead']['name']
                    lead_role = team['lead']['role']
                    lead_user = create_user(env, lead_name, generate_login(lead_name), company)
                    lead_emp = create_employee(env, lead_user, lead_role, dept, manager_emp)
                    print(f"      🌟 Trưởng nhóm: {lead_name}")
                    total_created += 1

                    # Named Members report to Lead
                    for mem in team['members']:
                        mem_user = create_user(env, mem['name'], generate_login(mem['name']), company)
                        create_employee(env, mem_user, mem['role'], dept, lead_emp)
                        print(f"         🔹 NV: {mem['name']}")
                        total_created += 1
                    
                    # Extra Staff report to Lead
                    for _ in range(team['extra_staff']):
                        r_name = get_random_name()
                        r_user = create_user(env, r_name, generate_login(r_name), company)
                        create_employee(env, r_user, "Nhân viên kinh doanh", dept, lead_emp)
                        total_created += 1
                    print(f"         ... +{team['extra_staff']} NVKD khác")

            # Handle Standard Members (PQT)
            if 'members' in dept_data:
                for mem in dept_data['members']:
                    mem_user = create_user(env, mem['name'], generate_login(mem['name']), company)
                    create_employee(env, mem_user, mem['role'], dept, manager_emp)
                    print(f"      🔹 NV: {mem['name']}")
                    total_created += 1

            # Handle Sub-Departments (PTN)
            if 'sub_depts' in dept_data:
                for sub in dept_data['sub_depts']:
                    sub_dept = env['hr.department'].create({
                        'name': sub['name'],
                        'parent_id': dept.id,
                        'company_id': company.id
                    })
                    # Extra staff in sub-dept report to Manager of Parent Dept (for now, or we create a sub-lead?)
                    # Assuming report to Main Dept Manager
                    for _ in range(sub['extra_staff']):
                        r_name = get_random_name()
                        r_user = create_user(env, r_name, generate_login(r_name), company)
                        create_employee(env, r_user, "Kỹ thuật viên", sub_dept, manager_emp)
                        total_created += 1
                    print(f"      📂 Phòng con {sub['name']}: +{sub['extra_staff']} NV")

            # Handle Extra Staff (Directly under Manager)
            if 'extra_staff' in dept_data:
                for _ in range(dept_data['extra_staff']):
                    r_name = get_random_name()
                    r_user = create_user(env, r_name, generate_login(r_name), company)
                    create_employee(env, r_user, "Chuyên viên", dept, manager_emp)
                    total_created += 1
                print(f"      ... +{dept_data['extra_staff']} NV khác")

        env.cr.commit()
        print("\n" + "="*80)
        print(f"✅ HOÀN TẤT! Tổng cộng đã tạo {total_created} nhân sự.")
        print("="*80)

def create_user(env, name, login, company):
    # Check existing
    existing = env['res.users'].search([('login', '=', login)], limit=1)
    if existing:
        # Add suffix
        login = f"{login}{random.randint(100, 999)}"
    
    vals = {
        'name': name,
        'login': login,
        'password': PASSWORD_DEFAULT,
        'email': f"{login}@sgc.vn",
        'company_id': company.id,
        'company_ids': [(4, company.id)],
    }
    
    # Attempt to set groups if field exists (Odoo 19 changes)
    # For now, just basic user creation
    return env['res.users'].create(vals)

def create_employee(env, user, job_title, dept, parent):
    vals = {
        'name': user.name,
        'user_id': user.id,
        'job_title': job_title,
        'department_id': dept.id,
        'parent_id': parent.id if parent else False,
        'work_email': user.email,
        'company_id': dept.company_id.id
    }
    return env['hr.employee'].create(vals)

if __name__ == '__main__':
    main()

