from enum import Enum

class ActivityType(str, Enum):
    forum_comment = "forum_comment"
    internship_accepted = "internship_accepted"
    material_uploaded = "material_uploaded"
    forum_answer = "forum_answer"