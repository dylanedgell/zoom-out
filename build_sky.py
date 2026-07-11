"""Convert the ESO Milky Way equirectangular panorama into 6 cube faces for a
Cesium SkyBox.

Source: ESO / S. Brunier "The Milky Way panorama" (eso0932a), CC BY 4.0.
Downloaded by the pipeline into sky/_src/milkyway_pano.jpg.

Emits sky/px.jpg ... sky/nz.jpg (positive/negative X, Y, Z) at FACE px each,
using the standard OpenGL cube-map face conventions so the faces are seamless.

Usage: python3 build_sky.py
"""
import os
import urllib.request
import numpy as np
from PIL import Image

HERE = os.path.dirname(__file__)
SRC = os.path.join(HERE, "sky", "_src", "milkyway_pano.jpg")
OUT = os.path.join(HERE, "sky")
# ESO / S. Brunier "The Milky Way panorama" (eso0932a), CC BY 4.0.
PANO_URL = "https://cdn.eso.org/images/large/eso0932a.jpg"
FACE = 1024  # px per cube face


def ensure_source() -> None:
    if os.path.exists(SRC):
        return
    os.makedirs(os.path.dirname(SRC), exist_ok=True)
    print(f"Downloading {PANO_URL} ...")
    urllib.request.urlretrieve(PANO_URL, SRC)

# For each face, the 3D direction as a function of face coords a,b in [-1,1]
# (a = horizontal left→right, b = vertical top→bottom). Standard GL cube map.
FACES = {
    "px": lambda a, b: (np.ones_like(a),      -b,               -a),
    "nx": lambda a, b: (-np.ones_like(a),     -b,                a),
    "py": lambda a, b: (a,                     np.ones_like(a),  b),
    "ny": lambda a, b: (a,                    -np.ones_like(a), -b),
    "pz": lambda a, b: (a,                    -b,                np.ones_like(a)),
    "nz": lambda a, b: (-a,                   -b,               -np.ones_like(a)),
}


def main() -> None:
    ensure_source()
    src = np.asarray(Image.open(SRC).convert("RGB"))
    H, W = src.shape[:2]

    lin = (np.arange(FACE) + 0.5) / FACE * 2 - 1  # [-1, 1]
    a, b = np.meshgrid(lin, lin)                   # a across cols, b across rows

    for name, fn in FACES.items():
        dx, dy, dz = fn(a, b)
        norm = np.sqrt(dx * dx + dy * dy + dz * dz)
        dx, dy, dz = dx / norm, dy / norm, dz / norm

        lon = np.arctan2(dx, dz)        # -pi..pi
        lat = np.arcsin(np.clip(dy, -1, 1))  # -pi/2..pi/2

        sx = ((lon / (2 * np.pi)) + 0.5) * W
        sy = (0.5 - lat / np.pi) * H
        sx = np.clip(sx.astype(np.int64), 0, W - 1)
        sy = np.clip(sy.astype(np.int64), 0, H - 1)

        face = src[sy, sx]
        Image.fromarray(face, "RGB").save(os.path.join(OUT, name + ".jpg"), quality=88)
        print(f"wrote sky/{name}.jpg  {FACE}x{FACE}")


if __name__ == "__main__":
    main()
