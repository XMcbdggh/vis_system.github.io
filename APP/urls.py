#做api路由
from .exts import  api
from .apis_display import *
from .apis_analysis import *

api.add_resource(Givedata, '/giveData/')
api.add_resource(GivePieData, '/givePieData/')
api.add_resource(GiveBarData, '/giveBarData/')
api.add_resource(GiveTimeBarData, '/giveTimeBarData/')
api.add_resource(Activities, '/activities/')
api.add_resource(MissActivities, '/missActivities/')
api.add_resource(QualityScores, '/qualityScores/')
api.add_resource(compositeQualityScore, '/compositeQualityScore/')