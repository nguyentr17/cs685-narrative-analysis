# [CS685] Examining Medical Narratives of Eating Disorder Recovery on Reddit

## Code Structure
- `/topic_modeling/` contains the code for the topic modeling experiments. 
    - `/data/input/custom_stopwords.txt` contains custom stopwords. 
    - `/data/analysis/topic_label_*.txt` contains the topic labels for `k=*` and top 10 keywords for each topic. 
    - `/data/positive_topic_dist.csv` contains the topic distribution for positive posts.

    - `/script/lmw_result.ipynb` contains code for preprocessing, training and analyzing the topic modeling results.
    - `/script/lmw.py` contains helper code for training the LDA model.
