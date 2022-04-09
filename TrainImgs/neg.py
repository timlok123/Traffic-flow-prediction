import os

def generate_negative_description_file():
    # open the output file for writing. will overwrite all existing data in there
    with open(r'C:\Stuff\HKU\Git\CarsML\Traffic-flow-prediction\TrainImgs\neg.txt', 'w') as f:
        # loop over all the filenames
        for filename in os.listdir(r'C:\Stuff\HKU\Git\CarsML\Traffic-flow-prediction\TrainImgs\neg'):
            f.write('neg/' + filename + '\n')

generate_negative_description_file()

#C:\Users\howai\Downloads\opencv\build\x64\vc15\bin\opencv_createsamples.exe -info C:\Stuff\HKU\Git\CarsML\Traffic-flow-prediction\TrainImgs\pos.txt -w 20 -h 20 -num 5000 -vec pos.vec
#C:\Users\howai\Downloads\opencv\build\x64\vc15\bin\opencv_traincascade.exe -data C:\Stuff\HKU\Git\CarsML\Traffic-flow-prediction\TrainImgs\cascade\  -vec C:\Stuff\HKU\Git\CarsML\Traffic-flow-prediction\TrainImgs\pos.vec -bg C:\Stuff\HKU\Git\CarsML\Traffic-flow-prediction\TrainImgs\neg.txt -numPos 200 -numNeg 100 -numStages 10 -w 20 -h 20