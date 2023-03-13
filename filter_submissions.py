from db import engine, engine2, engine3, engine4, engine5
import pandas as pd
from sqlalchemy import text

def filter_out(num_words):
    # query = f"SELECT * FROM subreddit_submission_metadata WHERE LENGTH(selftext) >= {num_chars};"
    query = f"select * from subreddit_submission_metadata where (length(selftext) - length(replace(selftext, ' ', '')) + 1) >= {num_words};"
    df = pd.read_sql_query(text(query),con=engine.connect())
    print(f"{len(df)} submissions with {num_words} or more words")
    return df

if __name__ == "__main__":
    filtered_300 = filter_out(300)
    filtered_300.to_sql('filtered_300', con=engine5, if_exists='append', index=False)
    # filtered_200 = filter_out(200)
    # filtered_200.to_sql('filtered_200', con=engine4, if_exists='append', index=False)
    # metadata_query = "select * from subreddit_submission_metadata;"
    # metadata_df = pd.read_sql_query(text(metadata_query), con=engine.connect())
    # metadata_df.to_sql('subreddit_submission_metadata', con=engine2, if_exists='append', index=False)
    # content_query = "select * from submission_content;"
    # content_df = pd.read_sql_query(text(content_query), con=engine.connect())
    # content_df.to_sql('submission_content', con=engine3, if_exists='append', index=False)