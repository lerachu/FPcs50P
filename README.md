# Dietary mineral deficiency calculator
#### Video Demo:  <https://youtu.be/qd5qtbbptpo>
#### Description:

## data.csv
 Table with daily norms of minerals for different categories of people, taking into account age gender for people over nine(or equel) and pregnancy or lactation for women.

## requirments.txt 
 Libraries necessary for the program to work (requiring installation)

## test_project.py
 File with 4 unit tests:
##### 1. test_human_parser():
Test on correct determining command line arguments correctness and check on correct determining of human category
##### 2. test_count_mineral_norm_for_person():
 Test on correctness of output of information from a csv table (data.csv) for categories of people
##### 3. test_human(monkeypatch):
 Test on input processing using _monkeypatch_ and check on correct determining of human category
##### 4. test_food_plan_for_a_day(monkeypatch):
 Test on input processing using _monkeypatch_  and check on correct yielding results

## project.py
 File with a program for determining the daily mineral deficiency in the diet
#### How to use:
 * User can run the programm with or without the command line arguments. 
 * If user do not use command line arguments - he will further be prompted for necessary information.
 * All the instructions are displayed on the screen during program run.

#### Design
1. First program calls **parse_arguments** function that uses **argpars** library and returns _parser object_, then via this object checks if the user entered command line arguments.
2. 
* If they did, program calls **human_parser** function, which checks command line args on correctness and returns _None_ if incorrect, or else _"human category"_ as tuple.
If command line args are incorrect program **exits**.
* If they did not entered command line arguments, the program calls **human** function that will prompt user for necessary information until correct inputs, and next will return _"human category"_ as tuple.
3. Next, program creates _Minerals object_ by calling **Minerals.choose** method of **Minerals** class (which aссepts _"human category"_ as tuple mentioned above).
**_Minerals class objects_** aim to count the daily intake of minerals and compare them to norms. 
Its **"choose"** class method prompts user to choose the minerals of interest that they want to track (The list of minerals is in _microelements_ class variable). 
If user didn't choose any - the method returns None, else it returns call of **initialization** function with dict of chosen minerals (where "key" is mineral name, "value" is 0) and _"human category"_ as tuple.
**Initialization** function assings instance variable *_minerals* to delivered dict, and assigns instance variable *_norm* to return value of **norms_for_minerals** object, method which eccepts the _"human category"_ as tuple, and _Minerals object_. For each element in *minerals* dictionary of _Minerals object_ the function counts norms using **count_mineral_norm_for_person** class method that returns the norm for given _element_ and _"human category"_ from the __**data.csv**__ table. 
**norms_for_minerals** function returns dict of norms (where "key" is mineral name, "value" is norm from csv table).
**Initialization** function returns the _Minerals object_.
4. Next, program checks if user chose any mineral.
If not program **exits**.
5. Next, the program enters loop, where it iterate over **food_plan_for_a_day** generator function which prompts user for name of the food and its weight. Using **requests** library function searchs the food in the remote database and returns 5 options, from which user should choose more suitable one by the description. If there are no suitable options user types "n" and program prompts for better quiry.
If user chooses option , the function **yields** the tuple of chosen product and its weight.
For yielded tuple the program calls **add_food** instance method.
**add_food** instance method of **Minerals** class updates values in minerals dict (that tracks minerals intake of diet) if the mineral is contained in food, by calling **update** function on element (mineral) with counted weight (which updates dictionary).
**food_plan_for_a_day** generator function repetitevly prompts for food until empty string.
 Next, program calls **print_shortages** method on _Minerals object_, which calls **compare_with_norms** method, which counts mineral deficit in the diet; and then prints the deficit values for minerals.
 Then program asks user if he want to add more food. If user enters "n" program breaks out of the loop. 
 
