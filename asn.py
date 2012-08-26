from settings import sql
import cymruwhois

cur=sql.cursor()

# get all ips where there is no asn
cur.execute("select ip from client where asn is Null");
ips=[x[0].split("/")[0] for x in cur.fetchall()]
cw=cymruwhois.Client(memcache_host=None)
lu=cw.lookupmany(ips)
for l in lu:
    cur.execute("select asn from asn where asn=%s"%l.asn)
    r=cur.fetchone()
    if not r:
        cur.execute("insert into asn (asn,owner) values(%s,'%s')"%(l.asn,l.owner))
    cur.execute("update client set asn=%s where ip='%s' and asn is Null"%(l.asn,l.ip))
sql.commit()    
