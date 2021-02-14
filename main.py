from music21 import *
import random

# these matrices are the probabilities of picking that degree of the scale/mode
# according to what degree the previous note was
aeolianProbabilities = [[30, 40, 45, 55, 80, 85, 99],  # first note
                        [10, 55, 55, 60, 65, 70, 99],  # tonic
                        [40, 45, 70, 80, 85, 95, 99],  # supertonic
                        [15, 40, 45, 70, 85, 95, 99],  # mediant
                        [5, 15, 45, 50, 85, 95, 99],  # subdominant
                        [5, 10, 15, 50, 55, 90, 99],  # dominant
                        [10, 15, 20, 30, 65, 70, 99],  # submediant
                        [35, 40, 45, 50, 55, 60, 99]]  # leading
dorianProbabilities = [[30, 40, 45, 55, 80, 85, 99],  # first note
                        [10, 55, 55, 60, 65, 70, 99],  # tonic
                        [40, 45, 70, 80, 85, 95, 99],  # supertonic
                        [15, 40, 45, 70, 85, 95, 99],  # mediant
                        [5, 15, 45, 50, 85, 95, 99],  # subdominant
                        [5, 10, 15, 50, 55, 90, 99],  # dominant
                        [10, 15, 20, 30, 65, 70, 99],  # submediant
                        [35, 40, 45, 50, 55, 60, 99]]  # leading
phrygianProbabilities = [[30, 40, 45, 55, 80, 85, 99],  # first note
                        [10, 55, 55, 60, 65, 70, 99],  # tonic
                        [40, 45, 70, 80, 85, 95, 99],  # supertonic
                        [15, 40, 45, 70, 85, 95, 99],  # mediant
                        [5, 15, 45, 50, 85, 95, 99],  # subdominant
                        [5, 10, 15, 50, 55, 90, 99],  # dominant
                        [10, 15, 20, 30, 65, 70, 99],  # submediant
                        [35, 40, 45, 50, 55, 60, 99]]  # leading
locrianProbabilities = [[30, 40, 45, 55, 80, 85, 99],  # first note
                        [10, 55, 55, 60, 65, 70, 99],  # tonic
                        [40, 45, 70, 80, 85, 95, 99],  # supertonic
                        [15, 40, 45, 70, 85, 95, 99],  # mediant
                        [5, 15, 45, 50, 85, 95, 99],  # subdominant
                        [5, 10, 15, 50, 55, 90, 99],  # dominant
                        [10, 15, 20, 30, 65, 70, 99],  # submediant
                        [35, 40, 45, 50, 55, 60, 99]]  # leading

modeProbMatrices = {
  "aeolian": aeolianProbabilities,
  "dorian": dorianProbabilities,
  "phrygian": phrygianProbabilities,
  "locrian": locrianProbabilities
}

"""
prevPitch is a pitch.Pitch object of the previous note in the melody
mode is a str (aeolian|dorian|phyrgian|locrian)
keySig is a key.Key object (the mode keysignature)
getModePitch uses modeProbMatrices to get a random note from the mode depending
on the previous pitch (returns a pitch.Pitch object) and sets the octave so that
the interval between prevPitch and the next pitch is small as can be
"""


def get_mode_pitch(prevPitch, mode, keySig):
  degree = keySig.getScaleDegreeFromPitch(prevPitch) - 1
  randomInt = random.randint(0, 99)
  chosenPitch = pitch.Pitch()

  #pick random degree of mode
  probArray = modeProbMatrices.get(mode)[degree + 1]
  for n in range(7):
    if randomInt < probArray[n]:
      chosenPitch = keySig.getPitches()[n]
      break

  #choose octave so its the smallest interval to prevPitch
  chosenPitch.octave = 5
  if abs(prevPitch.midi - (chosenPitch.midi - 12)) < abs(prevPitch.midi - chosenPitch.midi):
    chosenPitch.octave -= 1
  elif abs(prevPitch.midi - (chosenPitch.midi + 12)) < abs(prevPitch.midi - chosenPitch.midi):
    chosenPitch.octave += 1

  return chosenPitch

if __name__ == '__main__':
  # pick a random mode
  # so random mode from aeolian, dorian, phrygian, locrian
  randomNum = random.randint(1, 4)
  mode = ""
  if randomNum == 1:
    mode = "aeolian"
  elif randomNum == 2:
    mode = "dorian"
  elif randomNum == 3:
    mode = "phrygian"
  elif randomNum == 4:
    mode = "locrian"

  keySig = key.Key()
  keySig.mode = mode

  # pick random tonic for the mode
  keySig.tonic = pitch.Pitch(random.randint(0, 11))

  #keySig.show('text')

  melody = stream.Measure(number=1)
  melody.append(keySig)
  prevPitch = keySig.getPitches()[0]
  prevPitch.octave = 5
  for i in range(16):
    tmpNote = note.Note()
    prevPitch = get_mode_pitch(prevPitch, mode, keySig)
    tmpNote.pitch = prevPitch
    #print (tmpNote.pitch.ps)
    #print(tmpNote.nameWithOctave)
    melody.append(tmpNote)

  melody.show('text')
  melody.show('midi')
