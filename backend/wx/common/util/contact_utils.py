from wx.common.enum.contact_type import ContactType


class ContactUtils(object):

    @staticmethod
    def contact_type(username: str):
        if username.endswith("@openim"):
            return ContactType.OPENIM
        elif username.startswith("gh_"):
            return ContactType.GH
        else:
            return ContactType.NORMAL
