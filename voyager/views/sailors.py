from collections import namedtuple

from flask import g
from flask import escape
from flask import render_template
from flask import request
from flask import Flask,redirect

from voyager.db import get_db, execute
from voyager.validate import validate_field, render_errors
from voyager.validate import NAME_RE, INT_RE, DATE_RE

def _adding_sailor_name(conn,add_sailor_name,add_sailor_age,add_sailor_experience):
    return execute(conn, f"INSERT INTO Sailors(name,age,experience) VALUES ('{add_sailor_name}','{add_sailor_age}','{add_sailor_experience}')")

def _adding_boats(conn,add_boat_name,add_boat_color):
    return execute(conn, f"INSERT INTO Boats(name,color) VALUES ('{add_boat_name}','{add_boat_color}')")

def _adding_voyages(conn,add_sid,add_bid,add_date):
    return execute(conn, f"INSERT INTO Voyages(sid,bid,date_of_voyage) VALUES ('{add_sid}','{add_bid}','{add_date}')")

def sailors(conn):
    return execute(conn, "SELECT s.sid, s.name, s.age, s.experience FROM Sailors AS s")

def pop_Boats(conn):
    return execute(conn, "SELECT Boats.name, count(*) FROM Boats INNER JOIN Voyages on Voyages.bid = Boats.bid GROUP BY Voyages.bid ORDER BY COUNT(*) DESC ")

def who_sailed(conn, b_name):
    return execute(conn, f"SELECT s.sid, s.name FROM Sailors AS s INNER JOIN Voyages ON s.sid = Voyages.sid INNER JOIN Boats ON Boats.bid = Voyages.bid WHERE Boats.name = '{b_name}'")

def which_sailor(conn,s_name):
    return execute(conn, f"SELECT b.bid, b.name FROM Boats AS b INNER JOIN Voyages ON b.bid = Voyages.bid INNER JOIN Sailors ON Sailors.sid = Voyages.bid WHERE Sailors.name = '{s_name}'")

def which_date(conn,v_date):
    return execute(conn, f"SELECT s.sid, s.name FROM Sailors AS s INNER JOIN Voyages on s.sid = Voyages.sid WHERE Voyages.date_of_voyage  = '{v_date}'")

def which_color(conn,b_color):
    return execute(conn, f"SELECT s.sid, s.name FROM Sailors AS s INNER JOIN Voyages on s.sid = Voyages.sid INNER JOIN Boats ON Boats.bid = Voyages.bid WHERE Boats.color = '{b_color}'")

#def insert_sailor(conn):
    #return execute(conn, INSERT INTO)


def views(bp):
    @bp.route("/boats/add", methods=["POST"])
    def add_boat_name() :
        if request.method == "POST":
            add_boat_name = request.form['add-boat-name']
            add_boat_color = request.form['add-color-name']
            with get_db() as conn:
                _adding_boats(conn,add_boat_name,add_boat_color)
            return redirect("/boats")
    
    @bp.route("/sailors/add", methods=["POST"])    
    def _add_sailor_name():
        if request.method == "POST":
            add_sailor_name = request.form['add-sailor-name']
            add_sailor_age = request.form['add-sailor-age']
            add_sailor_experience = request.form['add-sailor-experience']
            with get_db() as conn:
                _adding_sailor_name(conn, add_sailor_name,add_sailor_age,add_sailor_experience)
            return redirect("/sailors")

    @bp.route("/voyages/add", methods=["POST"])
    def _add_voyage_name():
        if request.method == "POST":
            add_sid = request.form["add-sid"]
            add_bid = request.form["add-bid"]
            add_date = request.form["add-date"]
        with get_db() as conn:
            _adding_voyages(conn,add_sid,add_bid,add_date)
        return redirect("/voyages")


    @bp.route("/sailors")
    def _get_all_sailors():
        with get_db() as conn:
            rows = sailors(conn)
        return render_template("table.html", name="Boats", rows=rows)

    @bp.route("/boats/by-popularity")
    def _get_pop_Boats():
        with get_db() as conn:
            rows = pop_Boats(conn)
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

    @bp.route("/sailors/who-sailed-on-date", methods=["POST"])
    def _get_dates():
        if request.method == "POST":
            v_date = request.form['date']
            with get_db() as conn:
                rows = which_date(conn, v_date)
            
            return render_template("table.html", rows=rows, name="Dates")

    
    @bp.route("/sailors/who-sailed-on-boat-of-color", methods=["POST"])
    def _get_colors():
        if request.method == "POST":
            b_color = request.form['color']
            with get_db() as conn:
                rows = which_color(conn, b_color)
            
            return render_template("table.html", rows=rows, name="Colors")

    
        