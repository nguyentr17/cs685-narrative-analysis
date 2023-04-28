import pandas as pd
import os
from utils import *
import pdb
from tqdm import tqdm
import os
import wandb

# tqdm.pandas()
openai.api_key = os.getenv('OPENAI_API_KEY')
narrative_df = pd.read_csv(
    'narrative_detection/narrative_posts_by_trained_classification.csv', index_col=0).reset_index(drop=True)
# narrative_df = narrative_df.head(1000)

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

chunk_size = 1

total_rows = len(narrative_df)

start_time = time.time()
current_time = start_time
current_token_count = 0
for i in range(start_row, total_rows, chunk_size):
    elapsed_time = time.time() - start_time
    if elapsed_time >= 60:  # If a minute has passed
        start_time = time.time()  # Reset the start time
        current_token_count = 0
    chunk_df = narrative_df.iloc[i:i+chunk_size]
    if chunk_size == 1:
        narrative = chunk_df['selftext'].values[0]
        num_tokens_narrative = num_tokens_from_string(narrative, "cl100k_base")
        narrative_plus_instruct = num_tokens_narrative + num_tokens_instructions
        current_token_count += pick_token_combination(narrative_plus_instruct)
        if current_token_count >= 4000:
            elapsed_time = time.time() - start_time
            time.sleep(60 - elapsed_time)
            start_time = time.time()
            current_token_count = pick_token_combination(
                narrative_plus_instruct)
    # chunk_df = chunk_df.progress_apply(
    #     apply_chatgpt, axis=1, prompt=get_new_instruction_prompt(), include_examples=True)
    chunk_df = chunk_df.apply(
        apply_chatgpt, axis=1, prompt=get_new_instruction_prompt(), include_examples=True)
    completed_df = pd.concat([completed_df, chunk_df], ignore_index=True)
    completed_df.to_csv(results_file)

    most_recent = completed_df.tail()
    columns = ['selftext', 'effect_type_0', 'effect_type_1',  'effect_type_2', 'factors_0', 'factors_1', 'factors_2', 'effect_details_0',
               'effect_details_1', 'effect_details_2']
    most_recent = most_recent[columns]
    table = wandb.Table(dataframe=most_recent)
    run.log({'most_recent': table})
    print(f"Completed rows: {len(completed_df)}")


print('FINISHED')
wandb.finish()
