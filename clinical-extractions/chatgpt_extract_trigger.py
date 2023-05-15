import json

import openai.error
import pandas as pd
from utils import *
from tqdm import tqdm
import os
import argparse
import time

# Set up logging
current_file = os.path.basename(__file__).split(".")[0]
LOGGER = set_logging(logging.getLogger(current_file), log_file=f"./logs/{current_file}.log")

# Set up arguments
parser = argparse.ArgumentParser()

parser.add_argument(
    '--experiment', action="store_true",
    help="Whether to run experiment",
    default=False
)
parser.add_argument(
    '--openai_key', type=str, required=True
)
parser.add_argument(
    '--max_num_posts', type=int, required=False
)
parser.add_argument(
    '--result_file', type=str, required=True
)
parser.add_argument(
    '--include_example', action="store_true", default=False
)

TRIGGER_RESPONSE_KEYS = set(["perspective", "age", "duration", "gender", "has_trigger", "trigger", "trigger_type"])


def apply_chatgpt_extract_trigger(row, prompt, include_examples, n = 6):
    narrative = row['selftext']
    num_tokens_narrative = num_tokens_from_string(narrative, "cl100k_base")
    LOGGER.info(f"Narrative: {narrative}")
    LOGGER.info(f"Token: {num_tokens_narrative}")

    if include_examples:
        narrative_plus_instruct = num_tokens_narrative + num_tokens_instructions
        if (narrative_plus_instruct + num_tokens_few_shot) < 4080:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                n = n,
                messages=[
                    {"role": "user", "content":prompt},
                    {"role": "user", "content":get_few_shot_examples()},
                    {"role": "user", "content": "Narrative: " + narrative}])
        elif (narrative_plus_instruct + num_tokens_few_shot_small) < 4080:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                n = n,
                messages=[
                    {"role": "user", "content":prompt},
                    {"role": "user", "content":get_small_few_shot_examples()},
                    {"role": "user", "content": "Narrative: " + narrative}])
        elif narrative_plus_instruct < 4080:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                n = n,
                messages=[
                    {"role": "user", "content":prompt},
                    {"role": "user", "content": narrative},])
        else:
            result = {}
    else:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                n=n,
                messages=[
                    {"role": "user", "content": prompt},
                    {"role": "user", "content": narrative},])
        except openai.error.RateLimitError as e:
            time.sleep(30)
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                n=n,
                messages=[
                    {"role": "user", "content": prompt},
                    {"role": "user", "content": narrative},])
    count = 0
    # pdb.set_trace()
    for i in range(n):
        result = response.choices[i].message.content
        LOGGER.info(f"Result: {result}")
        try:
            result = eval(result)
            if set(result.keys()) == TRIGGER_RESPONSE_KEYS:
                for key in TRIGGER_RESPONSE_KEYS:
                    row[f"{key}_{count}"] = result[key]
            # print(result)
            count += 1
        except Exception as e:
            LOGGER.info(F"Error: {e}")
        if count == 3:
            time.sleep(20)
            return row

    while (count < 3):
        for key in TRIGGER_RESPONSE_KEYS:
            row[f"{key}_{count}"] = None
        count += 1
    time.sleep(20)
    return row


if __name__ == "__main__":
    tqdm.pandas()
    args = parser.parse_args()
    openai.api_key = args.openai_key
    #narrative_df = pd.read_csv('../narrative_detection/annotated_narrative_posts_by_trained_classification.csv')
    narrative_df = pd.read_csv("../narrative_detection/narrative_post_with_topic_model_20.csv")
    if args.experiment:
        narrative_df = narrative_df[narrative_df["selected_for_experiment"] == 1]
    if args.max_num_posts is not None:
        narrative_df = narrative_df.head(args.max_num_posts)



    prompt_tracking_file = "./results/prompt_tracking_file.ndjson"
    current_prompt = get_trigger_instruction_prompt()
    # examples = get_trigger_examples(3, force_include_no_trigger=False, force_include_multiple_triggers=False)
    # current_prompt = "\n".join([current_prompt, "Here are some examples:", examples])
    # LOGGER.info(f"Prompt: {current_prompt}")
    # results_file = "./results/experiment_trigger_extraction_result_3_examples.csv"

    # examples = get_trigger_examples(3, force_include_no_trigger=False, force_include_multiple_triggers=True)
    # current_prompt = "\n".join([current_prompt, "Here are some examples:", examples])
    # LOGGER.info(f"Prompt: {current_prompt}")
    # results_file = "./results/experiment_trigger_extraction_result_3_examples_include_multiple_trigger.csv"

    examples = get_trigger_examples(1, force_include_no_trigger=False, force_include_multiple_triggers=True)
    current_prompt = "\n".join([current_prompt, "Here are some examples:", examples])
    LOGGER.info(f"Prompt: {current_prompt}")
    results_file = "./results/experiment_trigger_extraction_result_1_example_include_multiple_trigger.csv"

    time_now = time.time()

    if os.path.exists(results_file):
        completed_df = pd.read_csv(results_file)
        completed_ids = list(completed_df["id"].unique())
    else:
        completed_df = pd.DataFrame()
        completed_ids = []

    chunk_size = 5
    incomplete_df = narrative_df[~narrative_df["id"].isin(completed_ids)].reset_index()
    total_rows = len(incomplete_df)

    LOGGER.info(f"Number of narratives to process: {len(incomplete_df)} / {len(narrative_df)}")

    for i in range(0, total_rows, chunk_size):
        chunk_df = incomplete_df.iloc[i:i+chunk_size]
        chunk_df = chunk_df.progress_apply(apply_chatgpt_extract_trigger, axis=1, prompt=current_prompt, include_examples=args.include_example)
        completed_df = pd.concat([completed_df, chunk_df], ignore_index=True)
        completed_df.to_csv(results_file, index=False)
        print(f"Completed rows: {len(completed_df)}")


