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
        # self.before = int(datetime(2017,1,31,0,0).timestamp()) # Jan 31, 2017
        # self.after = int(datetime(2020,1,1,0,0).timestamp()) # Jan 1, 2020
        self.after = int(datetime(2015,1,1,0,0).timestamp()) # Jan 1, 2015

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
            # "EatingDisorders",
            # "eating_disorders",
            # "EatingDisorderHope",
            # "edsupport",
            # "EDAnonymous",
            # "EdAnonymousAdults",
            # "EDRecovery_public",
            # "EDRecovery", # unavailable
            # "AnorexiaNervosa",
            # "AnorexiaRecovery",
            # "ProAnaBuddies", # unavailable
            # "anorexiaflareuphelp",
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

    def get_older_columns(self):
        cols = [
            'created_utc',
            'id',
            'author',
            'title',
            'subreddit_id',
            'url',
            'subreddit',
            'selftext',
            'permalink',
            'score',
            'author_flair_text',
            'over_18',
        ]
        return cols

    def get_newer_columns(self):
        cols = [
            'subreddit',
            'selftext',
            'author_fullname',
            'title',
            'score',
            'link_flair_type',
            'author_flair_type',
            'over_18',
            'author_flair_text',
            'subreddit_id',
            'id',
            'author',
            'author_patreon_flair',
            'permalink',
            'url',
            'created_utc',
        ]
        return cols

    def get_columns(self):
        columns = [
            'author',
            'author_flair_css_class',
            'author_flair_text',
            'created_utc',
            # 'distinguished',
            # 'domain',
            # 'gilded',
            # 'hidden',
            # 'hide_score',
            'id',
            'is_self',
            'link_flair_css_class',
            'link_flair_text',
            # 'locked',
            # 'num_comments',
            # 'over_18',
            'permalink',
            # 'quarantine',
            # 'retrieved_utc',
            'score',
            'selftext',
            'subreddit',
            'subreddit_id',
            'title',
            # 'treatment_tags',
            'url',
            # 'utc_datetime_str',
        ]

        return columns

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
            self.before = int(datetime(2023,1,31,0,0).timestamp())
            print(f"Subreddit: {subreddit}\n")
            count = 0
            round = self.collection_round(subreddit=subreddit)

            try:
                df2 = round.groupby(['id'])['id'].count()
                print(f"    Unique IDs: {len(df2)}\n")
            except:
                print("     Collected 0, outside while loop\n")

            count += len(df2)

            try:
                text_author = round[['id','selftext']]
                text_author.to_sql('submission_content', con=engine, if_exists='append', index=False)

                limited = round[self.get_columns()]
                limited.to_sql('subreddit_submission_metadata', con=engine, if_exists='append', index=False)

            except Exception as e:
                print(f"    {e}")
                # try:    
                #     older_limited = round[self.get_old_columns()]
                #     older_limited.to_sql('subreddit_submission_metadata',con=engine,if_exists='append',index=False)
                # except Exception as e:
                #     print("OLDER LIMITED\n")
                #     print(f"    {e}")

            while round.shape[0] > 0:
                round = self.collection_round(subreddit=subreddit)

                try:
                    df2 = round.groupby(['id'])['id'].count()
                    print(f"    Unique IDs: {len(df2)}\n")
                except:
                    print("     Collected 0, in while loop\n")

                count += len(df2)
                try:
                    text_author = round[['id','selftext']]
                    text_author.to_sql('submission_content', con=engine, if_exists='append', index=False)

                    # limited = round[self.get_columns()]
                    limited = round[self.get_columns()]
                    limited.to_sql('subreddit_submission_metadata', con=engine, if_exists='append', index=False)
                except Exception as e:
                    print(f"    {e}")
                    # try:    
                    #     # older_limited = round[self.get_older_columns()]
                    #     older_limited = round[self.get_old_columns()]
                    #     older_limited.to_sql('subreddit_submission_metadata',con=engine,if_exists='append',index=False)
                    # except Exception as e:
                    #     print("OLDER LIMITED\n")
                    #     print(f"    {e}")

            print(f"    Subreddit Total Count: {count}\n")
