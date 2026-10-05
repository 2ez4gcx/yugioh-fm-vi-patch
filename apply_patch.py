#!/usr/bin/env python3
"""Ap ban va PPF3 len dia goc, co kiem sha256 truoc va sau.

Chay:  python apply_patch.py <dia_goc.bin> <ban_va.ppf> [dia_ra.bin]
Bo trong dia_ra.bin thi file ra dat canh dia goc, ten mac dinh:
         Yu-Gi-Oh! Forbidden Memories (VN).bin        (chi dich)
         Yu-Gi-Oh! Forbidden Memories (VN)(Mod5).bin  (dich + 5 la)
Ban va:  yugioh-fm-vi.ppf       - chi dich
         yugioh-fm-vi-5-la.ppf  - dich + thang mot tran duoc 5 la bai
Khong can cai them gi ngoai Python 3.  Khong sua dia goc.
"""
import hashlib
import os
import struct
import sys

# sha256 cua dia goc va cua dia da va - doc tu README de doi chieu
SHA_GOC = '6e22494a45bf50fa2d239cd3819a57163a5f9b91e0365babc3e101509b5c3a7c'
# ban va nhan biet qua dong mo ta trong dau file PPF (byte 6..55), nen doi ten file van dung
SHA_DICH = {
    b'Yu-Gi-Oh! FM (SLUS-01411) - ban dich tieng Viet':
        ('chi dich', '27557b2bcf5872e93d776a52a2531d9a2079f17ca11c9566f4a2a7526234dd0c',
         'Yu-Gi-Oh! Forbidden Memories (VN).bin'),
    b'Yu-Gi-Oh! FM (SLUS-01411) - Viet hoa + 5 la/tran':
        ('dich + 5 la moi tran', '48de3b1cd47eb1d590e794a8517f18b45584a47f7b4a9d053be3d10e78984727',
         'Yu-Gi-Oh! Forbidden Memories (VN)(Mod5).bin'),
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def viet_cue(dst):
    """Tao file .cue canh file .bin vua ra (dia 1 track, Mode2/2352)."""
    cue = os.path.splitext(dst)[0] + '.cue'
    dong = ['FILE "%s" BINARY' % os.path.basename(dst),
            '  TRACK 01 MODE2/2352',
            '    INDEX 01 00:00:00']
    with open(cue, 'wb') as f:
        f.write(('\r\n'.join(dong) + '\r\n').encode('utf-8'))
    return cue


def main(src, ppf, dst=None):
    data = bytearray(open(src, 'rb').read())
    if SHA_GOC and sha(data) != SHA_GOC:
        sys.exit('Dia goc khong dung (sha256 khong khop). Can dung ban .bin Mode2/2352 cua SLUS-01411.')
    p = open(ppf, 'rb').read()
    if p[:5] != b'PPF30' or p[5] != 2:
        sys.exit('Khong phai file PPF3.')
    ten, sha_dich, ten_ra = SHA_DICH.get(p[6:56].rstrip(b' '), ('khong ro', None, 'dia_da_va.bin'))
    print('ban va: %s' % ten)
    if not dst:
        dst = os.path.join(os.path.dirname(os.path.abspath(src)), ten_ra)
    if os.path.abspath(dst) == os.path.abspath(src):
        sys.exit('File ra trung file goc - chon ten khac.')
    # dau PPF3: 56 imagetype, 57 blockcheck, 58 undo, 59 dummy; ban ghi tu 60
    # (co them 1024 byte khoi kiem neu bat blockcheck) - dung chuan PPF-O-Matic
    undo = p[58]
    pos, n = 60 + (1024 if p[57] else 0), 0
    while pos < len(p):
        off = struct.unpack_from('<Q', p, pos)[0]
        ln = p[pos + 8]
        pos += 9
        data[off:off + ln] = p[pos:pos + ln]
        pos += ln + (ln if undo else 0)
        n += 1
    open(dst, 'wb').write(data)
    print('da tao %s' % viet_cue(dst))
    h = sha(data)
    print('da ap %d ban ghi -> %s' % (n, dst))
    print('sha256 dia ra: %s' % h)
    if sha_dich:
        print('KHOP ban phat hanh' if h == sha_dich else 'KHONG KHOP - dia goc co the khac ban chuan')


if __name__ == '__main__':
    if len(sys.argv) not in (3, 4):
        sys.exit(__doc__)
    main(*sys.argv[1:])
