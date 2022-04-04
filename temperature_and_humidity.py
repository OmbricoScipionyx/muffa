import subprocess
import datetime
from sqlalchemy import create_engine, text

engine = create_engine("mysql+pymysql://pizza:pizza@localhost/temp_hum?charset=utf8")

mac_address = "A4:C1:38:B3:5E:C7"

cmd = ["gatttool", "-b", mac_address, "--char-write-req", "--handle=0x0038", '--value=0100', "--listen"]

with engine.connect() as conn:         #establishing a connection
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1,  universal_newlines=True) as p:        
#    with open("/home/ubuntu/temp_project/data","a") as f:
        for line in p.stdout:
            # Notification handle = 0x0036 value: 9d 0a 34 3a 0b
            #print(line)
            if line.startswith("Notification handle = 0x0036 value:"):

                date = str(datetime.datetime.now())
                date = date.split(".")
                date = date[0]

                data = line.split(": ")
                data = data[1].split()

                hum =  "0x"+data[2]
                humidity = int(hum,16)

                temp1 = "0x"+data[1]+data[0]
                temperature = int(temp1,16)/100

                print(date, humidity, temperature)
                conn.execute(text(f"insert into t_h values ('{date}',{humidity},{temperature});"))       #insert the observation in the database
                #data = date+";"+str(humidity)+";"+ str(temperature)+"\n"
#                f.write(data)
