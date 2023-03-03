import bpy

# Contains informations for Blender to recognize and categorize the addon.
bl_info = {
    "name": "Dreamfoil Utils: X-Plane",
    "description": "Some utilities for X-Plane",
    "author": "Alfredo Fernandes, Dreamfoil Creations",
    "version": (0, 1, 8),
    "blender": (2, 80, 0),
    "warning": "",
    "category": "Object",
}
if "" not in locals():
    from . import dreamfoil_dataref_replace
    from . import dreamfoil_animations
    from . import dreamfoil_export_datarefs
else:
    import importlib
    dreamfoil_dataref_replace = importlib.reload(dreamfoil_dataref_replace)
    dreamfoil_animations = importlib.reload(dreamfoil_animations)
    dreamfoil_export_datarefs = importlib.reload(dreamfoil_export_datarefs)


# Function: register
# Registers the addon with all its classes and the menu function.
def register():
    dreamfoil_export_datarefs.register()
    dreamfoil_dataref_replace.register()
    dreamfoil_animations.register()

# Function: unregister
# Unregisters the addon and all its classes and removes the entry from the menu.
def unregister():
    dreamfoil_export_datarefs.unregister()
    dreamfoil_dataref_replace.unregister()
    dreamfoil_animations.unregister()


if __name__ == "__main__":
    register()
