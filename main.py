from flask import Flask, request, send_file
from spyne import Application, rpc, ServiceBase, Float
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from werkzeug.middleware.dispatcher import DispatcherMiddleware

app = Flask(__name__)

# Define the SOAP service
class CalculatorService(ServiceBase):
    @rpc(Float, Float, _returns=Float)
    def add(ctx, a, b):
        return a + b

    @rpc(Float, Float, _returns=Float)
    def subtract(ctx, a, b):
        return a - b

    @rpc(Float, Float, _returns=Float)
    def multiply(ctx, a, b):
        return a * b

    @rpc(Float, Float, _returns=Float)
    def divide(ctx, a, b):
        return a / b if b != 0 else 'Division by zero error'

# Create the Spyne application
soap_app = Application(
    [CalculatorService],
    tns='http://example.com/calculator',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

# Wrap the Spyne application in WSGI and Flask
wsgi_app = WsgiApplication(soap_app)
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {'/soap': wsgi_app})

# Route to serve the static WSDL file
@app.route('/calculator.wsdl')
def serve_wsdl():
    return send_file('calculator.wsdl', mimetype='text/xml')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
