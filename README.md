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

### Background Isolation Nodes

#### Solid Background for Image

Given an image, isolate the background, find the predominant color,
and make an image the same size as the source, but a solid color
matching the background.

That might sound strange, but it is usefull for the next node which
lifts an image off of its background.

#### Lift Image and Mask from Background

Given an image, mask covering the subject, and an assumed blank
background (which you probably got with Solid Background for Image)...

Make an image and mask where the subject comes across directly, but
the background is represented as pixels with the most possible
transparency which will yield the original image if composited on the
background.

You can use this to pick objects and their shadows off of a neutral
background so you can composite them onto an image somewhere.

It might not work well on detailed backgrounds, but if you are trying
to make a pastable image, just get the AI to make your image on a
background at least a little close to what you want and it should work
well.

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

#### Load Image and Info from Path

Take a file pathname as a string, and load the image and its prompt,
workflow, and extra info blocks as dictionaries. The GIR Loopy Dir node
is one way to get a list of paths. The 'extra' information can come if
you used 'Save image with extra metadata' when you saved it. But, sadly, if
you pass in a 'dict' then it rips it apart and puts that all at the top
level of Image.info, so if that happened to you, there is an 'all' output
which has a copy of Image.info itself.

## TODO

- iterate the dict replace? need loop detection.
- master node to encompass texttostringlist, choosing, and dicts
- sneaky backdoor to dynamic prompt lookup?
- YAML to dictionary? (just word lookup, not general)
- dump node for string list
- dump node for dictionary
