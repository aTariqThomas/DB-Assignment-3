from collections import namedtuple

from flask import g
from flask import escape
from flask import render_template
from flask import request

from voyager.db import get_db, execute
from voyager.validate import validate_field, render_errors
from voyager.validate import NAME_RE, INT_RE, DATE_RE

def sailors(conn):
    return execute(conn, "SELECT s.sid, s.name, s.age, s.experience FROM Sailors AS s")

def who_sailed(conn, b_name):
    return execute(conn, f"SELECT s.sid, s.name FROM Sailors AS s INNER JOIN Voyages ON s.sid = Voyages.sid INNER JOIN Boats ON Boats.bid = Voyages.bid WHERE Boats.name = '{b_name}'")

def which_sailor(conn,s_name):
    return execute(conn, f"SELECT b.bid, b.name FROM Boats AS b INNER JOIN Voyages ON b.bid = Voyages.bid INNER JOIN Sailors ON Sailors.sid = Voyages.bid WHERE Sailors.name = '{s_name}'")

def which_date(conn,v_date):
    return execute(conn, f"SELECT s.sid, s.name FROM Sailors AS s INNER JOIN Voyages on s.sid = Voyages.sid WHERE Dates.date_of_voyage  = '{v_date}")

def views(bp):

    @bp.route("/sailors")
    def _get_all_sailors():
        with get_db() as conn:
            rows = sailors(conn)
        return render_template("table.html", name="Boats", rows=rows)

    
    @bp.route("/sailors/who-sailed", methods=["POST"])
    def _get_input():
        if request.method == "POST":
            b_name = request.form['boat-name']
            with get_db() as conn:
                rows = who_sailed(conn, b_name)
            
            return render_template("table.html", rows=rows, name="Boats")

    @bp.route("/boats/sailed-by", methods=["POST"])
    def _get_b_input():
        if request.method == "POST":
            s_name = request.form['sailor-name']
            with get_db() as conn:
                rows = which_sailor(conn, s_name)
            
            return render_template("table.html", rows=rows, name="Sailors")

    @bp.route("/sailors/who-sailed-on-date", methods=["GET"])
    def _get_dates():
        if request.method == "POST":
            v_date = request.form['date']
            with get_db() as conn:
                rows = which_date(conn, v_date)
            
            return render_template("table.html", rows=rows, name="Dates")

    
        