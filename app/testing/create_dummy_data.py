from app.default.models import *
from app import db
from time import time

# A script to populate the database with fake information, for testing purposes

csv_string = """=~=~=~=~=~=~=~=~=~=~=~= PuTTY log 2018.11.01 15:22:25 =~=~=~=~=~=~=~=~=~=~=~=,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,
TurbSense - Version 1.30,,,,,,,,,,,,,,,,,,,
© Process Instruments (UK) Ltd,,,,,,,,,,,,,,,,,,,
Compiled: Jul 25 2018 09:14:39,,,,,,,,,,,,,,,,,,,
Processor running at 72MHz,,,,,,,,,,,,,,,,,,,
AHB bus clock: 72MHz,,,,,,,,,,,,,,,,,,,
APB1 bus clock: 36MHz,,,,,,,,,,,,,,,,,,,
APB2 bus clock: 72MHz,,,,,,,,,,,,,,,,,,,
Serial number: A2AA:C494:75B5:1E71,,,,,,,,,,,,,,,,,,,
Resetingoot flags,,,,,,,,,,,,,,,,,,,
Power On Reset,,,,,,,,,,,,,,,,,,,
Watchdog period: 3276 ms,,,,,,,,,,,,,,,,,,,
Starting scheduler...,,,,,,,,,,,,,,,,,,,
0000:00:00.000 Sensor: Default [Default],,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,
Full Power,Ref,Light Current,,,,,,1/2 Power,,Light Current,,,,,,,,,
0,5295.755,7.733, ***,1,3976.617,5.886, ***,2,2638.501,4.007, ***,3,1277.582,2.094, ***,0.001403,0.303,1,----
0,5283.66,7.714, ***,1,3976.617,5.886, ***,2,2638.501,4.007, ***,3,1277.582,2.094, ***,0.001403,0.304,1,----
0,5283.66,7.714, ***,1,3973.167,5.878, ***,2,2638.501,4.007, ***,3,1277.582,2.094, ***,0.001403,0.304,1,----
0,5283.66,7.714, ***,1,3973.167,5.878, ***,2,2637.188,4.005, ***,3,1277.582,2.094, ***,0.001403,0.304,1,----
0,5283.66,7.714, ***,1,3973.167,5.878, ***,2,2637.188,4.005, ***,3,1276.532,2.09, ***,0.001403,0.301,1,----
0,5281.878,7.704, ***,1,3973.167,5.878, ***,2,2637.188,4.005, ***,3,1276.532,2.09, ***,0.001402,0.304,1,----
0,5281.878,7.704, ***,1,3971.535,5.878, ***,2,2637.188,4.005, ***,3,1276.532,2.09, ***,0.001402,0.304,1,----
0,5281.878,7.704, ***,1,3971.535,5.878, ***,2,2636.063,3.989, ***,3,1276.532,2.09, ***,0.001403,0.297,1,----
0,5281.878,7.704, ***,1,3971.535,5.878, ***,2,2636.063,3.989, ***,3,1276.495,2.039, ***,0.001414,0.247,1,----
0,5280.94,7.711, ***,1,3971.535,5.878, ***,2,2636.063,3.989, ***,3,1276.495,2.039, ***,0.001416,0.243,1,----
0,5280.94,7.711, ***,1,3971.16,5.878, ***,2,2636.063,3.989, ***,3,1276.495,2.039, ***,0.001416,0.243,1,----
0,5280.94,7.711, ***,1,3971.16,5.878, ***,2,2635.688,4.001, ***,3,1276.495,2.039, ***,0.001416,0.249,1,----
0,5280.94,7.711, ***,1,3971.16,5.878, ***,2,2635.688,4.001, ***,3,1276.382,2.017, ***,0.00142,0.227,1,----
,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,
,For the A test interested in the  yellow column - 2000-6000 nA is acceptable range,,,,,,,,,,,,,,,,,,
,For the C test interested in the orange and blue columns - the orange column needs to be in the range 5-10 nA,,,,,,,,,,,,,,,,,,
"""


db.create_all()

u1 = User(username="Sam", admin=True)
u1.set_password("password")
db.session.add(u1)

u2 = User(username="John")
u2.set_password("password")
db.session.add(u2)

p1 = PartType(part_name="IPBI61 TurbSense")
db.session.add(p1)

p2 = PartType(part_name="IPBI80 New SoliSense")
db.session.add(p2)

s1 = Step(part_type_id=1,
          step_number=1,
          step_title="1",
          step_instructions="Take 1 x LED from the line side",
          step_image="/static/images/Test/step1.jpeg")
db.session.add(s1)

f1_1 = Field(step_id=1,
             field_name="LED Serial",
             batch_wide=False)
db.session.add(f1_1)

csv_file = Csv(body=csv_string)
db.session.add(csv_file)
db.session.commit()

# f1_2 = Field(step_id=1,
#              field_name="Weight",
#              batch_wide=False)
# db.session.add(f1_2)
#
# f1_3 = Field(step_id=1,
#              field_name="First Name",
#              batch_wide=False)
# db.session.add(f1_3)
#
# f1_3 = Field(step_id=1,
#              field_name="Last Name",
#              batch_wide=True)
# db.session.add(f1_3)


s2 = Step(part_type_id=1,
          step_number=2,
          step_title="2",
          step_instructions="Check orientation of negative leg(the one closest to the flat edge ofthe glass)",
          step_image="/static/images/Test/step1.jpeg")
db.session.add(s2)

# f2_1 = Field(step_id=2,
#              field_name="Skin Colour")
# db.session.add(f2_1)
#
# f2_2 = Field(step_id=2,
#              field_name="Hair Colour")
# db.session.add(f2_2)

s3 = Step(part_type_id=1,
          step_number=3,
          step_title="3",
          step_instructions="Cut as shown so the shorter leg is the negative leg (tin both legs)",
          step_image="/static/images/Test/step1.jpeg")
db.session.add(s3)

f3_1 = Field(step_id=2,
             field_name="Solder serial number",
             batch_wide=True)
db.session.add(f3_1)


for i in range(1, 10):
    b = Batch(batch_number=i, users=[u1], part_type_id=1)
    print("Creating batch ", i)
    db.session.add(b)
    db.session.commit()
    for j in range(1, 2):
        p = Part(batch_id=b.id, relative_id=j, start_timestamp=time())
        db.session.add(p)
        db.session.commit()
        for step in b.part_type.steps:
            for field in step.fields:
                pd = ProdData(part_id=p.id, field_id=field.id, field_data="testdata")
                db.session.add(pd)
                db.session.commit()

for i in range(11, 20):
    b = Batch(batch_number=i, users=[u1, u2], part_type_id=1)
    db.session.add(b)
    db.session.commit()
    for j in range(1, 9):
        p = Part(batch_id=b.id, relative_id=j)
        db.session.add(p)
        db.session.commit()
        for step in b.part_type.steps:
            for field in step.fields:
                pd = ProdData(part_id=p.id, field_id=field.id, field_data="")
                db.session.add(pd)
                db.session.commit()


db.session.commit()

