# Design
This file is a technical discussion some of the more interesting parts of how my project was implemented.

## General file structure
I split my project into a bunch of shorter python files (each around 50-100 lines) instead of having one enormous python file. I did this for two reasons. For one, it made it much easier to find specific things in the code. To find the code where I defined the "character" class, I just went to the file "characters.py". For another, it is in general good practice to split large code files into smaller parts because it allows different people to work on different parts of the code at the same time without interfering which one anothers' files. Although I did this project on my own, I tried to stick to good general principles.


## Running the Game (main.py)
I put all the code for running the game in the "Game." From the research I did on PyGame before starting this project, this seems to be the stylistic norm of Python/PyGame users. 

In initialization, the game object initializes all the relevant gameplay objects (the player, the crosshair, the score, the world, etc.) as well as several attributes. Of particular importance is the is_alive attribute and the enemies_remaining attribute. The is_alive attribute stores if the player is alive or not and this value is checked at each frame of gameplay so that the game knows when the display the leaderboard screen. The enemies_remaining attribute stores the number of enemies left in a room. When the counter reaches 0, a new room is created. Right after a new room is created, it is changed to the special value "-1" so the game knows that there are currently no enemies, but also no need to create a new room since one has already been created.

At the end of initialization, the game calls its own "run" method. This method is consists of a while loop, that first checks to see if the player is alive (using the is_alive attribute) and then doing the following actions, on each "frame" of the game: First, it checks to see if the game is quit or if the player hit the escape key (both actions resulting in the pygame window closing). Then, it checks to see if the mouse is down so it can trigger the crosshair to fire. After checking these basic things, the game calls its draw_game_screen method, which updates all sprites and then draws them as described later in the "Camera" section. Following this, the game waits a certain number of time (dependent on the FPS of the game) before doing it all again. This loop continues until the "is_alive" attribute switches to False (i.e. the player dies).

After the play dies, the game calls its "update_leaderboard" method, which prompts the user to input their name for adding their score for the leaderboard. As the user types their name, the screen is continually refreshed to display what the user has already typed. The user has the ability to type any alphanumeric character, and can submit their name by pressint the ENTER key. To make things display well later, I limited the user's input to 8 alphanumeric characters. The user's name and score are then added to the CSV file "leaderboard.csv." Following this, the draw_leaderboard method is called, which writes out the top 10 highscores by reading and then sorting the "leaderboard.csv" file. Then the top 10 scores are displayed, along with the names associated with the players. Then the game waits for the user to press the "R" button, which reinitializes the game and allows gameplay to continue.

## Map Creation (world.py)
The map creation was the most difficult part of this project to implement. Because the world generation required quite a bit of code to implement all the features I wanted, I ended up seperating all the code for world generation into a seperate World class, stored in world.py.

The world map consists of a large amount of "tiles" (floor tiles, wall tiles, etc.) which appear at different locations, each having different properties (for example, the player collides with wall tiles but not floor tiles). Additionally, the map is continually generated in all four directions at random (a new room is created whenever the previous room was "defeated"). Since I wanted the map to be infinitely expandable in all directions, I decided to store the map as a dictionary. The keys of the dictionary represent a particular location in the map, and the values represent what type of tile is at that location. For example, a very basic map could be stored as 
> {(2,3): "floor"}

If there is a floor tile at x=2, y=3.

This World class includes a map attribute, which stores the map of the world as a dictionary as explained above. In addition to a few other minor things, this class includes four vitally important methods: a method which creates a room (either rectangular or circular) centered at (0,0), a method which creates new tile sprites when new rooms are created, a method which goes through each of the tile sprites and updates them when the map changes, and a method which adds new rooms.
 

The most difficult of these methods to implement was the method to create new rooms. I implemented that method as follows:
- First, I used the create_room() method to generate a basic room centered at (0,0) of random shape/dimensions, saved to a dictionary seperate from the world map dictionary. I then adjusted this new_room dictionary to center this room on the player's current location.
- Then, I move the entire room pixel by pixel (either to the left, right, up, or down, as randomly determined) until the new room dictionary no longer intersects with any of the map that is already created.
- As I move the room, I create a third dictionary called new_hallway that creates a hallway (i.e. a pathway with walls on either side) which generate in the direction of the new room. This provides a path for the player to follow to the next room.
- Finally, I perform a sequence of updates to the true world map dictionary in a specific order such that there is always a path from the player to a new room. This specific order is described in more detail in the world.py file itself, but the basics of the preference order can be understood to first add walls in the correct locations, and then overwrite with the floor locations. This eliminates unnecessary walls such as the wall separating the new room from the hallway.

Other, less important notes on new room generation:
- I also wanted to add a feature that closed a "gate" behind the player when they activate the attack wave in a new room. To accomplish this, I found the intersection between the hallway dictionary and the new room dictionary. This intersection is where the gate would have to be. Thus, I saved its tile type as "gate_deactive." When the attack begins, its type updates to "gate" and it becomes a collision object. 
- To make it clear which direction the new room was in, I created a different colored floor (called "new_floor" for tiles in the new room and "new_path" for tiles in the created path) to point the way. Note that when the attack begins, the "new_path" tiles return to the normal floor color whereas the room stays in the new color, which is why it was necessary to have two different types for what were almost the same type of tile.
- At the center of each room, I added an "activation tile" that triggers the new attack when the player walks into it. This prevents the enemies from spawning until after the player is ready and in the new room.

## Camera (main.py)
Another major challenge was dealing with the camera. I wanted the camera to always focus on the player, so the location in which I drew the background tiles and the enemies depended on the player's location. However, other objects, such as the player health bar and crosshair, should not move when the player moves. This required me to use two coordinate different coordinate systems in different contexts.

Some objects, such as the crosshair, needed to know its coordinates as well as it's player-adjusted coordinates. It needed to know its screen coordinates so that it drew on the correct part of the screen, and it needed to know its player-adjusted coordinates that it knew when it hit an collided with an enemy (which used player-adjusted coordinates).

As a base, I used youtuber ClearCode's code (see links in README.md) to draw the player-adjusted sprites. All sprites drawn in a way that changes with the location of the player are in the CameraGroup group, which had a custom_draw method that allowed them to be drawn in the manner described above. All other elements are just drawn using PyGames default drawing settings.

In pygame, things appear "on top of" or "behind" one another depending on the order they were drawn. The camera draws things in the following order so that things appear right:
1. First, it fills the screen with the background color
2. Draws background sprites (all tiles)
3. Draws foreground sprites (characters, wall tiles) These are drawn from the top of the screen to the bottom, so that things lower on the screen are in the front of things behind them.
4. Draws UI elements that follow the player (such as enemy health bars)
5. Draws a rectangle at the top of the screen in the background, as a backdrop for the other UI elements
6. Draws UI elements that don't follow the player (such as the player health bar, the score, and the crosshair)

## Characters (character.py, player.py, slime.py, dark_slime.py)
All characters in the game (the player, as well as the enemy characters such as the slime and dark slime) inherit methods/attributes from the "character class," which contains all the basic functionality they have in common. I seperated out the common attribute/methods into this class so that I didn't have to write the same code twice. It also made it much easier to add/change methods that relating to all of the different types of characters.

The character class includes attributes/methods relevant to all characters, such as the method that checks moves the sprite and checks for collisions, the method that animates the sprite to their next animation frame graphic, and the method for taking some given amount of damage. Each object of the character class also creates a "health counter" object (see below).

The player class inherits all these methods, and adds on additional methods, such as getting the user's keyboard input, checking to see if the player is touching the activation tile in the center of each room, and checking to see if the player has died.

The Slime and Dark slime classes are very similar, and it would even have been possible to put them into the same "GenericSlime" class. However, I decided not to do this because if I were to develop the game further, I would have added more differences to how the two types of enemies behave (especially in their movement patterns). At present, both classes inherit all the charecter methods and have some new enemy-specific methods such as updating its direction of movement to move toward the player, and checking to see if the enemy is touching the player's hitbox. Also of interest is the fact that the enemies collide with themselves, which I accomplished by adding the enemies to their own collision group. Then the existing collision methods in the character class did the work for me!

## Health Counters and Health Bars (health_bars.py)
Every character has a certain amount of health, but I wanted different types of characters to have different types of health bars. Specifically, I wanted the player's health bar to be placed in the top left and the enemy's health bar to be placed directly under the enemy itself. To solve this, I created two types of classes: a single HealthCounter class, which all character's have, HealthBar class. Each HealthCounter object has either a PlayerHealthBar or an EnemyHealthBar, depending on the type of character. I could have instead added a conditional in the Character class itself, but having this intermediate felt much more natural to me.

The HealthCounter class just creates either a PlayerHealthBar or an EnemyHealthBar object, depending on the type of character. It has two methods; one that relays information about the health of the character going down to the health bar, and one that relays if the HealthBar reached its last frame of the animation (i.e. the character died) to the character itself.

The HealthBar Class defines everything that a PlayerHealthBar and an EnemyHealthBar have in common. This includes things such as how to update the health bar graphic when a certain amount of damage is dealth.

The PlayerHealthBar class places a scaled up version of the health bar graphic in the top left of the screen. When the player takes damage, it updates the health bar to the next image (the image of the health bar with less health). When the end of the animation is reached, the object tells the HealthCounter that the player died.

The EnemyHealthBar class places a smaller version of the health bar graphic directly under its enemy. Upon the enemy's spawn, there is a brief animation of the health bar "booting up" to full health, during the time the enemy is unable to be attacked. Then, the health bar just updates its position to follow where the enemy goes. When the health bar reaches the last image in its animation (0 health), then it tells HealthCounter that the enemy died.

## Score Counter and Digit Classes (score.py)
Since each sprite can only have a single image (or at least that is what is the design norm in pygame), I needed a separate sprite for each of the digits displaying the score. However, I still wanted some central entity to control everything relating to the score. This is what lead me to create two classes: the ScoreCounter class, which stores/updates the score creates/updates each of the digits when the score changes, and the "Digit" class, which displays a particular digit of the score in the appropriate place. When the score is changed, the ScoreCounter class tells each of its Digit objects to update to their new digit.

## Attacking: The Crosshair (crosshair.py)
The Crosshair class creates the crosshair, which is the player's way to defend itself from the enemies. On a high level, it updates itself each frame to change its location to the location of the mouse pointer. The class has a method that is called by the game when the mouse is clicked, that checks for a collision between the crosshair and any enemies. It then damages any enemies that fit this requirement.

The main difficulty in creating the crosshair was storing two locations: the location it appeared on the screen, and its location in the player-adjusted coordinates (which was needed to check for collisions with the enemy sprites). However, this was solved by just storing two attributes for the crosshairs location. A "rect" attribute, to store its location on the screen, and an "adjusted_rect" attribute, which stored its player-adjusted location. Here, the "rect" attribute is a PyGame specific way of storing information about the location/size of a sprite.

## Powerups (potion.py)
I really wanted to implement power ups in this game, and the way I ended up doing it was sometimes spawning a potion sprite (1/3 chance) in a defeated room before a new room is created. The Potion class looks at the world map dictionary and finds a location with the tile type "new_room". The potion then chooses a random type (either giving the player speed, allowing the player to do double damage, or making the crosshair bigger). Finally, the potion waits for the player to walk into the potion. When this happens, the potion applies its effect, disappears, and spawns the new room for the player to explore.

Since this game was very difficult to survive very long, I made the choice for power ups to build on top of one another and never go away. In the future, I may change this.

## The Leaderboard (main.py)
I wanted scores to be saved across multiple playing sessions, so I allowed the game to access a CSV file that stores all the previous scores of the player. This was necessary because any variables within python are discarded as soon as the program ends- I needed a separate file to store the scores so that they could be accessed indefinitely. 

## Settings.py
For things which may change in future iterations of the game (for example: the FPS, the player movement speed, the scaling factor for the graphics, etc.), I used a separate python file called "settings.py". This allows the values to be easily changed, so that you don't have to search in each of the files to find a particular value to change.
