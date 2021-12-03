"""
WSGI config for mventory project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
import socket

from opentelemetry.instrumentation.wsgi import OpenTelemetryMiddleware
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.mysql import MySQLInstrumentor
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
    )
resource = Resource(attributes={
    "service.name": "mventory",
    "environment": "dev",
    "host": socket.gethostname()
})

trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

otlp_exporter = OTLPSpanExporter(endpoint=f"{os.getenv('OTEL_EXPORTER_OTLP_ENDPOINT')}/v1/traces")

span_processor = BatchSpanProcessor(otlp_exporter)

trace.get_tracer_provider().add_span_processor(span_processor)

def request_hook(span, request):
    print(f"Request: {span.context}")

def response_hook(span, request, response):
    print(f"Response: {span.context}")



from django.core.wsgi import get_wsgi_application
DjangoInstrumentor().instrument(request_hook=request_hook, response_hook=response_hook)
LoggingInstrumentor().instrument(set_logging_format=True)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mventory.settings')

application = get_wsgi_application()
application = OpenTelemetryMiddleware(application)

