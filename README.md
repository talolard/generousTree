# GenerousTree
## An opinionated framework for LED light programming. 
GenerousTree is an art project to be displayed at Midburn 2016. Part of the project is the programming of lots of LED lights, to make interesting and beutiful patterns. Thats where this library comes in. 

## Design
Animating led strips on a structure sets forth a certain set of challanges. Structures tend to have sections, which we may want to light up independtly but also have some subtle relation between the sections. We definetly want to maintain some aesthetic cohesivness, as opposed to haveing some totally random display going on. 
### Section
A section in GT is some collection of LED pixels on a strip. The whole strip (lets say 25 LEDs) could be a section which we would control. But what if we want to wrap the tree around a cylander which 5 LEDs per slice, like a tree trunk? We could break down the whole strip into a 5X5 2d array like so
***Original***
```
PPPPPPPPPPPPPPPPPPPPPPPPP
```
***Sectioned***
```
PPPPP
PPPPP
PPPPP
PPPPP
PPPPP
```
Each section has a collection of pixels on the strip a frame rate paramter and a transition function. Some higher scope maintains a counter, the current frame number, and each section checks if it should apply it's transformation to itself given the current frame number. 
Say we have a Section with frame rate 3 and a global frame counter (GFC). We would apply the transition function eveytime GFC %frameRate==0
| GFC           | GFC %frameRate| transform? |
| ------------- |:-------------:| -----:|
| 0             | 0             | true  |
| 1             | 1             | false |
| 2             | 2             | false |
| 3             | 3             | true  |
| 4             | 4             | false |

The beauty of this is that each section can have its own frame rate, thus allowing us to run a few sections at different speeds or create effects of acceleration.

###SectionCollection
The SectionCollection is, as you may have guessed, a collection of sections. Its job is make sure that all of the sections play nice. For example, a section collection like the 2d array we had above would be a collection of 5 sections, each with (in this case 5 pixels). 
The section collection could set the frame rate between them so that the top updates quickly and the bottom slowly, or perhaps define a series of transformations with some ordered parameter for example
```python
transformations = [(lambda x:x**np.sin(a)) for a,item in range(len(SectionCollection.sectons))]

