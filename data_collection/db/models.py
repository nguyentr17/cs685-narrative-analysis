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
    link_flair_css_class = Column(String)
    link_flair_text = Column(String)
    author_flair_type = Column(String)
    over_18 = Column(Boolean)
    author_flair_text = Column(String)
    subreddit_id = Column(String)
    id = Column(
        String,
        primary_key=True,
        default=generate_uuid
    )
    is_self = Column(Boolean)
    author = Column(String)
    author_flair_css_class = Column(String)
    author_flair_text = Column(String)
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
    link_flair_css_class = Column(String)
    link_flair_text = Column(String)
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
    is_self = Column(Boolean)
    author = Column(String)
    author_flair_css_class = Column(String)
    author_flair_text = Column(String)
    permalink = Column(String)
    url = Column(String)
    created_utc = Column(Integer)

    __table_args__ = (UniqueConstraint("id", sqlite_on_conflict="IGNORE"),)


