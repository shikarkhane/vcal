# Run a test server.
import os
os.environ["TZ"] = "UTC"
from app import app
print app.url_map
app.run(host='127.0.0.1', port=8080, debug=True, threaded=True)