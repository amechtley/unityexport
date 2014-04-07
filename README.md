# unityexport

This package modifies Unity's import process of Maya files, enabling you to
register callbacks of type MSceneMessage.kBeforeExport. These callbacks will be
invoked when Unity converts your native Maya file to FBX in the background. It
also registers a callback that automatically adjusts the FBX export settings to
ensure blend shape data and animations can properly import into Unity 4.3 and
newer, when using Maya 2012 or newer.

To use it, simply import it in your studio-wide userSetup.py script. Thereafter,
if the unityexport.unity_project_version is not None, you can register any
callbacks you wish using the MSceneMessage.kBeforeExport type. For instance, the
following example userSetup script registers a callback that automatically
creates a locator in the scene each time a file is sent to Unity:

```python
# import studio-wide modules
import unityexport
import maya.cmds as cmds
import maya.OpenMaya as om

# add example callback
if unityexport.unity_project_version is not None:
    def some_callback(*args):
        """
        A callback to add a locator to each scene when it exports.
        @param args: A method signature requirement.
        """
        cmds.spaceLocator(n='some_callback_was_called')
    om.MSceneMessage.addCallback(om.MSceneMessage.kBeforeExport, some_callback)
```

# Creation Info

## Donations
http://adammechtley.com/donations/

## License
The MIT License

Copyright (c) 2014 Adam Mechtley (http://adammechtley.com)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the 'Software'), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.