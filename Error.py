#GroupError raised when invalid group/group not created
class GroupError(Exception):
    def __init__(self, msg='Group not found. Use /start first', *args, **kwargs):
        super().__init__(msg, *args, **kwargs)

#UserError raised when invalid user/user not created
class UserError(Exception):
    def __init__(self, msg='User not found', *args, **kwargs):
        super().__init__(msg, *args, **kwargs)

#InvalidLinkError raised when the link sent is not a valid NUSMods timetable link
class InvalidLinkError(Exception):
    def __init__(self, msg='Invalid link', *args, **kwargs):
        super().__init__(msg, *args, **kwargs)

#InvalidActionError raised when user has not entered /edit before editing timetable link
class InvalidActionError(Exception):
    def __init__(self, msg='Invalid Action! Use /edit first to edit your NUSMods timetable link', *args, **kwargs):
        super().__init__(msg, *args, **kwargs)
