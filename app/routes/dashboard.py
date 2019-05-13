"""
ETL API 1.0
dashboard.py
..................
Description
> contains endpoints for dashboard works using the API
"""

from . import routes
from config import muid_creds
from models.rds import RDSWorks
from flask import render_template


@routes.route('/viz')
def dashboard():
    try:
        rds = RDSWorks(**muid_creds)
        rds.connect_to_db()
        pv_total, pv_unique = get_pageviews_by_cuid(rds.cursor)
        print(pv_total, pv_unique)
        n_muids = get_muid_count(rds.cursor)
        rds.close_connection()
        pv_list = []
        for t, u in zip(pv_total, pv_unique):
            pv_list.append((t, pv_total[t], pv_unique[u]))
        return render_template("index.html", pv_list=pv_list, n_muids=n_muids)
    except Exception as e:
        print(e)
        return e


@routes.route('/dashboard/login')
def login():
    raise NotImplementedError


@routes.route('/dashboard/logout')
def logout():
    raise NotImplementedError


def get_pageviews_by_cuid(cur):
    query_total = """SELECT cuid, COUNT(page_url) FROM event_logs GROUP BY cuid"""
    query_unique = """SELECT cuid, COUNT(distinct page_url) FROM event_logs GROUP BY cuid"""
    try:
        cur.execute(query_total)
        result_total = cur.fetchall()
        cur.execute(query_unique)
        result_unique = cur.fetchall()
        total, unique = {i[0]: i[1] for i in result_total}, {
            i[0]: i[1] for i in result_unique}
        return total, unique
    except Exception as e:
        print(e)
        return None


def get_muid_count(cur):
    """
    Only get the ones not generated through onboarded records
    """
    query = """SELECT COUNT(DISTINCT muid) FROM event_logs"""
    try:
        cur.execute(query)
        result = cur.fetchone()
        return result[0]
    except Exception as e:
        print(e)
        return None
