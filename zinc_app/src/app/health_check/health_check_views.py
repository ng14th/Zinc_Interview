from datetime import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.db import connections, DatabaseError, OperationalError
from django.db.utils import ConnectionDoesNotExist
from rest_framework.response import Response
from datetime import datetime


def get_health_check_view():
    @api_view(['GET'])
    @permission_classes([AllowAny])
    def api_health_check_view(request):

        try:
            default_conn = connections['default']
            cursor = default_conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()

            return Response(
                {
                    "status": "ok",
                    "database": "reachable",
                    "time": datetime.now().isoformat(),
                },
                status=200
            )

        except (ConnectionDoesNotExist, OperationalError, DatabaseError) as e:
            return Response(
                {
                    "status": "not ok",
                    "database": "unreachable",
                    "error": str(e),
                    "time": datetime.now().isoformat(),
                },
                status=500
            )
    return api_health_check_view
