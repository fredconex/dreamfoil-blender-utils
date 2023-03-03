import bpy
import re
from bpy.props import *

# == GLOBAL VARIABLES
PROPS = [
    ('SearchFor', bpy.props.StringProperty(name='Search for', default='')),
    ('ReplaceWith', bpy.props.StringProperty(name='Replace with', default='')),
    ('ReplaceWithCaseSensitive', bpy.props.BoolProperty(name='Case Sensitve', default=True)),
    ('ReplaceSelected', bpy.props.BoolProperty(name='Selected Only', default=True)),
    ('ReplaceLights', bpy.props.BoolProperty(name='Lights', default=True)),
    ('ReplaceLightLevels', bpy.props.BoolProperty(name='Light Level', default=True)),
    ('ReplaceAnimations', bpy.props.BoolProperty(name='Dataref Path', default=True)),
    ('ReplaceManipulators', bpy.props.BoolProperty(name='Manipulators', default=True)),
]

def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):

    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)


def replace_dataref(pattern, repl, string):
    if bpy.context.scene.ReplaceWithCaseSensitive:
        replaced = re.sub(pattern, repl, string)
    else:
        replaced = re.sub(pattern, repl, string, flags=re.IGNORECASE)
    return replaced != string, replaced, string
   
class ReplaceDataref_Operator(bpy.types.Operator):
    bl_idname = "object.replacedataref_operator"
    bl_label = "Dataref Replace"
    SearchFor: bpy.props.BoolProperty(name="Search For")
    
    def execute(self, context):
        scene = context.scene
        ReplacedCount = 0
        selected = []
        replaced = []
        #selected.append(bpy.context.active_object.name)
        if scene.ReplaceSelected == True:
            for obj in bpy.data.objects:
                if obj.select_get() == True:
                    selected.append(obj.data.name)
        else:
            for obj in bpy.data.objects:
                selected.append(obj.name)
        
        print("Searching Datarefs")    
        ## Animations ##
        if scene.ReplaceAnimations == True:
            for obj in bpy.data.objects:
                if (obj.name in selected):
                    for dref in obj.xplane.datarefs:
                        replaced = replace_dataref(scene.SearchFor, scene.ReplaceWith, dref.path)
                        if replaced[0] == True:  
                            dref.path = replaced[1]                      
                            ReplacedCount = ReplacedCount+1
                            print("  Animation: @"+ obj.name + " replaced: '" + replaced[2]+ "' with '" + replaced[1]+"'")
                            
        ## Lights ##
        if scene.ReplaceLights == True:
            for obj in bpy.data.lights:
                if (obj.name in selected):
                    print(obj.xplane.dataref)
                    replaced = replace_dataref(scene.SearchFor, scene.ReplaceWith, obj.xplane.dataref)
                    if replaced[0] == True:  
                        obj.xplane.dataref = replaced[1]                      
                        ReplacedCount = ReplacedCount+1
                        print("  Light: @"+ obj.name + " replaced: '" + replaced[2] + "' with '" + replaced[1]+"'")

  
        ## Light Levels ##
        if scene.ReplaceLightLevels == True:
            for obj in bpy.context.scene.objects:
                if (obj.name in selected):
                    replaced = replace_dataref(scene.SearchFor, scene.ReplaceWith, obj.xplane.lightLevel_dataref)
                    if replaced[0] == True:
                        obj.xplane.lightLevel_dataref = replaced[1]
                        ReplacedCount = ReplacedCount+1
                        print("  Light Level: @"+ obj.name + " replaced: '" + replaced[2] + "' with '" + replaced[1]+"'")
                        
        ## Manipulators ##
        if scene.ReplaceManipulators == True:
            for obj in bpy.context.scene.objects:
                if (obj.name in selected):
                    replaced = replace_dataref(scene.SearchFor, scene.ReplaceWith, obj.xplane.manip.dataref1)
                    if replaced[0] == True:
                        obj.xplane.manip.dataref1 = replaced[1]
                        ReplacedCount = ReplacedCount+1
                        print("  Manipulator Dataref1: @"+ obj.name + " replaced: '" + replaced[2] + "' with '" + replaced[1]+"'")

                    replaced = replace_dataref(scene.SearchFor, scene.ReplaceWith, obj.xplane.manip.dataref2)
                    if replaced[0] == True:
                        obj.xplane.manip.dataref2 = replaced[1]
                        ReplacedCount = ReplacedCount+1
                        print("  Manipulator Dataref2: @"+ obj.name + " replaced: '" + replaced[2] + "' with '" + replaced[1]+"'")

                    replaced = replace_dataref(scene.SearchFor, scene.ReplaceWith, obj.xplane.manip.command)
                    if replaced[0] == True:
                        obj.xplane.manip.command = replaced[1]
                        ReplacedCount = ReplacedCount+1
                        print("  Manipulator Command: @"+ obj.name + " replaced: '" + replaced[2] + "' with '" + replaced[1]+"'")

                    replaced = replace_dataref(scene.SearchFor, scene.ReplaceWith, obj.xplane.manip.positive_command)
                    if replaced[0] == True:
                        obj.xplane.manip.positive_command = replaced[1]
                        ReplacedCount = ReplacedCount+1
                        print("  Manipulator Positive_cmnd: @"+ obj.name + " replaced: '" + replaced[2] + "' with '" + replaced[1]+"'")

                    replaced = replace_dataref(scene.SearchFor, scene.ReplaceWith, obj.xplane.manip.negative_command)
                    if replaced[0] == True:
                        obj.xplane.manip.negative_command = replaced[1]
                        ReplacedCount = ReplacedCount+1
                        print("  Manipulator Negative_cmnd: @"+ obj.name + " replaced: '" + replaced[2] + "' with '" + replaced[1]+"'")

        print("Search finished.")
        ShowMessageBox(str(ReplacedCount), "Total Replaced")
        return {'FINISHED'}
    
class Dreamfoil_Utils(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Dreamfoil Utils - Dataref Replace"
    bl_idname = "SCENE_PT_DFUtils"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.label(text="Dataref Replace:")
        row = layout.row()
        row.prop(scene, "SearchFor")
        row = layout.row()
        row.prop(scene, "ReplaceWith")
        row = layout.row()
        row.prop(scene, "ReplaceWithCaseSensitive")
        row.prop(scene, "ReplaceSelected")
        
        layout.label(text="Types:")
        row = layout.row()
        row.prop(scene, "ReplaceAnimations")
        row.prop(scene, "ReplaceManipulators")
        row.prop(scene, "ReplaceLights")
        row.prop(scene, "ReplaceLightLevels")
        row = layout.row()
        if scene.ReplaceManipulators or scene.ReplaceAnimations or scene.ReplaceLights or scene.ReplaceLightLevels:
            row.operator("object.replacedataref_operator", text="Replace")
        else:
            row.enabled = False
            row.operator("object.replacedataref_operator", text="Please select a type above")

def register():
    for (prop_name, prop_value) in PROPS:
        setattr(bpy.types.Scene, prop_name, prop_value)
    bpy.utils.register_class(ReplaceDataref_Operator)
    bpy.utils.register_class(Dreamfoil_Utils)

def unregister():
    bpy.utils.unregister_class(ReplaceDataref_Operator)
    bpy.utils.unregister_class(Dreamfoil_Utils)


if __name__ == "__main__":
    register()