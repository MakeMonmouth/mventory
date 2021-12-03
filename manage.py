#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
    )
from opentelemetry.propagate import set_global_textmap
from opentelemetry.propagators.b3 import B3MultiFormat



def main():
    set_global_textmap(B3MultiFormat())
    resource = Resource(attributes={
        "service.name": "mventory",
        "environment": "dev"
    })
    
    trace.set_tracer_provider(TracerProvider(resource=resource))
    tracer = trace.get_tracer(__name__)
    
    otlp_exporter = OTLPSpanExporter(endpoint="https://otlphttp.service.wallace.network/v1/traces")
    
    span_processor = BatchSpanProcessor(otlp_exporter)
    
    trace.get_tracer_provider().add_span_processor(span_processor)

    DjangoInstrumentor().instrument()
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mventory.settings')
    os.environ.setdefault("OPENTELEMETRY_PYTHON_DJANGO_INSTRUMENT", "True")
    LoggingInstrumentor().instrument(set_logging_format=True)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
