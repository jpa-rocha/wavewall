// MIDI setup

//attach a click listener to a play button
document.querySelector('#start')?.addEventListener('click', async () => {
    await Tone.start()
    console.log('audio is ready')
})
//instrument setup
const poly = new Tone.PolySynth();
poly.set({
    oscillator : {
        type : "square"
    },
  maxPolyphony : 36,
  volume : -10
});
const filter = new Tone.Filter();
const filterenv = new Tone.FrequencyEnvelope();
filterenv.set({
    baseFrequency : 5000
})

// Effects
// Chorus
const chorus = new Tone.Chorus();
chorus.set({
    wet : 0
});

// Reverb
const reverb = new Tone.Reverb();
reverb.set({
    wet : 0
});

// Vibrato 
const vibrato = new Tone.Vibrato();
vibrato.set({
    wet : 0
});

filterenv.connect(filter.frequency)

poly.chain(filter, chorus, reverb, vibrato, Tone.Destination);

// Values recieved from user input
// Wave type for Oscillator
function osc() {
    var wavetype = ["plain", "fat", "fm", "am", "square", "saw", "triangle", "sine"];
    var selection = [];
    var checker;
    var i;
    for (i = 0; i < wavetype.length; i++) {
        checker = document.getElementById(wavetype[i])
        if (checker.checked) {
            selection.push(checker.value)
        }}
        poly.set({
            oscillator :{
              type : selection.join("")
            }
        });
    }

// Modulation Options
// Disabling unselected oscillator types
function moddis(){
    var options = ["plain", "fat", "fm", "am"];
    var i;
    var checker;
    for (i = 0; i < options.length; i++) {  
        checker = document.getElementById(options[i])
        if(checker.checked) {
            if (options[i] == "fm"){
                document.getElementById("fmfieldset").disabled = false;
            }
            if(options[i] != "fm"){
                document.getElementById("fmfieldset").disabled = true;
            }
            if (options[i] == "am") {
                document.getElementById("amfieldset").disabled = false;
            }
            if(options[i] != "am") {
                document.getElementById("amfieldset").disabled = true;
            }
      }
    }
}

// FM options
function fmopt(){
    // Wave modulation selection
    var wavetype = ["fmsquare", "fmsaw", "fmtriangle", "fmsine"];
    var selection = document.getElementById("fm");
    var checker;
    var i;
    if(selection.checked) {
        poly.set({
            oscillator :{
              modulationType : "square"
            }
        });
        for (i = 0; i < wavetype.length; i++) {
        checker = document.getElementById(wavetype[i])
        if (checker.checked) {
            poly.set({
                oscillator :{
                  modulationType : checker.value
                }
            });
            }
        }
    }
}


// AM options
function amopt(){
    var wavetype = ["amsquare", "amsaw", "amtriangle", "amsine"];
    var selection = document.getElementById("am");
    var checker;
    var i;
    if(selection.checked) {
        poly.set({
            oscillator :{
              modulationType : "square"
            }
        });
        for (i = 0; i < wavetype.length; i++) {
        checker = document.getElementById(wavetype[i])
        if (checker.checked) {
            poly.set({
                oscillator :{
                  modulationType : checker.value
                }
            });
        }
        }
    }
}

// FAT options -> disabled

// PWM options -> disabled



// Volume control
function volumectr() {
var sourcevol = document.getElementById("vol")
  poly.set({
    volume : sourcevol.value
  });
}


// Values for Filter
//
// Determine filter type
function filtopt() {
    var types = ["lowpass", "bandpass", "highpass"]
    var i;
    var checker;
    for (i = 0; i < types.length; i++) {
        checker = document.getElementById(types[i]);
        if (checker.checked) {
            filter.set({
                type : checker.value
            })
        }
    }
}

// Determine Roll-off
function rollopt() {
    var roll = ["r12", "r24", "r48", "r96"]
    var i;
    var checker;
    for (i = 0; i < roll.length; i++) {
        checker = document.getElementById(roll[i]);
        if (checker.checked) {
            filter.set({
                rolloff : checker.value
            })
        }
    }
}

// Determine cutoff
function cutoffctr() {
    var co = document.getElementById("cutoff")
    filterenv.set({
        baseFrequency : co.value
    });
}

// Amplitude envelope control
function ampenvctr() {
    var attacka = document.getElementById("attacka");
    var decaya = document.getElementById("decaya");
    var sustaina = document.getElementById("sustaina");
    var releasea = document.getElementById("releasea");
    poly.set({
        envelope : {
            attack : attacka.value,
            decay : decaya.value,
            sustain : sustaina.value,
            release : releasea.value
        }
        });
    }


// Filter envelope control
function filenvctr() {
    var attackf = document.getElementById("attackf");
    var decayf = document.getElementById("decayf");
    var sustainf = document.getElementById("sustainf");
    var releasef = document.getElementById("releasef");
        filterenv.set({
            attack : attackf.value,
            decay : decayf.value,
            sustain : sustainf.value,
            release : releasef.value
        })
}


// Effect control

// Chorus
function chorusctr() {
    var choruscheck = document.getElementById("choruscheck");
    var depth = document.getElementById("depthchorus");
    var freq = document.getElementById("freqchorus");
    var delay = document.getElementById("delaychorus");
    var amount = document.getElementById("wetchorus");
    if (choruscheck.checked == true) {
        depth.disabled = false;
        freq.disabled = false;
        delay.disabled = false;
        amount.disabled = false;
        chorus.set({
            depth : depth.value,
            frequency : freq.value,
            delayTime : delay.value,
            wet : amount.value
        });    
    }
    else {
        depth.disabled = true;
        freq.disabled = true;
        delay.disabled = true;
        amount.disabled = true;
        chorus.set({
            wet : 0
        });
    }
}

// Reverb
function reverbctr() {
    var reverbcheck = document.getElementById("reverbcheck");
    var decay = document.getElementById("decayreverb");
    var amount = document.getElementById("wetreverb");
    if (reverbcheck.checked == true) {
        decay.disabled = false;
        amount.disabled = false;
        reverb.set({
            decay : decay.value,
            wet : amount.value
        });
    }
    else {
        decay.disabled = true;
        amount.disabled = true;
        reverb.set({
            wet : 0
        });
    }
}

// Vibrato
function vibratoctr(){
    var vibratocheck = document.getElementById("vibratocheck");
    var depth = document.getElementById("depthvibrato");
    var freq = document.getElementById("freqvibrato");
    var amount = document.getElementById("wetvibrato" );
    if (vibratocheck.checked == true){    
        depth.disabled = false;
        freq.disabled = false;
        amount.disabled = false;
        vibrato.set({
            depth : depth.value,
            frequency : freq.value,
            wet : amount.value
        });
    }
    else {
        depth.disabled = true;
        freq.disabled = true;
        amount.disabled = true;
        vibrato.set({
            wet : 0
        });
    }
}

// keyboard keys
var QWERTZ = [
    "a", "w", "s", "e", "d", "f", "t", "g", "z", "h", "u", "j", "k"
];

// transposing
var notes = [
    "C4", "C#4", "D4", "D#4", "E4", "F4", "F#4", "G4", "G#4", "A4", "A#4", "B4", "C5"
];
function transposerctr() {
    var transpose = document.getElementById("transposer");
    var i;
    var note;
    var octave;
    var checker;
    var ccount = 0
    for (i = 0; i < notes.length; i ++) {
        
        octave = transpose.value;
        checker = notes[i];
        if  (checker.charAt(0) == "C" && checker.length < 3) {
            ccount += 1;
        }
        if (ccount >= 2) {
            octave = Number(transpose.value) + 1
        }
        note = notes[i].slice(0,-1) + String(octave);
        notes[i] = note;
    }
}

var power = document.getElementById("power")
if (power.checked == true) {
    console.log("power on")
}
var pressed = new Set();
    document.addEventListener("keydown", (event) => {
    if (QWERTZ.includes(event.key)) {
        pressed.add(event.key);
        if (pressed.has(event.key)) {
            if (event.repeat == true){
                return;
         }
        poly.triggerAttack(notes[QWERTZ.indexOf(event.key)]);
        console.log(poly.activeVoices);
    }
    }})
    document.addEventListener("keyup", (event) => {
    if (pressed.has(event.key)) {
        pressed.delete(event.key);
        poly.triggerRelease(notes[QWERTZ.indexOf(event.key)]);
    }
    if (pressed.has(event.key) == false) {
        poly.triggerRelease(notes[QWERTZ.indexOf(event.key)]);
    }
    })


// Load function
function patchload(){
    osc();
    moddis();
    fmopt();
    amopt();
    filtopt();
    rollopt();
    cutoffctr();
    ampenvctr();
    filenvctr();
    chorusctr();
    reverbctr();
    vibratoctr();
    transposerctr();
    volumectr();
  }