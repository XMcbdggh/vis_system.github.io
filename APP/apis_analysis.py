#做api接口
import numpy as np
import pandas as pd
from flask import jsonify
from flask_restful import Resource, fields, marshal_with, reqparse
from sqlalchemy import func, extract
from .models import debris,db


# class Analysis(Resource):
class Activities(Resource):
    def get(self):
        # 定义查询条件
        conditions =  (debris.kg_of_collected_waste != 0)
        # 构建一个查询来按年和月分组并计算每组的数量
        results = db.session.query(
            extract('year', debris.startdate).label('year'),
            extract('month', debris.startdate).label('month'),
            func.count(debris.activity_id).label('count')
        ).filter(conditions).group_by(
            'year',
            'month'
        ).all()

        # 格式化结果为一个列表的字典
        activities = [
            {'year': int(year), 'month': int(month), 'count': count} for year, month, count in results
        ]

        # 返回 JSON 响应
        return jsonify(activities)
class MissActivities(Resource):
    def get(self):
        # 定义查询条件
        conditions = (debris.personal_use == 0) & \
                     (debris.fisheries == 0) & \
                     (debris.industrial == 0) & \
                     (debris.hygiene == 0) & \
                     (debris.others == 0) & \
                     (debris.kg_of_collected_waste != 0)

        # 执行查询并按年份和月份分组
        results = db.session.query(
            extract('year', debris.startdate).label('year'),
            extract('month', debris.startdate).label('month'),
            func.count().label('count')
        ).filter(conditions).group_by(
            'year',
            'month'
        ).all()

        # 格式化结果并返回
        activities = [
            {'year': int(year), 'month': int(month), 'count': count} for year, month, count in results
        ]

        return jsonify(activities)

class QualityScores(Resource):
    def get(self):
        # 定义missingData查询条件
        missConditions = (debris.personal_use == 0) & \
                         (debris.fisheries == 0) & \
                         (debris.industrial == 0) & \
                         (debris.hygiene == 0) & \
                         (debris.others == 0) & \
                         (debris.kg_of_collected_waste != 0)

        # 从数据库中查询数据
        missing_data = db.session.query(
            extract('year', debris.startdate).label('year'),
            extract('month', debris.startdate).label('month'),
            debris.activity_id
        ).filter(missConditions).all()

        total_data = db.session.query(
            extract('year', debris.startdate).label('year'),
            extract('month', debris.startdate).label('month'),
            debris.activity_id
        ).all()
        print(missing_data)
        # 将查询结果转换为DataFrame
        missing_data_df = pd.DataFrame(missing_data, columns=['year', 'month', 'activity_id'])
        total_data_df = pd.DataFrame(total_data, columns=['year', 'month', 'activity_id'])

        # 计算每个月的总条目数和缺失数据条目数
        missing_entries_by_year_month = missing_data_df.groupby(['year', 'month']).size()
        total_entries_per_month_whole = total_data_df.groupby(['year', 'month']).size()


        # 计算质量分数
        quality_scores = 100 - ((missing_entries_by_year_month / total_entries_per_month_whole) * 100)

        # 将质量分数与年月信息合并
        quality_scores_df = quality_scores.reset_index(name='quality_score')
        print('quality_scores_df',quality_scores_df)

        # 填充NaN值为100
        quality_scores_df['quality_score'] = quality_scores_df['quality_score'].fillna(100)

        # 转换为JSON
        quality_scores_json = quality_scores_df.to_dict(orient='records')
        return jsonify(quality_scores_json)

class compositeQualityScore(Resource):
    def get(self):
        # 定义missingData查询条件
        # missConditions = (debris.personal_use == 0) | \
        #                  (debris.fisheries == 0) | \
        #                  (debris.industrial == 0) | \
        #                  (debris.hygiene == 0) | \
        #                  (debris.others == 0) | \
        #                  (debris.kg_of_collected_waste == 0)
        missConditions = (debris.personal_use == 0) & \
                         (debris.fisheries == 0) & \
                         (debris.industrial == 0) & \
                         (debris.hygiene == 0) & \
                         (debris.others == 0) & \
                         (debris.kg_of_collected_waste != 0)

        # 从数据库中查询数据
        missing_data = db.session.query(
            extract('year', debris.startdate).label('year'),
            extract('month', debris.startdate).label('month'),
            debris.activity_id
        ).filter(missConditions).all()
        activities_data=db.session.query(
            extract('month', debris.startdate).label('month'),
            debris.activity_id
            ).all()
        total_data = db.session.query(
            extract('year', debris.startdate).label('year'),
            extract('month', debris.startdate).label('month'),
            debris.activity_id
        ).all()


        # 将查询结果转换为DataFrame
        missing_data_df = pd.DataFrame(missing_data, columns=['year', 'month', 'activity_id'])
        activities_per_month_df = pd.DataFrame(activities_data, columns=['month', 'activity_id'])
        total_data_df = pd.DataFrame(total_data, columns=['year', 'month', 'activity_id'])

        #计算month_weights
        activities_per_month = activities_per_month_df.groupby(['month']).size()
        total_activities = activities_per_month.sum()
        month_weights = activities_per_month / total_activities
        month_weights_df = month_weights.reset_index(name='weight')
        # month_weights_df['month'] = month_weights_df['month'].apply(
        #     lambda x: pd.to_datetime(x, format='%m').strftime('%b'))
        month_weights_dict = month_weights_df.set_index('month').to_dict()['weight']
        #更新month_weights
        month_weights=month_weights_dict

        # 计算每个月的总条目数和缺失数据条目数
        missing_entries_by_year_month = missing_data_df.groupby(['year', 'month']).size()
        max_missing_count=missing_entries_by_year_month.max()
        #计算缺失分数
        inverse_missing_score = 100 - ((missing_entries_by_year_month / max_missing_count) * 100)
        total_entries_per_month_whole = total_data_df.groupby(['year', 'month']).size()
        # 计算质量分数
        quality_scores = 100 - ((missing_entries_by_year_month / total_entries_per_month_whole) * 100)
        quality_scores_filled = quality_scores.fillna(100)

        #composite_quality_score
        w1 = 0.5
        w2 = 0.5
        months = range(1, 13)
        years=sorted(total_data_df['year'].unique())

        multi_index = pd.MultiIndex.from_product([years, months], names=["year", "month"])
        composite_quality_score = pd.Series(index=multi_index, dtype=float).fillna(0)  # Fill with 0 for months without data
        for year in years:
            for month in months:
                weight = month_weights.get(month, 1)  # Default weight is 1
                missing_score = inverse_missing_score.get((year, month),
                                                          0)  # Default missing score is 0 if not available
                quality_score = quality_scores_filled.get((year, month),
                                                          0)  # Default quality score is 0 if not available
                # Calculate weighted scores
                weighted_missing = missing_score * weight
                weighted_quality = quality_score * weight
                # Composite score calculation
                composite = (w1 * weighted_missing + w2 * weighted_quality) / (w1 + w2)
                composite_quality_score.loc[(year, month)] = composite
        print('composite_quality_score',composite_quality_score)

        composite_quality_score_df=composite_quality_score.reset_index(name='composite_quality_score')
        composite_quality_score_dict=composite_quality_score_df.to_dict(orient='records')


        return jsonify(composite_quality_score_dict)
