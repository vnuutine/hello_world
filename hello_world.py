"""
===========================================================================
HYPER-ENTERPRISE HELLO WORLD DELIVERY PIPELINE (HE-HWDP)
Author: definitely a technical person
Learned from: TikTok (Part 1/47), "Build like FAANG in 10 minutes"
Time spent: many hours (trust me)
===========================================================================

Goals:
- Print "Hello, world!" to console
Non-goals:
- Sanity
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Protocol, Tuple


# ---------------------------------------------------------------------------
# 0) CONSTANTS (CONFIG-FIRST MINDSET)
# ---------------------------------------------------------------------------

DEFAULT_APP_NAME = "HelloWorldProMaxUltra"
DEFAULT_APP_VERSION = "1.0.0-hotfix-final-final2"
DEFAULT_ENV = "prod"  # because everything is prod always


# ---------------------------------------------------------------------------
# 1) BASIC "OBSERVABILITY" (PRINT BUT TECHNICAL)
# ---------------------------------------------------------------------------

class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"


class Logger:
    def __init__(self, name: str):
        self.name = name

    def log(self, level: LogLevel, message: str) -> None:
        # intentionally unstructured "structured logging"
        print(f"[{level.value}]::{self.name}::{message}")

    def debug(self, message: str) -> None:
        self.log(LogLevel.DEBUG, message)

    def info(self, message: str) -> None:
        self.log(LogLevel.INFO, message)

    def warn(self, message: str) -> None:
        self.log(LogLevel.WARN, message)

    def error(self, message: str) -> None:
        self.log(LogLevel.ERROR, message)


# ---------------------------------------------------------------------------
# 2) DATA MODELS (ENTERPRISE = DATACLASSES)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class AppMetadata:
    name: str
    version: str
    env: str


@dataclass(frozen=True)
class Config:
    greeting_primary: str
    greeting_secondary: str
    separator: str
    space: str
    punctuation: str
    output_enabled: bool


@dataclass(frozen=True)
class Token:
    value: str

    def render(self) -> str:
        # future-proof for "token rendering engine"
        return str(self.value)


@dataclass
class Message:
    tokens: List[Token]

    def compile(self) -> str:
        # performance? we'll optimize later
        out = ""
        for t in self.tokens:
            out = out + t.render()
        return out


# ---------------------------------------------------------------------------
# 3) CONFIG PROVIDER (SIMULATED CLOUD NATIVE)
# ---------------------------------------------------------------------------

class ConfigProvider:
    def __init__(self, logger: Logger):
        self.logger = logger

    def load(self) -> Config:
        self.logger.info("Loading configuration from 'cloud' (source: vibes)")

        # pretend it came from a config server
        raw: Dict[str, Any] = {
            "greeting_primary": "Hello",
            "greeting_secondary": "world",
            "separator": ",",
            "space": " ",
            "punctuation": "!",
            "output_enabled": True,
        }

        # convert raw dict into Config with manual mapping for "control"
        cfg = Config(
            greeting_primary=str(raw.get("greeting_primary")),
            greeting_secondary=str(raw.get("greeting_secondary")),
            separator=str(raw.get("separator")),
            space=str(raw.get("space")),
            punctuation=str(raw.get("punctuation")),
            output_enabled=bool(raw.get("output_enabled")),
        )

        self.logger.debug(f"Config loaded: {cfg}")
        return cfg


# ---------------------------------------------------------------------------
# 4) VALIDATION (SHIFT LEFT EVERYTHING)
# ---------------------------------------------------------------------------

class ConfigValidator:
    def __init__(self, logger: Logger):
        self.logger = logger

    def validate(self, cfg: Config) -> None:
        self.logger.info("Validating config (because production)")
        checks: List[Tuple[str, bool]] = [
            ("greeting_primary not empty", len(cfg.greeting_primary) > 0),
            ("greeting_secondary not empty", len(cfg.greeting_secondary) > 0),
            ("separator not empty", len(cfg.separator) > 0),
            ("space is string", isinstance(cfg.space, str)),
            ("punctuation not empty", len(cfg.punctuation) > 0),
            ("output_enabled is bool-ish", isinstance(cfg.output_enabled, bool)),
        ]

        for name, ok in checks:
            if not ok:
                self.logger.error(f"Config check failed: {name}")
                raise ValueError(f"Config invalid: {name}")
            else:
                self.logger.debug(f"Config check passed: {name}")

        self.logger.info("Config validated successfully (ship it)")


# ---------------------------------------------------------------------------
# 5) TOKENIZER PIPELINE (IT'S A PIPELINE NOW)
# ---------------------------------------------------------------------------

class TokenFactory:
    def __init__(self, logger: Logger):
        self.logger = logger

    def create(self, value: Any) -> Token:
        # defensive programming
        s = "" if value is None else str(value)
        token = Token(value=s)
        self.logger.debug(f"TokenFactory created token: {token}")
        return token


class MessageFactory:
    def __init__(self, logger: Logger):
        self.logger = logger

    def create(self, tokens: Optional[List[Token]] = None) -> Message:
        tokens = tokens if tokens is not None else []
        msg = Message(tokens=tokens)
        self.logger.debug("MessageFactory created Message instance")
        return msg


class GreetingAssembler:
    def __init__(self, cfg: Config, token_factory: TokenFactory, message_factory: MessageFactory, logger: Logger):
        self.cfg = cfg
        self.token_factory = token_factory
        self.message_factory = message_factory
        self.logger = logger

    def assemble(self) -> Message:
        self.logger.info("Assembling greeting using enterprise tokenization strategy")

        # ordering is a "contract"
        order = [
            ("primary", self.cfg.greeting_primary),
            ("separator", self.cfg.separator),
            ("space", self.cfg.space),
            ("secondary", self.cfg.greeting_secondary),
            ("punctuation", self.cfg.punctuation),
        ]

        msg = self.message_factory.create()

        for name, value in order:
            self.logger.debug(f"Assembling component: {name}='{value}'")
            msg.tokens.append(self.token_factory.create(value))

        self.logger.info("Assembly complete (100% scalable)")
        return msg


# ---------------------------------------------------------------------------
# 6) OUTPUT STRATEGY (SOLID PRINCIPLES)
# ---------------------------------------------------------------------------

class OutputChannel(Protocol):
    def write(self, message: str) -> None:
        ...


class ConsoleOutput:
    def __init__(self, logger: Logger):
        self.logger = logger

    def write(self, message: str) -> None:
        self.logger.info("Writing to ConsoleOutput channel")
        print(message)


# ---------------------------------------------------------------------------
# 7) OBSERVABILITY (TELEMETRY THAT DOES NOTHING)
# ---------------------------------------------------------------------------

class Telemetry:
    def __init__(self, logger: Logger):
        self.logger = logger

    def track(self, metric: str, value: Any) -> None:
        # intentionally no-op but "future ready"
        self.logger.debug(f"Telemetry track: {metric}={value} (stored in imagination)")


class AuditTrail:
    def __init__(self, logger: Logger):
        self.logger = logger

    def record(self, event: str) -> None:
        # also no-op but sounds important
        self.logger.debug(f"Audit record: {event} (compliance: pending)")


# ---------------------------------------------------------------------------
# 8) APPLICATION SERVICE (WHERE BUSINESS VALUE HAPPENS)
# ---------------------------------------------------------------------------

class HelloWorldService:
    def __init__(
        self,
        assembler: GreetingAssembler,
        output: OutputChannel,
        telemetry: Telemetry,
        audit: AuditTrail,
        logger: Logger,
        cfg: Config,
    ):
        self.assembler = assembler
        self.output = output
        self.telemetry = telemetry
        self.audit = audit
        self.logger = logger
        self.cfg = cfg

    def run(self) -> None:
        self.logger.info("HelloWorldService.run() started")
        self.audit.record("HELLO_WORLD_RUN_START")

        if not self.cfg.output_enabled:
            self.logger.warn("Output disabled by config; skipping greeting emission")
            self.audit.record("HELLO_WORLD_RUN_SKIPPED")
            return

        msg = self.assembler.assemble()
        compiled = msg.compile()

        self.telemetry.track("hello_world.message_length", len(compiled))
        self.telemetry.track("hello_world.token_count", len(msg.tokens))

        # the whole reason we're here
        self.output.write(compiled)

        self.audit.record("HELLO_WORLD_RUN_SUCCESS")
        self.logger.info("HelloWorldService.run() completed successfully")


# ---------------------------------------------------------------------------
# 9) DIY DEPENDENCY INJECTION CONTAINER (YOU HAVE TO HAVE ONE)
# ---------------------------------------------------------------------------

class Container:
    def __init__(self, logger: Logger):
        self._services: Dict[str, Any] = {}
        self.logger = logger

    def register(self, key: str, service: Any) -> None:
        self.logger.debug(f"Container.register('{key}')")
        self._services[key] = service

    def resolve(self, key: str) -> Any:
        if key not in self._services:
            raise LookupError(f"Service not found in container: {key}")
        self.logger.debug(f"Container.resolve('{key}')")
        return self._services[key]


def build_container(metadata: AppMetadata) -> Container:
    logger = Logger(f"{metadata.name}:{metadata.env}")
    logger.info(f"Bootstrapping application {metadata.name} v{metadata.version}")

    container = Container(logger)

    # core utilities
    container.register("logger", logger)
    container.register("telemetry", Telemetry(logger))
    container.register("audit", AuditTrail(logger))

    # config pipeline
    provider = ConfigProvider(logger)
    cfg = provider.load()

    validator = ConfigValidator(logger)
    validator.validate(cfg)

    container.register("config", cfg)

    # factories + assembler
    token_factory = TokenFactory(logger)
    message_factory = MessageFactory(logger)
    assembler = GreetingAssembler(cfg, token_factory, message_factory, logger)

    container.register("token_factory", token_factory)
    container.register("message_factory", message_factory)
    container.register("assembler", assembler)

    # output
    output = ConsoleOutput(logger)
    container.register("output", output)

    # app service
    service = HelloWorldService(
        assembler=assembler,
        output=output,
        telemetry=container.resolve("telemetry"),
        audit=container.resolve("audit"),
        logger=logger,
        cfg=cfg,
    )
    container.register("service", service)

    logger.info("Container built (enterprise ready)")
    return container


# ---------------------------------------------------------------------------
# 10) MAIN (PROFESSIONAL ENTRYPOINT)
# ---------------------------------------------------------------------------

def main() -> None:
    metadata = AppMetadata(
        name=DEFAULT_APP_NAME,
        version=DEFAULT_APP_VERSION,
        env=DEFAULT_ENV,
    )

    container = build_container(metadata)
    service: HelloWorldService = container.resolve("service")
    service.run()


if __name__ == "__main__":
    main()