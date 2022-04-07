import subprocess
import datetime
from sqlalchemy import create_engine, text
import logging

engine = create_engine("mysql+pymysql://pizza:pizza@localhost/temp_hum?charset=utf8")

last_insert = datetime.datetime.now() - datetime.timedelta(seconds=60)

mac_address = "A4:C1:38:B3:5E:C7"

cmd = ["gatttool", "-b", mac_address, "--char-write-req", "--handle=0x0038", '--value=0100', "--listen"]

with engine.connect() as conn:         #establishing a connection
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1,  universal_newlines=True) as p:

        for line in p.stdout:
            
            # Notification handle = 0x0036 value: 9d 0a 34 3a 0b
            if line.startswith("Notification handle = 0x0036 value:"):

                # acquisiting current date and time
                date = str(datetime.datetime.now())
                date = date.split(".")
                date = date[0]

                # insulating temperature and humidity from notification andle
                data = line.split(": ")
                data = data[1].split()

                # converting temperature and humidity to standard measurement units
                hum =  "0x"+data[2]
                humidity = int(hum,16)

                temp1 = "0x"+data[1]+data[0]
                temperature = int(temp1,16)/100

                logging.info(date, humidity, temperature)

                # sending to database one observation per minute
                if (datetime.datetime.now()-last_insert).seconds >= 60:
                    #inserting observations in the database
                    conn.execute(text(f"insert into t_h values ('{date}',{humidity},{temperature});"))
                    # updating last insert
                    last_insert = datetime.datetime.now()

                    logging.info("Sent to database")
