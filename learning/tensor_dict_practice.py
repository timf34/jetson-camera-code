import json
import torch
from torch import Tensor as Tensor

# We have a dict where some values are Tensors, and some are not. We want to be able to convert the dict to a JSON string to save it to a file

# Create a dict with some Tensors and some non-Tensors

# First create some Tensors of different shapes 
t1 = torch.tensor([1, 2, 3])
t2 = torch.tensor([[1, 2, 3], [4, 5, 6]])
# Now using torch.rand
t3 = torch.rand(3, 3)

# Now create a dict with some Tensors and some non-Tensors
dict1 = {"t1": t1, "t2": t2, "t3": t3, "not_tensor": "Hello World!"}

# Now prepare to convert the dict to a JSON string, converting the tensors to serializable objects
# json_dict = {}
# for key, value in dict1.items():
#     if isinstance(value, Tensor):
#         json_dict[key] = value.tolist()
#     else:
#         json_dict[key] = value

# Now rewrite the above, but faster and more efficient
json_dict = {key: value.tolist() if isinstance(value, Tensor) else value for key, value in dict1.items()}

# Now convert the dict to a JSON string
json_string = json.dumps(json_dict)

# Now save the JSON string to a file
with open("json_dict.json", "w") as f:
    f.write(json_string)
