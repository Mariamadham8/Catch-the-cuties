# Catch-the-cuties
This is an educational image-based game developed to help children recognize objects interactively. The project includes computer vision, UI design, and game logic components.
The player selects a challenge type, then extracts specific objects from an image while considering an A* algorithm to evaluate how close their selection is to the target.


## 🔧 Technologies Used

- **Tkinter** – for building the main application interface and windows.
- **Figma** – for UI/UX design and prototyping.
- **YOLOv8** – for object detection in scene images.
- **Pygame** – for building the game logic and interaction.
- **A\* Algorithm** – to calculate the distance between the clicked and target objects, and provide feedback like “you’re close” or “you’re far” and the number of steps.

## 📸 Demo Screenshots

Here are some screenshots demonstrating different stages of the game:

### 🟢 Game Start Screen
The initial interface where the player can start the game.
<img src="C:/Users/user/Desktop/images/start_screen.jpg" alt="Game Start" width="600"/>


---

### 📂 Category Selection
The player is prompted to select a category of objects (e.g., fruits).
![Category Selection](C:/Users/user/Desktop/images/category_screen.jpg)

---

### ✅ Correct Selection
The child clicks on the correct object as prompted.
![Correct Selection](C:/Users/user/Desktop/images/correct_choice.jpg)

---

### 🟡 Wrong but Close
The child clicks on a wrong object, but it’s close to the target. A hint like "You’re close!" appears.
![Wrong Close](C:/Users/user/Desktop/images/wrong_close_choice.jpg)

---

### 🔴 Wrong and Far
The child clicks on a wrong object that is far from the target. The feedback shows "You’re far!".
![Wrong Far](C:/Users/user/Desktop/images/wrong_far_choice.jpg)

---

### 🎉 Final Congratulation Screen
After correctly identifying all target objects, the child is rewarded with a final “Congratulations” screen.
![Congrats Screen](C:/Users/user/Desktop/images/congrats.jpg)


## 👥 Team Members

- **Maryam Ahmed**
- **Mariam Adham**
- **Marwa Abu-Elkheir**



