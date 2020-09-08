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

Intro: continuous SL, sign gloss

Link: [Homepage](https://www-i6.informatik.rwth-aachen.de/~koller/RWTH-PHOENIX/), [Paper (CVIU'2015)](https://www-i6.informatik.rwth-aachen.de/publications/download/996/Koller-CVIU-2015.pdf)

### phoenix-2014-multisigner

Prepare LMDB Database:

* fullFrame-210x260px

``` bash
python scripts/lmdb_ph14_full_rgb.py /.../fullFrame-210x260px /lmdb/ph14/full_rgb_224 -nw 4
```

* trackedRightHand-92x132px

``` bash
python scripts/lmdb_ph14_hand_rgb.py /.../trackedRightHand-92x132px /lmdb/ph14/hand_rgb_112 -nw 4
```

## RWTH-PHOENIX-Weather 2014 T (German SL)

Intro: continuous SL, sign gloss, German translation

Link: [Homepage](https://www-i6.informatik.rwth-aachen.de/~koller/RWTH-PHOENIX-2014-T/), [Paper (CVPR'2018)](http://openaccess.thecvf.com/content_cvpr_2018/papers/Camgoz_Neural_Sign_Language_CVPR_2018_paper.pdf)

Prepare LMDB Database:

* fullFrame-210x260px

``` bash
python scripts/lmdb_ph14-t_full_rgb.py /.../fullFrame-210x260px /lmdb/ph14T/full_rgb_224 -nw 4
```
