from hello_world import (
    Config,
    GreetingAssembler,
    TokenFactory,
    MessageFactory,
    Logger,
    HelloWorldService,
)

class CapturingOutput:
    def __init__(self):
        self.writes = []

    def write(self, message: str) -> None:
        self.writes.append(message)

class CapturingTelemetry:
    def __init__(self):
        self.metrics = []

    def track(self, metric: str, value):
        self.metrics.append((metric, value))

class CapturingAudit:
    def __init__(self):
        self.events = []

    def record(self, event: str) -> None:
        self.events.append(event)

def test_service_writes_output_when_enabled():
    cfg = Config("Hello", "world", ",", " ", "!", True)
    logger = Logger("test")

    assembler = GreetingAssembler(cfg, TokenFactory(logger), MessageFactory(logger), logger)
    output = CapturingOutput()
    telemetry = CapturingTelemetry()
    audit = CapturingAudit()

    svc = HelloWorldService(assembler, output, telemetry, audit, logger, cfg)
    svc.run()

    assert output.writes == ["Hello, world!"]
    assert ("hello_world.message_length", len("Hello, world!")) in telemetry.metrics
    assert ("hello_world.token_count", 5) in telemetry.metrics
    assert "HELLO_WORLD_RUN_SUCCESS" in audit.events

def test_service_does_not_write_output_when_disabled():
    cfg = Config("Hello", "world", ",", " ", "!", False)
    logger = Logger("test")

    assembler = GreetingAssembler(cfg, TokenFactory(logger), MessageFactory(logger), logger)
    output = CapturingOutput()
    telemetry = CapturingTelemetry()
    audit = CapturingAudit()

    svc = HelloWorldService(assembler, output, telemetry, audit, logger, cfg)
    svc.run()

    assert output.writes == []
    assert "HELLO_WORLD_RUN_SKIPPED" in audit.events