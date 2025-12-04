#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tạo 30 khách hàng với thông tin đầy đủ cho SGC
"""
import xmlrpc.client

url = 'http://localhost:10019'
db = 'odoo19'
username = 'admin'
password = 'admin'

common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

print(f"✓ Kết nối Odoo thành công (User ID: {uid})\n")

# ========================================
# DANH SÁCH 30 KHÁCH HÀNG
# ========================================
customers_data = [
    # 1-5: CÔNG TY SẢN XUẤT
    {
        'name': 'CÔNG TY TNHH SẢN XUẤT THỰC PHẨM VIỆT NAM',
        'vat': '0312345678',
        'street': '123 Nguyễn Văn Linh',
        'street2': 'Phường Tân Phú, Quận 7',
        'city': 'TP. Hồ Chí Minh',
        'zip': '700000',
        'phone': '028-3775-1234',
        'mobile': '0903-123-456',
        'email': 'info@thucphamvietnam.com.vn',
        'website': 'https://thucphamvietnam.com.vn',
        'contact_name': 'Nguyễn Văn An',
        'title': 'Giám đốc',
        'industry': 'Sản xuất thực phẩm',
        'comment': 'Khách hàng VIP - Quan trắc định kỳ hàng quý',
    },
    {
        'name': 'CÔNG TY CỔ PHẦN DỆT MAY ĐỒNG NAI',
        'vat': '0315678901',
        'street': '456 Quốc lộ 1A',
        'street2': 'KCN Biên Hòa 1',
        'city': 'Biên Hòa, Đồng Nai',
        'zip': '810000',
        'phone': '0251-3821-234',
        'mobile': '0912-345-678',
        'email': 'contact@detmaydongnai.vn',
        'website': 'https://detmaydongnai.vn',
        'contact_name': 'Trần Thị Bình',
        'title': 'Phó Giám đốc',
        'industry': 'Dệt may',
        'comment': 'Cần báo cáo đánh giá tác động môi trường hàng năm',
    },
    {
        'name': 'NHÀ MÁY CHẾ BIẾN GỖ BÌNH DƯƠNG',
        'vat': '0318901234',
        'street': '789 Đại lộ Bình Dương',
        'street2': 'KCN Mỹ Phước 3',
        'city': 'Bình Dương',
        'zip': '820000',
        'phone': '0274-3567-890',
        'mobile': '0934-567-890',
        'email': 'admin@chebiengobinhduong.com',
        'website': 'https://chebiengobinhduong.com',
        'contact_name': 'Lê Văn Cường',
        'title': 'Trưởng phòng Môi trường',
        'industry': 'Chế biến gỗ',
        'comment': 'Quan trắc khí thải và nước thải định kỳ 6 tháng',
    },
    {
        'name': 'CÔNG TY TNHH SẢN XUẤT NHỰA VIỆT TIẾN',
        'vat': '0321234567',
        'street': '234 Tỉnh lộ 10',
        'street2': 'Khu công nghiệp Tân Bình',
        'city': 'TP. Hồ Chí Minh',
        'zip': '700000',
        'phone': '028-3812-3456',
        'mobile': '0945-678-901',
        'email': 'viettien@nhuaviettien.com',
        'website': 'https://nhuaviettien.com',
        'contact_name': 'Phạm Minh Đức',
        'title': 'Giám đốc Nhà máy',
        'industry': 'Sản xuất nhựa',
        'comment': 'Khách hàng mới - cần tư vấn hệ thống xử lý khí thải',
    },
    {
        'name': 'CÔNG TY CỔ PHẦN GIẤY VIỆT NAM',
        'vat': '0324567890',
        'street': '567 Quốc lộ 51',
        'street2': 'Phường Long Bình, TP. Biên Hòa',
        'city': 'Đồng Nai',
        'zip': '810000',
        'phone': '0251-3567-123',
        'mobile': '0956-789-012',
        'email': 'contact@giayvietnamese.vn',
        'website': 'https://giayvietnamese.vn',
        'contact_name': 'Hoàng Thị Em',
        'title': 'Trưởng phòng Kỹ thuật',
        'industry': 'Sản xuất giấy',
        'comment': 'Quan trắc định kỳ hàng tháng - nước thải công nghiệp',
    },
    
    # 6-10: XÂY DỰNG VÀ BẤT ĐỘNG SẢN
    {
        'name': 'CÔNG TY CỔ PHẦN ĐẦU TƯ XÂY DỰNG PHƯƠNG ĐÔNG',
        'vat': '0327890123',
        'street': '890 Nguyễn Huệ',
        'street2': 'Phường Bến Nghé, Quận 1',
        'city': 'TP. Hồ Chí Minh',
        'zip': '700000',
        'phone': '028-3827-4567',
        'mobile': '0967-890-123',
        'email': 'phuongdong@construction.com.vn',
        'website': 'https://phuongdongcons.com.vn',
        'contact_name': 'Nguyễn Quang Hải',
        'title': 'Giám đốc Dự án',
        'industry': 'Xây dựng',
        'comment': 'Cần lập báo cáo ĐTM cho dự án khu đô thị mới',
    },
    {
        'name': 'CÔNG TY TNHH BẤT ĐỘNG SẢN SÀI GÒN',
        'vat': '0330123456',
        'street': '123 Võ Văn Tần',
        'street2': 'Phường 6, Quận 3',
        'city': 'TP. Hồ Chí Minh',
        'zip': '700000',
        'phone': '028-3930-5678',
        'mobile': '0978-901-234',
        'email': 'saigon@bdssaigon.vn',
        'website': 'https://bdssaigon.vn',
        'contact_name': 'Trần Văn Khải',
        'title': 'Phó Tổng Giám đốc',
        'industry': 'Bất động sản',
        'comment': 'Khách hàng thường xuyên - nhiều dự án cần tư vấn',
    },
    {
        'name': 'TỔNG CÔNG TY XÂY DỰNG SỐ 1',
        'vat': '0333456789',
        'street': '456 Lý Thường Kiệt',
        'street2': 'Phường 8, Quận Tân Bình',
        'city': 'TP. Hồ Chí Minh',
        'zip': '700000',
        'phone': '028-3844-6789',
        'mobile': '0989-012-345',
        'email': 'info@xaydung1.com.vn',
        'website': 'https://xaydung1.com.vn',
        'contact_name': 'Lê Thị Lan',
        'title': 'Trưởng phòng HSE',
        'industry': 'Xây dựng',
        'comment': 'Quan trắc môi trường lao động cho công nhân',
    },
    {
        'name': 'CÔNG TY TNHH NHÀ Ở XÃ HỘI VIỆT NAM',
        'vat': '0336789012',
        'street': '789 Võ Thị Sáu',
        'street2': 'Phường 7, Quận 3',
        'city': 'TP. Hồ Chí Minh',
        'zip': '700000',
        'phone': '028-3933-7890',
        'mobile': '0990-123-456',
        'email': 'contact@nhaoxahoi.vn',
        'website': 'https://nhaoxahoi.vn',
        'contact_name': 'Phạm Văn Minh',
        'title': 'Giám đốc',
        'industry': 'Nhà ở xã hội',
        'comment': 'Cần lập kế hoạch bảo vệ môi trường',
    },
    {
        'name': 'CÔNG TY CỔ PHẦN THÉP XÂY DỰNG MIỀN NAM',
        'vat': '0339012345',
        'street': '234 Xa lộ Hà Nội',
        'street2': 'Phường Hiệp Phú, TP. Thủ Đức',
        'city': 'TP. Hồ Chí Minh',
        'zip': '700000',
        'phone': '028-3724-1234',
        'mobile': '0901-234-567',
        'email': 'steel@thepxaydungmn.com',
        'website': 'https://thepxaydungmn.com',
        'contact_name': 'Nguyễn Thị Nga',
        'title': 'Quản đốc Nhà máy',
        'industry': 'Sản xuất thép',
        'comment': 'Quan trắc tiếng ồn, bụi và khí thải',
    },
    
    # 11-15: Y TẾ - BỆNH VIỆN
    {
        'name': 'BỆNH VIỆN ĐA KHOA QUỐC TẾ THÀNH ĐÔ',
        'vat': '0342345678',
        'street': '567 Nguyễn Tri Phương',
        'street2': 'Phường 9, Quận 10',
        'city': 'TP. Hồ Chí Minh',
        'zip': '700000',
        'phone': '028-3862-5678',
        'mobile': '0912-345-678',
        'email': 'admin@thanhdobosp.vn',
        'website': 'https://thanhdobosp.vn',
        'contact_name': 'BS. Trần Văn Phúc',
        'title': 'Giám đốc Bệnh viện',
        'industry': 'Y tế',
        'comment': 'Quan trắc nước thải y tế và khử khuẩn',
    },
    {
        'name': 'PHÒNG KHÁM ĐA KHOA ĐẠI VIỆT',
        'vat': '0345678901',
        'street': '890 Phan Xích Long',
        'street2': 'Phường 2, Quận Phú Nhuận',
        'city': 'TP. Hồ Chí Minh',
        'zip': '700000',
        'phone': '028-3844-8901',
        'mobile': '0923-456-789',
        'email': 'daiviet@clinicvn.com',
        'website': 'https://phongkhamdaiviet.vn',
        'contact_name': 'ThS. BS Lê Minh Tuấn',
        'title': 'Giám đốc Phòng khám',
        'industry': 'Y tế',
        'comment': 'Cần giấy phép xả nước thải y tế',
    },
    {
        'name': 'BỆNH VIỆN CHUYÊN KHOA SẢN NHI BÌNH DƯƠNG',
        'vat': '0348901234',
        'street': '123 Đại lộ Bình Dương',
        'street2': 'Phường Phú Hòa, TP. Thủ Dầu Một',
        'city': 'Bình Dương',
        'zip': '820000',
        'phone': '0274-3567-234',
        'mobile': '0934-567-890',
        'email': 'info@sannibd.vn',
        'website': 'https://benhviensan nhibd.vn',
        'contact_name': 'BS. CKII Nguyễn Thị Xuân',
        'title': 'Phó Giám đốc',
        'industry': 'Y tế',
        'comment': 'Quan trắc định kỳ 3 tháng',
    },
    {
        'name': 'TRUNG TÂM Y TẾ QUẬN TÂN BÌNH',
        'vat': '0351234567',
        'street': '456 Lạc Long Quân',
        'street2': 'Phường 10, Quận Tân Bình',
        'city': 'TP. Hồ Chí Minh',
        'zip': '700000',
        'phone': '028-3862-4567',
        'mobile': '0945-678-901',
        'email': 'ttyt@tanbinhhealth.gov.vn',
        'website': 'https://yttanbinh.gov.vn',
        'contact_name': 'Ông Phạm Quốc Việt',
        'title': 'Giám đốc Trung tâm',
        'industry': 'Y tế công',
        'comment': 'Dịch vụ công - ưu đãi giá',
    },
    {
        'name': 'BỆNH VIỆN MẮT QUỐC TẾ DND',
        'vat': '0354567890',
        'street': '789 Cách Mạng Tháng 8',
        'street2': 'Phường 11, Quận 3',
        'city': 'TP. Hồ Chí Minh',
        'zip': '700000',
        'phone': '028-3930-7890',
        'mobile': '0956-789-012',
        'email': 'contact@dnd-eyehospital.com',
        'website': 'https://benhvienmatdnd.vn',
        'contact_name': 'PGS.TS.BS Lê Văn Đồng',
        'title': 'Giám đốc Chuyên môn',
        'industry': 'Y tế',
        'comment': 'Khách hàng VIP - ưu tiên phục vụ',
    },
    
    # 16-20: KHÁCH SẠN - RESORT - NHÀ HÀNG
    {
        'name': 'KHÁCH SẠN GRAND PLAZA HỒ CHÍ MINH',
        'vat': '0357890123',
        'street': '234 Nguyễn Huệ',
        'street2': 'Phường Bến Nghé, Quận 1',
        'city': 'TP. Hồ Chí Minh',
        'zip': '700000',
        'phone': '028-3827-8901',
        'mobile': '0967-890-123',
        'email': 'reservation@grandplaza.vn',
        'website': 'https://grandplazahcm.com',
        'contact_name': 'Ông Võ Thành Long',
        'title': 'Tổng Giám đốc',
        'industry': 'Khách sạn',
        'comment': 'Quan trắc nước thải và môi trường lao động bếp',
    },
    {
        'name': 'RESORT BIỂN XANH VŨNG TÀU',
        'vat': '0360123456',
        'street': '567 Thùy Vân',
        'street2': 'Phường Thắng Tam',
        'city': 'Vũng Tàu, Bà Rịa - Vũng Tàu',
        'zip': '790000',
        'phone': '0254-3567-456',
        'mobile': '0978-901-234',
        'email': 'info@bienxanhresort.com',
        'website': 'https://bienxanhvungtau.vn',
        'contact_name': 'Bà Nguyễn Thu Hà',
        'title': 'Giám đốc Vận hành',
        'industry': 'Resort',
        'comment': 'Cần giấy phép xả nước thải ra biển',
    },
    {
        'name': 'NHÀ HÀNG TIỆC CƯỚI PALACE',
        'vat': '0363456789',
        'street': '890 Xa lộ Hà Nội',
        'street2': 'Phường Thảo Điền, TP. Thủ Đức',
        'city': 'TP. Hồ Chí Minh',
        'zip': '700000',
        'phone': '028-3744-6789',
        'mobile': '0989-012-345',
        'email': 'palace@wedding.vn',
        'website': 'https://palacewedding.vn',
        'contact_name': 'Ông Trần Đức Thắng',
        'title': 'Chủ nhà hàng',
        'industry': 'Nhà hàng',
        'comment': 'Quan trắc bếp - tiếng ồn, nhiệt độ',
    },
    {
        'name': 'KHÁCH SẠN SUNRISE BÌNH DƯƠNG',
        'vat': '0366789012',
        'street': '123 Phạm Văn Đồng',
        'street2': 'Phường Phú Hòa, TP. Thủ Dầu Một',
        'city': 'Bình Dương',
        'zip': '820000',
        'phone': '0274-3856-012',
        'mobile': '0990-123-456',
        'email': 'sunrise@hotel bd.com',
        'website': 'https://sunrisehotelbd.vn',
        'contact_name': 'Bà Lê Thu Thảo',
        'title': 'Giám đốc Khách sạn',
        'industry': 'Khách sạn',
        'comment': 'Quan trắc định kỳ 6 tháng',
    },
    {
        'name': 'TẬP ĐOÀN ĂN UỐNG GOLDEN GATE',
        'vat': '0369012345',
        'street': '456 Lê Thánh Tông',
        'street2': 'Phường Bến Thành, Quận 1',
        'city': 'TP. Hồ Chí Minh',
        'zip': '700000',
        'phone': '028-3827-2345',
        'mobile': '0901-234-567',
        'email': 'hr@goldengate-group.vn',
        'website': 'https://goldengate-group.com.vn',
        'contact_name': 'Bà Đỗ Hải Yến',
        'title': 'Giám đốc Vận hành',
        'industry': 'Chuỗi nhà hàng',
        'comment': 'Hệ thống 50+ nhà hàng - hợp đồng dài hạn',
    },
    
    # 21-25: NHÀ MÁY - KHU CÔNG NGHIỆP
    {
        'name': 'CÔNG TY TNHH SẢN XUẤT LINH KIỆN ĐIỆN TỬ SAMSUNG',
        'vat': '0372345678',
        'street': '789 Đường số 1, KCN Việt Nam - Singapore',
        'street2': 'Phường Thường Thạnh, Quận Cái Răng',
        'city': 'TP. Cần Thơ',
        'zip': '900000',
        'phone': '0292-3730-678',
        'mobile': '0912-345-678',
        'email': 'env@samsung-vietnam.vn',
        'website': 'https://samsung.com.vn',
        'contact_name': 'Ông Kim Jong Un',
        'title': 'Environment Manager',
        'industry': 'Điện tử',
        'comment': 'Khách hàng lớn - yêu cầu cao về chất lượng',
    },
    {
        'name': 'NHÀ MÁY SẢN XUẤT GIÀY DA VIỆT NAM',
        'vat': '0375678901',
        'street': '234 KCN Long Thành',
        'street2': 'Huyện Long Thành',
        'city': 'Đồng Nai',
        'zip': '810000',
        'phone': '0251-3567-901',
        'mobile': '0923-456-789',
        'email': 'contact@shoesvietnamese.com',
        'website': 'https://giaydavietnam.vn',
        'contact_name': 'Ông Phan Văn Tú',
        'title': 'Giám đốc Sản xuất',
        'industry': 'Sản xuất giày dép',
        'comment': 'Quan trắc môi trường lao động - hóa chất và bụi',
    },
    {
        'name': 'CÔNG TY CỔ PHẦN HÓA CHẤT ĐỒNG NAI',
        'vat': '0378901234',
        'street': '567 Quốc lộ 51',
        'street2': 'KCN Long Bình, Biên Hòa',
        'city': 'Đồng Nai',
        'zip': '810000',
        'phone': '0251-3678-234',
        'mobile': '0934-567-890',
        'email': 'info@hoachatdongnai.vn',
        'website': 'https://hoachatdongnai.vn',
        'contact_name': 'Ông Nguyễn Trọng Nghĩa',
        'title': 'Trưởng phòng EHS',
        'industry': 'Hóa chất',
        'comment': 'Quan trắc thường xuyên - chất nguy hại',
    },
    {
        'name': 'NHÀ MÁY CHẾ BIẾN THỦY SẢN MIỀN TÂY',
        'vat': '0381234567',
        'street': '890 Quốc lộ 1A',
        'street2': 'Xã Long Hòa, Huyện Cần Giuộc',
        'city': 'Long An',
        'zip': '850000',
        'phone': '0272-3567-567',
        'mobile': '0945-678-901',
        'email': 'seafood@mientay.vn',
        'website': 'https://thuysanmientay.com.vn',
        'contact_name': 'Bà Võ Thị Mai',
        'title': 'Phó Giám đốc',
        'industry': 'Chế biến thủy sản',
        'comment': 'Quan trắc nước thải và mùi hôi',
    },
    {
        'name': 'CÔNG TY TNHH SẢN XUẤT PHỤ TÙNG Ô TÔ VIỆT NAM',
        'vat': '0384567890',
        'street': '123 KCN Đồng An',
        'street2': 'Huyện Thuận An',
        'city': 'Bình Dương',
        'zip': '820000',
        'phone': '0274-3890-890',
        'mobile': '0956-789-012',
        'email': 'autoparts@vietnam-auto.vn',
        'website': 'https://phutungoto-vn.com',
        'contact_name': 'Ông Lê Quốc Anh',
        'title': 'Giám đốc Nhà máy',
        'industry': 'Cơ khí',
        'comment': 'Quan trắc tiếng ồn, dầu mỡ và kim loại nặng',
    },
    
    # 26-30: TRƯỜNG HỌC - CÔNG TRÌNH CÔNG CỘNG
    {
        'name': 'TRƯỜNG ĐẠI HỌC CÔNG NGHỆ TP.HCM',
        'vat': '0387890123',
        'street': '456 Lý Thường Kiệt',
        'street2': 'Phường 14, Quận 10',
        'city': 'TP. Hồ Chí Minh',
        'zip': '700000',
        'phone': '028-3865-0123',
        'mobile': '0967-890-123',
        'email': 'hcmut@hcmut.edu.vn',
        'website': 'https://hcmut.edu.vn',
        'contact_name': 'PGS.TS Trần Văn Bảo',
        'title': 'Phó Hiệu trưởng',
        'industry': 'Giáo dục',
        'comment': 'Quan trắc phòng thí nghiệm hóa học',
    },
    {
        'name': 'TRUNG TÂM THƯƠNG MẠI VINCOM CENTER',
        'vat': '0390123456',
        'street': '789 Đồng Khởi',
        'street2': 'Phường Bến Nghé, Quận 1',
        'city': 'TP. Hồ Chí Minh',
        'zip': '700000',
        'phone': '028-3827-3456',
        'mobile': '0978-901-234',
        'email': 'management@vincom.vn',
        'website': 'https://vincom.com.vn',
        'contact_name': 'Bà Đặng Thu Hương',
        'title': 'Giám đốc Vận hành',
        'industry': 'Thương mại',
        'comment': 'Quan trắc hệ thống điều hòa và nước thải',
    },
    {
        'name': 'SÂN BAY QUỐC TẾ TÂN SƠN NHẤT',
        'vat': '0393456789',
        'street': 'Trường Sơn',
        'street2': 'Phường 2, Quận Tân Bình',
        'city': 'TP. Hồ Chí Minh',
        'zip': '700000',
        'phone': '028-3848-5383',
        'mobile': '0989-012-345',
        'email': 'environment@tansonnhat.aero',
        'website': 'https://tansonnhatairport.vn',
        'contact_name': 'Ông Võ Hữu Đức',
        'title': 'Phó Cảng vụ trưởng',
        'industry': 'Hàng không',
        'comment': 'Quan trắc tiếng ồn máy bay và chất lượng không khí',
    },
    {
        'name': 'BỆNH VIỆN ĐA KHOA TRUNG ƯƠNG CẦN THƠ',
        'vat': '0396789012',
        'street': '234 Hòa Bình',
        'street2': 'Phường Xuân Khánh, Quận Ninh Kiều',
        'city': 'TP. Cần Thơ',
        'zip': '900000',
        'phone': '0292-3730-789',
        'mobile': '0990-123-456',
        'email': 'bvct@cantho-hospital.vn',
        'website': 'https://benhvien-cantho.vn',
        'contact_name': 'ThS.BS Lê Văn Thành',
        'title': 'Giám đốc Bệnh viện',
        'industry': 'Y tế công',
        'comment': 'Bệnh viện hạng I - yêu cầu cao',
    },
    {
        'name': 'CÔNG TY CỔ PHẦN CẤP NƯỚC THÀNH PHỐ',
        'vat': '0399012345',
        'street': '567 Cộng Hòa',
        'street2': 'Phường 13, Quận Tân Bình',
        'city': 'TP. Hồ Chí Minh',
        'zip': '700000',
        'phone': '028-3997-7777',
        'mobile': '0901-234-567',
        'email': 'sawaco@sawaco.com.vn',
        'website': 'https://sawaco.com.vn',
        'contact_name': 'Ông Phạm Đức Toàn',
        'title': 'Tổng Giám đốc',
        'industry': 'Cấp nước',
        'comment': 'Quan trắc chất lượng nước sạch định kỳ',
    },
]

# ========================================
# TẠO KHÁCH HÀNG
# ========================================
print("="*70)
print("👥 TẠO 30 KHÁCH HÀNG CHO SGC")
print("="*70 + "\n")

created = 0
existing = 0
errors = 0

# Lấy country Vietnam
vietnam_id = models.execute_kw(db, uid, password,
    'res.country', 'search',
    [[('code', '=', 'VN')]], {'limit': 1})

vietnam_id = vietnam_id[0] if vietnam_id else False

for idx, customer in enumerate(customers_data, 1):
    try:
        # Kiểm tra tồn tại theo mã số thuế
        existing_customer = models.execute_kw(db, uid, password,
            'res.partner', 'search',
            [[('vat', '=', customer['vat'])]], {'limit': 1})
        
        if existing_customer:
            existing += 1
            print(f"  {idx:2d}. ⊘ {customer['name'][:50]:<50} [Đã tồn tại]")
            continue
        
        # Chuẩn bị dữ liệu
        partner_data = {
            'name': customer['name'],
            'is_company': True,
            'customer_rank': 1,
            'vat': customer['vat'],
            'street': customer['street'],
            'street2': customer.get('street2', ''),
            'city': customer['city'],
            'zip': customer.get('zip', ''),
            'country_id': vietnam_id,
            'phone': customer.get('phone', ''),
            'email': customer['email'],
            'website': customer.get('website', ''),
            'comment': customer.get('comment', ''),
        }
        
        # Tạo công ty
        partner_id = models.execute_kw(db, uid, password,
            'res.partner', 'create', [partner_data])
        
        # Tạo người liên hệ (contact person) nếu có
        if customer.get('contact_name'):
            contact_data = {
                'name': customer['contact_name'],
                'parent_id': partner_id,
                'type': 'contact',
                'function': customer.get('title', ''),
                'email': customer['email'],
                'phone': customer.get('phone', ''),
            }
            models.execute_kw(db, uid, password,
                'res.partner', 'create', [contact_data])
        
        created += 1
        industry_icon = {
            'Sản xuất': '🏭',
            'Xây dựng': '🏗️',
            'Y tế': '🏥',
            'Khách sạn': '🏨',
            'Giáo dục': '🎓',
        }.get(customer.get('industry', '')[:10], '🏢')
        
        print(f"  {idx:2d}. ✅ {customer['name'][:50]:<50} {industry_icon}")
        
    except Exception as e:
        errors += 1
        if errors <= 3:  # Print chi tiết 3 lỗi đầu
            print(f"  {idx:2d}. ❌ {customer['name'][:50]}")
            print(f"        Lỗi: {str(e)}\n")
        else:
            print(f"  {idx:2d}. ❌ {customer['name'][:50]:<50} [Lỗi]")

# ========================================
# TÓM TẮT
# ========================================
print("\n" + "="*70)
print("✅ HOÀN THÀNH!")
print("="*70)
print(f"""
📊 Tóm tắt:
  • Đã tạo mới: {created} khách hàng
  • Đã tồn tại: {existing} khách hàng
  • Lỗi: {errors}
  • Tổng cộng: {len(customers_data)} khách hàng

🏢 Phân loại khách hàng:
  • Công ty sản xuất: 5 (Thực phẩm, Dệt may, Gỗ, Nhựa, Giấy)
  • Xây dựng & BĐS: 5 (Xây dựng, Phát triển dự án, Thép)
  • Y tế: 5 (Bệnh viện, Phòng khám)
  • Khách sạn & Resort: 5 (Khách sạn, Resort, Nhà hàng)
  • Nhà máy & KCN: 5 (Điện tử, Giày da, Hóa chất, Thủy sản, Ô tô)
  • Công trình công: 5 (Trường học, TT thương mại, Sân bay, Cấp nước)

✨ Thông tin đầy đủ:
  ✓ Tên công ty
  ✓ Mã số thuế (10 chữ số)
  ✓ Địa chỉ chi tiết
  ✓ Điện thoại & Email
  ✓ Website
  ✓ Người đại diện & Chức vụ
  ✓ Ghi chú về nhu cầu dịch vụ

📍 Kiểm tra trong Odoo:
  → Sales → Customers
  → Hoặc CRM → Customers
""")

