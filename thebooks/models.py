import hashlib
import os

from sqlalchemy import Column, Integer, String, Float, Boolean, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from thebooks import db, app
from flask_login import UserMixin
from datetime import datetime
import enum


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    active = Column(Boolean, default=True)

def initialize_database():
    if not os.path.exists('thebooks.db'):
        db.create_all()
        print("Đã tạo cơ sở dữ liệu 'thebooks.db'")
    else:
        print("Cơ sở dữ liệu 'thebooks.db' đã tồn tại")

# Gọi hàm để kiểm tra và tạo cơ sở dữ liệu nếu chưa có
with app.app_context():
    initialize_database()


class TheLoai(BaseModel):
    ten = Column(String(50), nullable=False, unique=True)
    sachs = relationship('Sach', backref='the_loai', lazy=True)

    def __str__(self):
        return self.ten


class Sach(BaseModel):
    ten = Column(String(50), nullable=False, unique=True)
    gia = Column(Float, default=50000)
    so_luong = Column(Integer, default=0)
    hinh_anh = Column(String(200))
    nxb = Column(String(50))
    tac_gia = Column(String(100), nullable=False)
    the_loai_id = Column(Integer, ForeignKey(TheLoai.id), nullable=False)
    phieu_nhaps = relationship('ChiTietPhieuNhap', backref='sach', lazy=True)
    khach_hangs = relationship('BinhLuan', backref='sach', lazy=True)
    don_hangs = relationship('ChiTietDonHang', backref='sach', lazy=True)
    quy_dinh_nhap_sach = relationship('QuyDinhNhapSach', backref='sach', uselist=False, lazy=True)

    def __str__(self):
        return self.ten


class PhieuNhap(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ngay_nhap = Column(DateTime, default=datetime.now)
    sachs = relationship('ChiTietPhieuNhap', backref='phieu_nhap', lazy=True)
    quan_ly_kho_id = Column(Integer, ForeignKey('quan_ly_kho.id'), nullable=False)


class ChiTietPhieuNhap(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    so_luong = Column(Integer, default=0)
    sach_id = Column(Integer, ForeignKey(Sach.id), nullable=False)
    phieu_nhap_id = Column(Integer, ForeignKey(PhieuNhap.id), nullable=False)


class BinhLuan(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    binh_luan = Column(String(500))
    ngay_tao = Column(DateTime, default=datetime.now)
    sach_id = Column(Integer, ForeignKey(Sach.id), nullable=False)
    khach_hang_id = Column(Integer, ForeignKey('khach_hang.id'), nullable=False)


class UserRole(enum.Enum):
    quan_tri_vien = 1
    quan_ly = 2
    quan_ly_kho = 3
    nhan_vien = 4
    khach_hang = 5


class NguoiDung(BaseModel, UserMixin):
    ten = Column(String(50), nullable=False)
    username = Column(String(30), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    email = Column(String(30), unique=True)
    sdt = Column(String(20), unique=True)
    dia_chi = Column(String(200))
    role = Column(Enum(UserRole), default=UserRole.khach_hang)
    khach_hang = relationship('KhachHang', uselist=False, backref='nguoi_dung', lazy=True)
    nhan_vien = relationship('NhanVien', uselist=False, backref='nguoi_dung', lazy=True)
    quan_tri_vien = relationship('QuanTriVien', uselist=False, backref='nguoi_dung', lazy=True)
    quan_ly = relationship('QuanLy', uselist=False, backref='nguoi_dung', lazy=True)
    quan_ly_kho = relationship('QuanLyKho', uselist=False, backref='nguoi_dung', lazy=True)

    def __str__(self):
        return self.ten


class KhachHang(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    avatar = Column(String(200), default='https://res.cloudinary.com/demo/image/upload/getting-started/shoes.jpg')
    nguoi_dung_id = Column(Integer, ForeignKey(NguoiDung.id), nullable=False)
    don_hangs = relationship('DonHang', backref='khach_hang', lazy=True)
    sachs = relationship('BinhLuan', backref='khach_hang', lazy=True)


class NhanVien(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    nguoi_dung_id = Column(Integer, ForeignKey(NguoiDung.id), nullable=False)
    don_hangs = relationship('DonHang', backref='nhan_vien', lazy=True)


class StatusEnum(enum.Enum):
    cho_thanh_toan = 1
    dang_giao = 2
    da_thanh_toan = 3
    da_huy = 4


class DonHang(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ngay_tao = Column(DateTime, default=datetime.now)
    status = Column(Enum(StatusEnum), default=StatusEnum.da_thanh_toan)
    ngay_thanh_toan = Column(DateTime, default=datetime.now)
    ngay_huy = Column(DateTime)
    sachs = relationship('ChiTietDonHang', backref='don_hang', lazy='subquery')
    khach_hang_id = Column(Integer, ForeignKey(KhachHang.id), nullable=False)
    nhan_vien_id = Column(Integer, ForeignKey(NhanVien.id))


class ChiTietDonHang(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    so_luong = Column(Integer, default=1)
    gia = Column(Float, default=0)
    sach_id = Column(Integer, ForeignKey(Sach.id), nullable=False)
    don_hang_id = Column(Integer, ForeignKey(DonHang.id), nullable=False)


class QuanLyKho(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    nguoi_dung_id = Column(Integer, ForeignKey(NguoiDung.id), nullable=False)
    phieu_nhap = relationship('PhieuNhap', backref='quan_ly_kho', lazy=True)


class QuanLy(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    nguoi_dung_id = Column(Integer, ForeignKey(NguoiDung.id), nullable=False)


class QuanTriVien(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    nguoi_dung_id = Column(Integer, ForeignKey(NguoiDung.id), nullable=False)


class QuyDinhNhapSach(db.Model):
    __tablename__ = 'quy_dinh_nhap_sach'
    id = db.Column(db.Integer, primary_key=True)
    so_luong_nhap_toi_thieu = db.Column(db.Integer)
    so_luong_ton_toi_thieu = db.Column(db.Integer)
    sach_id = db.Column(db.Integer, db.ForeignKey('sach.id'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        nguoi_dung = NguoiDung(
            ten='Trịnh Đoàn Hậu',
            username='doanhau',
            password=hashlib.md5('12345'.encode()).hexdigest(),
            email='trinhdoanhauu@gmail.com',
            sdt='0346469539',
            dia_chi='Hồ Chí Minh',
            role=UserRole.quan_ly,
            quan_ly=QuanLy()
        )
        db.session.add(nguoi_dung)

        # Tạo 5 thể loại
        theloai_list = [
            TheLoai(ten='Công nghệ thông tin'),
            TheLoai(ten='Lịch sử'),
            TheLoai(ten='Văn học'),
            TheLoai(ten='Khoa học'),
            TheLoai(ten='Kinh tế')
        ]
        db.session.add_all(theloai_list)

        sach_mau = [
            {'ten': 'Python Programming', 'gia': 150000, 'so_luong': 10,
             'hinh_anh': 'https://images-na.ssl-images-amazon.com/images/I/81L3B8zRbYL.jpg', 'the_loai_id': 1,
             'nxb': 'NXB Công Nghệ', 'tac_gia': 'John Zelle'},

            {'ten': 'JavaScript: The Good Parts', 'gia': 200000, 'so_luong': 5,
             'hinh_anh': 'https://images-na.ssl-images-amazon.com/images/I/51Zt+N9GzZL.jpg', 'the_loai_id': 1,
             'nxb': 'O\'Reilly Media', 'tac_gia': 'Douglas Crockford'},

            {'ten': 'Introduction to Algorithms', 'gia': 300000, 'so_luong': 7,
             'hinh_anh': 'https://images-na.ssl-images-amazon.com/images/I/41WZW9G1miL.jpg', 'the_loai_id': 1,
             'nxb': 'MIT Press', 'tac_gia': 'Thomas H. Cormen'},

            {'ten': 'The Pragmatic Programmer', 'gia': 250000, 'so_luong': 4,
             'hinh_anh': 'https://images-na.ssl-images-amazon.com/images/I/41j7u40g7PL.jpg', 'the_loai_id': 1,
             'nxb': 'Addison-Wesley', 'tac_gia': 'Andrew Hunt'},

            {'ten': 'Clean Code', 'gia': 220000, 'so_luong': 8,
             'hinh_anh': 'https://images-na.ssl-images-amazon.com/images/I/51nF39mC5bL.jpg', 'the_loai_id': 1,
             'nxb': 'Prentice Hall', 'tac_gia': 'Robert C. Martin'},

            {'ten': 'Learning Python', 'gia': 180000, 'so_luong': 6,
             'hinh_anh': 'https://images-na.ssl-images-amazon.com/images/I/51eZaqP1P2L.jpg', 'the_loai_id': 1,
             'nxb': 'O\'Reilly Media', 'tac_gia': 'Mark Lutz'},

            {'ten': 'Fluent Python', 'gia': 270000, 'so_luong': 5,
             'hinh_anh': 'https://images-na.ssl-images-amazon.com/images/I/51nH9R1Z5ML.jpg', 'the_loai_id': 1,
             'nxb': 'O\'Reilly Media', 'tac_gia': 'Luciano Ramalho'},

            {'ten': 'Head First Java', 'gia': 240000, 'so_luong': 3,
             'hinh_anh': 'https://images-na.ssl-images-amazon.com/images/I/51hB-Vj6zFL.jpg', 'the_loai_id': 1,
             'nxb': 'O\'Reilly Media', 'tac_gia': 'Kathy Sierra'},

            {'ten': 'Eloquent JavaScript', 'gia': 160000, 'so_luong': 12,
             'hinh_anh': 'https://images-na.ssl-images-amazon.com/images/I/51XQws5e7NL.jpg', 'the_loai_id': 1,
             'nxb': 'No Starch Press', 'tac_gia': 'Marijn Haverbeke'},

            {'ten': 'You Don\'t Know JS', 'gia': 190000, 'so_luong': 9,
             'hinh_anh': 'https://images-na.ssl-images-amazon.com/images/I/51M16B1FqLL.jpg', 'the_loai_id': 1,
             'nxb': 'O\'Reilly Media', 'tac_gia': 'Kyle Simpson'},

            {'ten': 'The Art of Computer Programming', 'gia': 500000, 'so_luong': 2,
             'hinh_anh': 'https://images-na.ssl-images-amazon.com/images/I/51xuM2Hqg1L.jpg', 'the_loai_id': 1,
             'nxb': 'Addison-Wesley', 'tac_gia': 'Donald E. Knuth'},

            {'ten': 'Artificial Intelligence: A Modern Approach', 'gia': 400000, 'so_luong': 5,
             'hinh_anh': 'https://images-na.ssl-images-amazon.com/images/I/41Jty7kJ36L.jpg', 'the_loai_id': 1,
             'nxb': 'Prentice Hall', 'tac_gia': 'Stuart Russell'},

            {'ten': 'The Mythical Man-Month', 'gia': 210000, 'so_luong': 4,
             'hinh_anh': 'https://images-na.ssl-images-amazon.com/images/I/51lpxDg8K5L.jpg', 'the_loai_id': 1,
             'nxb': 'Addison-Wesley', 'tac_gia': 'Frederick P. Brooks Jr.'},

            {'ten': 'Design Patterns', 'gia': 330000, 'so_luong': 3,
             'hinh_anh': 'https://images-na.ssl-images-amazon.com/images/I/41q-r9W4CWL.jpg', 'the_loai_id': 1,
             'nxb': 'Addison-Wesley', 'tac_gia': 'Erich Gamma'},

            {'ten': 'The Phoenix Project', 'gia': 280000, 'so_luong': 6,
             'hinh_anh': 'https://images-na.ssl-images-amazon.com/images/I/51Ew+Wh4fzL.jpg', 'the_loai_id': 1,
             'nxb': 'IT Revolution Press', 'tac_gia': 'Gene Kim'},

            {'ten': 'Deep Learning', 'gia': 350000, 'so_luong': 2,
             'hinh_anh': 'https://images-na.ssl-images-amazon.com/images/I/51MKlKvTXQL.jpg', 'the_loai_id': 1,
             'nxb': 'MIT Press', 'tac_gia': 'Ian Goodfellow'},

            {'ten': 'Python Data Science Handbook', 'gia': 240000, 'so_luong': 5,
             'hinh_anh': 'https://images-na.ssl-images-amazon.com/images/I/51Vw6lsqqyL.jpg', 'the_loai_id': 1,
             'nxb': 'O\'Reilly Media', 'tac_gia': 'Jake VanderPlas'},

            {'ten': 'Understanding Machine Learning', 'gia': 260000, 'so_luong': 4,
             'hinh_anh': 'https://images-na.ssl-images-amazon.com/images/I/51nPzCD5xuL.jpg', 'the_loai_id': 1,
             'nxb': 'MIT Press', 'tac_gia': 'Shai Shalev-Shwartz'},
        ]

        for s in sach_mau:
            sach = Sach(**s)
            db.session.add(sach)

        db.session.commit()
        print("Dữ liệu mẫu đã được thêm vào cơ sở dữ liệu.")

