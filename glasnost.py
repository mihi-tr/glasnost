import itertools,re #we are going to need them
import psycopg2,datetime

sql=psycopg2.connect(database="glasnost",user="glasnost")
cur=sql.cursor()


class Log:
    def __init__(self,file=None,sql=None):
        if file:
            self.parse(file)
        if sql:
            self.store(sql)
    
    def parse(self,file):
        f=open(file)
        self.client=self.extract_client(f)
        self.testresults=[r for r in self.extract_test_results(f)]
        f.close()
    
    def store(self,sql):
        self.sql=sql
        self.store_client()
        for t in self.testresults:
            self.store_testresult(t)
    
    def store_client(self):
        self.client["time"]=datetime.datetime.fromtimestamp(int(self.client["time"])/1000)
        self.sql.execute("""insert into client (ip,time) values
        ('{ip}','{time}');""".format(**self.client))
        self.sql.execute("""select id from client where ip='{ip}' and
        time='{time}' limit 1;""".format(**self.client))
        self.clientid=self.sql.fetchone()[0]
        print self.clientid
     
    def store_testresult(self,t):
        test=t["test"]
        self.sql.execute("""insert into test (test, mode, port, client_id)
        values
        ('{test}','{mode}',{port},{clientid});""".format(clientid=self.clientid,**test))
        " determine self id "
        self.sql.execute("""select id from test where client_id={clientid}
        order by (id) desc limit 1""".format(clientid=self.clientid))
        testid=self.sql.fetchone()[0]
        who=["client","server"]
        for w in who:
            self.store_result(w,t[w],testid)
    
    def store_result(self,who,result,testid):
        self.sql.execute("""insert into result (test_id, who, received,
        transmitted, seconds, rxrate, txrate) values
        ({testid},'{who}',{received},{transmitted},{seconds},{rxrate},{txrate});
        """.format(testid=testid,who=who,**result))
        
    def extract_re(self,lines,regex):
        regex=re.compile(regex)
        ln=itertools.dropwhile(lambda x: not regex.match(x), lines)
        return regex.match(ln.next()).groups()

    def extract_test(self,lines):
        return dict(zip(('time','test','mode','port'),
           self.extract_re(lines,"^([0-9]+) Received: replay ([a-zA-Z]+) as ([a-z]+) on port ([0-9]+)")))

    def extract_client(self,lines):
        return dict(zip(('time','ip'),self.extract_re(lines,"^([0-9]+) Client .* ([0-9.]+) connected")))

    def extract_server_results(self,lines):
        return dict(zip(('time','transmitted','received','seconds','txrate','rxrate'),
        self.extract_re(lines,"^([0-9]+) Transmitted ([0-9]+) bytes and received ([0-9]+) bytes in ([0-9.]+) seconds: ([0-9.]+) ([0-9.]+) bps")))

    def extract_client_results(self,lines):
        return dict(zip(('time','transmitted','received','seconds','txrate','rxrate'),
        self.extract_re(lines,"^([0-9]+) Client: Transferred ([0-9]+) bytes and received ([0-9]+) bytes in ([0-9.]+) seconds: ([0-9.]+) ([0-9.]+) bps")))

    def extract_test_results(self,lines):
        while lines:
            yield {"test": self.extract_test(lines), "server": self.extract_server_results(lines),
                "client": self.extract_client_results(lines)}

if __name__=="__main__":
    log=Log("testdata.log",cur)
    sql.commit()
