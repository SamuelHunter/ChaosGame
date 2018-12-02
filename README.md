# ChaosGame
Method for randomly creating a fractal within a given polygon

This program follows an iterative (non-recursive) algorithm to create fractals:
  1. Start from a random point within the polygon
  2. Go to the midpoint of the current point and a randomly selected vertex
  3. Repeat steps 1 and 2 until picture is suitable
  
Parameters:\
  -Regular polygon or custom points\
  -Polygon sides, radius, center, rotation\
  -No repeats (prevents same vertex from being chosen twice in a row)\
  -Factor for midpoint (eg move 1/3 distance between current point and midpont instead of 1/2)\
  -Dot resolution and scale\
  -Colors
  
Examples:

Serpinski's Triangle (10^6 dots)
![](https://github.com/SamuelHunter/ChaosGame/blob/master/Chaos_Game_3_10^6_color.png)

Square (10^5 dots, no repeats)
![](https://github.com/SamuelHunter/ChaosGame/blob/master/Chaos_Game_4_10^5_norepeat_color.png)

Pentagon (10^5 dots)
![](https://github.com/SamuelHunter/ChaosGame/blob/master/Chaos_Game_5_10^5_norepeat_color.png)

[Read more here](https://en.wikipedia.org/wiki/Chaos_game)\
[Also look at this](http://www.shodor.org/interactivate/activities/TheChaosGame/)
