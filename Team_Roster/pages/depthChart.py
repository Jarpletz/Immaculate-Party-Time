from flask import render_template, request, jsonify
from app import db
from app.models import People, Fielding, Team
from sqlalchemy import func

def ShowDepthChart(teamID, year):
    year = request.args.get('year', type=int)
    stat = request.args.get('stat', 'percentage')

    positions_stats = {}

    positions = ['1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF', 'C', 'P', 'OF']

    for position in positions:
        if stat == 'percentage':
            position_query = db.session.query(
                People.nameFirst,
                People.nameLast,
                Fielding.position,
                (func.sum(Fielding.f_InnOuts) /
                 func.select([func.sum(Fielding.f_InnOuts)]).filter(
                     Fielding.teamID == teamID,
                     Fielding.yearID == year,
                     Fielding.position == position
                 )) * 100).label('stat_value')
            position_query = position_query.filter(
                Fielding.teamID == teamID,
                Fielding.yearID == year,
                Fielding.position == position
            ).group_by(Fielding.playerID, Fielding.position).order_by('stat_value DESC').limit(6)

        
