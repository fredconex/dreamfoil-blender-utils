from bpy import *
import bpy
from bpy.props import StringProperty

Datarefs = []

## Enable All Animations ##
class DisableAnims(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "scene.disable_anims"
    bl_label = "Disable ALL"

    dataref : StringProperty(default="")

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        print(self.dataref)
        for obj in bpy.context.scene.objects:
            if obj.animation_data and obj.animation_data.action and obj.animation_data.action.fcurves:
                for fcurve in obj.animation_data.action.fcurves:
                    print(f"{obj.name}")
                    print(fcurve.mute)
                    fcurve.mute = True
        return {'FINISHED'}

## Disable All Animations ##
class EnableAnims(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "scene.enable_anims"
    bl_label = "Enable ALL"

    dataref : StringProperty(default="")

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        print(self.dataref)
        for obj in bpy.context.scene.objects:
            if obj.animation_data and obj.animation_data.action and obj.animation_data.action.fcurves:
                for fcurve in obj.animation_data.action.fcurves:
                    print(f"{obj.name}")
                    print(fcurve.mute)
                    fcurve.mute = False
        return {'FINISHED'}

## Disable Dataref ##
class MuteDataref(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "scene.mute_anim"
    bl_label = "ON"

    dataref : StringProperty(default="")

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        print(self.dataref)
        for obj in bpy.context.scene.objects:
            if obj.animation_data and obj.animation_data.action and obj.animation_data.action.fcurves:
                if obj.xplane.datarefs:
                    for dref in obj.xplane.datarefs:
                        if dref.path == self.dataref:
                            for fcurve in obj.animation_data.action.fcurves:
                                print(f"{obj.name}")
                                print(fcurve.mute)
                                fcurve.mute = fcurve.mute = True
        return {'FINISHED'}

## Enable Dataref ##
class UnMuteDataref(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "scene.unmute_anim"
    bl_label = "OFF"

    dataref : StringProperty(default="")

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        print(self.dataref)
        for obj in bpy.context.scene.objects:
            if obj.animation_data and obj.animation_data.action and obj.animation_data.action.fcurves:
                if obj.xplane.datarefs:
                    for dref in obj.xplane.datarefs:
                        if dref.path == self.dataref:
                            for fcurve in obj.animation_data.action.fcurves:
                                print(f"{obj.name}")
                                print(fcurve.mute)
                                fcurve.mute = fcurve.mute = False
        return {'FINISHED'}

## Select ##
class SelectAnim(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "scene.select_animdref"
    bl_label = "Select"

    dataref : StringProperty(default="")
    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        for obj in bpy.context.scene.objects:
            if obj.animation_data and obj.animation_data.action and obj.animation_data.action.fcurves:
                if obj.xplane.datarefs:
                    for dref in obj.xplane.datarefs:
                        if dref.path == self.dataref:
                            for fcurve in obj.animation_data.action.fcurves:
                                obj.select_set(True)
        return {'FINISHED'}

def isMuted(dataref):
    Mt = False
    for obj in bpy.context.scene.objects:
            if obj.animation_data and obj.animation_data.action and obj.animation_data.action.fcurves:
                hasDataref = False
                if obj.xplane.datarefs:
                    for dref in obj.xplane.datarefs:
                        if dref.path == dataref:
                            for fcurve in obj.animation_data.action.fcurves:
                                if fcurve.mute == True:
                                    Mt = True
    return Mt
    
class AnimDatarefsPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Dreamfoil Utils - Dataref Animations"
    bl_idname = "SCENE_PT_DFDatarefAnims"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout

        scene = context.scene

        # Create a simple row.
        #layout.label(text=" Datarefs used:")
        
        Datarefs = []
        for obj in bpy.context.scene.objects:
            for dref in obj.xplane.datarefs:
                if (not dref.path in Datarefs) and (dref.path != "") and (dref.anim_type == "transform"):
                 Datarefs.append(dref.path)
        Datarefs.sort()

        row = layout.row()
        row.operator("scene.enable_anims")
        row.operator("scene.disable_anims")
        row.operator("object.export_datarefs")

        for dref in Datarefs:
            row = layout.row()
            row.label(text=dref)
            row.scale_x = 0.2
            row.operator("scene.select_animdref").dataref = dref
            if isMuted(dref) == False:
                row.operator("scene.mute_anim").dataref = dref
            else:
                row.operator("scene.unmute_anim").dataref = dref


def register():
    bpy.utils.register_class(MuteDataref)
    bpy.utils.register_class(UnMuteDataref)
    bpy.utils.register_class(DisableAnims)
    bpy.utils.register_class(EnableAnims)
    bpy.utils.register_class(SelectAnim)
    bpy.utils.register_class(AnimDatarefsPanel)


def unregister():
    bpy.utils.unregister_class(MuteDataref)
    bpy.utils.unregister_class(unMuteDataref)
    bpy.utils.unregister_class(DisableAnims)
    bpy.utils.unregister_class(EnableAnims)
    bpy.utils.unregister_class(SelectAnim)
    bpy.utils.unregister_class(AnimDatarefsPanel)


if __name__ == "__main__":
    register()