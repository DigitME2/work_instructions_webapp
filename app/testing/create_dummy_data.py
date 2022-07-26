from app.default.models import *
from app.extensions import db
from time import time

# A script to populate the database with fake information, for testing purposes

db.create_all()

u1 = User(username="Sam", admin=True)
u1.set_password("password")
db.session.add(u1)

u2 = User(username="John")
u2.set_password("password")
db.session.add(u2)

p1 = PartType(part_name="")
db.session.add(p1)

p2 = PartType(part_name="")
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

csv_file = Csv(body="1,2,3,4")
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

