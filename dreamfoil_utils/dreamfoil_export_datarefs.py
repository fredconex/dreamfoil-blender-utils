import bpy
import bpy
import os

from bpy.props import StringProperty, BoolProperty
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator

Datarefs = []

def GetDatarefsIdx(name):
    Index = -1
    for x in range(len(Datarefs)):
        dref = Datarefs[x]
        if dref[0] == name:
            Index = x
    return Index
        
def GetMinMaxValue(obj):
    for drefidx, dref in enumerate(obj.xplane.datarefs):
        if Datarefs[GetDatarefsIdx(dref.path)][1] is None or dref.show_hide_v1 < Datarefs[GetDatarefsIdx(dref.path)][1]:
            Datarefs[GetDatarefsIdx(dref.path)][1] = dref.show_hide_v1
        if Datarefs[GetDatarefsIdx(dref.path)][2] is None or dref.show_hide_v1 > Datarefs[GetDatarefsIdx(dref.path)][2]:
            Datarefs[GetDatarefsIdx(dref.path)][2] = dref.show_hide_v1
        if Datarefs[GetDatarefsIdx(dref.path)][1] is None or dref.show_hide_v2 < Datarefs[GetDatarefsIdx(dref.path)][1]:
            Datarefs[GetDatarefsIdx(dref.path)][1] = dref.show_hide_v2
        if Datarefs[GetDatarefsIdx(dref.path)][2] is None or dref.show_hide_v2 > Datarefs[GetDatarefsIdx(dref.path)][2]:
            Datarefs[GetDatarefsIdx(dref.path)][2] = dref.show_hide_v2

      
    if obj.animation_data is not None:
        action = obj.animation_data.action
        if action and action.fcurves is not None:
            for fcu in action.fcurves:
                for drefidx, dref in enumerate(obj.xplane.datarefs):
                    if "xplane.datarefs["+str(drefidx)+"]" in fcu.data_path:
                        for keyframe in fcu.keyframe_points:
                            if Datarefs[GetDatarefsIdx(dref.path)][1] is None or keyframe.co[1] < Datarefs[GetDatarefsIdx(dref.path)][1]:
                                Datarefs[GetDatarefsIdx(dref.path)][1] = keyframe.co[1]
                            if Datarefs[GetDatarefsIdx(dref.path)][2] is None or keyframe.co[1] > Datarefs[GetDatarefsIdx(dref.path)][2]:
                                Datarefs[GetDatarefsIdx(dref.path)][2] = keyframe.co[1]

class OT_TestOpenFilebrowser(Operator, ImportHelper):

    bl_idname = "object.export_datarefs"
    bl_label = "Export Datarefs"
   
    # ImportHelper mixin class uses this
    filename_ext = ".txt"    
   
    filter_glob: StringProperty(
        default='*.txt',
        options={'HIDDEN'}
    )
    
    some_boolean: BoolProperty(
        name='Do a thing',
        description='Do a thing with the file you\'ve selected',
        default=True,
    )

    def execute(self, context):
        filename, extension = os.path.splitext(self.filepath)
        
        ## Animation ##
        for obj in bpy.context.scene.objects:
            for dref in obj.xplane.datarefs:
                if (GetDatarefsIdx(dref.path) == -1) and (dref.path != ""):
                    D = [dref.path, None, None, dref.anim_type]
                    Datarefs.append(D)
        Datarefs.sort()
        
        for obj in bpy.context.scene.objects:
            GetMinMaxValue(obj)
            
        f = open(self.filepath, "w")
        print('####### Animations - Dataref Min Max Type', file=f)
        print('', file=f)
        for dref in Datarefs:
            print(dref[0], dref[1], dref[2], dref[3], file=f)
        f.close()        
        
        return {'FINISHED'}

    def invoke(self, context, _event):
        import os
        self.filepath = "Datarefs" + self.filename_ext
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


def register():
    bpy.utils.register_class(OT_TestOpenFilebrowser)


def unregister():
    bpy.utils.unregister_class(OT_TestOpenFilebrowser)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.export_datarefs('INVOKE_DEFAULT')