"""
This module modifies Unity's import process for Maya files in order to enable
you to register callbacks using MSceneMessage.kBeforeExport. It also registers a
callback that automatically adjusts the FBX export settings to ensure blend
shape data and animations can properly import into Unity 4.3 and newer, when
using Maya 2012 or newer.

This module should be imported in your studio-wide userSetup.py. If the Maya
process is not owned by Unity, it will have no effect. If it is owned by Unity,
it will modify the FBXMayaExport.mel script that Unity copies into the project's
Temp folder.

To use it, simply import the module in your userSetup.py script, and if the
unity_project_version attribute is not None, register your callback using
MSceneMessage.addCallback(), specifying a type of MSceneMessage.kBeforeExport.
"""

import os.path
import re
import sys
import maya.mel as mel
import maya.OpenMaya as om


def configure_fbx_export_settings(*args):
    """
    A callback to force adjustments to FBX export settings before export.
    @param args: A method signature requirement.
    """
    # NOTE: must use MEL because Python version of FBX commands don't work
    # mel.eval('FBXExportInAscii -v true;')  # enable for debugging
    mel.eval('FBXExportHardEdges -v false;')
    if unity_project_version[0] >= 5:
        return
    # make adjustments to FBX exporter settings to accommodate blend shapes
    if maya_version >= 2012:
        mel.eval('FBXExportFileVersion -v FBX201100;')


def get_unity_project_version():
    """
    Get the version of the Unity project that launched Maya. This method works
        by first looking for a '-script' command line argument, whose value is a
        file 'FBXMayaMain.mel' in a folder 'Temp'. It then looks for the
        'ProjectSettings.asset' file in a 'ProjectSettings' folder sibling to
        the 'Temp' folder.
    @return: A tuple containing (major, minor, maintenance) integers for the
        Unity version of the project from which Maya was launched, if it was
        launched by Unity; otherwise, None.
    """
    try:
        startup_script = get_startup_script()
        directory, script = os.path.split(startup_script)
        if (
            os.path.basename(directory) == 'Temp' and
            script == 'FBXMayaMain.mel'
        ):
            project_settings_asset_path = os.path.join(
                os.path.dirname(directory),
                'ProjectSettings',
                'ProjectSettings.asset'
            )
            if not os.path.exists(project_settings_asset_path):
                return None
            with open(project_settings_asset_path) as f:
                return tuple(
                    map(
                        int,
                        re.search(
                            '\d+[.]\d+[.]\d+', f.read()
                        ).group(0).split('.')
                    )
                )
        else:
            return None
    except Exception:
        return None


def get_startup_script():
    """
    Gets the path to the startup script specified with the '-script' flag in the
        command-line arguments, if there was one.
    @return: The path to the startup script if there was one, otherwise None.
    """
    try:
        return sys.argv[sys.argv.index('-script') + 1]
    except Exception:
        return None


def modify_fbx_export_script(path_to_fbx_export_script):
    """
    Modifies the local copy of FBXMayaExport.mel in the Unity project's Temp
        folder to invoke the FBXExport command through the file command, in
        order to properly send MSceneMessages before the export happens.
    @param path_to_fbx_export_script: Path to the FBXMayaExport.mel script in
        the Temp folder of the Unity project hosting the Maya session.
    """
    with open(path_to_fbx_export_script) as f:
        contents = f.read()
    contents = re.sub(
        'FBXExport -f ',
        'file -force -type "FBX export" -exportAll ',
        contents
    )
    with open(path_to_fbx_export_script, 'w+') as f:
        f.write(contents)


## the version of Maya currently running
maya_version = mel.eval('getApplicationVersionAsFloat();')
## the version of Unity being used by the project hosting the Maya instance
unity_project_version = get_unity_project_version()

# perform actions if the current Maya instance is hosted by Unity
if unity_project_version is not None:
    modify_fbx_export_script(
        os.path.join(
            os.path.dirname(get_startup_script()), 'FBXMayaExport.mel'
        )
    )
    om.MSceneMessage.addCallback(
        om.MSceneMessage.kBeforeExport, configure_fbx_export_settings
    )