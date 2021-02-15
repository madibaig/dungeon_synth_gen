from music21 import *
import random

# these matrices are the probabilities of picking that degree of the scale/mode
# according to what degree the previous note was
aeolianProbabilities = [[30, 40, 45, 55, 80, 85, 99],  # first note
                        [3, 55, 55, 60, 65, 70, 99],  # tonic
                        [40, 43, 70, 80, 85, 95, 99],  # supertonic
                        [15, 40, 43, 70, 85, 95, 99],  # mediant
                        [5, 15, 45, 48, 85, 95, 99],  # subdominant
                        [5, 10, 15, 50, 53, 90, 99],  # dominant
                        [10, 15, 20, 30, 65, 68, 99],  # submediant
                        [35, 40, 45, 50, 55, 95, 99]]  # leading
dorianProbabilities =  [[30, 40, 45, 55, 80, 85, 99],  # first note
                        [3, 55, 55, 60, 65, 70, 99],  # tonic
                        [40, 43, 70, 80, 85, 95, 99],  # supertonic
                        [15, 40, 43, 70, 85, 95, 99],  # mediant
                        [5, 15, 45, 48, 85, 95, 99],  # subdominant
                        [5, 10, 15, 50, 53, 90, 99],  # dominant
                        [10, 15, 20, 30, 65, 68, 99],  # submediant
                        [35, 40, 45, 50, 55, 95, 99]]  # leading
phrygianProbabilities =[[30, 40, 45, 55, 80, 85, 99],  # first note
                        [3, 55, 55, 60, 65, 70, 99],  # tonic
                        [40, 43, 70, 80, 85, 95, 99],  # supertonic
                        [15, 40, 43, 70, 85, 95, 99],  # mediant
                        [5, 15, 45, 48, 85, 95, 99],  # subdominant
                        [5, 10, 15, 50, 53, 90, 99],  # dominant
                        [10, 15, 20, 30, 65, 68, 99],  # submediant
                        [35, 40, 45, 50, 55, 95, 99]]  # leading
locrianProbabilities = [[30, 40, 45, 55, 80, 85, 99],  # first note
                        [3, 55, 55, 60, 65, 70, 99],  # tonic
                        [40, 43, 70, 80, 85, 95, 99],  # supertonic
                        [15, 40, 43, 70, 85, 95, 99],  # mediant
                        [5, 15, 45, 48, 85, 95, 99],  # subdominant
                        [5, 10, 15, 50, 53, 90, 99],  # dominant
                        [10, 15, 20, 30, 65, 68, 99],  # submediant
                        [35, 40, 45, 50, 55, 95, 99]]  # leading

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

"""
total_length returns the total length (in multiples of quarter note) of rhythms
where rhythms is a stream of duration objects
"""
def total_length(rhythms):
  sum = 0
  for d in rhythms:
    sum += d.quarterLength
  return sum

"""
generate_rhythms returns a list of durations (rhythms)
totalLength is the total length in quarter notes that the rhythms should sum to
shortestLength is the smallest length rhythm (in quarter notes) that can be used
longestLength is the longest length rhythm
interval is the possible rhythmic intervals between shortestLength and longest
that can be used to pick random durations

the function randomly generates for now, by adding a random multiple of 0.5 to
shortestLength for each rhythm
"""
def generate_rhythms(totalLength, shortestLength, longestLength, interval):
  #make a stream of durations (rhythms)
  #add random durations to the stream until motif_length is full then return
  rhythms = []
  lengthSoFar = 0
  while lengthSoFar < totalLength:
    randomDuration = shortestLength + \
                     interval * \
                     random.randint(0, int((longestLength - shortestLength)
                                           / interval))
    rhythms.append(duration.Duration(randomDuration))
    lengthSoFar += randomDuration
    pass
  if lengthSoFar != totalLength:
    lastDur = rhythms.pop().quarterLength
    rhythms.append(duration.Duration(totalLength - (lengthSoFar - lastDur)))
  return rhythms

"""
generate_melody returns a Measure stream object that contains a melody
keySig should be a key.Key object (the key used)
bars is the length of the melody in bars
motifLength is the length of the melodic phrase used in bars (this is not 
implemented yet so for now just put the same value as bars)
shortestLength is the shortest length rhythm that should be used in the melody
longestLength is the longest length rhythm
interval is the possible rhythmic intervals between shortestLength and longest
that can be used to pick random durations
"""

def generate_melody(
    keySig, bars, motifLength, shortestLength, longestLength, interval):
  motifRepeats = int(bars / motifLength)
  #generate the rhythms
  #then for each note/rhythm, pick a random pitch
  rhythms = generate_rhythms(motifLength * 4,
                             shortestLength, longestLength, interval)
  #remember to deal with motifLength

  motif = stream.Measure(number=1)
  motif.append(keySig)
  prevPitch = keySig.getPitches()[0]
  prevPitch.octave = 5

  for i in rhythms:
    if random.randint(0, 100) > 95:
      #10% chance of a rest note
      restNote = note.Rest()
      restNote.duration = i
      motif.append(restNote)
    else:
      tmpNote = note.Note()
      prevPitch = get_mode_pitch(prevPitch, keySig.mode, keySig)
      tmpNote.pitch = prevPitch
      tmpNote.duration = i
      motif.append(tmpNote)

  melody = stream.Measure()
  melody.repeatAppend(motif, motifRepeats)

  #vary the last motif repetition (25% chance)
  if random.randint(0, 3) > 1:
    lastMotif = melody.getElementsByClass(stream.Measure)[-1]
    #vary pitches of 4 last notes (possibly)
    numberOfPitchVaries = random.randint(1, 4)
    for n in range(1, numberOfPitchVaries):
      lastMotif[-n].pitch = \
        get_mode_pitch(lastMotif[-n].pitch, keySig.mode, keySig)
    #could add other possible varies like grace notes, rhythms, cutting notes

  return melody

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

  melody = generate_melody(keySig, 4, 2, 0.5, 1, 0.5)

  melody.show('text')
  melody.show('midi')
