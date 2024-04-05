#做api接口
from flask import jsonify
from flask_restful import Resource, fields, marshal_with, reqparse
from sqlalchemy import func, extract
from .models import debris,db


#all geo Data
geoData = {
    'county_name': fields.String,
    'kg_of_collected_waste': fields.Float,
    'name': fields.String(attribute='id'),  # 'name' 字段映射到数据库中的 'id'
    'startData': fields.Integer(attribute=lambda x: x.startdate.year),  # 提取年份
    'type': fields.Nested({
        'fisheries': fields.Float,
        'hygiene': fields.Float,
        'industrial': fields.Float,
        'others': fields.Float,
        'personal_use': fields.Float
    }),
    'value': fields.List(fields.Float, attribute=lambda x: [float(coord) for coord in x.geom_wkt.strip('POINT()').split()])  # 解析经纬度
}
class Givedata(Resource):
   # @marshal_with(geoData)
    def get(self):
        """
        GET
        :return: {
            "county_name": data.county_name,
            "kg_of_collected_waste": data.kg_of_collected_waste,
            "name": str(data.activity_id),  # 假设 activity_id 是数据库中的 id
            "startData": data.startdate.year,  # 提取年份
            "type": {
                "fisheries": data.fisheries,
                "hygiene": data.hygiene,
                "industrial": data.industrial,
                "others": data.others,
                "personal_use": data.personal_use
            },
            "geom_wkt": [float(coord) for coord in data.geom_wkt.strip('POINT()').split()]  # 解析经纬度
                             }
        """
        # 假设 data 是从数据库查询到的数据
        datas = debris.query.all()
        geoDatas = []
        for data in datas:
            formatted_data = {
            "county_name": data.county_name,
            "kg_of_collected_waste": data.kg_of_collected_waste,
            "name": str(data.activity_id),  # 假设 activity_id 是数据库中的 id
            "startData": data.startdate.year,  # 提取年份
            "type": {
                "fisheries": data.fisheries,
                "hygiene": data.hygiene,
                "industrial": data.industrial,
                "others": data.others,
                "personal_use": data.personal_use
            },
            "geom_wkt": [float(coord) for coord in data.geom_wkt.strip('POINT()').split()]  # 解析经纬度
                             }
            geoDatas.append(formatted_data)
        return jsonify(geoDatas)

class GivePieData(Resource):
    def get(self):
        datas = debris.query.all()
        # 初始化一个字典来聚集数据
        county_aggregated_data = {}

        for data in datas:
            # 如果县名在字典中不存在，则初始化
            if data.county_name not in county_aggregated_data:
                county_aggregated_data[data.county_name] = {
                    "others": 0,
                    "hygiene": 0,
                    "industrial": 0,
                    "fisheries": 0,
                    "personal_use": 0
                }

            # 累加每个类型的值
            county_aggregated_data[data.county_name]["others"] += data.others or 0
            county_aggregated_data[data.county_name]["hygiene"] += data.hygiene or 0
            county_aggregated_data[data.county_name]["industrial"] += data.industrial or 0
            county_aggregated_data[data.county_name]["fisheries"] += data.fisheries or 0
            county_aggregated_data[data.county_name]["personal_use"] += data.personal_use or 0

        # 将聚集后的数据转换成所需的格式
        result = []
        for county_name, types in county_aggregated_data.items():
            result.append({
                "county_name": county_name,
                "data": [
                    {"name": "others", "value": types["others"]},
                    {"name": "hygiene", "value": types["hygiene"]},
                    {"name": "industrial", "value": types["industrial"]},
                    {"name": "fisheries", "value": types["fisheries"]},
                    {"name": "personal_use", "value": types["personal_use"]}
                ]
            })

        return jsonify(result)

class GiveBarData(Resource):
    def get(self):
        datas = debris.query.all()

        # 初始化聚集结果
        aggregated_data = {
            "others": 0,
            "hygiene": 0,
            "industrial": 0,
            "fisheries": 0,
            "personal_use": 0,
            "kg_of_collected_waste": 0
        }

        # 对数据进行迭代，累加各个字段的值
        for data in datas:
            aggregated_data["others"] += data.others or 0
            aggregated_data["hygiene"] += data.hygiene or 0
            aggregated_data["industrial"] += data.industrial or 0
            aggregated_data["fisheries"] += data.fisheries or 0
            aggregated_data["personal_use"] += data.personal_use or 0
            aggregated_data["kg_of_collected_waste"] += data.kg_of_collected_waste or 0

        # 构造返回数据
        result = {
            "county_name": "Norway",
            "data": [
                {"name": "others", "value": aggregated_data["others"]},
                {"name": "hygiene", "value": aggregated_data["hygiene"]},
                {"name": "industrial", "value": aggregated_data["industrial"]},
                {"name": "fisheries", "value": aggregated_data["fisheries"]},
                {"name": "personal_use", "value": aggregated_data["personal_use"]},
                {"name": "kg_of_collected_waste", "value": aggregated_data["kg_of_collected_waste"]}
            ]
        }
        print(jsonify(result))
        return jsonify(result)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('currentProvince', required=True, type=str, help="Province is required.")
        args = parser.parse_args()
        print(args)
        current_province = args['currentProvince']
        print(current_province)
        # 查询数据库中所有county_name等于currentProvince的记录
        datas = debris.query.filter_by(county_name=current_province).all()
        print(datas)

        # 初始化聚集结果
        aggregated_data = {
            "others": 0,
            "hygiene": 0,
            "industrial": 0,
            "fisheries": 0,
            "personal_use": 0,
            "kg_of_collected_waste": 0
        }

        # 对数据进行迭代，累加各个字段的值
        for data in datas:
            aggregated_data["others"] += data.others or 0
            aggregated_data["hygiene"] += data.hygiene or 0
            aggregated_data["industrial"] += data.industrial or 0
            aggregated_data["fisheries"] += data.fisheries or 0
            aggregated_data["personal_use"] += data.personal_use or 0
            aggregated_data["kg_of_collected_waste"] += data.kg_of_collected_waste or 0

        # 构造返回数据
        result = {
            "county_name": current_province,
            "data": [
                {"name": "others", "value": aggregated_data["others"]},
                {"name": "hygiene", "value": aggregated_data["hygiene"]},
                {"name": "industrial", "value": aggregated_data["industrial"]},
                {"name": "fisheries", "value": aggregated_data["fisheries"]},
                {"name": "personal_use", "value": aggregated_data["personal_use"]},
                {"name": "kg_of_collected_waste", "value": aggregated_data["kg_of_collected_waste"]}
            ]
        }

        return jsonify(result)


class GiveTimeBarData(Resource):
    def get(self):
        # 使用debris模型直接查询和排序
        # 按年份和县名聚合数据
        query_results = debris.query.with_entities(
            extract('year', debris.startdate).label('year'),
            debris.county_name,
            func.sum(debris.kg_of_collected_waste).label('total_kg_of_collected_waste'),
            func.sum(debris.personal_use).label('total_personal_use'),
            func.sum(debris.hygiene).label('total_hygiene'),
            func.sum(debris.industrial).label('total_industrial'),
            func.sum(debris.fisheries).label('total_fisheries'),
            func.sum(debris.others).label('total_others')
        ).group_by(
            'year',
            debris.county_name
        ).order_by(
            'year',
            debris.county_name
        ).all()

        # 对结果进行格式化
        formatted_results = {}
        for result in query_results:
            year_key = int(result.year)  # 确保年份为整数
            if year_key not in formatted_results:
                formatted_results[year_key] = []

            county_data = {
                "county_name": result.county_name,
                "data": [
                    {"name": "kg_of_collected_waste", "value": result.total_kg_of_collected_waste},
                    {"name": "personal_use", "value": result.total_personal_use},
                    {"name": "hygiene", "value": result.total_hygiene},
                    {"name": "industrial", "value": result.total_industrial},
                    {"name": "fisheries", "value": result.total_fisheries},
                    {"name": "others", "value": result.total_others}
                ]
            }

            formatted_results[year_key].append(county_data)
            for year in formatted_results:
                formatted_results[year].sort(key=lambda x: x['data'][0]['value'], reverse=True)

        # return formatted_results
        return jsonify(formatted_results)

