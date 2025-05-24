import json
import os
from django.conf import settings


def populate_from_json(model, json_path, data_key, item_processor):
    json_file = os.path.join(settings.BASE_DIR, json_path)
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
            items = data.get(data_key, [])
            for item in items:
                kwargs = item_processor(item)
                model.objects.get_or_create(**kwargs)
    except FileNotFoundError:
        print(f"Archivo no encontrado: {json_file}")
    except json.JSONDecodeError:
        print(f"Formato JSON inválido: {json_file}")

