from flask import Flask, jsonify, request
from scapy.all import IP, ICMP, sr1

app = Flask(__name__)

# For health checks
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"})

@app.route('/api/ping', methods=['GET'])
def api_ping():
    # Required parameter: IP (string)
    ip = request.args.get('IP')
    if ip is None:
        return jsonify('None'), 503, {'Content-Type': 'text/plain;charset=UTF-8'}
    count = request.args.get('count', type=int, default=4)
    timeout = request.args.get('timeout', type=int, default=1)
    data = request.args.get('data', type=int, default=56)

    # Log the parameters
    #log_message = f"IP: {ip}, Count: {count}, Timeout: {timeout}, Data: {data}"
    #app.logger.info(log_message)

    try:
        for i in range(count):
            print(i)
            icmp_packet = IP(dst=ip) / ICMP() / ('P' * data)
            response = sr1(icmp_packet, timeout=timeout, verbose=False)
            return jsonify({'status':'success','response': response.summary()}), 200, {'Content-Type': 'text/plain;charset=UTF-8'}
    
    except Exception as e:
        return jsonify('None'), 503, {'Content-Type': 'text/plain;charset=UTF-8'}


# Ping route
@app.route('/ping', methods=['GET'])
def ping():
    return "Pong"

if __name__ == '__main__':
    app.run(debug=True)
