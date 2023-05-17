# [CS685] Examining Medical Narratives of Eating Disorder Recovery on Reddit

## Code Structure (tasks are described by Section 5)

1. Narrative Detection
- `/narrative_detection/explore_data.ipynb` contains the code to train the classification task
2. Domain-Specific Sentiment Lexicons
- `/data-collection` contains both code to crawl the data nd code for sentiment polarity
  - `/embeddings/word2vec_word_embeddings.ipynb` and `./word_types.ipynb` are used to train the embeddings and compute scores respectively
3. Instruction Prompting for Trigger and Factor Extraction
- `/clinical-extractions/` contains the code for the extraction of trigger and factors
  - `./chatgpt.py` is the code to extract helpful and harmful factors
  - `./chatgpt_extract_trigger.py` is the code to extract triggers
  - `./utils.py` contains all the prompts used and experimented with
  - `./sample_selection_trigger_extraction.ipynb` uses topic modeling to generate samples for evaluation and few-shot prompting. It also contains code for evaluation.
  
4. Topic Modeling
- `/topic_modeling/` contains the code for the topic modeling experiments.
  - `/data/input/custom_stopwords.txt` contains custom stopwords.
  - `/data/analysis/topic_label_*.txt` contains the topic labels for `k=*` and top 10 keywords for each topic.
  - `/data/positive_topic_dist.csv` contains the topic distribution for positive posts.

  - `/script/lmw_result.ipynb` contains code for preprocessing, training and analyzing the topic modeling results.
  - `/script/lmw.py` contains helper code for training the LDA model.
5. Power and Agency Analysis



