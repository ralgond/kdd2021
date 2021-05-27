# kdd2021

## Requirements

Run on Windows 10 with CUDA and WSL(Windows Subsystem for Linux)

## Prepare
```
install Visual Studio 2019 with Visual C++

install jdk 1.8

install maven 3.6.0

install python 3.7.0

install pip
```

mkdir -p ml/tsad/

cd ml/tsad/

unzip general_final.zip -d kdd2021

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

## Prepare train-only and test-only data
mkdir only_train_input

mkdir only_test_input

python gen_train_input.py

python gen_test_input.py

## Prepare luminol result
mkdir lu_dd_output

mkdir lu_dd_output/0.2

python gen_lu_dd_02.py

## Prepare hotsax result
git clone git@github.com:ralgond/grammarviz2_src.git

cd grammarviz2_src

mvn package -Psingle

cd ..

mkdir gv_hotsax_output

cd gv_hotsax_output/

mkdir 100 125 150 175 200 225 25 250 300 350 400 450 50 500 550 600 650 75 700 750 800

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

python gen_gv_hotsax.py 700

## Prepare RRA result
mkdir gv_rra_output

cd gv_rra_output

mkdir 100 125 150 200 25 300 350 400 450 50 500 550 600 75

cd ..

python gen_gv_rra.py 25

python gen_gv_rra.py 50

python gen_gv_rra.py 75

python gen_gv_rra.py 100

python gen_gv_rra.py 125

python gen_gv_rra.py 150

python gen_gv_rra.py 175

python gen_gv_rra.py 200

python gen_gv_rra.py 225

python gen_gv_rra.py 250

python gen_gv_rra.py 300

python gen_gv_rra.py 350

python gen_gv_rra.py 400

python gen_gv_rra.py 450

python gen_gv_rra.py 500

python gen_gv_rra.py 550

python gen_gv_rra.py 600

## Run
mkdir output

python main.py 1

```
output/main.csv is the result
```