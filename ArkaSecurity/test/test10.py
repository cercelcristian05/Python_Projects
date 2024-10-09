import torchvision.models as models

# Get a list of available model names in torchvision
model_names = [name for name in dir(models) if name.islower() and not name.startswith("__")]

# Print the available models
print("Available PyTorch Models:")
for name in model_names:
    print(f"- {name}")
