"""BIM storeys (tools/bim_to_25d.py output) as 2.5D training-env worlds.

    ARIADNE_BIM_DIR=maps_bim python driver3d.py --world bim      # or eval3d.py ... --world bim

Episode index -> one of the .npz worlds in ARIADNE_BIM_DIR (sorted, cycled) and a seeded random start
>= 1.2 m from obstacles. Heights and ceiling come from the BIM, as in warehouse_env.py for the Isaac warehouse.
"""

import functools
import glob
import os

import numpy as np
from scipy.ndimage import distance_transform_edt

from env3d import Env3D
from procwarehouse import ProcScene

BIM_DIR = os.environ.get("ARIADNE_BIM_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "maps_bim"))


@functools.lru_cache(maxsize=None)
def bim_worlds(bim_dir=BIM_DIR):
    files = sorted(glob.glob(os.path.join(bim_dir, "*.npz")))
    if not files:
        raise FileNotFoundError(f"no BIM worlds (*.npz) in {bim_dir}; run tools/bim_to_25d.py first")
    return files


@functools.lru_cache(maxsize=64)
def load_world(path):
    d = np.load(path)
    return d["gt"].astype(int), d["height"].astype(np.float32), float(d["H"])


class BimEnv3D(Env3D):
    def import_ground_truth(self, episode_index):
        files = bim_worlds()
        self.world_file = files[episode_index % len(files)]
        gt, _, _ = load_world(self.world_file)
        dist = distance_transform_edt(gt == 255)
        cand = np.argwhere(dist >= 3)  # >= 1.2 m from obstacles
        if not len(cand):
            cand = np.argwhere(dist >= 2)
        y, x = cand[np.random.default_rng(2000 + episode_index).integers(len(cand))]
        return gt.copy(), np.array([x, y])

    def make_scene(self, rng):
        _, height, H = load_world(self.world_file)
        return ProcScene(self.ground_truth, height, H)
