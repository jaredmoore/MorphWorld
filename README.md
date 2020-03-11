# morphing-block-dude

Visualizer:

https://cis.gvsu.edu/~moorejar/Visualizer/visualizer.html

UML [In-Progress]:
https://www.lucidchart.com/invitations/accept/8c41399f-97e7-46bf-9aef-fc4781d9a59c

Notes:

- The coordinates in this code represent the center of each block. However, in the visualizer, coordinates represent each intersect.
- Morphs and Movement cannot occur on the same frame
- Morphs from an odd to even height/width will force the morphology to shift to the a negative y/z slightly (positive when negative is impossible) to mantain discrete coordinate values. 