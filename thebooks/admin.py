import os

from flask_admin.contrib.sqla.fields import QuerySelectField
from flask_admin.form import FileUploadField
from thebooks import admin, db, dao, utils, upload_image_to_cloudinary
from thebooks.models import Sach, TheLoai, KhachHang, QuyDinhNhapSach, PhieuNhap, ChiTietPhieuNhap, NguoiDung, NhanVien, QuanLy, QuanTriVien, QuanLyKho
from flask import session, redirect, request
from flask_admin.contrib.sqla import ModelView
from flask_login import logout_user, current_user
from flask_admin import expose, BaseView
from thebooks.models import UserRole

from cloudinary.uploader import upload as cloudinary_upload
class MyView(ModelView):
    edit_modal = True,
    create_modal = True


class AuthenticatedNhanVien(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == UserRole.nhan_vien


class AuthenticatedQuanLyKho(MyView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == UserRole.quan_ly_kho


class AuthenticatedQuanLy(MyView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == UserRole.quan_ly


class AuthenticatedQuanTri(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == UserRole.quan_tri_vien


class AuthenticatedKhachHang(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == UserRole.khach_hang


class SachView(AuthenticatedQuanLy):
    column_list = ['id', 'ten', 'gia', 'so_luong', 'the_loai', 'tac_gia', 'nxb', 'hinh_anh']
    form_columns = ['ten', 'gia', 'so_luong', 'the_loai_id', 'tac_gia', 'nxb', 'hinh_anh', 'active']

    form_extra_fields = {
        'the_loai_id': QuerySelectField(
            'Thể loại',
            query_factory=lambda: TheLoai.query.all(),
            get_label='ten',
            allow_blank=False
        ),
        'hinh_anh': FileUploadField('Hình ảnh', base_path='static/uploads/', allowed_extensions=('jpg', 'jpeg', 'png', 'gif'))
    }

    def on_model_change(self, form, model, is_created):
        # Kiểm tra và lưu tệp hình ảnh lên Cloudinary
        if form.hinh_anh.data and hasattr(form.hinh_anh.data, 'filename'):
            print("Tệp hình ảnh:", form.hinh_anh.data.filename)
            print("Kích thước tệp:", form.hinh_anh.data.read())  # Đọc một lần để kiểm tra kích thước
            form.hinh_anh.data.seek(0)  # Đặt lại con trỏ về đầu tệp sau khi đọc
            image_url = upload_image_to_cloudinary(form.hinh_anh.data)
            if image_url:
                model.hinh_anh = image_url
            else:
                print("Không thể tải lên hình ảnh.")

        # Lấy ID của thể loại từ form
        model.the_loai_id = form.the_loai_id.data.id if form.the_loai_id.data else None

        # Kiểm tra quy định nhập sách
        quy_dinh = QuyDinhNhapSach.query.filter_by(sach_id=model.id).first()
        if quy_dinh:
            if form.so_luong.data < quy_dinh.so_luong_nhap_toi_thieu:
                raise ValueError(f"Số lượng nhập vào không được nhỏ hơn {quy_dinh.so_luong_nhap_toi_thieu}.")

        # Tạo quy định nhập sách nếu sách được tạo mới
        if is_created:
            quy_dinh_nhap_sach = QuyDinhNhapSach(
                so_luong_nhap_toi_thieu=QuyDinhNhapSach.so_luong_nhap_toi_thieu,
                so_luong_ton_toi_thieu=QuyDinhNhapSach.so_luong_ton_toi_thieu,
                sach_id=model.id
            )
            db.session.add(quy_dinh_nhap_sach)

        db.session.commit()  # Lưu thay đổi vào cơ sở dữ liệu

class TheLoaiView(AuthenticatedQuanLy):
    pass


class QuyDinhNhapSachView(MyView):
    column_list = ['id', 'so_luong_nhap_toi_thieu', 'so_luong_ton_toi_thieu']
    form_columns = ['so_luong_nhap_toi_thieu', 'so_luong_ton_toi_thieu']

    def on_model_change(self, form, model, is_created):
        # Xử lý khi quy định nhập sách được thay đổi
        pass  # Bạn có thể thêm logic tùy chỉnh tại đây nếu cần

class ThongKeTheoDoanhThuView(AuthenticatedQuanTri):
    @expose('/')
    def index(self):
        thang = request.args.get('thang')
        nam = request.args.get('nam')
        return self.render('admin/stats-revenuo.html', thong_ke=dao.thong_ke_doanh_thu_theo_thang(thang=thang, nam=nam), nam=nam, thang=thang)


class ThongKeTheoTanSuatView(AuthenticatedQuanTri):
    @expose('/')
    def index(self):
        thang = request.args.get('thang')
        nam = request.args.get('nam')
        return self.render('admin/stats-frequency.html', thong_ke=dao.thong_ke_theo_tan_suat(thang=thang, nam=nam), nam=nam, thang=thang)


class BanSachView(AuthenticatedNhanVien):
    @expose('/')
    def index(self):
        return self.render('admin/sell.html', thong_tin_don_hang=utils.cart_info(session.get('don_hang')))


class PhieuNhapView(AuthenticatedQuanLyKho):
    form_columns = ['ngay_nhap', 'quan_ly_kho_id']
    column_list = ['id', 'ngay_nhap', 'quan_ly_kho.nguoi_dung']


class ChiTietPhieuNhapView(AuthenticatedQuanLyKho):
    column_list = ['sach', 'phieu_nhap', 'so_luong']
    form_columns = ['sach_id', 'phieu_nhap_id', 'so_luong']


class NhanVienView(AuthenticatedQuanLy):
    column_list = ['id', 'nguoi_dung']
    form_columns = ['nguoi_dung_id']
    form_extra_fields = {
        'nguoi_dung_id': QuerySelectField(
            'Người Dùng',
            query_factory=lambda: NguoiDung.query.all(),
            get_label='ten',
            allow_blank=False
        )
    }


class KhachHangView(AuthenticatedQuanLy):
    column_list = ['id', 'nguoi_dung']
    form_columns = ['nguoi_dung_id']
    form_extra_fields = {
        'nguoi_dung_id': QuerySelectField(
            'Người Dùng',
            query_factory=lambda: NguoiDung.query.all(),
            get_label='ten',
            allow_blank=False
        )
    }

    def on_model_change(self, form, model, is_created):
        # Lấy id của người dùng được chọn từ QuerySelectField
        model.nguoi_dung_id = form.nguoi_dung_id.data.id  # Chọn id của đối tượng NguoiDung

class QuanLyView(AuthenticatedQuanLy):
    column_list = ['id', 'nguoi_dung']
    form_columns = ['nguoi_dung_id']
    form_extra_fields = {
        'nguoi_dung_id': QuerySelectField(
            'Người Dùng',
            query_factory=lambda: NguoiDung.query.all(),
            get_label='ten',
            allow_blank=False
        )
    }


class QuanLyKhoView(AuthenticatedQuanLy):
    column_list = ['id', 'nguoi_dung']
    form_columns = ['nguoi_dung_id']
    form_extra_fields = {
        'nguoi_dung_id': QuerySelectField(
            'Người Dùng',
            query_factory=lambda: NguoiDung.query.all(),
            get_label='ten',
            allow_blank=False
        )
    }


class QuanTriView(AuthenticatedQuanLy):
    column_list = ['id', 'nguoi_dung']
    form_columns = ['nguoi_dung_id']
    form_extra_fields = {
        'nguoi_dung_id': QuerySelectField(
            'Người Dùng',
            query_factory=lambda: NguoiDung.query.all(),
            get_label='ten',
            allow_blank=False
        )
    }


# class KhachHangView(AuthenticatedQuanLy):
#     pass


class NguoiDungView(AuthenticatedQuanLy):
    pass


class LogoutView(BaseView):
    @expose("/")
    def index(self):
        logout_user()
        return redirect('/admin')


admin.add_view(SachView(Sach, db.session))
admin.add_view(TheLoaiView(TheLoai, db.session))
admin.add_view(PhieuNhapView(PhieuNhap, db.session))
admin.add_view(ChiTietPhieuNhapView(ChiTietPhieuNhap, db.session))
admin.add_view(NhanVienView(NhanVien, db.session))
admin.add_view(QuanLyView(QuanLy, db.session))
admin.add_view(QuanTriView(QuanTriVien, db.session))
admin.add_view(QuanLyKhoView(QuanLyKho, db.session))
admin.add_view(KhachHangView(KhachHang, db.session))
admin.add_view(NguoiDungView(NguoiDung, db.session))
admin.add_view(QuyDinhNhapSachView(QuyDinhNhapSach, db.session))

admin.add_view(BanSachView(name='Bán sách'))
admin.add_view(ThongKeTheoDoanhThuView(name='Thống kê theo doanh thu'))
admin.add_view(ThongKeTheoTanSuatView(name='Thống kê theo tần suất'))
admin.add_view(LogoutView(name='Logout'))
