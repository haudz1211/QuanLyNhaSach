import math

from flask import render_template, request, redirect, session, jsonify
from thebooks import app, dao, login_manager, utils
from flask_login import login_user, logout_user
from thebooks.admin import *


@app.route('/')
def index():
    kw = request.args.get('kw')
    the_loai_id = request.args.get('the_loai_id')
    trang = request.args.get('trang')

    du_lieu = dao.lay_sach(kw, the_loai_id, trang)
    sach = du_lieu['sach']

    so_trang = math.ceil(du_lieu['so_sach'] / app.config['PAGE_SIZE'])

    return render_template('index.html', sach=sach, so_trang=so_trang)


@app.route('/thebooks/static')
def static_books():
    kw = request.args.get('kw')
    the_loai_id = request.args.get('the_loai_id')
    trang = request.args.get('trang')

    du_lieu = dao.lay_sach(kw, the_loai_id, trang)
    sach = du_lieu['sach']

    so_trang = math.ceil(du_lieu['so_sach'] / app.config['PAGE_SIZE'])

    return render_template('index.html', sach=sach, so_trang=so_trang)



@app.context_processor
def common_respones():
    return {
        'the_loai': dao.lay_the_loai(),
        'thong_tin_gio_hang': utils.cart_info(session.get('gio_hang'))
    }


@app.route('/register', methods=['get', 'post'])
def register():
    error_message = None
    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        if password.__eq__(confirm):
            try:
                dao.them_khach_hang(ten=request.form.get('hoTen'),
                                    username=request.form.get('username'),
                                    password=password,
                                    sdt=request.form.get('sdt'),
                                    email=request.form.get('email'),
                                    dia_chi=request.form.get('diaChi'),
                                    avatar=request.files.get('avatar'))
            except Exception as ex:
                error_message = str(ex)
            else:
                return redirect('/login')
        else:
            error_message = 'Mật khẩu không khớp'

    return render_template('register.html', error_message=error_message)


@app.route('/admin/dang_nhap', methods=['post'])
def login_admin():
    username = request.form.get('username')
    password = request.form.get('password')

    user = dao.chung_thuc_nguoi_dung(username=username, password=password)
    if user:
        login_user(user)

    return redirect('/admin')


@app.route('/login', methods=['get', 'post'])
def login():
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        nguoi_dung = dao.chung_thuc_nguoi_dung(username=username, password=password)
        if nguoi_dung:
            login_user(nguoi_dung)

            next = request.args.get('next')
            if next:
                return redirect(next)

            return redirect('/')

    return render_template('login.html')


@login_manager.user_loader
def load_user(id):
    return dao.lay_nguoi_dung_theo_id(id)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/gio_hang')
def cart():
    return render_template('cart.html')


@app.route('/api/gio_hang', methods=['post'])
def add_to_cart():
    data = request.json

    gio_hang = session.get('gio_hang')
    if gio_hang is None:
        gio_hang = {}

    id = str(data.get('id'))
    if id in gio_hang:
        gio_hang[id]['so_luong'] += 1
    else:
        sach = dao.lay_sach_theo_id(id)
        gio_hang[id] = {
            'id': id,
            'ten': sach.ten,
            'gia': sach.gia,
            'so_luong': 1,
            'the_loai': sach.the_loai.ten,
            'tac_gia': sach.tac_gia,
            'hinh_anh': sach.hinh_anh
        }

    session['gio_hang'] = gio_hang

    return jsonify(utils.cart_info(gio_hang))


@app.route('/api/gio_hang/<sach_id>', methods=['put'])
def update_cart(sach_id):
    gio_hang = session.get('gio_hang')

    if gio_hang and sach_id in gio_hang:
        so_luong = request.json.get('so_luong')
        gio_hang[sach_id]['so_luong'] = int(so_luong)

    session['gio_hang'] = gio_hang
    return jsonify(utils.cart_info(gio_hang))


@app.route('/api/gio_hang/<sach_id>', methods=['delete'])
def delete_cart(sach_id):
    gio_hang = session.get('gio_hang')

    if gio_hang and sach_id in gio_hang:
        del gio_hang[sach_id]

    session['gio_hang'] = gio_hang
    return jsonify(utils.cart_info(gio_hang))


@app.route('/api/dat_hang', methods=['post'])
def pay():
    gio_hang = session.get('gio_hang')
    if dao.them_don_hang(gio_hang=gio_hang, khach_hang_id=current_user.id):
        del session['gio_hang']
        return jsonify({'status': 200})

    return jsonify({'status': 500, 'error_message': 'Something wrong!'})


@app.route('/api/don_hang/<sach_id>', methods=['get'])
def add_order(sach_id):
    don_hang = session.get('don_hang')
    if don_hang is None:
        don_hang = {}

    if sach_id in don_hang:
        don_hang[sach_id]['so_luong'] += 1
    else:
        sach = dao.lay_sach_theo_id(sach_id)
        don_hang[sach_id] = {
            'id': sach.id,
            'ten': sach.ten,
            'the_loai': sach.the_loai.ten,
            'gia': sach.gia,
            'so_luong': 1
        }

    session['don_hang'] = don_hang

    data = {
        'sach': don_hang[sach_id],
        'thong_tin': utils.cart_info(don_hang)
    }

    return jsonify(data)


@app.route('/api/don_hang/<sach_id>', methods=['put'])
def update_order(sach_id):
    don_hang = session.get('don_hang')
    if don_hang and sach_id in don_hang:
        so_luong = request.json.get('so_luong')
        don_hang[sach_id]['so_luong'] = int(so_luong)

    session['don_hang'] = don_hang
    return jsonify(utils.cart_info(don_hang))


@app.route('/api/don_hang/<sach_id>', methods=['delete'])
def delete_order(sach_id):
    don_hang = session.get('don_hang')
    if don_hang and sach_id in don_hang:
        del don_hang[sach_id]

    session['don_hang'] = don_hang
    return jsonify(utils.cart_info(don_hang))


@app.route('/api/khach_hang/<sdt>', methods=['get'])
def get_customer(sdt):
    khach_hang = dao.lay_khach_hang_theo_sdt(sdt)
    data = {}
    if khach_hang:
        data = {
            'id': khach_hang.id,
            'ten': khach_hang.ten,
            'sdt': khach_hang.sdt,
            'dia_chi': khach_hang.dia_chi
        }

    return jsonify(data)


@app.route('/api/don_hang/dat_hang', methods=['post'])
def pay_order():
    don_hang = session.get('don_hang')
    khach_hang_id = request.json.get('khach_hang_id')
    if dao.them_don_hang(gio_hang=don_hang, khach_hang_id=khach_hang_id, nhan_vien_id=current_user.id):
        del session['don_hang']
        return jsonify({'status': 200})

    return jsonify({'status': 500, 'error_message': 'Something wrong!'})


@app.route('/ho_so')
def load_profile():
    return render_template('profile.html')


@app.route('/sach/<id>')
def details(id):
    return render_template('details.html',
                           sach=dao.lay_sach_theo_id(id),
                           binh_luan=dao.lay_binh_luan(id))


@app.route('/api/sach/<id>/binh_luan', methods=['post'])
def add_comment(id):
    try:
        b = dao.them_binh_luan(sach_id=id, binh_luan=request.json.get('binh_luan'))
    except Exception as ex:
        return jsonify({'status': 500, 'err_msg': str(ex)})
    else:
        return jsonify({'status': 200, 'comment': {
            'binh_luan': b.binh_luan,
            'ngay_tao': b.ngay_tao,
            'khach_hang': {
                'avatar': b.khach_hang.avatar
            }
        }})


if __name__ == '__main__':
    app.run(debug=True)