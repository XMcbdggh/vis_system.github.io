from .exts import db
#model：类
#必须继承 db.Model
class debris(db.Model):
    __tablename__ = 'debris'

    activity_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    startdate = db.Column(db.Date)  # 或者使用 db.Date，如果只需要日期而不是时间
    county_name = db.Column(db.String(255))  # 根据需要调整字符串长度
    geom_wkt = db.Column(db.Text)  # 地理坐标的长度可能很长，可以使用 db.Text
    kg_of_collected_waste = db.Column(db.Float)
    others = db.Column(db.Float)
    hygiene = db.Column(db.Float)
    industrial = db.Column(db.Float)
    fisheries = db.Column(db.Float)
    personal_use = db.Column(db.Float)