# Design
This file is a technical discussion some of the more interesting parts of how my project was implemented.

## General file structure
I split my project into a bunch of shorter python files (each around 50-100 lines) instead of having one enormous pythong file. I did this for two reasons. For one, it made it much easier to find things in the code. To find the code where I defined the "character" class, I just went to that file. For another, it is in general good practice to do this because it allows different people to work on different parts of the code at the same time without interfering which one anothers' python files. Although I did this project on my own, I tried to stick to good general principles.

## Map Creation
The map creation was perhaps the most difficult part of this project to implement. I'm still not entirely happy with in, but what I have now works well enough for basic gameplay.

The world map consists of a large amount of "tiles" (floor tiles, wall tiles, etc.) which appear at different locations, each having different properties (for example, the player collides with wall tiles but not floor tiles). Additionally, the map is continually generated in all four directions at random.

Since I wanted the map to be infinitely expandable in all directions, I decided to store the map as a dictionary. The keys of the dictionary represent a particular location in the map, and the values represent what type of tile is at that location. For example, a very basic map could be stored as 
> {(2,3): "floor"}

If there is a floor tile at x=2, y=3.

In helpers.py, I included a few helper functions that can randomly generate very simply maps that create a single room centered at (0,0). The generate_room() function creates either a rectangular room (of random dimensions, both an integer between 10 and 15 (inclusive)) or a circular room (of random radius, an integer between 5 and 10). I separated out these helper functions to not clutter the rest of the world generation code. These helper functions were the base on which I built the rest of the world creation.

Originally, I included everything to do with the world generation in the Game class itself. However, I thought this made the code hard to navigate, so I eventually created a "world" class to contain all the world generation code. It is also good to separate the World class because it would allow different types of world generation, using different classes in place of the "World" class.

This World class includes a map attribute, which stores the map of the world as a dictionary as explained above. In addition to a few other minor things, this class includes three vitally important methods: a method which creates new tile sprites when new rooms are created, a method which goes through each of the tile sprites and updates them when the map changes, and a method which adds new rooms. 

The most difficult of these methods to implement was the method to create new rooms. I implemented that method as follows:
- First, I used the helper functions to generate a new room of random shape/dimensions. I center this room on the player's current location. I save this room to a dictionary separate from the world map.
- Then, I move the entire rook pixel by pixel (either to the left, right, up, or down, as randomly determined) until the new room dictionary no longer intersects with any of the map that is already created.
- As I move the room, I create a third dictionary that creates a hallway (i.e. a pathway with walls on either side) which generate in the direction of the new room.
- Finally, I perform a sequence of updates to the true world map dictionary in a specific order such that there is always a path from the player to a new room. This specific order is described in more detail in the world.py file itself, but the basics of the preference order can be understood to first add walls in the correct locations, and then overwrite the floor locations. This eliminates unnecessary walls such as the wall separating the new room from the hallway.

Other, less important notes on new room generation:
- I also wanted to add a feature that closed a "gate" behind the player when they activate the attack wave in a new room. To accomplish this, I found the intersection between the hallway dictionary and the new room dictionary. This intersection is where the gate would have to be. Thus, I saved its tile type as "gate_deactive." When the attack begins, its type updates to "gate."
- To make it clear which direction the new room was in, I created a different colored floor (called "new_floor" for tiles in the new room and "new_path" for tiles in the created path) to point the way. Note that when the attack begins, the "new_path" tiles return to the normal floor color whereas the room stays in the new color, which is why it was necessary to have two different types for what were really the same type of tile.
- At the center of each room, I added an "activation tile" that triggers the new attack when the player walks into it. This prevents the enemies from spawning until after the player is ready and in the new room.

## Camera
Another major challenge was dealing with the camera. I wanted the camera to always focus on the player, so the location I drew the background tiles and the enemies depended on the player's location. However, other objects, such as the player health bar and crosshair, should not move when the player moves. This forced me to use two coordinate different coordinate systems in different contexts.

Some objects, such as the crosshair, needed to know its coordinates as well as it's player-adjusted coordinates. It needed to know its screen coordinates so that it drew on the correct part of the screen, and it needed to know its player-adjusted coordinates that it knew when it collided with an enemy on the screen.

As a base, I used youtuber ClearCode's code (see links at end of file) to draw the player-adjusted sprites. All sprites drawn in a way that changes with the location of the player are in the CameraGroup group. All other elements are just drawn using PyGames default drawing settings.

In pygame, things appear "on top of" or "behind" one another depending on the order they were drawn. The camera draws things in the following order so that things appear right:
1. Fill the screen with the background color
2. Background sprites (all tiles)
3. Foreground sprites (characters, wall tiles) These are drawn from the top of the screen to the bottom, so that things lower on the screen are in the front of things behind them.
4. UI elements that follow the player (such as enemy health bars)
5. A rectangle at the top of the screen in the background, as a backdrop for the other UI elements
6. UI elements that don't follow the player (such as the player health bar, the score, and the crosshair)
Since 

## Characters 
All characters in the game (the player, as well as the enemy characters such as the slime and dark slime) are specific instances of their classes. The player, slime, and dark slime classes are in turn all inherit methods/attributes from the "character class."

The character class includes attributes/methods relevant to all characters, such as the method that checks moves the sprite and checks for collisions, the method that animates the sprite to move to the next frame, and the method for taking some given amount of damage. Each object of the character class also creates a "health counter" object (see below).

The player class inherits all these methods, and adds on additional methods, such as getting the user's keyboard input, checking to see if the player is touching the activation tile in the center of each room, and checking to see if the player has died.

The Slime and Dark slime classes are very similar, and it would even have been possible to put them into the same "GenericSlime" class. However, I decided not to do this because if I were to develop the game further, I would have added more differences to how the two types of enemies behave. At present, both classes inherit all the charecter methods and have some new enemy-specific methods such as updating its direction of movement to move toward the player, and checking to see if the enemy is touching the player's hitbox. Also of interest is the fact that the enemies collide with themselves, which I accomplished by placing enemies making them collide with the group of enemy sprites.

## Health Counters and Health Bars
Every character has a certain amount of health, but different types of characters have different types of health bars. Specifically, I wanted the player's health bar to be placed in the top left and the enemy's health bar to be placed directly under the enemy itself. To solve this discrepancy, I created two types of classes: a single HealthCounter class, which all character's have. On top of this, each HealthCounter object has either a PlayerHealthBar or an EnemyHealthBar, depending on the type of character. I could have instead added a conditional in the Character class itself, but having this intermediate felt much more natural to me.

The HealthCounter class just creates either a PlayerHealthBar or an EnemyHealthBar object, depending on the type of character. It has two methods; one that relays information about the health of the character going down to the health bar, and one that relays if the HealthBar reached its last frame of the animation (i.e. the character died) to the character itself.

The HealthBar Class defines everything that a PlayerHealthBar and an EnemyHealthBar have in common. This includes things such as how to update the health bar graphic when a certain amount of damage is dealth.

The PlayerHealthBar class places a scaled up version of the health bar graphic in the top left of the screen. When the player takes damage, it updates the health bar to the next image (the image of the health bar with less health). When the end of the animation is reached, the object tells the HealthCounter that the player died.

The EnemyHealthBar class places a smaller version of the health bar graphic directly under its enemy. Upon the enemy's spawn, there is a brief animation of the health bar "booting up" to full health, during the time the enemy is unable to be attacked. Then, the health bar just updates its position to follow where the enemy goes. When the health bar reaches the last image in its animation (0 health), then it tells HealthCounter that the enemy died.

## Score Counter and Digit Classes
Since each sprite can only have a single image (or at least that is what is the design norm in pygame), I needed a separate sprite for each of the digits displaying the score. However, I still wanted some central entity to control everything relating to the score. This is what lead me to create two classes: the ScoreCounter class, which stores/updates the score creates/updates each of the digits when the score changes, and the "Digit" class, which displays a particular digit of the score in the appropriate place.

## Attacking: The Crosshair
The Crosshair class creates the crosshair, which is the player's way to defend itself from the enemies. On a high level, it updates itself each frame to go towards the mouse pointer. The class has a method that is called by the game when the mouse is clicked, that checks for a collision between the crosshair and any enemies. It then damages any enemies that fit this requirement.

The main difficulty in creating the crosshair was storing two locations: the location it appeared on the screen, and its location in the player-adjusted coordinates (which was needed to check for collisions with the enemy sprites).

## Powerups:
I really wanted to implement power ups in this game, and the way I ended up doing it was sometimes spawning a potion sprite in a defeated room before a new room is created. The Potion class looks at the world map dictionary and finds a location with the tile type "new_room". The potion then chooses a random type (either giving the player speed, allowing the player to do double damage, or making the crosshair bigger). Finally, the player waits for the player to collide with in. When this happens, the potion applies its effect, disappears, and spawns the new room for the player to explore.

Since this game was very difficult to survive very long, I made the choice for power ups to build on top of one another and never go away. In the future, I may change this.

## Running the Game
I put all the code for running the game in the "Game" class rather than in its own file because it seems cleaner, and it is what several tutorials I followed learning pygame did. 

In initialization, the game object creates all the relevant objects (the player, the crosshair, the score, the world, etc.). Of particular importance is the is_alive attribute (which stores if the player is alive or not) and the enemies_remaining attribute (which stores the number of enemies in a room. When it reaches 0, a new room is created. Right after a new room is created, it is changed to the temporary value of "-1" so the game knows that there are currently no enemies, but also no need to create a new room since one has already been created).

At the end of initialization, the game calls its own "run" method. This method is what runs the entire game. First, it checks to see if the game is quit or if the player hit the escape key (both actions resulting in the pygame window closing). Then, it checks to see if the mouse is down so it can trigger the crosshair to fire. After checking these basic things, the game calls its draw_game_screen method, which updates all sprites and then draws them as described earlier in the "Camera" section. Following this, the game waits a certain number of time (dependent on the FPS of the game) before doing it all again. This loop continues until the "is_alive" attribute switches to False (i.e. the player dies).

After the play dies, the game calls its "update_leaderboard" method, which prompts the user to input their name for adding their score for the leaderboard. To make things display well later, I limited the user's input to 8 alphanumeric characters. The user's name and score are then added to the CSV file "leaderboard.csv." Following this, the draw_leaderboard method is called, which writes out the top 10 highscores by reading and then sorting the "leaderboard.csv" file. Then the game waits for the user to press the "R" button, which reinitializes the game and allows gameplay to continue.

## The Leaderboard
I wanted scores to be sa ves across multiple playing sessions, so I allowed the game to access a CSV file that stores all the previous scores of the player. This was necessary because any variables within python are discarded as soon as the program ends- I needed a separate file to store the scores so that they could be accessed indefinitely. 

## Settings.py
For things which may change in future iterations of the game (for example: the FPS, the player movement speed, the scaling fact for the graphics, etc.), I used a separate python file called "settings.py". This allows the values to be easily changed, so that you don't have to search in each of the files to find a particular value to change.