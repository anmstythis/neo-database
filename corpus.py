from staffpost import StaffPost

class Corpus(StaffPost):
    def __init__ (self, title, speciality):
        self.title = title
        self.speciality = speciality
        super().insertinfo('corpus')
        super().keys()

    def createtable(self):
        script = '''
            create table if not exists corpus(
                id integer primary key,
                title text not null,
                speciality text not null
            ) 
        '''
        return script