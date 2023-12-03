from staffpost import StaffPost

class StaffInCorp(StaffPost):
    def __init__(self, staff_id, corp_id):
        self.staff_id = staff_id
        self.corp_id = corp_id
        super().keys()