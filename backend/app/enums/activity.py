from enum import Enum

class ActivityType(str, Enum):
    material_posted = "material_posted"
    forum_comment = "forum_comment"
    internship_accepted = "internship_accepted"
    material_uploaded = "material_uploaded"
    forum_answer = "forum_answer"