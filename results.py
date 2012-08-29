from settings import sql
import datetime

cur=sql.cursor()

'create the client results:'
cur.execute("""INSERT INTO client_results 
SELECT id,ip,asn,time,cc,summary.stest,min(rate) FROM client INNER JOIN 
(SELECT test.client_id,test.test,max(rxrate)/max(txrate)  AS
rate,mode,test.test AS stest FROM result,test WHERE test_id=test.id 
GROUP
BY test.client_id,mode,test.port,test.test HAVING max(txrate)>0) summary ON summary.client_id=id
WHERE id NOT IN 
(SELECT id FROM client_results) GROUP BY client.id,client.asn,client.time,client.cc,client.ip,summary.stest;""")
''' Don't ask me about this statement: it evolved iteratively 
    If you still want to know: the inner part calculates the
    max(rxrate)/max(txrate) (the final ratio as
    described in the paper) for each port and mode, the select then selects
    the minimum rate (so we catch them shapers) and creates a summary table
    - also includes information about the test. I will definitely hate
      myself once I have to debug this...'''

today=datetime.datetime.now()
last_year=datetime.date(today.year-1,today.month,today.day)
cur.execute("""delete from country_results;""")
cur.execute("""insert into country_results select
client_results.cc,client_results.test,count(id) as total,shaped.shaped,
round(shaped.shaped/count(id)::numeric*100,2) from
client_results left outer join (select cc,count(id) as shaped,test from
client_results where rating < 0.5 group by cc,test) shaped on
shaped.cc=client_results.cc and shaped.test=client_results.test where time>
'%s' group by
client_results.cc,shaped.shaped,client_results.test,shaped.test;"""%last_year)
cur.execute("""update country_results set shaped=0 where shaped is
Null;""")
cur.execute("""update country_results set percent_shaped=0 where percent_shaped is
Null;""")

cur.execute("""delete from provider_results""");
cur.execute("""insert into provider_results select owner, test, sum(total)
as total, sum(shaped) as
shaped,round(sum(shaped)/sum(total)::numeric*100,2) from asn inner join (select
client_results.asn, client_results.test, count(id) as total,
shaped.shaped as shaped from client_results left outer join (select
asn,test,count(id) as shaped from client_results where rating<0.5 group by
asn,test) as shaped on shaped.asn=client_results.asn and
shaped.test=client_results.test where client_results.time > '%s'
group by client_results.asn,client_results.test,shaped.shaped) as r on r.asn=asn.asn
group by asn.owner,r.test;"""%last_year)
cur.execute("update provider_results set shaped=0, percent_shaped=0 where shaped is Null");

sql.commit()
