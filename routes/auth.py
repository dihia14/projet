from flask import Blueprint, request, session, redirect, url_for, render_template
from managers.database_manager import UserDatabase

auth_blueprint = Blueprint("auth", __name__)
db_manager = UserDatabase()

@auth_blueprint.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    user = db_manager.get_user(username)

    if user:
        session["username"] = username
        session["is_admin"] = user[4]
        return redirect(url_for("admin.admin_dashboard", username=username)) if user[4] else redirect(url_for("user.profile", username=username))
    else:
        return redirect(url_for("auth.login", error="Invalid credentials"))
