import random

EXAMPLE_COMMENTS = [
    "What did you think of this video?",
    "Let me know your favorite part!",
    "Would you like to see more like this?",
    "Drop your thoughts in the comments!",
    "Appreciate the support, you're awesome!"
]

def auto_engage_comments(video_id):
    print(f"[Comments] Simulating comment engagement on video: {video_id}")
    comment = random.choice(EXAMPLE_COMMENTS)
    print(f"[Comments] Auto-comment: {comment}")
