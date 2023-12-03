class StaffPost:
    def __init__ (self, post, salary):
        self.post = post
        self.salary = salary

    def createtable(self):
        script = '''
                    create table if not exists staff_post(
                        id integer primary key,
                        post varchar(25) not null,
                        salary integer not null
                    )
                '''
        return script
    
    def insertinfo(self, table):
        script = f"insert into {table} {tuple(self.__dict__.keys())} values {tuple(self.__dict__.values())}"
        return script
    
    def keys(self):
        keys = f"{list(self.__dict__.keys())}"
        return keys