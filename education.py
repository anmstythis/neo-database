from staffpost import StaffPost

class Education(StaffPost):
    def __init__ (self, title, speciality, qualification, typeofedu):
        self.title = title
        self.speciality = speciality
        self.qualification = qualification
        self.typeofedu = typeofedu
        super().insertinfo('education')
        super().keys()

    def createtable(self):
        script = '''
            create table if not exists education(
                id integer primary key,
                title text not null,
                speciality text not null,
                qualification text not null,
                typeofedu text not null
            )
        '''
        return script