import pygame
import cv2
import numpy as np
import random
import heapq
from ultralytics import YOLO
import subprocess
import sys
from pathlib import Path

OUTPUT_PATH = Path(__file__).parent

def open_gui1():
    subprocess.Popen(["python", str(OUTPUT_PATH / "gui1.py")])

def open_congratulations_ui():
    pygame.quit()
    subprocess.Popen(["python", str(OUTPUT_PATH / "gui6.py")])
    sys.exit()

def start_game(scene_image_path):
    pygame.init()

    # تحميل الصورة الأصلية
    scene_image = cv2.imread(scene_image_path)
    scale_percent = 50
    width = int(scene_image.shape[1] * scale_percent / 100)
    height = int(scene_image.shape[0] * scale_percent / 100)
    dim = (width, height)
    scene_image = cv2.resize(scene_image, dim, interpolation=cv2.INTER_AREA)

    scene_height, scene_width = scene_image.shape[:2]
    scene_rgb = cv2.cvtColor(scene_image, cv2.COLOR_BGR2RGB)
    scene_surface = pygame.image.frombuffer(scene_rgb.tobytes(), (scene_width, scene_height), 'RGB')

    screen = pygame.display.set_mode((scene_width, scene_height))

    # تحميل صورة الزر وتحديد مكانه
    button_image = pygame.image.load(r"D:/Faculty/AI/Catch-The-Cuties-Game-main/build/assets/frame2/button_1.png").convert_alpha()
    button_rect = button_image.get_rect(topleft=(1, 400))

    def detect_objects_in_scene(scene_image):
        model = YOLO('yolov8n.pt')
        results = model(scene_image)

        objects = []
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cls = int(box.cls[0])
                name = model.names[cls]
                objects.append({
                    'name': name.lower(),
                    'bbox': [x1, y1, x2, y2]
                })
        return objects

    objects = detect_objects_in_scene(scene_image)

    font = pygame.font.SysFont(None, 36)
    required_objects = ['apple', 'banana', 'orange', 'cat', 'dog', 'cow', 'elephant','chair', 'couch', 'bed', 'dining table', 'car', 'bus', 'motorcycle', 'bicycle','carrot']
    available_targets = [obj for obj in objects if obj['name'] in required_objects]

    if not available_targets:
        print("❌ No required objects found in the scene!")
        pygame.quit()
        return

    target_queue = available_targets.copy()
    random.shuffle(target_queue)

    def set_new_target():
        if target_queue:
            current_target = target_queue.pop(0)
            name = current_target['name']
            bbox = current_target['bbox']
            print(f"🔎 New target: {name}")
            return name, bbox
        else:
            return None, None

    target_name, target_bbox = set_new_target()
    GRID_SIZE = 20

    def to_grid_coords(pos):
        return (pos[0] // GRID_SIZE, pos[1] // GRID_SIZE)

    def astar_search(start, goal, grid_width, grid_height):
        directions = [(1,0), (-1,0), (0,1), (0,-1)]
        open_set = []
        heapq.heappush(open_set, (0, start))
        
        came_from = {}
        g_score = {start: 0}
        
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])
        
        while open_set:
            _, current = heapq.heappop(open_set)
            
            if current == goal:
                return g_score[current]
            
            for dx, dy in directions:
                neighbor = (current[0] + dx, current[1] + dy)
                
                if 0 <= neighbor[0] < grid_width and 0 <= neighbor[1] < grid_height:
                    tentative_g = g_score[current] + 1
                    
                    if neighbor not in g_score or tentative_g < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g
                        f_score = tentative_g + heuristic(neighbor, goal)
                        heapq.heappush(open_set, (f_score, neighbor))
        
        return float('inf')

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and target_name:
                x, y = pygame.mouse.get_pos()

                # ✅ تحقق من زر الرجوع
                if button_rect.collidepoint((x, y)):
                    pygame.quit()
                    open_gui1()
                    sys.exit()

                for obj in objects:
                    x1, y1, x2, y2 = obj['bbox']
                    if x1 <= x <= x2 and y1 <= y <= y2:
                        print(f"✅ You clicked on: {obj['name']}")

                        if obj['name'] == target_name:
                            print("🎉 Correct! Moving to next target.")
                            target_name, target_bbox = set_new_target()
                            if not target_name:
                                print("🏆 All targets completed! Good job.")
                                running = False
                                pygame.time.delay(1000)
                                open_congratulations_ui()
                        else:
                            print("❌ Wrong object! Checking distance...")

                            clicked_cell = to_grid_coords((x, y))
                            target_center = ((target_bbox[0] + target_bbox[2]) // 2,
                                             (target_bbox[1] + target_bbox[3]) // 2)
                            target_cell = to_grid_coords(target_center)

                            grid_width = scene_width // GRID_SIZE
                            grid_height = scene_height // GRID_SIZE

                            distance = astar_search(clicked_cell, target_cell, grid_width, grid_height)
                            print(f"📏 A* Path Length to correct target: {distance} steps")

                            if distance <= 5:
                                print("🔥 You're very close!")
                            elif distance <= 15:
                                print("👍 You're close!")
                            else:
                                print("❄️ You're far!")
                        break

        screen.blit(scene_surface, (0, 0))
        screen.blit(button_image, button_rect.topleft)

        if target_name:
            text_surface = font.render(f"Find: {target_name}", True, (255, 0, 0))
            screen.blit(text_surface, (10, 10))

        pygame.display.update()

    pygame.quit()
