import json,datetime
from settings import sql,json_dir

cur=sql.cursor()

def dump_json(query,columns,file):
    cur.execute(query)
    f=open(file,"w")
    json.dump([dict(zip(columns,r)) for r in cur.fetchall()],f)
    f.close()

" countries.json "
dump_json("""select
cc,sum(total),sum(shaped),sum(shaped)/sum(total)::real*100 from
country_results group by cc;""", ["cc","total","shaped","percent"],
"%s/countries.json"%json_dir)

"countries-test.json"

cur.execute("""select distinct(test) from country_results;""")
tests=[r[0] for r in cur.fetchall()]
f=open("%s/tests.json"%json_dir,"w")
json.dump(tests,f)
f.close()

for test in tests:
    dump_json("""select cc,total,shaped,percent_shaped from
    country_results where
    test='%s';"""%test,["cc","total","shaped","percent"],
    "%s/countries-%s.json"%(json_dir,test))

cur.execute("""select distinct(cc) from client_results;""")
ccs=[r[0] for r in cur.fetchall()]

for cc in ccs:
    dump_json("""select
    owner,sum(total),sum(shaped),sum(shaped)::real/sum(total)::real*100
    from provider_results where owner in (select owner from asn where asn
    in (select asn from client_results where cc='%s')) group by
    owner;"""%cc,["provider","total","shaped","percent"],"%s/country-%s.json"%(json_dir,cc))
    for test in tests:
        dump_json("""select owner,total,shaped,percent_shaped from
        provider_results where owner in (select owner from asn where asn in
        (select asn from client_results where cc='%s') and
        test='%s');"""%(cc,test),["provider","total","shaped","percent"],
           "%s/country-%s-%s.json"%(json_dir,cc,test))

cur.execute("""select distinct(owner) from provider_results;""")
for provider in [r[0] for r in cur.fetchall()]:
    if provider:
        provider_cleaned=provider.replace("/","-")
    dump_json("""select test,total,shaped,percent_shaped from provider_results where
    owner='%s';"""%(provider),["test","total","shaped","percent"],
    "%s/provider-%s.json"%(json_dir,provider_cleaned))

today=datetime.datetime.now()
last_year=datetime.date(today.year-1,today.month,today.day)

cur.execute("""select min(time),max(time) from client_results where time >
'%s';"""%last_year)
f=open("%s/period.json"%json_dir,"w")
json.dump(dict(zip(["begin","end"],['%s'%d for d in cur.fetchone()])), f)
f.close()
