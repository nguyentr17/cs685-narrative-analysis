import pandas as pd
import os
from utils import *
import pdb
from tqdm import tqdm

tqdm.pandas()

openai.api_key = os.getenv('OPENAI_API_KEY')
narrative_df = pd.read_csv('narrative_detection/narrative_posts_by_trained_classification.csv')
test_df = narrative_df.head()
test_df = test_df.progress_apply(apply_chatgpt, axis=1, prompt=get_new_instruction_prompt(), include_examples=True)
pdb.set_trace()
unique_filename = get_unique_filename()
test_df.to_csv(unique_filename)


