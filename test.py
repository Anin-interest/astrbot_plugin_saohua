from pathlib import Path

import yaml

with open(Path(__file__).parent / "resources/reply.yaml", "r", encoding="utf-8") as f:
    data :dict = yaml.safe_load(f)

    print(data.keys())


    f.close()

