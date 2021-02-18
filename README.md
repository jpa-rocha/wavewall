# **WAVEWALL**

<br>

## **Description**:
WAVEWALL is an online synthesizer built using the tone.js javascript library, it allows the user to alter different parameters in order to create different patches.
The instrument can be played using the computer keyboard with keys "A" (C4) to "K" (C5) representing the white keys on a piano keayboard,
and "W", "E", "T", "Y" and "U" representing the black keys.

The synthesizer can be used without registering on any device with a phisical keyboard, 
although initially, the inclusion of MIDI control was planned, this feature was ultimatelly dropped due to time constraints.

If a user chooses to register they can name and save up to 10 different patches to reuse as presets.
In this case, all the parameters from the synthesizer are saved into the wavewall.db and can be called back using the list at the bottom of the page.

Should a user not be happy with any of their saved patches, they can access their user page at the top of the website, where their created patches are listed by name,
and delete any of their creations.

<br>

## **Project Structure**:
The project was divided in three main folders, **main** or project folder, **static** and **templates**:
  
<br>

### **Main**:
The main folder includes the app.py file which controls the website and communicates between the user and the database.
The app uses the configuration used in the "Finance" app from CS50.
It has the following 8 routes:

- **main**

    Renders the splash screen.

- **error**

    Takes in possible error messages from other pages and renders a page with the appropriate error number and message.

- **synth**

    This route serves two functions, first it collects the current status of all radio buttons, checkboxes and sliders from the synth.html page and inserts them into the database. Secondly, it queries the database according to patch name selected and loads the saved parameters into the synth.html page.

- **user**

    Renders the user.html page and lists patches after querying the database for patches saved under users user_id.
    It also listens to delete requests which allow the user to eliminate any saved patch.

- **login**

    Handles user log in, gives exceptions in case of username being wrong/inexistant in the database or when username/password is absent from form.

- **logout**

    Logs user out - taken from "Finance".

- **register**

    Handles user registration, insures that username is unique and that username and password were provided.

- **about**

    Renders the about.html page

Essential for the app functionality is also the helpers.py file in which two functions are defined:

- **empty**
    
    returns false if list is not empty, it is used for some database queries.

- **login_required**

    taken from "Finance", is a decorator that allows that part of the html is hidden to unlogged users.


Lastly gunicorn_config.py and Procfile allow that the app is deployed on Heroku.  

<br>

### **Static**:

This folder is itself devided into two different folders **css** and **js**.
The css folder includes the ***style.css*** file which is linked to in the layout.html, this file, not being essentia for the fnctionality of the program, is probably the one that could do with the most work, and it can definetely be revisited when there is a better understanding of layouts, color theory and other visual elements. That being said it is in working order.  

<br>

The js folder has two files, **tone.js** which is

 > ... a Web Audio framework for creating interactive music in the browser. The architecture of Tone.js aims to be familiar to both musicians and audio programmers creating web-based audio applications. On the high-level, Tone offers common DAW (digital audio workstation) features like a global transport for synchronizing and scheduling events as well as prebuilt synths and effects. Additionally, Tone provides high-performance building blocks to create your own synthesizers, effects, and complex control signals.

More information, examples and demos can be found at https://tonejs.github.io/.  
<br>

The second file, **script.js** defines the different parts of the synthesizer (the synthesizer itself, the filter and its envelope and the different effects) as constansts. The file also defines sixteen different functions that take information from the synth.html page and set the different paramaters of the synthesizers parts.  
The functions are:  

- **osc**  
    Controls the wave shape and the type of oscillator for the synthesizer.

- **moddis**  
    Determines the if the oscillator type selected is either  FM and AM  and disables the modulation field if any other type is selected.

- **fmopt**  
    Determines the modulating wave for the FM type oscillator.

- **amopt**  
    Determines the modulating wave for the AM type oscillator.

- **volumectr**  
    Sets the synthesizer volume if the power slider is set to "on".

- **filtopt**  
    Allows the user to switch between three filter types: lowpass, bandpass and highpass.

- **rollopt**  
    Defines the steepness of the wave curve.

- **cutoff**  
    Defines the cut-off frequency for the filter.

- **ampenvctr**  
    Sets the amplitude Attack, Decay, Sustain and Release.

- **filenvctr**  
    Sets the filter Attack, Decay, Sustain and Release.

- **chorusctr**  
    Defines if the chorus effect is turned on and modulates four different effect parameters: Depth, Frequency, Delay and Amount.
    If the effect is turned off it disables the paramater sliders.

- **reverbctr**  
    Defines if the reverb effect is turned on and modulates two different effect parameters: Decay and Amount.
    If the effect is turned off it disables the paramater sliders.

- **vibratoctr**  
    Defines if the vibrato effect is turned on and modulates three different effect parameters: Depth, Frequency, and Amount.
    If the effect is turned off it disables the paramater sliders.

- **transposerctr**  
    Transposes the synthesizer keyboard from the preset C4-C5 range, down to C2-C3 or up to C6-C7.

- **powercheck**  
    When turned the power slide is turned on the function grants the website permisssion to use the Web Audio API, and it defines the keyboard, .code was used in order to account for different keyboard layouts.
    When the power slider is turned off the volume is turned to -1000. This solution is surely not the best but it was the only that was found that maintained the applications fnctionality.

- **patchload**  
    Is a function that contains all the previous paramater functions (does not include powercheck()) and is called onload from layout.html body. It used in order to load the different parameter that are queried from the database, so that they are ready to play as soon as the page loads.

<br>

### **Templates**:  
The templates folder holds the seven different .html page that the user sees plus the **layout.html** page which functions as a base for all other pages except **main.html**.  




