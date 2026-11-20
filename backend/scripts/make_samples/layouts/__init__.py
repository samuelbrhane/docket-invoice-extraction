from scripts.make_samples.layouts import altura, bruno, energia, imballi, pulito, speedline

RENDERERS = {
    "altura": altura.render,
    "bruno": bruno.render,
    "energia": energia.render,
    "imballi": imballi.render,
    "pulito": pulito.render,
    "speedline": speedline.render,
}

__all__ = ["RENDERERS"]