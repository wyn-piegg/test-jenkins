# -*- coding: UTF-8 -*-

import json
import codecs


def main():
    config = {}
    with codecs.open("config.json", "r", "utf-8") as f:
        config = json.loads(f.read())
    if not config:
        return

    s = ""
    template = config.get("template_file", "templatecpp.txt")
    with codecs.open(template, "r", "utf-8") as f:
        s = f.read()
    if not s:
        return

    s = s % config

    file = config["file_name"]
    with codecs.open(file, "w", "utf-8") as f:
        f.write(s)
        f.flush()


if __name__ == '__main__':
    main()