import pandas as pd
import os
from utils import *
import pdb
from tqdm import tqdm
import os
import wandb

tqdm.pandas()
openai.api_key = os.getenv('OPENAI_API_KEY')
narrative_df = pd.read_csv(
    'narrative_detection/narrative_posts_by_trained_classification.csv', index_col=0).reset_index(drop=True)
narrative_df = narrative_df.head(1000)

# pdb.set_trace()
run = wandb.init(project="cs685-narrative-extraction", entity='acampbell1798')

results_file = "clinical-extractions/results/prompt_fewshot.csv"
if os.path.exists(results_file):
    completed_df = pd.read_csv(results_file, index_col=0)
    start_row = len(completed_df)
    print(f'Starting at row {start_row}')
else:
    completed_df = pd.DataFrame()
    start_row = 0

chunk_size = 5

total_rows = len(narrative_df)

for i in range(start_row, total_rows, chunk_size):
    chunk_df = narrative_df.iloc[i:i+chunk_size]
    chunk_df = chunk_df.progress_apply(
        apply_chatgpt, axis=1, prompt=get_new_instruction_prompt(), include_examples=True)
    completed_df = pd.concat([completed_df, chunk_df], ignore_index=True)
    completed_df.to_csv(results_file)
    print(f"Completed rows: {len(completed_df)}")

    most_recent = completed_df.tail()
    columns = ['selftext', 'effect_type_0', 'effect_type_1',  'effect_type_2', 'factors_0', 'factors_1', 'factors_2', 'effect_details_0',
               'effect_details_1', 'effect_details_2']
    most_recent = most_recent[columns]
    table = wandb.Table(dataframe=most_recent)
    run.log({'most_recent': table})

print('FINISHED')
wandb.finish()
