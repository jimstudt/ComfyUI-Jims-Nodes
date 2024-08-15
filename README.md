# Jim's ComfyUI Nodes

## Grumpy Old Man Notice

Because, MY GOD PEOPLE! Would it kill you to write a line of instuction
on how to use a node? Between trying to sort out obsolete nodes and finding
just the right set of nodes which will perform a function together then
having that mess on my screen... It's just got to be easier to write my own.

## Promises

- I promise nothing. If I have accidentally left this somewhere and you
  found it, maybe just move along. This is just me scratching my own itches.

## Nodes

### Zoom and Enhance Nodes

#### Zoom On Segment

Find the largest segment in the segs and crop the image to it. You can 
specify a padding percentage for each side.

You also get to specify about how many megapixels you want the cropped
image to ultimately be. That is used to compute the "upscale_by"
output which is just perfect for running into The Ultimate Upscaler.

Use this to crop to your main character in a larger scene, or to their
face.  For faces you probably want the bottom pad to be larger than
the others.

### String Lists

#### Text To String List

Take a block of text, strip out blank lines and comments (begin with
'#'). Whitespace trim the surviving lines and put them into a list of
strings. 

You can have an optional prefix, also a string list. If present it
will show up at the front of the result.  So you can chain these.

#### Choose From String List

Choose a random string from a list of strings. It returns an empty
string if there are none in the list.

The string list passes through so you can chain these.

### Text Dictionary Nodes

#### Define Word

Take an optional dictionary, a key, and value and set the key to that
value. If there is no input dictionary, then it is assumed to be
empty.

#### Lookup Word

Take a dictionary and a key and look up the corresponding word.  Empty
string results key is not defined.  The dictionary passes through for
chaining.

#### Substitute Words

Take a dictionary and a string and swap in the definition for each
word where it appears in the string.

DANGER: Currently, one pass in random but descending keylength order! Probably
want to iterate until stable, so definitions can include other keys.
Keylength order prevents EYE from matching EYECOLOR.

Passes through the dictionary for your chaining pleasure.


## TODO

- iterate the dict replace? need loop detection.
- master node to encompass texttostringlist, choosing, and dicts
- sneaky backdoor to dynamic prompt lookup?
- YAML to dictionary? (just word lookup, not general)
- dump node for string list
- dump node for dictionary
