from staffpost import StaffPost

class Staff(StaffPost):
    def __init__ (self, surname, firstname, middlename, birthday):
        self.surname = surname
        self.firstname = firstname
        self.middlename = middlename
        self.birthday = birthday
        super().insertinfo('staff')
        super().keys()
    
    def createtable(self):
        script = '''
                    create table if not exists staff(
                        id integer primary key,
                        surname text not null,
                        firstname text not null,
                        middlename text,
                        birthday date not null,
                        post_id integer,
                        edu_id integer,
                        foreign key (post_id) references staff_post(id),
                        foreign key (edu_id) references education(id)
                    )
                '''
        return script
    
