import copy

from util.BoundingBoxCollection import BoundingBoxCollection
from util.SafeListEditor import safely_remove_list_indexes as safe_rm
from util.Box import Box


class Tracker:
    """
    A class to "smooth out" the tracking of identified items.  The object recognition software can occasionally fail to
    identify objects in a frame.  Doing so may lead to objects in a scene not being described to the user.  This class
    provides a degree of "inertia" to bounding box identifications, so as to reduce the chances of boxes which have been
    identified for a single frame, or boxes which have dropped out of a single frame, from being erroneously describes
    (or not described) to the user.
    """

    def __init__(self, iou_threshold=0.9, min_frames=1, allowed_absence=0):
        """
        The constructor for the class.

        @param iou_threshold:   A float which is the minimum value for the Intersection over Union value to identify two
                                bounding boxes as being from the same item.
        @param min_frames:      An int which is the minimum number of frames an item must be present for before being
                                reported as a valid track.
        @param allowed_absence: An int which is the maximum number of frames which an item may not appear for before it
                                is no longer reported as a valid track.
        """
        self.__tracks__: list = list()
        self.__frame_count__: int = 0
        self.__min_frames_for_track__ = min_frames
        self.__allowed_absence__ = allowed_absence
        self.__min_iou_to_continue_track__ = iou_threshold
        self.__next_track_uid__ = 0

    def add_new_frame(self, frame_bounding_boxes: BoundingBoxCollection):
        """
        Adds a new frame to the tracker.  Updates any items currently being tracked, and adds and removes tracks for
        items as required.

        @param frame_bounding_boxes: A BoundingBoxCollection object which is the bounding boxes for items in the frame.
        @return:
        """
        self.__frame_count__ = self.__frame_count__ + 1
        self.__add_frame_bounding_boxes_to_tracks__(frame_bounding_boxes)
        self.__remove_old_tracks__()

    def __remove_old_tracks__(self):
        """
        Removes any tracked items that have not been identified in recent frames.  The exact number of frames an item
        can be absent for is set in the class constructor.

        @return:
        """
        oldest_allowed_track = self.__frame_count__ - self.__allowed_absence__
        indexes_to_remove = list()
        for i in range(len(self.__tracks__)):
            track: Tracker.Track = self.__tracks__[i]
            if track.get_last_seen() < oldest_allowed_track:
                indexes_to_remove.append(i)

        safe_rm(self.__tracks__, indexes_to_remove)

    def __add_frame_bounding_boxes_to_tracks__(self, frame_boxes: BoundingBoxCollection):
        """
        Takes a collection of bounding boxes and add new ones to the list of tracks.  Bounding boxes which correspond to
        existing tracks are identified, and the appropriate tracks updated.

        @param frame_boxes: A BoundingBoxCollection object which contains the items identified in this frame.
        @return:
        """
        bbox_indexes_to_remove = list()

        for track_index in range(len(self.__tracks__)):
            for bbox_index in range(frame_boxes.size()):
                if self.__update_track_if_box_overlaps__(track_index, frame_boxes[bbox_index]) \
                        and not bbox_indexes_to_remove.__contains__(bbox_index):
                    bbox_indexes_to_remove.append(bbox_index)
        self.__get_rid_of_boxes_that_are_now_updated_tracks__(frame_boxes, bbox_indexes_to_remove)
        self.__add_remaining_boxes_as_new_tracks__(frame_boxes)

    def __update_track_if_box_overlaps__(self, track_index: int, new_bbox: Box) -> bool:
        """
        Updates the given track if the given bounding box overlaps with it.

        @param track_index: An int which is the index of the track to update.
        @param new_bbox:    A Box object which is the bounding box to check against the track.
        @return:            A bool describing if the track was updated.
        """
        existing_track: Tracker.Track = self.__tracks__[track_index]
        current_frame = copy.deepcopy(self.__frame_count__)
        iou_threshold = self.__min_iou_to_continue_track__

        iou = existing_track.get_box().get_iou(new_bbox)
        if iou > iou_threshold:
            self.__replace_bbox_label_if_conf_lower_than_existing_label__(existing_track.get_box(), new_bbox)
            existing_track.sighted(new_bbox, current_frame)
            return True
        else:
            return False

    @classmethod
    def __replace_bbox_label_if_conf_lower_than_existing_label__(cls, tracked_bbox: Box, new_bbox: Box):
        """
        Compares the labels between two boxes, and replaces the label of the new box if the confidence value for the
        tracked box is higher.  This should mean that each track is always labeled with the highest confidence value.

        @param tracked_bbox:    A Box object which is the box of the existing track.
        @param new_bbox:        A Box object which is the new bounding box.
        @return:
        """
        if tracked_bbox.confidence > new_bbox.confidence:
            new_bbox.confidence = tracked_bbox.confidence
            new_bbox.label = tracked_bbox.label

    @classmethod
    def __get_rid_of_boxes_that_are_now_updated_tracks__(cls, boxes: BoundingBoxCollection, indexes: list):
        """
        An explanatory function.  The function name describes what the actual safe_rm() call is supposed to achieve.

        @param boxes:   A BoundingBoxCollection object which is to have any boxes corresponding to existing tracks
                        removed.
        @param indexes: A list of int values, which are the indices of the bounding boxes in the collection which have
                        been used to update existing tracks.
        @return:
        """
        safe_rm(boxes, indexes)

    def __add_remaining_boxes_as_new_tracks__(self, frame_boxes: BoundingBoxCollection):
        """
        Adds the given bounding boxes to the list of current tracks.

        @param frame_boxes: A BoundingBoxCollection object, which contains the boxes to add as new tracks.
        @return:
        """
        current_frame = copy.deepcopy(self.__frame_count__)
        for remaining_bbox in frame_boxes:
            new_track = Tracker.Track(remaining_bbox, current_frame, self.__next_track_uid__)
            self.__tracks__.append(new_track)
            self.__next_track_uid__ += 1

    def get_current_tracks(self) -> (BoundingBoxCollection, list):
        """
        A getter for the currently tracked items.  Will return tracks that haven't been seen for a set number of frames,
        and will not return tracks that have only been seen for fewer than a given number of frames.  Both of these
        thresholds are set in the class constructor.

        @return:    A tuple containing a BoundingBoxCollection, and a list of int values.  These are the currently
                    tracked bounding boxes, and the unique tracking ID numbers for the corresponding tracks.
        """
        active_tracks = BoundingBoxCollection()
        track_uids = list()
        for index in range(len(self.__tracks__)):
            track: Tracker.Track = self.__tracks__[index]
            if track.get_frames_detected() >= self.__min_frames_for_track__:
                active_tracks.add(track.get_box())
                track_uids.append(track.get_uid())
        return copy.deepcopy(active_tracks), copy.deepcopy(track_uids)

    class Track:
        """
        A child class to hold the details for each individual track.  This helps make the parent class less cluttered.
        """

        def __init__(self, box: Box, frame_last_seen: int, uid: int):
            """
            The constructor.

            @param box:             A Box object, which is the bounding box of the track.
            @param frame_last_seen: An int, which is the frame number the tracked item was last seen on.
            @param uid:             A unique identification number for this track.
            """
            self.__box__: Box = box
            self.__last_seen__: int = frame_last_seen
            self.__detected_for__: int = 1
            self.__uid__: int = uid

        def sighted(self, box: Box, frame: int):
            """
            Updates the track when the tracked item is sighted.

            @param box:     A Box object, which is the new bounding box to assign to the track.
            @param frame:   An int, which is the frame number that the tracked item has been sighted in.
            @return:
            """
            self.__box__ = box
            self.__last_seen__ = frame
            self.__detected_for__ += 1

        def get_last_seen(self) -> int:
            """
            A getter for the last frame that this item was actually spotted on.

            @return:    An int which is the number of the frame this item was last actually seen.
            """
            return self.__last_seen__

        def get_box(self) -> Box:
            """
            A getter for the bounding box associated with this track.

            @return: A Box object, which is the bounding box for the tracked item.
            """
            return self.__box__

        def get_frames_detected(self) -> int:
            """
            A getter for the number of frames that this item has been detected for.

            @return:    An int which is the number of frames this item has been detected in.
            """
            return self.__detected_for__

        def get_uid(self) -> int:
            """
            A getter for the unique identification number (UID) of this track.

            @return: An int which is the UID number of this track.
            """
            return self.__uid__

        def __str__(self):
            """
            An override of the __str__() function for this object.  Used in debugging.

            @return: A summary string for this object, which includes the internal values presented in readable form.
            """
            return "Track UID: " + str(self.__uid__) + ", last seen on frame: " + str(self.__last_seen__) + ", for " + \
                str(self.__detected_for__) + " frames"



