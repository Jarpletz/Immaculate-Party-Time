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
            position_query = (
                db.session.query(
                    People.nameFirst,
                    People.nameLast,
                    Fielding.position,
                    (func.sum(Fielding.f_InnOuts) / func.sum(Fielding.f_InnOuts).over()).label('stat_value')
                )
                .join(Fielding, People.playerID == Fielding.playerID)
                .filter(
                    Fielding.teamID == teamID,
                    Fielding.yearID == year,
                    Fielding.position == position
                )
                .group_by(People.playerID, Fielding.position)
                .order_by(func.sum(Fielding.f_InnOuts).desc())
                .limit(6)
            )

        elif stat == 'PA':
            position_query = db.session.query(
                People.nameFirst,
                People.nameLast,
                Fielding.position,
                func.sum(Fielding.f_PA).label('stat_value')
            )
            position_query = position_query.filter(
                Fielding.teamID == teamID,
                Fielding.yearID == year,
                Fielding.position == position
            ).group_by(Fielding.playerID, Fielding.position).order_by('stat_value DESC').limit(6)
        else:
            return jsonify({'error': 'Invalid statistic selected'}), 400
        
        positions_stats[position] = position_query.all()

    return render_template('depthChart.html', positions_stats=positions_stats, stat=stat, teamID=teamID, year=year)

        
