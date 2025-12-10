from observability.logger import log_json
import json


def test_structured_log_format(capsys):
    log_json("test_event", level="INFO", key="value")

    out = capsys.readouterr().out.strip()
    parsed = json.loads(out)

    assert parsed["event"] == "test_event"
    assert parsed["level"] == "INFO"
    assert parsed["key"] == "value"
    assert "timestamp" in parsed
