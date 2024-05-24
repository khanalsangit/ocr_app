# Ultralytics YOLO 🚀, AGPL-3.0 license

import torch
import time
from ultralytics.engine.results import Results
from ultralytics.models.yolo.detect.predict import DetectionPredictor
from ultralytics.utils import DEFAULT_CFG, ops


class OBBPredictor(DetectionPredictor):
    """
    A class extending the DetectionPredictor class for prediction based on an Oriented Bounding Box (OBB) model.

    Example:
        ```python
        from ultralytics.utils import ASSETS
        from ultralytics.models.yolo.obb import OBBPredictor

        args = dict(model='yolov8n-obb.pt', source=ASSETS)
        predictor = OBBPredictor(overrides=args)
        predictor.predict_cli()
        ```
    """

    def __init__(self, cfg=DEFAULT_CFG, overrides=None, _callbacks=None):
        """Initializes OBBPredictor with optional model and data configuration overrides."""
        super().__init__(cfg, overrides, _callbacks)
        self.args.task = "obb"

    def postprocess(self, preds, img, orig_imgs):
        """Post-processes predictions and returns a list of Results objects."""
        preds = ops.non_max_suppression(
            preds,
            self.args.conf,
            self.args.iou,
            agnostic=self.args.agnostic_nms,
            max_det=self.args.max_det,
            nc=len(self.model.names),
            classes=self.args.classes,
            rotated=True,
        )

     
        start_time = time.time()
        if not isinstance(orig_imgs, list):  # input images are a torch.Tensor, not a list
            orig_imgs = ops.convert_torch2numpy_batch(orig_imgs)

        custom_labels = {
            0:'chhabi',
            1:'lal',
            2:'tamang',
            3:'sumit',
            4:'tamang'
        }
        results = []
        for pred, orig_img, img_path in zip(preds, orig_imgs, self.batch[0]):
            rboxes = ops.regularize_rboxes(torch.cat([pred[:, :4], pred[:, -1:]], dim=-1))
            rboxes[:, :4] = ops.scale_boxes(img.shape[2:], rboxes[:, :4], orig_img.shape, xywh=True)
            # xywh, r, conf, cls
            obb = torch.cat([rboxes, pred[:, 4:6]], dim=-1)
            results.append(Results(orig_img, path=img_path, names=self.model.names, obb=obb))
        
        for result in results:
            import cv2
            all_info = result.obb
            No_of_box = len(all_info)
            annotated_img = result.orig_img.copy()

            for box in all_info:
                # Extract the bounding box coordinates and convert them to integers
                x1, y1, x2, y2, x3, y3, x4, y4 = [int(coord) for coord in box.xyxyxyxy.flatten()]

                # Extract the class id
                class_id = int(box.cls)
                
                # Extract the default label and map it to the custom label
                default_label = result.names[class_id]
                custom_label = custom_labels.get(class_id, default_label)  

                # Draw the bounding box
                points = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
                for j in range(4):
                    cv2.line(annotated_img, points[j], points[(j + 1) % 4], (0, 255, 0), 2)

                # Put the custom label text near the bounding box
                cv2.putText(annotated_img, custom_label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        
           
            if annotated_img.shape[2] == 3:  # if the image has 3 channels
                numArray = annotated_img
            else:
                raise ValueError("Unexpected number of channels in annotated image.")

            # cv2.imshow("Image",annotated_img)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
        print("Total time",time.time() - start_time)
        
        return results
        
