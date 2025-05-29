import re
from json import loads

from loguru import logger


class RSCParser:
    @staticmethod
    def parse(text: str) -> dict:
        try:
            text = text.encode('latin-1').decode('utf-8')
        except UnicodeEncodeError as e:
            pass
        finally:
            text = text.replace('\xa0', ' ')
        decode_text = text.replace('1:{"data":[{"data":{"title"', '\n1:{"data":[{"data":{"title"')
        pattern = re.compile(
            r'(?P<key>[a-zA-Z0-9]+):'                           # Именованная группа "key"
            r'(?:[a-zA-Z0-9]+,)?'                               # Опциональный доп. ключ (не захватывается)
            r'(?P<content>.*(?:\n(?!\s*[a-zA-Z0-9]+:).*)*)'     # Именованная группа "content"
        )
        results = {}
        for m in pattern.finditer(decode_text):
            key = m.group('key')
            content = RSCParser._try_parse_json(m.group('content'))
            results[key] = content
        for key, value in results.items():
            if isinstance(value, dict):
                results[key] = RSCParser._try_inject_placeholder(value, results)
        return results

    @staticmethod
    def _try_parse_json(json: str) -> dict | str:
        try:
            return loads(json)
        except Exception as e:
            return json

    @staticmethod
    def _try_inject_placeholder(json: dict, placeholders: dict[str, str]) -> dict:
        for key, value in json.items():
            if isinstance(value, list):
                json[key] = [RSCParser._try_inject_placeholder(e, placeholders) for e in value]
            elif isinstance(value, dict):
                json[key] = RSCParser._try_inject_placeholder(value, placeholders)
            elif isinstance(value, str) and len(value) != 0 and value[0] == "$":
                placeholder = value[1:]
                if placeholder not in placeholders:
                    logger.warning(f"SKIP UNKNOWN PLACEHOLDER - {placeholder}")
                else:
                    json[key] = placeholders[placeholder]
        return json

