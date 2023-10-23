from flask import Flask, jsonify, request, make_response
from scapy.all import IP, ICMP, sr1
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=['1/second'],
    storage_uri="memory://",
    )

@app.errorhandler(429)
def ratelimit_handler(e):
    return make_response(
            jsonify("None"),
            503,
            {'Content-Type': 'text/plain;charset=UTF-8'}
    )

# For health checks
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"})

#@limiter.limit("1/minute") 
@app.route('/api/ping', methods=['GET'])
def api_ping():
    
    app.logger.info( f"=======================")
    
    ip = request.args.get('IP')
    if ip is None:
        return jsonify('None'), 503, {'Content-Type': 'text/plain;charset=UTF-8'}
    count = request.args.get('count', type=int, default=1)
    timeout = request.args.get('timeout', type=int, default=1)
    data = request.args.get('data', type=int, default=56)

    # Log the parameters
    log_message = f" Request received - IP: {ip}, Count: {count}, Timeout: {timeout}, Data: {data}"
    app.logger.info(log_message)

    num_recieved = 0

    for i in range(count) :
        try:
            icmp_packet = IP(dst=ip) / ICMP() / ('P' * data)
            res = sr1(icmp_packet, timeout=timeout, verbose=False)
            num_recieved+=1 
            app.logger.info( f"sr num {i+1}: {res}")

        except Exception as e:
            app.logger.error( f"ERROR in scapy library: {e}")

    res = {'status':'success','sent': count, 'received': num_recieved}
    app.logger.info(f"Response send: {res}")
    return jsonify(res), 200, {'Content-Type': 'text/plain;charset=UTF-8'}


# Ping route
@app.route('/ping', methods=['GET'])
def ping():
    return "Pong"


if __name__ == '__main__':
    app.run(debug=True)
