from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, ListAttribute, NumberAttribute, JSONAttribute, UTCDateTimeAttribute
from datetime import datetime
import hashlib

class User(Model):
    class Meta:
        table_name = "users"
        region = "us-east-2"

    uid = UnicodeAttribute(hash_key=True)
    email = UnicodeAttribute()
    membership_type = NumberAttribute(default=0)
    membership_start = UTCDateTimeAttribute(null=True)
    payment = JSONAttribute(null=True)      # {credit_card, security, expiry, name, address, phone}
    websites = JSONAttribute(null=True)     # {url1:{name}, url2: ...}

class Website(Model):
    class Meta:
        table_name = "websites"
        region = "us-east-2"

    url = UnicodeAttribute(hash_key=True)
    current_code = UnicodeAttribute(null=True)
    contacts = JSONAttribute(null=True)         # {contact_location:frequency}


class Update(Model):
    class Meta:
        table_name = "updates"
        region = "us-east-2"

    url = UnicodeAttribute(hash_key=True)
    last_checked = UTCDateTimeAttribute(null=True)
    last_updated = UTCDateTimeAttribute(null=True)

class Log(Model):
    class Meta:
        table_name = "updates"
        region = "us-east-2"

    log_id = UnicodeAttribute(hash_key=True)
    log_event = UnicodeAttribute(null=True)
    log_time = UTCDateTimeAttribute(null=True)

    # log id =hashlib.md5(("some event" + str(int(time.time()))).encode("utf-8")).hexdigest(),


# if not User.exists():
#     User.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)

# user = User(uid="as2932", email="maharshmellow@gmail.com", payment={"credit_card":"3992392920196327", "address":"1708 Street"})

# user.save()



# print(User.get("as2932").payment)
