from elasticapm.contrib.flask import ElasticAPM
from flask import Flask
import os
import time
import random
import logging
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['ELASTIC_APM'] = {
    'SERVICE_NAME': 'log-generator',
    'SERVER_URL': os.getenv('ELASTIC_APM_SERVER_URL'),
    'SECRET_TOKEN': os.getenv('ELASTIC_APM_SECRET_TOKEN'),
    'ENVIRONMENT': os.getenv('NODE_ENV', 'development'),
    'DEBUG': True,
    'LOG_LEVEL': 'debug',
}

apm = ElasticAPM(app)

print(f"APM Configuration:")
print(f"  Server URL: {os.getenv('ELASTIC_APM_SERVER_URL')}")
print(f"  Service Name: log-generator")
print(f"  Environment: {os.getenv('NODE_ENV', 'development')}")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def home():
    logger.info('Home endpoint accessed')
    return {'status': 'running', 'service': 'log-generator'}

@app.route('/generate-logs')
def generate_logs():
    log_types = ['INFO', 'WARN', 'ERROR']
    log_type = random.choice(log_types)

    if log_type == 'INFO':
        logger.info(f'Generated INFO log at {time.time()}')
    elif log_type == 'WARN':
        logger.warning(f'Generated WARNING log at {time.time()}')
    else:
        logger.error(f'Generated ERROR log at {time.time()}')

    time.sleep(random.uniform(0.1, 0.5))

    return {'log_type': log_type, 'timestamp': time.time()}

@app.route('/simulate-error')
def simulate_error():
    logger.error('Simulated error endpoint called')
    raise Exception('This is a simulated error for APM testing')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
