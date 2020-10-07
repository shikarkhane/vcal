
import os
import json

from base import create_app

#if 'SERVERTYPE' in os.environ and os.environ['SERVERTYPE'] == 'AWS Lambda':

json_data = open('zappa_settings.json')
#env_vars = json.load(json_data)['demo']['environment_variables']
env_vars = {"TZ": "UTC"}
for key, val in env_vars.items():
    os.environ[key] = val

app = create_app()


# if __name__ == "__main__":
#     app.run(debug=True, host='127.0.0.1', port=int(os.environ.get('PORT', 8080)))

from base.common.jobs import weekly_reminder

weekly_reminder()