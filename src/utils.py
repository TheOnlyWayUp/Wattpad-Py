from pydantic import BaseModel


def get_fields(model: BaseModel) -> list[str]:
    """Return fields of a model, preferring an alias if present."""
    attribs = []
    for name, field in model.model_fields.items():
        if field.alias:
            attribs.append(field.alias)
        else:
            attribs.append(name)
    return attribs
