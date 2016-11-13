"""
The Bestory Project
"""

# class CommentableThing(Thing):
#     comments_count = Column(Integer)
#
#
# class Comment(LikeableThing, CommentableThing):
#     __tablename__ = "comments"
#
#     id = Column(Integer, primary_key=True)
#     author_id = Column(Integer, ForeignKey("author.id"))
#
#     content = Column(Text)
#
#     submit_date = Column(DateTime)
#     edit_date = Column(DateTime, nullable=True)
#
#     author = relation(User, back_populates="comments")
