//attach a click listener to a play button
document.querySelector('#start')?.addEventListener('click', async () => {
    await Tone.start()
    console.log('audio is ready')
})
//instrument setup
const poly = new Tone.PolySynth(Tone.Synth).toDestination();
poly.set({
  voice0 : {
    oscillator :{
      type : "square"
    }
  },
  voice1 : {
    oscillator: {
      type : "square"
    }
  },
  maxPolyphony : 12,
  volume : -10
});

// Oscilloscope setup
var oscilloscope = new Nexus.Oscilloscope('#oscilloscope')
oscilloscope.connect(poly)
oscilloscope.bufferLength = 64;

// Values recieved from user input
//
// Wave type for Oscillator 1
// Select square wave
var square1 = document.getElementById("square1");
square1.oninput = function(){
if(square1.checked) {
  poly.set({
    voice0 : {
      oscillator :{
        type : this.value
      }
    }
  });
}}

// Select sawtooth wave
var saw1 = document.getElementById("saw1");
saw1.oninput = function(){
if(saw1.checked) {
  poly.set({
    voice0 : {
      oscillator :{
        type : this.value
      }
    }
  });
}}

// Select sine wave
var sine1 = document.getElementById("sine1");
sine1.oninput = function(){
if(sine1.checked) {
  poly.set({
    voice0 : {
      oscillator :{
        type : this.value
      }
    }
  });
}}

// Values for Oscillator 2
//
// Wave type for Oscillator 2
// Select square wave
var square2 = document.getElementById("square2");
square2.oninput = function(){
if(square2.checked) {
  poly.set({
    voice1 : {
      oscillator :{
        type : this.value
      }
    }
  });
  }}

// Select sawtooth wave
var saw2 = document.getElementById("saw2");
saw2.oninput = function(){
if(saw2.checked) {
  poly.set({
    voice1 : {
      oscillator :{
        type : this.value
      }
    }
  });
}}

// Select sine wave
var sine2 = document.getElementById("sine2");
sine2.oninput = function(){
if(sine2.checked) {
  poly.set({
    voice1 : {
      oscillator :{
        type : this.value
      }
    }
  });
}}

// Volume control
var sourcevol = document.getElementById("vol1");
sourcevol.oninput = function() {
  poly.set({
    volume : this.value
  });
  }

// Harmonicity control
var freq = document.getElementById("freq");
freq.oninput = function() {
  poly.set({
    harmonicity : this.value
  });
}

// Values for Filter
//
// Determine filter type
// Select low-pass filter
var lowpass = document.getElementById("lowpass");
lowpass.oninput = function() {
if(lowpass.checked) {
  poly.set({
    voice0 : {
      filter :{
        type : this.value
      }
    },
    voice1 : {
      filter : {
        type : this.value
      }
    }
  });
}}

//Select high-pass filter
var highpass = document.getElementById("highpass");
highpass.oninput = function() {
if(highpass.checked) {
  poly.set({
    voice0 : {
      filter : {
        type : this.value
      }
    },
    voice1 : {
      filter : {
        type : this.value
      }
    }
  });
}}

// Determine cutoff
var cutoff = document.getElementById("cutoff");
cutoff.oninput = function() {
    poly.set({
        voice0 : {
          filter : {
            frequency : this.value
          }
        },
        voice1 : {
          filter : {
            frequency : this.value
          }
        }
      });
      console.log("test")
    }

// Amplitude envelope control
// Attack
var attacka = document.getElementById("attacka");
attacka.oninput = function() {
  poly.set({
    voice0 : {
      envelope : {
        attack : this.value
      }
    },
    voice1 : {
      envelope : {
        attack : this.value
      }
    }
  });
}

// Decay
var decaya = document.getElementById("decaya");
decaya.oninput = function() {
  poly.set({
    voice0 : {
      envelope : {
        decay : this.value
      }
    },
    voice1 : {
      envelope : {
        decay : this.value
      }
    }
  });
}

// Sustain
var sustaina = document.getElementById("sustaina");
sustaina.oninput = function() {
  poly.set({
    voice0 : {
      envelope : {
        sustain : this.value
      }
    },
    voice1 : {
      envelope : {
        sustain : this.value
      }
    }
  });
}

// Release
var releasea = document.getElementById("releasea");
releasea.oninput = function() {
  poly.set({
    voice0 : {
      envelope : {
        release : this.value
      }
    },
    voice1 : {
      envelope : {
        release : this.value
      }
    }
  });
}


// Filter envelope control
// Attack
var attackf = document.getElementById("attackf");
attackf.oninput = function() {
  poly.set({
    voice0 : {
      filterEnvelope : {
        attack : this.value
      }
    },
    voice1 : {
      filterEnvelope : {
        attack : this.value
      }
    }
  });
}

// Decay
var decayf = document.getElementById("decayf");
decayf.oninput = function() {
  poly.set({
    voice0 : {
      filterEnvelope : {
        decay : this.value
      }
    },
    voice1 : {
      filterEnvelope : {
        decay : this.value
      }
    }
  });
}

// Sustain
var sustainf = document.getElementById("sustainf");
sustainf.oninput = function() {
  poly.set({
    voice0 : {
      filterEnvelope : {
        sustain : this.value
      }
    },
    voice1 : {
      filterEnvelope : {
        sustain : this.value
      }
    }
  });
}

// Release
var releasef = document.getElementById("releasef");
releasef.oninput = function() {
  poly.set({
    voice0 : {
      filterEnvelope : {
        release : this.value
      }
    },
    voice1 : {
      filterEnvelope : {
        release : this.value
      }
    }
  });
}



// keyboard keys
var QWERTZ = [
    "a", "w", "s", "e", "d", "f", "t", "g", "z", "h", "u", "j", "k"
];
var notes = [
    "C4", "C#4", "D4", "D#4", "E4", "F4", "F#4", "G4", "G#4", "A4", "A#4", "B4", "C5"
];
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

// testing button
function play(){
    console.log(poly.get())
    console.log(poly.voice0.get);
    console.log(pressed)
  }