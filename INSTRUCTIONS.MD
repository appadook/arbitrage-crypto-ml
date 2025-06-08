# Instructions to run the notebook
To run the 'ML Project crypto-arbitrage.ipynb' notebook, it should be done in 3 steps

### Step 1
Running the pre-processing of the data, cleaning, filtering and gettingt the data ready for further encoding, one-hot encoding, feature transformation and other data mining processes.

### Step 2
Running the `script.py` file using the following:
```
python script.py
```
This will do the necessary feature transformation to the dataset and create a strategy column for two different datasets
1. A dataset where the strategy is the best route with the inclusion of 'no profitable stragey' if the fees outweigh the profits
2. A dataset where the strategy is the best route with the exclusion of 'no profitable stragey' so we can just identify where the biggest echange arbitrage is found.


### Step 3
Loading the two new datasets back in to the notebook for further data mining and running the evaluation experiments.