import psycopg2
import pygeoip

sql=psycopg2.connect(database="glasnost",user="glasnost")

geoip=pygeoip.GeoIP("geoip/GeoIP.dat")

json_dir="html/json/"

