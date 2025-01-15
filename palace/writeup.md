# Project Writeup
Not actually a total writeup, just some notes.

## Choosing the game

## Code features

### Function type annotations

Function type annotations (`def foo() -> type`:) are something I had seen, but not used before. However, when I wrote my `__init__` and `__str__` functions, VSCode automatically added them, so I decided it was a good thing to add throughout my code. I learned that they do not actually force the function to return that value, but instead are just for documentation purposes. For some reason, though, you cannot use a type annotation of a class within the definition of that class; in those cases I opted to use `None` (I maybe could/should have used `any`).

### Programming style

Operating on objects in-place instead of returning a new object feels a bit weird to me. It's a little harder for me to understand and read -- it's less intuitive. However, this is OOP, so I will OOP.

### `turn` in the main loop

This one's a doozy. I actually used this or something like it in another project I did at some point -- I think. Can't remember which one or where to look at the moment. I still think it's clever, instead of writing both player turns, just write one and switch off. I guess some people never learn...
