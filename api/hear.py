import datetime
from uuid import uuid4

from flask import Blueprint, request, Response

from JsonResponse import JsonResponse
from .common import (
    Hear,
    User
)

# authenticate user

hear = Blueprint('hear', __name__)
