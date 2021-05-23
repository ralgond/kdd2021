# kdd2021

## prepare
mkdir -p ml/tsad/

cd ml/tsad/

git clone git@github.com:ralgond/kdd2021.git

cd kdd2021

pip install -r requirements.txt

mkdir samples_tmp

```
copy kdd samples to directory samples_tmp.
```
ls -l samples_tmp
```
-rwxrwxrwx 1 thuang thuang  1436310 Oct  8  2020 001_UCR_Anomaly_35000.txt
-rwxrwxrwx 1 thuang thuang  1440018 Oct  8  2020 002_UCR_Anomaly_35000.txt
-rwxrwxrwx 1 thuang thuang  1440000 Oct  8  2020 003_UCR_Anomaly_35000.txt
-rwxrwxrwx 1 thuang thuang   198000 Oct  8  2020 004_UCR_Anomaly_2500.txt
-rwxrwxrwx 1 thuang thuang   147312 Oct  8  2020 005_UCR_Anomaly_4000.txt
-rwxrwxrwx 1 thuang thuang   147312 Oct  8  2020 006_UCR_Anomaly_4000.txt
-rwxrwxrwx 1 thuang thuang   147312 Oct  8  2020 007_UCR_Anomaly_4000.txt
-rwxrwxrwx 1 thuang thuang   147312 Oct  8  2020 008_UCR_Anomaly_4000.txt
-rwxrwxrwx 1 thuang thuang   147312 Oct  8  2020 009_UCR_Anomaly_4000.txt
```

mkdir samples

python gen_right_format_samples.py

rm -rf samples_tmp

## prepare luminol result
mkdir lu_dd_output

mkdir lu_dd_output/0.2

python gen_lu_dd_02.py

## prepare train-only and test-only data
mkdir only_train_input

mkdir only_test_input

python gen_train_input.py

python gen_test_input.py


## prepare hotsax result
git clone git@github.com:ralgond/grammarviz2_src.git

cd grammarviz2_src

mvn package -Psingle

cd ..

mkdir gv_hotsax_output

cd gv_hotsax_output/

mkdir 100 125 150 175 200 225 25 250 300 350 400 450 50 500 550 600 650 700 75 750 800

cd ..

python gen_gv_hotsax.py 25

python gen_gv_hotsax.py 50

python gen_gv_hotsax.py 75

python gen_gv_hotsax.py 100

python gen_gv_hotsax.py 125

python gen_gv_hotsax.py 150

python gen_gv_hotsax.py 175

python gen_gv_hotsax.py 200

python gen_gv_hotsax.py 225

python gen_gv_hotsax.py 250

python gen_gv_hotsax.py 300

python gen_gv_hotsax.py 350

python gen_gv_hotsax.py 400

python gen_gv_hotsax.py 450

python gen_gv_hotsax.py 500

python gen_gv_hotsax.py 550

python gen_gv_hotsax.py 600

python gen_gv_hotsax.py 650


## run
mkdir output

python main.py 1