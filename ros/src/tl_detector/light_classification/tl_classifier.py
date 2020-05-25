from styx_msgs.msg import TrafficLight
import numpy as np
import tensorflow as tf

class TLClassifier(object):
    def __init__(self):
        GRAPH_PATH = r'light_classification/model/frozen_graph.pb'
        
        self.graph = tf.Graph()
        self.threshold = 0.55
        
        with self.graph.as_default():
            graph_def = tf.GraphDef()
            with tf.gfile.GFile(GRAPH_PATH, 'rb') as model:
                graph_def.ParseFromString(model.read())
                tf.import_graph_def(graph_def, name = '')
                
            self.image_tensor = self.graph.get_tensor_by_name('image_tensor:0')
            self.boxes = self.graph.get_tensor_by_name('detection_boxes:0')
            self.scores = self.graph.get_tensor_by_name('detection_scores:0')
            self.classes = self.graph.get_tensor_by_name('detection_classes:0')
            self.num_detections = self.graph.get_tensor_by_name('num_detections:0')
            
        self.sess = tf.Session(graph = self.graph)

    def get_classification(self, image):
        """Determines the color of the traffic light in the image

        Args:
            image (cv::Mat): image containing the traffic light

        Returns:
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)

        """
        #TODO implement light color prediction
        with self.graph.as_default():
            img_exp = np.expand_dims(image, axis = 0)
            boxes, scores, classes, num_detections = self.sess.run([self.boxes, self.scores, self.classes, self.num_detections], feed_dict={self.image_tensor: img_exp})
        
        boxes = np.squeeze(boxes)
        scores = np.squeeze(scores)
        classes = np.squeeze(classes).astype(np.int32)
        
        # Check if the top score is significant, if so, use label
        if scores[0] > self.threshold:
            if classes[0] == 1:
                return TrafficLight.GREEN
            if classes[0] == 2:
                return TrafficLight.RED
            elif classes[0] == 3:
                return TrafficLight.YELLOW
        return TrafficLight.UNKNOWN
