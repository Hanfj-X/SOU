"""
1.基础感知
Q1: Category Enumeration(CE): How many distinct categories of small objects in this image?
Q2: Object Counting(OC): How many small objects are present in this image?
2.空间推理
Q3: Category Recognition(CR): What is the small object at point [x,y] in this image?
Q4: Object Location(OL): Which is the bounding boxes of the small object within the red rectangular area in this image?
3.细粒度理解
Q5: Specific Category Counting(SCC)：How many small objects belonging to the category "cars" are present in the image?
Q6: Peripheral Object Identification(POI)：What is the category of the “rightmost” small object in the image?
"""
import random

from json_manager import JsonManager
from pycocotools.coco import COCO
import cv2 as cv
random.seed(42)
Q_title = ['Category Enumeration', 'Object Counting', 'Category Recognition', 'Object Location', 'Specific Category Counting', 'Peripheral Object Identification']
Q_labels = ['CE', 'OC', 'CR', 'OL', 'SCC', 'POI']
# Q_questions = ['How many distinct categories of small objects in this image?',
#               'How many small objects are present in this image?',
#               'What is the small object at point [xxx,yyy] in this image?',
#               'Which is the bounding boxes of the small object within the red rectangular area in this image?',
#               'How many small objects belonging to the category XXX are present in the image?',
#               'What is the category of the XXXmost small object in the image?'
#               ]
categories_list = ['people', 'rider', 'bicycle', 'motor', 'vehicle', 'traffic-sign', 'traffic-light', 'traffic-camera', 'warning-cone']

def create_message(Q_index: int, opts: list, ans_idx: int):
    """
    Creates a formatted message for the conversation with options for the question.

    Args:
        Q_index: Index of the question type (0-5)
        opts: List of answer options
        ans_idx: Index of the correct answer in the options list

    Returns:
        A list containing the user and assistant messages for the conversation
    """
    options_string = ''
    for idx in range(len(opts)):
        options_string += '\n' + chr(65+idx) +': ' +opts[idx]
    return [
        {
        "role": "user",
        "content": "<image>" + Q_questions[Q_index] + options_string
        },
        {
        "role": "assistant",
        "content": chr(65+ans_idx)
        }
    ]

def shuffle_answer(opts, ans):
    """
    Shuffles the answer options and returns the new options and the index of the correct answer.

    Args:
        opts: List of answer options
        ans: Index of the correct answer in the original options list

    Returns:
        Tuple containing the shuffled options and the new index of the correct answer
    """
    new_opts = random.sample(opts, len(opts))
    new_ans = new_opts.index(opts[ans])
    return new_opts, new_ans

if __name__ == '__main__':
    # Process each question type (0-5)
    for task_id in range(6):
        # task_id = 4
        option_num = 4 # Number of answer options for each question (always 4)

        my_json = JsonManager(Q_title[task_id] + '.json')
        my_json.clear_all_data()

        coco = COCO("Annotations_Driving\\val.json")

        count = 0
        for image_info in coco.loadImgs(coco.imgs.keys()):
            if count % 100 == 0:
                print(f'当前进度：{count}/{len(coco.loadImgs(coco.imgs.keys()))}')
            count += 1
            
            if image_info['width'] * image_info['height'] > 6000000: continue

            Q_questions = ['How many distinct categories of small objects in this image?',
                           'How many small objects are present in this image?',
                           'What is the small object at point [xxx,yyy] in this image?',
                           'Which is the bounding boxes of the small object within the red rectangular area in this image?',
                           'How many small objects belonging to the category XXX are present in the image?',
                           'What is the category of the XXXmost small object in the image?'
                           ]
            
            annotations = coco.loadAnns(coco.getAnnIds(imgIds=image_info['id']))
            options = []
            obj_num = 0
            obj_categories = []
            obj_category_set = []
            bboxes = []

            if task_id == 0: # Q1: Category Enumeration(CE): How many distinct categories of small objects in this image?
                for antt in annotations:
                    if not antt['ignore'] and antt['category_id'] not in obj_category_set:
                        obj_category_set.append(antt['category_id'])
                category_num = len(obj_category_set)
                options = [x for x in range(1+len(categories_list)) if x is not category_num]
                options = random.sample(options, option_num - 1)
                options.append(category_num)

            elif task_id == 1: # Q2: Object Counting(OC): How many small objects are present in this image?
                for antt in annotations:
                    if not antt['ignore']:
                        obj_num += 1
                options = [x for x in range(100) if x not in [obj_num - 1, obj_num, obj_num + 1]]
                options = random.sample(options, option_num - 1)
                options.append(obj_num)

            elif task_id == 2:  # Q3: Category Recognition(CR): What is the small object at point [x,y] in this image?
                for antt in annotations:
                    if not antt['ignore']:
                        bboxes.append(antt['bbox'])
                        obj_categories.append(categories_list[antt['category_id']-1])
                random_index = random.randrange(len(obj_categories))
                pick_bbox = bboxes[random_index]
                pick_category = obj_categories[random_index]
                pick_x = pick_bbox[0] + pick_bbox[2]//2
                pick_y = pick_bbox[1] + pick_bbox[3]//2
                Q_questions[task_id] = Q_questions[task_id].replace('xxx', str(pick_x))
                Q_questions[task_id] = Q_questions[task_id].replace('yyy', str(pick_y))
                options = [categories_list[x] for x in range(len(categories_list)) if categories_list[x] is not pick_category]
                options = random.sample(options, option_num - 1)
                options.append(pick_category)

            elif task_id == 3: # Q4: Object Location(OL): Which is the bounding boxes of the small object within the red rectangular area in this image?
                for antt in annotations:
                    if not antt['ignore']:
                        bboxes.append(antt['bbox'])
                random_index = random.randrange(len(bboxes))
                pick_bbox = bboxes[random_index]
                pick_x1 = pick_bbox[0]
                pick_y1 = pick_bbox[1]
                pick_x2 = pick_bbox[0] + pick_bbox[2]
                pick_y2 = pick_bbox[1] + pick_bbox[3]

                image = cv.imread('Images_Driving\\' + image_info['file_name'])
                cv.rectangle(image, (pick_bbox[0], pick_bbox[1]), (pick_bbox[0] + pick_bbox[2], pick_bbox[1] + pick_bbox[3]), (0, 0, 255), 5)
                cv.imwrite(Q_title[task_id] + '\\' + image_info['file_name'], image)

                opt_id = 0
                while opt_id < 3:
                    rw = random.randrange(10, 100)
                    rh = random.randrange(10, 100)
                    if rw * rh < 1024:
                        rx1 = random.randrange(image.shape[1] - rw)
                        ry1 = random.randrange(image.shape[0] - rh)
                        rx2 = rx1 + rw
                        ry2 = ry1 + rh
                        inter_x1 = max(pick_x1, rx1)
                        inter_y1 = max(pick_y1, ry1)
                        inter_x2 = min(pick_x2, rx2)
                        inter_y2 = min(pick_y2, ry2)
                        inter_area = max(0, inter_x2 - inter_x1) * max(0, inter_y2 - inter_y1)
                        b1_area = pick_bbox[2] * pick_bbox[3]
                        b2_area = rw * rh
                        iou = inter_area / (b1_area + b2_area - inter_area + 1e-6)
                        if iou < 0.5:
                            options.append('[' + str(rx1) + ',' + str(ry1) + ',' + str(rx2) + ',' + str(ry2) + ']')
                            opt_id += 1
                options.append('[' + str(pick_x1) + ',' + str(pick_y1) + ',' + str(pick_x2) + ',' + str(pick_y2) + ']')

                # image = cv.resize(image, (1778, 1000))
                # cv.imshow('image', image)
                # cv.waitKey(0)

            elif task_id == 4:  # Q5: Specific Category Counting(SCC)：How many small objects belonging to the category "cars" are present in the image?
                for antt in annotations:
                    if not antt['ignore']:
                        obj_categories.append(categories_list[antt['category_id']-1])
                        if antt['category_id'] not in obj_category_set:
                            obj_category_set.append(antt['category_id'])
                random_index = random.randrange(len(obj_categories))
                pick_category = obj_categories[random_index]
                pick_count = obj_categories.count(pick_category)
                Q_questions[task_id] = Q_questions[task_id].replace('XXX', str(pick_category))
                options = [x for x in range(100) if x is not pick_count]
                options = random.sample(options, option_num - 1)
                options.append(pick_count)

            elif task_id == 5: # Q6: Peripheral Object Identification(POI)：What is the category of the “rightmost” small object in the image?
                mosts = ['right', 'left', 'top', 'bottom']
                most_id = random.randrange(len(mosts))
                pick_most = mosts[most_id]
                Q_questions[task_id] = Q_questions[task_id].replace('XXX', str(pick_most))
                small_most = 1000000
                big_most = 0
                for antt in annotations:
                    if not antt['ignore']:
                        box = antt['bbox']
                        if pick_most == 'right':
                            big_temp = box[0] + box[2]
                            if big_temp > big_most:
                                big_most = big_temp
                                most_category = categories_list[antt['category_id']-1]
                        elif pick_most == 'left':
                            small_temp = box[0]
                            if small_temp < small_most:
                                small_most = small_temp
                                most_category = categories_list[antt['category_id']-1]
                        elif pick_most == 'top':
                            small_temp = box[1]
                            if small_temp < small_most:
                                small_most = small_temp
                                most_category = categories_list[antt['category_id']-1]
                        elif pick_most == 'bottom':
                            big_temp = box[1] + box[3]
                            if big_temp > big_most:
                                big_most = big_temp
                                most_category = categories_list[antt['category_id']-1]
                options = [categories_list[x] for x in range(len(categories_list)) if categories_list[x] is not most_category]
                options = random.sample(options, option_num - 1)
                options.append(most_category)


            options = [str(x) for x in options]
            options, answer = shuffle_answer(options, option_num - 1)
            new_massage = create_message(task_id, options, answer)
            my_json.add_conversation(new_massage, ["images/" + image_info['file_name']])
