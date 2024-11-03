def cart_info(gio_hang=None):
    tong_tien, tong_so_luong = 0, 0

    if gio_hang:
        for g in gio_hang.values():
            tong_so_luong += g['so_luong']
            tong_tien += g['so_luong'] * g['gia']

    return {
        'tong_tien': tong_tien,
        'tong_so_luong': tong_so_luong
    }