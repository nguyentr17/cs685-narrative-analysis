from sqlalchemy import Column, ForeignKey, String, Integer, UniqueConstraint
from sqlalchemy.types import DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class TextContent(Base):
    """Submission Text Content"""

    __tablename__ = "submission_content"

    """Same id as subreddit_submission_metadata table"""
    id = Column(
        String,
        primary_key=True,
        default=generate_uuid
    )

    selftext = Column(String)
    __table_args__ = (UniqueConstraint("id", sqlite_on_conflict="IGNORE"),)

class Filtered200(Base):
    """Filtered for >=200 words"""

    __tablename__ = "filtered_200"

    subreddit = Column(String)
    selftext = Column(String)
    author_fullname = Column(String)
    title = Column(String)
    score = Column(Integer)
    link_flair_type = Column(String)
    author_flair_type = Column(String)
    over_18 = Column(Boolean)
    author_flair_text = Column(String)
    subreddit_id = Column(String)
    id = Column(
        String,
        primary_key=True,
        default=generate_uuid
    )
    author = Column(String)
    author_patreon_flair = Column(Boolean)
    permalink = Column(String)
    url = Column(String)
    created_utc = Column(Integer)

    __table_args__ = (UniqueConstraint("id", sqlite_on_conflict="IGNORE"),)

class SubredditSubmissionMetadata(Base):
    """Subreddit Submission Metadata"""

    __tablename__ = "subreddit_submission_metadata"

    subreddit = Column(String)
    selftext = Column(String)
    author_fullname = Column(String)
    title = Column(String)
    score = Column(Integer)
    link_flair_type = Column(String)
    author_flair_type = Column(String)
    over_18 = Column(Boolean)
    author_flair_text = Column(String)
    subreddit_id = Column(String)
    id = Column(
        String,
        ForeignKey("submission_content.id", ondelete="CASCADE"),
        primary_key=True,
        default=generate_uuid
    )
    author = Column(String)
    author_patreon_flair = Column(Boolean)
    permalink = Column(String)
    url = Column(String)
    created_utc = Column(Integer)

    # gilded = Column(Integer)
    # link_flair_richtext = Column(Text) #? []
    # subreddit_name_prefixed = Column(String)
    # hidden = Column(Boolean)
    # pwls = Column(Integer)
    # link_flair_css_class = Column(String)
    # thumbnail_height = Column(Float)
    # top_awarded_type = Column(String)
    # hide_score = Column(Boolean)
    # quarantine = Column(Boolean)
    # link_flair_text_color = Column(String)
    # upvote_ratio = Column(Float)
    # author_flair_background_color = Column(String)
    # subreddit_type = Column(String)
    # total_awards_received = Column(Integer)
    # media_embed = Column(JSON) #? {}
    # thumbnail_width = Column(Float)
    # author_flair_template_id = Column(String)
    # is_original_content = Column(Boolean)
    # secure_media = Column(String)
    # is_reddit_media_domain = Column(Boolean)
    # is_meta = Column(Boolean)
    # category = Column(String)
    # secure_media_embed = Column(Text) #? {}
    # link_flair_text = Column(String)
    # is_created_from_ads_ui = Column(Boolean)
    # author_premium = Column(Boolean)
    # thumbnail = Column(String)
    # edited = Column(Boolean)
    # author_flair_css_class = Column(String)
    # author_flair_richtext = Column(Text)
    # gildings = Column(Text) #? {}
    # content_categories = Column(String)
    # is_self = Column(Boolean)
    # wls = Column(Integer)
    # removed_by_category = Column(String)
    # domain = Column(String)
    # allow_live_comments = Column(Boolean)
    # suggested_sort = Column(String)
    # view_count = Column(String)
    # archived = Column(Boolean)
    # no_follow = Column(Boolean)
    # is_crosspostable = Column(Boolean)
    # pinned = Column(Boolean)
    # all_awardings = Column(Text) #? []
    # awarders = Column(Text)
    # media_only = Column(Boolean)
    # can_gild = Column(Boolean)
    # spoiler = Column(Boolean)
    # locked = Column(Boolean)
    # treatment_tags = Column(Text) #? []
    # removed_by = Column(String)
    # distinguished = Column(String)
    # link_flair_background_color = Column(String)
    # is_robot_indexable = Column(Boolean)
    # discussion_type = Column(String)
    # num_comments = Column(Integer)
    # send_replies = Column(Boolean)
    # whitelist_status = Column(String)
    # contest_mode = Column(Boolean)
    # author_flair_text_color = Column(String)
    # parent_whitelist_status = Column(String)
    # stickied = Column(Boolean)
    # subreddit_subscribers = Column(Integer)
    # num_crossposts = Column(Integer)
    # media = Column(String)
    # is_video = Column(Boolean)
    # retrieved_utc = Column(Integer)
    # updated_utc = Column(Integer)
    # utc_datetime_str = Column(DateTime)
    # post_hint = Column(String)
    # url_overridden_by_dest = Column(String)
    # preview = Column(String)
    # is_gallery = Column(String)
    # media_metadata = Column(String)
    # gallery_data = Column(String)
    # crosspost_parent_list = Column(String)
    # crosspost_parent = Column(String)

    __table_args__ = (UniqueConstraint("id", sqlite_on_conflict="IGNORE"),)


