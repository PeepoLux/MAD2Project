# from models import *
# from app import cache

# @cache.memoize(30)
# def venue_feed(user_id):
#     user = Users.query.filter_by(user_id = user_id).first()
#     blogs_to_display = db.session.query(Venues, Shows).filter(
#         Following.following == BlogPost.user_id).filter(Following.user_id == user_id).order_by(desc(BlogPost.timestamp)).limit(3).all()
#     return user,blogs_to_display