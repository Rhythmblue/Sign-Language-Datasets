# Sign Language Datasets

Here, we introduce several publicly available sign language datasets. They are suitable for multiple sign language (SL) processing tasks, including SL recognition, translation and generation.

We also provide the creation method of LMDB, which is space-saving and loading-friendly. All frames are converted to JPG format and saved as binary file in LMDB database.

## Usage

```bash
usage: lmdb_dataset_modality.py [-h] [-nw NUM_WORKERS] [-tt TARGET_TMP_PATH] source_path target_path
```

- `source_path`: the path where original data stored
- `target_path`: the path where lmdb will be stored
- `target_tmp_path`: the path where transformed images stored. If `-tt ...` not set, temporary `.jpg` file will be deleted after stored in LMDB.

## RWTH-PHOENIX-Weather 2014 (German SL)

Keywords: continuous SL, sign gloss

Links: [Homepage](https://www-i6.informatik.rwth-aachen.de/~koller/RWTH-PHOENIX/), [Paper (CVIU'2015)](https://www-i6.informatik.rwth-aachen.de/publications/download/996/Koller-CVIU-2015.pdf)

### phoenix-2014-multisigner

#### LMDB Database

  fullFrame-210x260px

``` bash
python scripts/lmdb_ph14_full_rgb.py .../fullFrame-210x260px lmdb/ph14/full_rgb_224 -nw 4
```

trackedRightHand-92x132px

``` bash
python scripts/lmdb_ph14_hand_rgb.py .../trackedRightHand-92x132px lmdb/ph14/hand_rgb_112 -nw 4
```

## RWTH-PHOENIX-Weather 2014 T (German SL)

Keywords: continuous SL, sign gloss, German translation

Links: [Homepage](https://www-i6.informatik.rwth-aachen.de/~koller/RWTH-PHOENIX-2014-T/), [Paper (CVPR'2018)](http://openaccess.thecvf.com/content_cvpr_2018/papers/Camgoz_Neural_Sign_Language_CVPR_2018_paper.pdf)

### LMDB Database

fullFrame-210x260px

``` bash
python scripts/lmdb_ph14-t_full_rgb.py .../fullFrame-210x260px lmdb/ph14T/full_rgb_224 -nw 4
```

## Pose Annotation

In [STMC](https://arxiv.org/abs/2002.03187) (AAAI'20), authors use [HRNet](https://github.com/stefanopini/simple-HRNet) (CVPR'19) to conduct automatic pose annotation.
The estimated upper-body keypoint array `(T, 7, 2)` are saved in a `Dict` indexed with video name.
Each keypoint is recorded as `(w, h)` and normalized between `[0, 1]`.

#### Download Links

|Dataset | HRNet|
|--|--|
|PHOENIX-2014 |[GoogleDrive](https://drive.google.com/file/d/1_c0L8IW0PYZ1MWsKZ8sOsXDJ4lv40z5Z/view?usp=sharing) |
|PHOENIX-2014-T |[GoogleDrive](https://drive.google.com/file/d/1k1EVdtW989etPKKEiR5Bua7ksCC5Xe-L/view?usp=sharing) |

#### How to read

``` python
import pickle as pkl
with open('pose_phoenix2014_up_hrnet_TxN_wh.pkl', 'rb') as f:
    dict_pose = pkl.load(f)
print(dict_pose['01April_2010_Thursday_heute_default-0'].shape)
```
