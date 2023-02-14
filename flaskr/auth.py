# @Time     : 2023/2/13 22:35
# @Author   : CN-LanBao
import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():
    if "POST" == request.method:
        username, password = request.form["username"], request.form["username"]
        db = get_db()
        error = None

        if not username:
            error = "Username is required"
        elif not password:
            error = "Password is required"
        elif db.execute(
            "SELECT id FROM user WHERE username = ?", (username,)
        ).fetchone() is not None:
            error = "User {} is already register.".format(username)

        if error is None:
            db.execute("INSERT INTO user (username, password) VALUES (?, ?)", (username, generate_password_hash(password)))
            db.commit()
            return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if "POST" == request.method:
        username, password = request.form["username"], request.form["password"]
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()

        if user is None:
            error = "Incorrect username"
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password"

        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    g.user = None if user_id is None else get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,))


def login_required(view):
    @functools.wraps(view)
    def wrapper(**kwargs):
        return redirect(url_for("auth.login")) if g.user is None else view(**kwargs)
    return wrapper
