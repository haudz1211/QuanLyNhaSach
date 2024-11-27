import datetime
import hashlib
import cloudinary.uploader
from thebooks.models import Sach, TheLoai, NguoiDung, KhachHang, UserRole, DonHang, ChiTietDonHang, BinhLuan, StatusEnum
from thebooks import app, db
from sqlalchemy import func
from flask_login import current_user


def lay_the_loai():
    the_loai = TheLoai.query.filter(TheLoai.active.__eq__(True))

    return the_loai.all()


def lay_tat_ca_sach():
    return Sach.query.filter(Sach.active.__eq__(True)).all()


def lay_sach_theo_id(id):
    return Sach.query.get(id)


def lay_sach(kw=None, the_loai_id=None, trang=None):
    sach = Sach.query

    if kw:
        sach = sach.filter(Sach.ten.contains(kw))

    if the_loai_id:
        sach = sach.filter(Sach.the_loai_id.__eq__(the_loai_id))

    so_sach = sach.count()

    page_size = app.config['PAGE_SIZE']
    if trang:
        trang = int(trang)
        start = (trang - 1) * page_size
        return {
            'sach': sach.slice(start, start + page_size).all(),
            'so_sach': so_sach
        }
    else:
        return {
            'sach': sach.slice(0, page_size).all(),
            'so_sach': so_sach
        }


def them_nguoi_dung(ten=None,username=None, password=None, sdt=None, email=None, dia_chi=None, hinh_anh =None, role=None):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    nguoi_dung = NguoiDung(ten=ten, username=username, password=password, sdt=sdt, email=email, dia_chi=dia_chi,hinh_anh=hinh_anh, role=role)

    db.session.add(nguoi_dung)
    return nguoi_dung


def them_khach_hang(ten=None,username=None, password=None, sdt=None, email=None, dia_chi=None, avatar=None):
    nguoi_dung = them_nguoi_dung(ten, username, password, sdt, email, dia_chi, avatar, UserRole.khach_hang)
    khach_hang = KhachHang(nguoi_dung=nguoi_dung)

    if avatar:
        res = cloudinary.uploader.upload(avatar)
        khach_hang.avatar = res['secure_url']
        nguoi_dung.hinh_anh = res['secure_url']
    db.session.add(khach_hang)
    db.session.commit()


def chung_thuc_nguoi_dung(username=None, password=None):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())

    return NguoiDung.query.filter(NguoiDung.username.__eq__(username),
                                  NguoiDung.password.__eq__(password)).first()

def lay_nguoi_dung_theo_id(id):
    return NguoiDung.query.get(id)

def them_don_hang(gio_hang=None, khach_hang_id=None, nhan_vien_id=None):
    if gio_hang:
        khach_hang = lay_nguoi_dung_theo_id(khach_hang_id).khach_hang
        nhan_vien = None
        if nhan_vien_id:
            nhan_vien = lay_nguoi_dung_theo_id(nhan_vien_id).nhan_vien
        h = DonHang(khach_hang=khach_hang, nhan_vien=nhan_vien)
        db.session.add(h)

        try:
            for g in gio_hang.values():
                sach = Sach.query.get(g['id'])
                if not sach:
                    raise Exception(f"Sách với ID {g['id']} không tồn tại.")

                # Kiểm tra số lượng sách có đủ hay không
                if sach.so_luong < g['so_luong']:
                    raise Exception(f"Số lượng không đủ cho sách '{sach.ten}'.")

                # Trừ số lượng sách trong kho
                sach.so_luong -= g['so_luong']

                # Thêm chi tiết đơn hàng
                c = ChiTietDonHang(
                    sach_id=g['id'],
                    gia=g['gia'],
                    so_luong=g['so_luong'],
                    don_hang=h
                )
                db.session.add(c)

            # Commit tất cả thay đổi
            db.session.commit()
            return True

        except Exception as e:
            db.session.rollback()  # Rollback nếu có lỗi
            return str(e)  # Trả về lỗi cụ thể cho frontend

    return "Giỏ hàng trống!"


def lay_khach_hang_theo_sdt(sdt=None):
    return NguoiDung.query.filter(NguoiDung.sdt.__eq__(sdt)).first()


def lay_binh_luan(id):
    return BinhLuan.query.filter(BinhLuan.sach_id.__eq__(id)).all()


def them_binh_luan(sach_id, binh_luan):
    d = BinhLuan(sach_id=sach_id, binh_luan=binh_luan, khach_hang=current_user.khach_hang)
    db.session.add(d)
    db.session.commit()

    return d


def thong_ke_doanh_thu_theo_thang(thang=None, nam=None):
    query = db.session.query(TheLoai.id, TheLoai.ten, func.sum(ChiTietDonHang.so_luong * ChiTietDonHang.gia),
                             func.sum(ChiTietDonHang.so_luong)) \
        .join(Sach, Sach.the_loai_id.__eq__(TheLoai.id), isouter=True) \
        .join(ChiTietDonHang, ChiTietDonHang.sach_id.__eq__(Sach.id)) \
        .join(DonHang, ChiTietDonHang.don_hang_id.__eq__(DonHang.id))
    if nam:
        query = query.filter(func.extract('year', DonHang.ngay_thanh_toan) == nam)
    if thang:
        query = query.filter(func.extract('month', DonHang.ngay_thanh_toan) == thang)
    return query.group_by(TheLoai.id).all()


def thong_ke_theo_tan_suat(thang=None, nam=None):
    query = db.session.query(Sach.id, Sach.ten, TheLoai.ten, func.sum(ChiTietDonHang.so_luong)) \
        .join(Sach, Sach.the_loai_id.__eq__(TheLoai.id)) \
        .join(ChiTietDonHang, ChiTietDonHang.sach_id.__eq__(Sach.id)) \
        .join(DonHang, ChiTietDonHang.don_hang_id.__eq__(DonHang.id))

    if thang:
        query = query.filter(func.extract('year', DonHang.ngay_thanh_toan) == nam)

    if nam:
        query = query.filter(func.extract('month', DonHang.ngay_thanh_toan) == thang)

    return query.group_by(Sach.id).order_by(-Sach.id).all()




if __name__ == '__main__':
    with app.app_context():
        print(thong_ke_theo_tan_suat())