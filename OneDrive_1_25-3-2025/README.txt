1. There are two dataset files in the folder.
2. Each row is as follows: 
   <Node ID - Person u> <Node ID - Person v> <Probability of spread from u to v>
3. Hyperparameters to use:

Dataset 1:
No. Of Randomized Instances: 500
k = 50

Dataset 2: 
No. Of Randomized Instances: 100
k = 50

4. Compile "infection.cc" with "g++ infection.cc -o infection".

5. Run "./infection <dataset_file_path> <seed_file_path>" to compute spread based on your seed set on the given dataset.


