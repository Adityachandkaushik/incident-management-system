from flask import Blueprint, jsonify

routes_bp = Blueprint("routes", **name**)

@routes_bp.route("/health")
def health_check():

```
return jsonify({
    "status": "healthy",
    "message": "Incident Management System is running"
})
```
