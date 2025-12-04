#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Import sản phẩm hóa chất & vật tư từ danh sách có sẵn
"""
import xmlrpc.client

url = 'http://localhost:10019'
db = 'odoo19'
username = 'admin'
password = 'admin'

common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

print(f"✓ Kết nối Odoo thành công (User ID: {uid})")

# ========================================
# TẠO/LẤY DANH MỤC
# ========================================
def get_or_create_category(name, parent_name=None):
    parent_id = False
    if parent_name:
        parent_id = models.execute_kw(db, uid, password,
            'product.category', 'search', [[('name', '=', parent_name)]], {'limit': 1})
        parent_id = parent_id[0] if parent_id else False
    
    cat_id = models.execute_kw(db, uid, password,
        'product.category', 'search', [[('name', '=', name)]], {'limit': 1})
    
    if cat_id:
        return cat_id[0]
    
    return models.execute_kw(db, uid, password,
        'product.category', 'create', [{
            'name': name,
            'parent_id': parent_id,
        }])

# ========================================
# TẠO/LẤY ĐƠN VỊ TÍNH
# ========================================
def get_or_create_uom(name):
    # Tìm UoM có sẵn
    uom_id = models.execute_kw(db, uid, password,
        'uom.uom', 'search', [[('name', '=', name)]], {'limit': 1})
    
    if uom_id:
        return uom_id[0]
    
    # Nếu không có, dùng Unit (ID=1) làm mặc định
    return 1

print("\n=== Chuẩn bị Danh mục & Đơn vị tính ===")

# Tạo danh mục
cat_hoa_chat = get_or_create_category('Hóa chất phân tích', 'Dịch vụ Môi trường')
cat_thiet_bi = get_or_create_category('Thiết bị & Vật tư', 'Dịch vụ Môi trường')
cat_dich_vu = get_or_create_category('Dịch vụ phân tích', 'Dịch vụ Môi trường')

print(f"  ✓ Danh mục: Hóa chất (ID: {cat_hoa_chat}), Thiết bị (ID: {cat_thiet_bi})")

# Tạo đơn vị tính
uom_map = {}
for uom_name in ['Chỉ tiêu', 'g', 'mL', 'Cái', 'Bình', 'Lần', 'Đơn vị', 'Hệ thống', 'Liên']:
    uom_map[uom_name] = get_or_create_uom(uom_name)
    print(f"  ✓ Đơn vị: {uom_name} (ID: {uom_map[uom_name]})")

# ========================================
# DANH SÁCH SẢN PHẨM TỪ ẢNH
# ========================================
products_data = [
    # Từ ảnh 1
    {'name': '1,1,2 Trichloro ethan', 'price': 550000, 'cost': 550000, 'uom': 'Chỉ tiêu', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': '1,1 dichloethane', 'price': 550000, 'cost': 550000, 'uom': 'Chỉ tiêu', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': '1,3 Butadien', 'price': 550000, 'cost': 550000, 'uom': 'Chỉ tiêu', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': '1,5-diphenylcabazid', 'price': 0, 'cost': 0, 'uom': 'g', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': '1,8-Dihydroxy-2-(4-sulfophenylazo)naphthalene-3,6-disulfonic acid trisodium salt', 'price': 550000, 'cost': 550000, 'uom': 'g', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': '2,4-Diclophenoxy axeticaxit (2,4-D)', 'price': 700000, 'cost': 700000, 'uom': 'Chỉ tiêu', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': '4-aminoantipyrin', 'price': 0, 'cost': 0, 'uom': 'g', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Acetic acid', 'price': 0, 'cost': 0, 'uom': 'mL', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Acetone', 'price': 550000, 'cost': 550000, 'uom': 'Chỉ tiêu', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Acetone', 'price': 0, 'cost': 0, 'uom': 'mL', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Acetonitrile', 'price': 500000, 'cost': 500000, 'uom': 'Chỉ tiêu', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Acetylen', 'price': 500000, 'cost': 500000, 'uom': 'Chỉ tiêu', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Acid ascorbic', 'price': 0, 'cost': 0, 'uom': 'g', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Acid Barbituric', 'price': 0, 'cost': 0, 'uom': 'g', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Acid boric', 'price': 0, 'cost': 0, 'uom': 'g', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Acid flohydric', 'price': 0, 'cost': 0, 'uom': 'mL', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Acid hydrochloric', 'price': 0, 'cost': 0, 'uom': 'mL', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Acid hydrochloric (AAS)', 'price': 0, 'cost': 0, 'uom': 'mL', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Acid L-glutamic khan', 'price': 0, 'cost': 0, 'uom': 'g', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Acid nitric', 'price': 0, 'cost': 0, 'uom': 'mL', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Acid nitric (AAS)', 'price': 0, 'cost': 0, 'uom': 'mL', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Acid octhophosphoric', 'price': 0, 'cost': 0, 'uom': 'mL', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Acid salicylic', 'price': 0, 'cost': 0, 'uom': 'g', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Acid stearic', 'price': 0, 'cost': 0, 'uom': 'g', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Acid succinic', 'price': 0, 'cost': 0, 'uom': 'g', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Acid Sulfuric', 'price': 0, 'cost': 0, 'uom': 'mL', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Acid Sulfuric (AAS)', 'price': 0, 'cost': 0, 'uom': 'mL', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Acid Sulphamic', 'price': 0, 'cost': 0, 'uom': 'g', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Acid Tartaric', 'price': 0, 'cost': 0, 'uom': 'g', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': '[Adapter] Cổ sạc 5v-2A', 'price': 0, 'cost': 0, 'uom': 'Cái', 'type': 'consu', 'category': cat_thiet_bi},
    {'name': 'Ag', 'price': 200000, 'cost': 200000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Al', 'price': 200000, 'cost': 200000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    
    # Từ ảnh 2
    {'name': 'Aldrin', 'price': 700000, 'cost': 700000, 'uom': 'Chỉ tiêu', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Alkaline peptone water', 'price': 0, 'cost': 0, 'uom': 'g', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Allylthiourea', 'price': 0, 'cost': 0, 'uom': 'g', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Ammonia solution NH4OH 25-28%, Chai 500ml', 'price': 0, 'cost': 0, 'uom': 'mL', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Ammonium axetat', 'price': 0, 'cost': 0, 'uom': 'g', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Ammonium chloride', 'price': 0, 'cost': 0, 'uom': 'g', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Ammonium hydroxide (DD Amoniac)', 'price': 0, 'cost': 0, 'uom': 'mL', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Ammonium Iron (II) sunfate hexahydrate (FAS)', 'price': 0, 'cost': 0, 'uom': 'g', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Ammonium molybdate tetrahydrate', 'price': 0, 'cost': 0, 'uom': 'g', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Ammonium Sulphate', 'price': 0, 'cost': 0, 'uom': 'g', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Amoni', 'price': 170000, 'cost': 170000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Amoni (bình theo N)', 'price': 120000, 'cost': 120000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'ảnh sa', 'price': 0, 'cost': 0, 'uom': 'Đơn vị', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Ánh sáng', 'price': 0, 'cost': 0, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Anilin', 'price': 550000, 'cost': 550000, 'uom': 'Chỉ tiêu', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Antimon (Sb)', 'price': 250000, 'cost': 250000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Antimony', 'price': 250000, 'cost': 250000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Ấn ướng tiểp khách', 'price': 0, 'cost': 0, 'uom': 'Đơn vị', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'APEO (Alkylphenol Ethoxylate)', 'price': 1000000, 'cost': 1000000, 'uom': 'Chỉ tiêu', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Ấp xuất không khí', 'price': 500000, 'cost': 500000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': '[AQ]ACCUV 12V05Ah', 'price': 0, 'cost': 0, 'uom': 'Cái', 'type': 'consu', 'category': cat_thiet_bi},
    {'name': '[AQ]ACCUV 12V20Ah', 'price': 0, 'cost': 0, 'uom': 'Cái', 'type': 'consu', 'category': cat_thiet_bi},
    {'name': '[AQ]Acquy 12v7.2Ah', 'price': 0, 'cost': 0, 'uom': 'Bình', 'type': 'consu', 'category': cat_thiet_bi},
    {'name': 'Arabinogalactan', 'price': 0, 'cost': 0, 'uom': 'g', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Arginine dihydrolase borth', 'price': 0, 'cost': 0, 'uom': 'Đơn vị', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Arginine-dihydrolase borth', 'price': 0, 'cost': 0, 'uom': 'Đơn vị', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'As', 'price': 150000, 'cost': 150000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Asen', 'price': 150000, 'cost': 150000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Aseton', 'price': 550000, 'cost': 550000, 'uom': 'Chỉ tiêu', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Ant acetic', 'price': 550000, 'cost': 550000, 'uom': 'Chỉ tiêu', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Ant Acrylic', 'price': 550000, 'cost': 550000, 'uom': 'Chỉ tiêu', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Ant Glohydic', 'price': 550000, 'cost': 550000, 'uom': 'Chỉ tiêu', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Ant fomic', 'price': 550000, 'cost': 550000, 'uom': 'Chỉ tiêu', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Ant Methacrylic', 'price': 550000, 'cost': 550000, 'uom': 'Chỉ tiêu', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Ant sunfuric', 'price': 250000, 'cost': 250000, 'uom': 'Chỉ tiêu', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Ba', 'price': 200000, 'cost': 200000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Bac', 'price': 200000, 'cost': 200000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Bactiident oxidasae', 'price': 0, 'cost': 0, 'uom': 'Đơn vị', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Bản làm việc 1m2x60', 'price': 0, 'cost': 0, 'uom': 'Cái', 'type': 'consu', 'category': cat_thiet_bi},
    {'name': 'Bản làm việc 60Cmx1m2', 'price': 0, 'cost': 0, 'uom': 'Cái', 'type': 'consu', 'category': cat_thiet_bi},
    {'name': 'Báo cáo tổng kết dự dụng báo cáo đánh giá tác động môi trường', 'price': 0, 'cost': 0, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Báo cáo xả thải', 'price': 0, 'cost': 0, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Báo đường hệ thống sư lý nước thải YẾ', 'price': 0, 'cost': 0, 'uom': 'Lần', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Báo hành, bảo trì hệ thống', 'price': 0, 'cost': 0, 'uom': 'Lần', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Báo lờ vi khuẩn tỵ lấn tình sulfit', 'price': 0, 'cost': 0, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Barium clorua', 'price': 0, 'cost': 0, 'uom': 'g', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Barium perchlorate hydrate', 'price': 0, 'cost': 0, 'uom': 'g', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Be', 'price': 250000, 'cost': 250000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'bể chứa bùn', 'price': 0, 'cost': 0, 'uom': 'Cái', 'type': 'consu', 'category': cat_thiet_bi},
    {'name': 'Bể điều nhiệt đ C+8 Memmert', 'price': 0, 'cost': 0, 'uom': 'Cái', 'type': 'consu', 'category': cat_thiet_bi},
    {'name': 'Benzene', 'price': 400000, 'cost': 400000, 'uom': 'Chỉ tiêu', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Benzene hexachloride (BHC)', 'price': 700000, 'cost': 700000, 'uom': 'Chỉ tiêu', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Bể rửa siêu âm', 'price': 0, 'cost': 0, 'uom': 'Cái', 'type': 'consu', 'category': cat_thiet_bi},
    {'name': 'Biển hiệu Công ty Nam Việt', 'price': 0, 'cost': 0, 'uom': 'Cái', 'type': 'consu', 'category': cat_thiet_bi},
    {'name': 'Bình bọt ABC-4 Kg', 'price': 0, 'cost': 0, 'uom': 'Bình', 'type': 'consu', 'category': cat_thiet_bi},
    {'name': 'Bình bọt ABC 4kg', 'price': 0, 'cost': 0, 'uom': 'Bình', 'type': 'consu', 'category': cat_thiet_bi},
    {'name': 'Bình bọt ABC 8 Kg', 'price': 0, 'cost': 0, 'uom': 'Bình', 'type': 'consu', 'category': cat_thiet_bi},
    {'name': 'Bình bọt ABC 8kg', 'price': 0, 'cost': 0, 'uom': 'Bình', 'type': 'consu', 'category': cat_thiet_bi},
    {'name': 'Bình bọt BC 4kg', 'price': 0, 'cost': 0, 'uom': 'Bình', 'type': 'consu', 'category': cat_thiet_bi},
    {'name': 'Bình bọt BC 8KG', 'price': 0, 'cost': 0, 'uom': 'Bình', 'type': 'consu', 'category': cat_thiet_bi},
    {'name': 'Bình khí dùng XHTBB-ABC', 'price': 0, 'cost': 0, 'uom': 'Bình', 'type': 'consu', 'category': cat_thiet_bi},
    {'name': 'Bình khí CO2 3 kg', 'price': 0, 'cost': 0, 'uom': 'Bình', 'type': 'consu', 'category': cat_thiet_bi},
    
    # Từ ảnh 3
    {'name': 'Bình Ehl CO2 5 kg', 'price': 0, 'cost': 0, 'uom': 'Bình', 'type': 'consu', 'category': cat_thiet_bi},
    {'name': 'Bình xe đầy bột khí ABC', 'price': 0, 'cost': 0, 'uom': 'Bình', 'type': 'consu', 'category': cat_thiet_bi},
    {'name': 'Bình xe đầy bột khí BC', 'price': 0, 'cost': 0, 'uom': 'Bình', 'type': 'consu', 'category': cat_thiet_bi},
    {'name': 'Blood agar base', 'price': 0, 'cost': 0, 'uom': 'Đơn vị', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Bo', 'price': 250000, 'cost': 250000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Bộ chưng cất đạm: BUCHI Distillation Unit K-350', 'price': 0, 'cost': 0, 'uom': 'Cái', 'type': 'consu', 'category': cat_thiet_bi},
    {'name': 'BOD5', 'price': 120000, 'cost': 120000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'BOD5 (20°C)', 'price': 120000, 'cost': 120000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Bộ hóa học Iạnh Hitachi HF53', 'price': 0, 'cost': 0, 'uom': 'Cái', 'type': 'consu', 'category': cat_thiet_bi},
    {'name': 'Bộ hóa Hydra HG', 'price': 0, 'cost': 0, 'uom': 'Cái', 'type': 'consu', 'category': cat_thiet_bi},
    {'name': 'Bộ khí chuẩn (6 khí: CO2, O2, SO2, CO, NO, NO2)', 'price': 0, 'cost': 0, 'uom': 'Cái', 'type': 'consu', 'category': cat_thiet_bi},
    {'name': 'Bộ lấy mẫu Khí thải CS000', 'price': 0, 'cost': 0, 'uom': 'Cái', 'type': 'consu', 'category': cat_thiet_bi},
    {'name': 'Bom Apex', 'price': 0, 'cost': 0, 'uom': 'Cái', 'type': 'consu', 'category': cat_thiet_bi},
    {'name': 'Bơm chìm', 'price': 0, 'cost': 0, 'uom': 'Cái', 'type': 'consu', 'category': cat_thiet_bi},
    {'name': 'Bơm chìm nước', 'price': 0, 'cost': 0, 'uom': 'Cái', 'type': 'consu', 'category': cat_thiet_bi},
    {'name': 'Bơm định lượng', 'price': 0, 'cost': 0, 'uom': 'Cái', 'type': 'consu', 'category': cat_thiet_bi},
    {'name': 'Bơm lấy mẫu bụi thế tích lớn TFA-2 Staplex', 'price': 0, 'cost': 0, 'uom': 'Cái', 'type': 'consu', 'category': cat_thiet_bi},
    {'name': 'Bơm lấy mẫu Gilair 5', 'price': 0, 'cost': 0, 'uom': 'Cái', 'type': 'consu', 'category': cat_thiet_bi},
    {'name': 'Bơm lấy mẫu lưu lượng thấp: Gilair Pro', 'price': 0, 'cost': 0, 'uom': 'Cái', 'type': 'consu', 'category': cat_thiet_bi},
    {'name': 'Bơm lấy mẫu thể tích lớn Sibata HVC 500', 'price': 0, 'cost': 0, 'uom': 'Cái', 'type': 'consu', 'category': cat_thiet_bi},
    {'name': 'Bơm màng MBR', 'price': 0, 'cost': 0, 'uom': 'Cái', 'type': 'consu', 'category': cat_thiet_bi},
    {'name': 'Bồn hóa chất', 'price': 0, 'cost': 0, 'uom': 'Hệ thống', 'type': 'consu', 'category': cat_thiet_bi},
    {'name': 'Bộ phá mẫu: Anton Paar Multiwave 3000 microwave', 'price': 0, 'cost': 0, 'uom': 'Đơn vị', 'type': 'consu', 'category': cat_thiet_bi},
    {'name': 'Bor', 'price': 250000, 'cost': 250000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Br2', 'price': 500000, 'cost': 500000, 'uom': 'Chỉ tiêu', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Brilliant green bile broth 2%', 'price': 0, 'cost': 0, 'uom': 'g', 'type': 'consu', 'category': cat_hoa_chat},
    
    # Từ ảnh 4
    {'name': 'BrO3-', 'price': 500000, 'cost': 500000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Brom', 'price': 0, 'cost': 0, 'uom': 'mL', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Bromat', 'price': 500000, 'cost': 500000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Bromocresol green', 'price': 0, 'cost': 0, 'uom': 'g', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Bức xạ cực tím', 'price': 200000, 'cost': 200000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Bức xạ điện từ', 'price': 200000, 'cost': 200000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Bức xạ ion hóa', 'price': 200000, 'cost': 200000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Bức xạ nhiệt', 'price': 56000, 'cost': 56000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Bức xạ từ ngoại', 'price': 200000, 'cost': 200000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Buffered peptone water', 'price': 0, 'cost': 0, 'uom': 'g', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Bụi', 'price': 150000, 'cost': 150000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Bụi Amiăng', 'price': 2000000, 'cost': 2000000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Bụi bông', 'price': 350000, 'cost': 350000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Bụi Chi', 'price': 140000, 'cost': 140000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Bụi hạt', 'price': 200000, 'cost': 200000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Bụi hô hấp', 'price': 100000, 'cost': 100000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Bụi hô hấp (mẫu thời điểm)', 'price': 100000, 'cost': 100000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Bụi kim loại', 'price': 140000, 'cost': 140000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Bụi (PM)', 'price': 3500000, 'cost': 3500000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    
    # Từ ảnh 5
    {'name': 'Bụi PM0.3 (trong lượng, kích thước ≤0.3), mẫu thời điểm', 'price': 200000, 'cost': 200000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Bụi PM0.5 (trong lượng, kích thước ≤0.5), mẫu thời điểm', 'price': 200000, 'cost': 200000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'bui pm 10', 'price': 0, 'cost': 0, 'uom': 'Đơn vị', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Bụi PM 10', 'price': 3500000, 'cost': 3500000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Bụi PM10 (trong lượng, kích thước ≤10), mẫu thời điểm', 'price': 200000, 'cost': 200000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Bụi PM1 (trong lượng, kích thước ≤1), mẫu thời điểm', 'price': 200000, 'cost': 200000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Bụi PM2.5', 'price': 2000000, 'cost': 2000000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Bụi PM5 (trong lượng, kích thước ≤5), mẫu thời điểm', 'price': 200000, 'cost': 200000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Bụi Silic', 'price': 2000000, 'cost': 2000000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Bụi Silic (mẫu đánh giá theo thời lượng tiếp xúc)', 'price': 200000, 'cost': 200000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Bụi than', 'price': 200000, 'cost': 200000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Bụi than (mẫu đánh giá theo thời lượng tiếp xúc)', 'price': 200000, 'cost': 200000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Bụi thép', 'price': 140000, 'cost': 140000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Bụi toàn phần', 'price': 91000, 'cost': 91000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Bụi toàn phần (mẫu đánh giá theo thời lượng tiếp xúc)', 'price': 800000, 'cost': 800000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Bụi toàn phần (mẫu thời điểm)', 'price': 91000, 'cost': 91000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Bụi tổng', 'price': 91000, 'cost': 91000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Butanol', 'price': 350000, 'cost': 350000, 'uom': 'Chỉ tiêu', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Bút đo pH Extech PH100', 'price': 0, 'cost': 0, 'uom': 'Cái', 'type': 'consu', 'category': cat_thiet_bi},
    {'name': 'Butyl Acetate', 'price': 350000, 'cost': 350000, 'uom': 'Chỉ tiêu', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Butyl axetat', 'price': 350000, 'cost': 350000, 'uom': 'Chỉ tiêu', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Butyl Cellosolle', 'price': 350000, 'cost': 350000, 'uom': 'Chỉ tiêu', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Ca', 'price': 120000, 'cost': 120000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Ca2+', 'price': 120000, 'cost': 120000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Cacbon', 'price': 0, 'cost': 0, 'uom': 'g', 'type': 'consu', 'category': cat_hoa_chat},
    {'name': 'Cacbon hữu cơ', 'price': 400000, 'cost': 400000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Các hợp chất polyclobiphenyl tương tự dioxin (dl-PCB)', 'price': 550000, 'cost': 550000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Các paraffin mạch ngắn chứa Clo (SCCP)', 'price': 550000, 'cost': 550000, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
    {'name': 'Các Phụ kiện và đường ống', 'price': 0, 'cost': 0, 'uom': 'Chỉ tiêu', 'type': 'consu', 'category': cat_thiet_bi},
    {'name': 'Các thông số khí tượng', 'price': 0, 'cost': 0, 'uom': 'Chỉ tiêu', 'type': 'service', 'category': cat_dich_vu},
]

print(f"\n=== Lấy thuế mặc định ===")
# Tìm thuế 8%
tax_8_id = models.execute_kw(db, uid, password,
    'account.tax', 'search',
    [[('name', 'ilike', '8%'), ('type_tax_use', '=', 'sale')]], {'limit': 1})

if not tax_8_id:
    print("  ! Không tìm thấy thuế 8%, sẽ tạo mới...")
    tax_8_id = [models.execute_kw(db, uid, password,
        'account.tax', 'create', [{
            'name': 'Thuế GTGT 8%',
            'amount': 8.0,
            'amount_type': 'percent',
            'type_tax_use': 'sale',
        }])]

print(f"  ✓ Thuế 8% (ID: {tax_8_id[0]})")

print(f"\n=== Import {len(products_data)} Sản phẩm ===")

created = 0
skipped = 0
errors = 0

for idx, prod in enumerate(products_data, 1):
    try:
        # Kiểm tra tồn tại
        existing = models.execute_kw(db, uid, password,
            'product.template', 'search',
            [[('name', '=', prod['name'])]], {'limit': 1})
        
        if existing:
            skipped += 1
            continue
        
        # Lấy UoM ID
        uom_id = uom_map.get(prod['uom'], 1)
        
        # Tính giá bán (nếu chưa có thì = giá vốn * 1.3)
        list_price = prod['price'] if prod['price'] > 0 else prod['cost'] * 1.3
        
        # Tạo mã tham chiếu nội bộ (Internal Reference)
        # Ví dụ: HC001 cho hóa chất, TB001 cho thiết bị, DV001 cho dịch vụ
        if prod['category'] == cat_hoa_chat:
            default_code = f"HC{idx:04d}"
        elif prod['category'] == cat_thiet_bi:
            default_code = f"TB{idx:04d}"
        else:
            default_code = f"DV{idx:04d}"
        
        # Chuẩn bị dữ liệu sản phẩm đầy đủ
        product_data = {
            'name': prod['name'],
            'type': prod['type'],  # 'consu' = Tiêu dùng, 'service' = Dịch vụ
            'categ_id': prod['category'],
            'list_price': list_price,
            'standard_price': prod['cost'],
            'uom_id': uom_id,
            'sale_ok': True,
            'purchase_ok': True if prod['type'] == 'consu' else False,
            'default_code': default_code,  # Mã tham chiếu nội bộ
            'invoice_policy': 'order',  # Chính sách xuất HĐ: Số lượng đã đặt
            'taxes_id': [(6, 0, tax_8_id)],  # Thuế khách hàng 8%
            'description': f"Sản phẩm {prod['name']}",  # Ghi chú nội bộ
            'description_sale': f"{prod['name']} - Giá: {list_price:,.0f} VND/{prod['uom']}",
        }
        
        # Tạo sản phẩm
        product_id = models.execute_kw(db, uid, password,
            'product.template', 'create', [product_data])
        
        created += 1
        if idx % 10 == 0:
            print(f"  {idx}/{len(products_data)}: ✓ Đã tạo {created} sản phẩm...")
        
    except Exception as e:
        errors += 1
        if errors <= 3:  # Chỉ print 3 lỗi đầu chi tiết
            print(f"  ✗ LỖI '{prod['name']}':\n{str(e)}\n")

print(f"\n{'='*60}")
print(f"✓ Hoàn thành!")
print(f"  - Đã tạo mới: {created}")
print(f"  - Đã tồn tại: {skipped}")
print(f"  - Lỗi: {errors}")
print(f"{'='*60}")

