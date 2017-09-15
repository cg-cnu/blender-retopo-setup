'''
# Blender - Retopology Workflow Setup

Automates the workflow in the tutorial by [Zacharias Reinhardt](https://youtu.be/2hEHtKH55Us).
Make the sculpt active and in 3d view press space and type retopo workflow.
'''

bl_info = {
	"name": "Retopo Workflow",
	"description": "setup and automate the retopo workflow",
	"author": "Sreenivas Alapati(cg-cnu)",
	"version": (1, 0),
	"blender": (2, 79, 0),
	"category": "Mesh"}

import bpy 

def main(self, context):
	C = bpy.context
	D = bpy.data
	O = bpy.ops
	name = C.active_object.name

	if D.objects[name].type != 'MESH':
		self.report({'WARNING'}, " Valid mesh object not selected ")
		return {'FINISHED'}
	
	O.mesh.primitive_plane_add() # add plant mesh
	C.object.location.xyz = bpy.data.objects[name].location.xyz # set its positon to sculpt's origin 
	C.active_object.name = name + '_retopo' # rename the object as name_retopo
	retopo = C.active_object.name # get the name of the object as retopo         

	# rotate and translate
	bpy.ops.object.editmode_toggle()
	bpy.ops.transform.translate(value=(0, 10, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
	bpy.ops.transform.rotate(value=1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
	bpy.ops.object.editmode_toggle()

	# scene settings
	bpy.context.scene.tool_settings.use_snap = True
	bpy.context.scene.tool_settings.snap_element = 'FACE'
	bpy.context.scene.tool_settings.use_snap_project = True

	# mirror modifier
	O.object.modifier_add(type='MIRROR') # apply mirror modifier
	bpy.context.object.modifiers["Mirror"].use_y = True
	bpy.context.object.modifiers["Mirror"].use_x = False

	D.objects[retopo].modifiers['mirror'].use_clip = True # enable clipping
	D.objects[retopo].modifiers['mirror'].name = name + '_mirror'

	bpy.context.object.modifiers["Mirror"].show_expanded = False

	# subsurf modifier
	O.object.modifier_add(type='SUBSURF')
	bpy.context.object.modifiers["Subsurf"].levels = 2
	bpy.context.object.modifiers["Subsurf"].subdivision_type = 'SIMPLE'

	# shrinkwrap modifier 
	O.object.modifier_add(type='SHRINKWRAP')
	D.objects[retopo].modifiers['Shrinkwrap'].target = bpy.data.objects[name]
	D.objects[retopo].modifiers["Shrinkwrap"].offset = 0.002
	D.objects[retopo].modifiers["Shrinkwrap"].use_keep_above_surface = True
	bpy.context.object.modifiers["Shrinkwrap"].wrap_method = 'PROJECT'
	bpy.context.object.modifiers["Shrinkwrap"].use_negative_direction = True

	D.objects[retopo].modifiers['Shrinkwrap'].name = name + '_shrinkwrap'
	bpy.context.object.modifiers["Shrinkwrap"].show_on_cage = True


	# blender render material
	if bpy.context.scene.render.engine == 'BLENDER_RENDER'
		bpy.context.object.active_material.diffuse_color = (0.8, 0.153118, 0.0239938)
		bpy.context.object.active_material.specular_color = (0, 0, 0)

	# cycles material
	if bpy.context.scene.render.engine == 'CYCLES'
		bpy.ops.material.new()
		bpy.context.object.active_material.name = "retopoMtl"
		bpy.context.object.active_material.diffuse_color = (0.8, 0.166372, 0.0489808)
		bpy.context.object.active_material.specular_color = (0, 0, 0)

	self.report({'INFO'}, " Created setup for retopo ")

class RetopoWorkflow(bpy.types.Operator):
	""" sets the object ready for retopo """
	bl_idname = "object.retopo_workflow"
	bl_label = "Retopo Workflow"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		return context.active_object is not None

	def execute(self, context):
		main(self, context)
		return {'FINISHED'}

def register():
	bpy.utils.register_class(RetopoWorkflow)

def unregister():
	bpy.utils.unregister_class(RetopoWorkflow) 

if __name__ == "__main__":
	register()