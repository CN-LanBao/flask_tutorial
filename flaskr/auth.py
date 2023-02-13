# @Time     : 2023/2/13 22:35
# @Author   : CN-LanBao
import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db


bp = Blueprint("auth", __name__, url_prefix="/auth")
