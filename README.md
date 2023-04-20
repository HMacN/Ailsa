# The AILSA System

The Artificial Intelligence Loss of Sight Assistant (AILSA) system is a technology demonstrator for software-based solutions to the problems that people with difficulty seeing encounter on a daily basis. At present the system can help people identify objects on a table in front of them and can use a haptic feedback “bracelet” to guide their hand to a chosen object.
So far, however, the system is extremely limited in its ability to help people work out their location.  Two common problems for people who have difficulty seeing are: navigation of indoors spaces that are unfamiliar to them; and locating items in a room. Adding this functionality to the AILSA system would represent a significant improvement in the amount of help this system can offer to people.

A brief description of each of the implemented classes in this project is given below.

## Wrapper Classes
The Detector, Display, Frame, and Recorder classes are “wrapper” classes around OpenCV2 and TensorFlow functionality.  By keeping references to these libraries inside wrapper classes, the process of replacing these libraries, or of altering the program to handle changes in library behaviour, is made much easier, as most of the program functionality is insulated from the library’s API.
The Detector class is used to provide a simple API with which to access the combined functionality of the OpenCV2 VideoCapture class, and the TensorFlow model.  The model can be set by altering the URL provided in the class constructor, and the class allows retrieval of both the frame and the bounding boxes detected in it.
The BoxList and Frame classes were created to provide easy to use wrappers for the data being passed between the other classes, namely the bounding box data, and the picture in the frame.  The Frame class was also used to handle conversions between the two image formats in use in the project.
The Display and Recorder classes are ancillary to the functioning of the program and were mainly used to make reviewing the working of the program easier during development.  They were not intended to be user-friendly systems for interacting with the AISLA system.  They display the current frame in a window, and record the output to an mp4 file, respectively.

## Subsumption Unit
The Subsumption Unit is a class to perform an alternative to Non-Maximum Suppression (NMS).  Takes lists of items which can be subsumed by each other, and then will remove (subsume) any bounding boxes which overlap with each other if they are on the same predefined subsumption list.  This is to avoid the problem with NMS where, for example, items on top of a table are suppressed and not reported to the user.
Lists of items which can be subsumed into each other can be entered into the class as lists of strings, which should allow for ease of use by future developers.  The threshold for how much a box needs to overlap before it is subsumed can also be adjusted.

## Tracker
The Tracker class is used to provide “inertia” to object detections.  Objects must show up in a set number of frames (this number is adjustable) before being reported as a valid track by this class.  The objects may then disappear from view for a set number of frames (also adjustable) before they are removed from the list of valid tracks.  This is used to make up for items being detected either spuriously (false positive) for a small number of frames, and for the system’s occasional failure to detect an item for a few frames (false negative).
The Tracker takes a list of bounding boxes as a parameter for each frame, and it returns a similar list.

## Knowledge Unit
The Knowledge Unit (KU) is the core logical class of the program and holds the functionality to draw inferences from the list of tracked bounding boxes and return summaries of this data to the user.
The get_list_of_all_seen_items() function returns a list of all items which the KU has seen at any point  since being instantiated, and the how_many_have_you_seen() function returns the maximum count of a particular item category that has been sighted in any one frame.
The when_did_you_see() function returns a list of the times when the given item type was last seen, timed from the frame when the item went out of view.
If a custom item category has been defined, then the get_list_of_seen_items_in_category() function allows retrieval of the list of items in this category that have been seen.
The describe_scene() function returns a Python dictionary object which contains a simple breakdown of the scene into items on the left, in the centre, and on the right.  If a custom item category has been defined, then items in this category are also listed in a separate list.
To get a simple description of where in a scene an object is, the where_is() function can be used.  This returns a list of (currently only the vertical) relationships between the target item and other items in the scene.
Finally, the items_between_user_and() function returns a list of any items in the current scene which may be between the user and the target item.

## Main
The main class in the delivered code was not considered to be a major component, and chiefly exists to allow the showcasing of the functionality of the other classes.  It consists of an event loop, controlled by the ability of the Detector class to retrieve another frame from the input video.  This loop includes the logic to take the detected bounding boxes for the current frame, and to pass them to each of the relevant classes in order.
Options to display, or record, the altered video input are controlled by commenting out the relevant lines of code.  The outputs are identical to the input video feed, except that they have the detected bounding boxes annotated onto them.

