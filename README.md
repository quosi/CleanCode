![CleanCode_CheatSheet](/img/CleanCode_CheatSheet.png "Clean Code Cheat-Sheet")

# Deploy CleanCode 

As this bundle of data analysis code grew to the medium size collection of a python scripts, it is perfect for a little Clean Code exercise. The following steps where applied in order to create an easy to use and clean python application. <br>
[>> Go straight to that clean python application & user instructions >>](src/README.md)

## STEP 1

<img align="right" width="300" src="img/screenshot1.png" alt="Original state, collection of python scripts">

Some steps to create a nice ditigal working environment for a clean start:
- initialise a git repository for version controll and link it to a remote URL
- create and/or activate your virtual environment for this project
- move working files like ```*.ipynb``` out of this repository or at least
- create a ```.gitignore``` file do hide certain files like ```notes.txt``` from git version controll

<img align="right" width="300" src="img/screenshot2.png" alt="Initialise git and clean up working files">

- draw diagram to plan code structure
- tea break ☕

<br><br><br><br>

## STEP 2

<img align="right" width="450" src="img/screenshot3.png" alt="Refactoring of code functionality into seperate function.">

Now its about time to dig into this code collection and start cleaning!
- delet unused imports
- restructure and refactor code as planed
- create python classes and modules to include all previously scattered processing functionality
- get rid of redundant / duplicate code
- make all function names camelCase
- rename variables to show there intention
- delet unnecessary functionality <br>
  like the processing of ```global max```, ```global min```, ```global mean``` and ```global average``` values in the example code
- deleted unnecessary columns from dataframe <br>
  like ```algo```, ```dm tools```, ```target``` and <br>```size``` values in the example code
- more tea ☕

<br><br><br>

## STEP 3

<img align="right" width="450" src="img/screenshot4.png" alt="Writing unittests with pytest for individual functions.">

- write unittests
- solve bugs 🐞
- add main.py script to inherit all processing functionality
- add command line interface for easy handling
- solve more bugs 🐜
- add documentation to functions and classes
- write ```requirements.txt``` to collect used python libraries
- write basic user instructions in ```README.md``` file for your git repository

<br><br><br>



