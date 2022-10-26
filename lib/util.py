import base64
import numpy as np

# TODO Do we stil use these?
def ndarray_to_json(ndarray):
    return {
        "shape": ndarray.shape,
        "type": str(ndarray.dtype),
        "bytes": base64.b64encode(ndarray.tobytes()).decode("utf-8"),
    }


def ndarray_from_json(json):
    return np.frombuffer(base64.b64decode(json["bytes"]), dtype=json["type"]).reshape(
        json["shape"]
    )
