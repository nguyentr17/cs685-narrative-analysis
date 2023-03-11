from db import engine
# from db import get_session
# import db.models as models

from datetime import datetime
from pmaw import PushshiftAPI
import pandas as pd

class Collection:
    def __init__(self):
        self.api = PushshiftAPI()
        self.before = int(datetime(2023,1,31,0,0).timestamp())  # Jan 31, 2023
        self.after = int(datetime(2020,1,1,0,0).timestamp()) # Jan 1, 2020

    def get_nutrition_subreddits(self):
        subreddits = [
            "nutrition",
            "EatCheapAndHealthy",
            "ketogains",
            "SportNutrition",
            "EatHealthy",
            "intuitiveeating",
            "HealthFoodChat",
            "FitnessFood",
            "Macrofoodients",
            "xxfitness",
            "veganfitness",
            "runmeals",
            # "workout", # unavailable
            "bodyweightfitness",
            "Dietandhealth",
            "diet",
            # "dieting", # unavailable
            "PlantBasedDiet",
            "Pescetarian"
        ]
        return subreddits

    def get_ed_subreddits(self):
        subreddits = [
            "EatingDisorders",
            "eating_disorders",
            "EatingDisorderHope",
            "edsupport",
            "EDAnonymous",
            "EdAnonymousAdults",
            "EDRecovery_public",
            # "EDRecovery", # unavailable
            "AnorexiaNervosa",
            "AnorexiaRecovery",
            # "ProAnaBuddies", # unavailable
            "anorexiaflareuphelp",
            "bulimia",
            "BulimiaRecovery", # not from paper
            "BulimiaAndAnaSupport",
            "BingeEatingDisorder",
            "BingeEatingRecovery",  # not from paper
            "bingeeating",
            "PurgingDisorder",
            "NotOtherwiseSpecified",
            # "Ednos", # unavailable
        ]
        return subreddits

    def get_columns(self):
        cols = [
            'subreddit',
            'selftext',
            'author_fullname',
            'gilded',
            'title',
            'subreddit_name_prefixed',
            'hidden',
            'pwls',
            'quarantine',
            'link_flair_text_color',
            'upvote_ratio',
            'subreddit_type',
            'total_awards_received',
            'is_original_content',
            'is_reddit_media_domain',
            'is_meta',
            'score',
            'is_created_from_ads_ui',
            'author_premium',
            'thumbnail',
            'edited',
            'is_self',
            'link_flair_type',
            'wls',
            'author_flair_type',
            'domain',
            'allow_live_comments',
            'archived',
            'no_follow',
            'pinned',
            'over_18',
            'media_only',
            'can_gild',
            'spoiler',
            'locked',
            'author_flair_text',
            'subreddit_id',
            'link_flair_background_color',
            'id',
            'is_robot_indexable',
            'author',
            'num_comments',
            'send_replies',
            'whitelist_status',
            'contest_mode',
            'author_patreon_flair',
            'permalink',
            'parent_whitelist_status',
            'stickied',
            'url',
            'subreddit_subscribers',
            'created_utc',
            'num_crossposts',
            'is_video',
            'retrieved_utc',
            'updated_utc',
            'utc_datetime_str',
        ]
        return cols

    def get_time_range(self, oldest_date):
        self.before = oldest_date
        print(f"    Time Range: {datetime.fromtimestamp(self.after)} - {datetime.fromtimestamp(self.before)}")
        return self.before, self.after
    
    def get_batch(self, before, after, subreddit, limit=1000):
        submissions = self.api.search_submissions(subreddit=subreddit, limit=limit, before=before, after=after)
        print(f"    Batch Retrieved {len(submissions)} submissions from PushShift")
        submissions_df = pd.DataFrame(submissions)
        return submissions_df

    def collection_round(self, subreddit):
        submissions_df = self.get_batch(self.before, self.after, subreddit=subreddit)
        try:
            before, after = self.get_time_range(submissions_df["created_utc"].tolist()[-1])
        except:
            print(f"    Round Retrieved: {len(submissions_df)}\nUnable to establish new time range.")
        return submissions_df

    def get_submissions(self):
        for subreddit in self.get_ed_subreddits():
            print(f"Subreddit: {subreddit}\n")
            count = 0
            round = self.collection_round(subreddit=subreddit)
            # round = round.loc[round['id'] != '']
            # round = round.loc[round['id'] != None]
            count += round.shape[0]
            print(f"    Count: {count}\n")

            try:
                text_author = round[['id','selftext']]
                text_author.to_sql('submission_content', con=engine, if_exists='append', index=False)

                limited = round[self.get_columns()]
                limited.to_sql('subreddit_submission_metadata', con=engine, if_exists='append', index=False)
            except Exception as e:
                print(f"    {e}")

            while round.shape[0] > 0:
                round = self.collection_round(subreddit=subreddit)
                count += round.shape[0]
                print(f"    Count: {count}\n")
                try:
                    text_author = round[['id','selftext']]
                    text_author.to_sql('submission_content', con=engine, if_exists='append', index=False)

                    limited = round[self.get_columns()]
                    limited.to_sql('subreddit_submission_metadata', con=engine, if_exists='append', index=False)
                except Exception as e:
                    print(f"    {e}")