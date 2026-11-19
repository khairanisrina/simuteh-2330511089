"""bercak.py: analisis bercak SIMUTEH (dipakai ulang mulai P7)."""

import os
import json
import cv2
import numpy as np

from utils_tepi import mask_daun_awal, bercak_awal


PARAM_BERCAK = {
    "kanal": 2,
    "k": 4.0,
    "se_bentuk": "elips",
    "se_open": 5,
    "se_close": 5,
    "luas_min": 20,
    "bulat_min": 0.5,
    "rasio_maks": 1.8,
    "batas_ringan": 0.1,
    "batas_berat": 2.0,
    "mm_per_px": 0.4375
}


_BENTUK = {
    "elips": cv2.MORPH_ELLIPSE,
    "persegi": cv2.MORPH_RECT,
    "silang": cv2.MORPH_CROSS
}


def _se(p, uk):
    """Membuat structuring element berdasarkan parameter."""
    return cv2.getStructuringElement(
        _BENTUK[p["se_bentuk"]],
        (uk, uk)
    )


def bersihkan(biner, p):
    """
    Membersihkan citra biner menggunakan opening dan closing.
    Opening membuang titik derau dan komponen tipis.
    Closing menutup celah pada komponen.
    """

    hasil = biner.copy()

    # TODO 1: Opening
    if p["se_open"] > 0:

        se_open = _se(
            p,
            p["se_open"]
        )

        hasil = cv2.morphologyEx(
            hasil,
            cv2.MORPH_OPEN,
            se_open
        )

    # TODO 2: Closing
    if p["se_close"] > 0:

        se_close = _se(
            p,
            p["se_close"]
        )

        hasil = cv2.morphologyEx(
            hasil,
            cv2.MORPH_CLOSE,
            se_close
        )

    return hasil


def ukur_dan_saring(biner, p):
    """
    Melabeli komponen terhubung, mengukur bentuknya,
    lalu menyaring komponen berdasarkan parameter.
    """

    # TODO 3: Label komponen terhubung
    n, lbl, st, cen = cv2.connectedComponentsWithStats(
        (biner > 0).astype(np.uint8),
        connectivity=8
    )

    keluar = np.zeros_like(biner)
    daftar = []

    # Mengabaikan label 0 karena merupakan latar belakang
    for i in range(1, n):

        mask_komponen = (
            (lbl == i).astype(np.uint8)
        )

        kontur, _ = cv2.findContours(
            mask_komponen,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_NONE
        )

        if len(kontur) == 0:
            continue

        # TODO 4: Menghitung ukuran dan bentuk komponen

        luas = int(
            st[i, cv2.CC_STAT_AREA]
        )

        keliling = cv2.arcLength(
            kontur[0],
            True
        )

        kebulatan = (
            0.0
            if keliling == 0
            else 4 * np.pi * luas / keliling ** 2
        )

        w, h = cv2.minAreaRect(
            kontur[0]
        )[1]

        rasio = (
            max(w, h) /
            max(min(w, h), 1)
        )

        # TODO 5: Penyaringan komponen
        if (
            luas >= p["luas_min"]
            and kebulatan >= p["bulat_min"]
            and rasio <= p["rasio_maks"]
        ):

            keluar[lbl == i] = 255

            # Menyimpan informasi komponen yang lolos
            daftar.append({

                "label": int(i),

                "luas_px": luas,

                "luas_mm2": round(
                    luas * p["mm_per_px"] ** 2,
                    2
                ),

                "keliling_px": round(
                    float(keliling),
                    1
                ),

                "kebulatan": round(
                    float(kebulatan),
                    2
                ),

                "rasio_aspek": round(
                    float(rasio),
                    2
                ),

                "cx": int(cen[i][0]),

                "cy": int(cen[i][1])
            })

    return keluar, daftar


def analisis_daun(img_praproses, p=None):
    """
    Masukan:
        Citra BGR hasil praproses.

    Keluaran:
        Mask daun, mask bercak, jumlah bercak,
        persentase bercak, kelas mutu, dan ukuran bercak.
    """

    p = {
        **PARAM_BERCAK,
        **(p or {})
    }

    # Membuat mask daun
    m_daun = mask_daun_awal(
        img_praproses
    )

    # Membuat citra biner bercak awal
    biner = bercak_awal(
        img_praproses,
        m_daun,
        kanal=p["kanal"],
        k=p["k"]
    )

    # Membersihkan citra biner
    hasil_bersih = bersihkan(
        biner,
        p
    )

    # Mengukur dan menyaring setiap bercak
    m_bercak, daftar = ukur_dan_saring(
        hasil_bersih,
        p
    )

    # TODO 6: Menghitung persentase bercak
    luas_daun = int(
        (m_daun > 0).sum()
    )

    luas_bercak = int(
        (m_bercak > 0).sum()
    )

    persen = (
        0.0
        if luas_daun == 0
        else (luas_bercak / luas_daun) * 100
    )

    # TODO 7: Menentukan kelas mutu
    if persen >= p["batas_berat"]:

        kelas = "Bercak Berat"

    elif persen >= p["batas_ringan"]:

        kelas = "Bercak Ringan"

    else:

        kelas = "Sehat"

    return {
        "mask_daun": m_daun,
        "mask_bercak": m_bercak,
        "jumlah_bercak": len(daftar),
        "persen_bercak": round(float(persen), 3),
        "kelas": kelas,
        "bercak": daftar
    }


def simpan_param(p, path="../hasil/param_bercak.json"):

    os.makedirs(
        os.path.dirname(path) or ".",
        exist_ok=True
    )

    with open(path, "w") as f:

        json.dump(
            {
                **PARAM_BERCAK,
                **(p or {})
            },
            f,
            indent=2
        )
