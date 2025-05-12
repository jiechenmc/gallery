import pyroscope

from app.routers import users
from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# pyroscope.configure(
#   application_name = "pytel", # replace this with some name for your application
#   server_address   = "http://pyroscope:4040", # replace this with the address of your Pyroscope server
# )

app = FastAPI()
app.include_router(users)

resource = Resource(attributes={
    "service.name": "fastapi-service"
})

provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)

otlp_exporter = OTLPSpanExporter()

span_processor = BatchSpanProcessor(otlp_exporter)
provider.add_span_processor(span_processor)

FastAPIInstrumentor.instrument_app(app)
