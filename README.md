# kdd2021

## Final Score and The Rank of Me

My rank is 14 and the score is 75.2, the certificate is [here](https://compete.hexagon-ml.com/certificate/giJUy/), and the code is [here](https://github.com/ralgond/kdd2021/releases/tag/v75.2).

I am still trying to boost my score, and now I have boosted my score to 81.6, the code is [here](https://github.com/ralgond/kdd2021/releases/tag/v81.6).

## Requirements

Run on Windows 10 with CUDA

## Prepare
```
install Visual Studio 2019 with Visual C++

install python 3.7.0

install pip
```

md ml\tsad\kdd2021

cd ml\tsad\kdd2021

```
unzip code into directory kdd2021
```

pip install -r requirements.txt

md samples_tmp

```
copy kdd samples to directory samples_tmp.
```

md samples

python gen_right_format_samples.py

del samples_tmp

## Prepare P2P result
python gen_p2p.py 1

## Prepare STD result
python gen_diff_std.py 1

python gen_acc_std.py 1

## Prepare MP result
python gen_mp.py 1

python gen_diff_mp_selfjoin.py 1

python gen_diff_mp_abjoin.py 1

python gen_acc_mp_selfjoin.py 1

python gen_acc_mp_abjoin.py 1

## Run
mkdir -p output

python main3.py 1

```
The result file is output/main3.csv
```
