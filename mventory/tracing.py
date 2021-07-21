from logging import getLogger
from pkg_resources import iter_entry_points

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
)

logger = getLogger(__file__)

initialized = False

def init_tracing():
  global initialized
  if initialized:
    return
  initialized = True

  provider = TracerProvider()
  trace.set_tracer_provider(provider)

  provider.add_span_processor(BatchExportSpanProcessor(ConsoleSpanExporter()))
  auto_instrument()


# function should be provided out of box as `opentelemetry.instrumentation.auto_instrumentation.auto_instrument`
def auto_instrument():
  for entry_point in iter_entry_points("opentelemetry_instrumentor"):
      try:
          entry_point.load()().instrument()
      except Exception: 
          logger.exception("Instrumenting of %s failed", entry_point.name)
