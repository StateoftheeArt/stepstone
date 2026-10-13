// Signature behaviors use only parts present in the approved artwork.
export const PIP_PERSONALITIES={
  "fox": {
    "playLabel": "Follow a firefly",
    "hello": "sniffs hello and curls its tail.",
    "response": "tracks a firefly with a curious tail swish.",
    "snack": "settles in for a careful little nibble.",
    "part": ".sprite-tail",
    "greetFrames": [
      "none",
      "rotate(-10deg)",
      "rotate(7deg)",
      "none"
    ],
    "playFrames": [
      "none",
      "rotate(-18deg)",
      "rotate(14deg)",
      "rotate(-8deg)",
      "none"
    ],
    "idleFrames": [
      "none",
      "rotate(-5deg)",
      "none"
    ],
    "bodyFrames": [
      "none",
      "translateX(-2px) rotate(-2deg)",
      "translateX(3px) rotate(2deg)",
      "none"
    ],
    "toy": "firefly",
    "duration": 1900,
    "origin": "47px 50px",
    "idleDuration": 5.8
  },
  "cat": {
    "playLabel": "Chase the yarn",
    "hello": "gives a slow blink and a soft tail curl.",
    "response": "reaches for a gently rolling ball of yarn.",
    "snack": "takes a nibble, then tidies its whiskers.",
    "part": ".sprite-tail",
    "greetFrames": [
      "none",
      "rotate(8deg)",
      "rotate(-5deg)",
      "none"
    ],
    "playFrames": [
      "none",
      "rotate(18deg)",
      "translateY(-2px) rotate(-12deg)",
      "none"
    ],
    "idleFrames": [
      "none",
      "rotate(4deg)",
      "rotate(-2deg)",
      "none"
    ],
    "bodyFrames": [
      "none",
      "scaleY(.94) scaleX(1.06)",
      "translateX(4px) rotate(3deg)",
      "none"
    ],
    "toy": "yarn",
    "duration": 2200,
    "origin": "45px 50px",
    "idleDuration": 5.93
  },
  "frog": {
    "playLabel": "Hop to the ripple",
    "hello": "dips its head in a friendly nod.",
    "response": "crouches, hops and lands beside a ripple.",
    "snack": "takes a bite and gives a contented little nod.",
    "part": ".sprite-feet",
    "greetFrames": [
      "none",
      "scaleY(.94)",
      "none"
    ],
    "playFrames": [
      "none",
      "scaleY(.84)",
      "translateY(-5px) scaleY(1.04)",
      "none"
    ],
    "idleFrames": [
      "none",
      "scaleY(.97)",
      "none"
    ],
    "bodyFrames": [
      "none",
      "scaleY(.87)",
      "translateY(-9px)",
      "translateY(-2px)",
      "none"
    ],
    "toy": "ripple",
    "duration": 1600,
    "origin": "32px 57px",
    "idleDuration": 6.06
  },
  "axolotl": {
    "playLabel": "Make a bubble",
    "hello": "fans its feathery gills to say hello.",
    "response": "ripples its gills as a bubble floats past.",
    "snack": "nibbles softly while its gills settle.",
    "part": ".sprite-gills",
    "greetFrames": [
      "none",
      "scaleX(1.09)",
      "scaleX(.98)",
      "none"
    ],
    "playFrames": [
      "none",
      "scaleX(1.15)",
      "scaleX(.9)",
      "scaleX(1.07)",
      "none"
    ],
    "idleFrames": [
      "none",
      "scaleX(1.035)",
      "none"
    ],
    "bodyFrames": [
      "none",
      "translateX(-2px) rotate(-2deg)",
      "translateX(2px) rotate(2deg)",
      "none"
    ],
    "toy": "bubble",
    "duration": 2400,
    "origin": "32px 29px",
    "idleDuration": 6.19
  },
  "owl": {
    "playLabel": "Catch a feather",
    "hello": "tilts its head and offers a small wing greeting.",
    "response": "opens its wings to catch a falling feather.",
    "snack": "takes a small bite and looks quietly satisfied.",
    "part": ".sprite-wings",
    "greetFrames": [
      "none",
      "scaleX(1.04)",
      "none"
    ],
    "playFrames": [
      "none",
      "scaleX(1.2)",
      "scaleX(.94)",
      "scaleX(1.1)",
      "none"
    ],
    "idleFrames": [
      "none",
      "scaleX(1.02)",
      "none"
    ],
    "bodyFrames": [
      "none",
      "rotate(-5deg)",
      "rotate(4deg) translateY(-2px)",
      "none"
    ],
    "toy": "feather",
    "duration": 2100,
    "origin": "32px 39px",
    "idleDuration": 6.32
  },
  "bunny": {
    "playLabel": "Follow the clover",
    "hello": "perks up both ears to listen.",
    "response": "raises its ears and hops toward a clover leaf.",
    "snack": "nibbles and lets its ears relax.",
    "part": ".sprite-ears",
    "greetFrames": [
      "none",
      "scaleY(1.06)",
      "rotate(-3deg)",
      "none"
    ],
    "playFrames": [
      "none",
      "scaleY(.94)",
      "translateY(-3px) scaleY(1.08)",
      "none"
    ],
    "idleFrames": [
      "none",
      "rotate(-2deg)",
      "rotate(2deg)",
      "none"
    ],
    "bodyFrames": [
      "none",
      "scaleY(.94)",
      "translateY(-7px)",
      "none"
    ],
    "toy": "clover",
    "duration": 1700,
    "origin": "32px 22px",
    "idleDuration": 6.45
  },
  "robot": {
    "playLabel": "Scan the signal",
    "hello": "lights up its eyes in a friendly scan.",
    "response": "scans a signal and makes two measured robot steps.",
    "snack": "pauses for a little recharge.",
    "part": ".sprite-eyes",
    "greetFrames": [
      "none",
      "translateX(-1px)",
      "translateX(1px)",
      "none"
    ],
    "playFrames": [
      "none",
      "translateX(-2px)",
      "scaleY(.75)",
      "translateX(2px)",
      "none"
    ],
    "idleFrames": [
      "none",
      "translateX(.6px)",
      "translateX(-.6px)",
      "none"
    ],
    "bodyFrames": [
      "none",
      "translateX(-3px)",
      "translateX(3px)",
      "none"
    ],
    "toy": "signal",
    "duration": 1800,
    "origin": "32px 27px",
    "idleDuration": 6.58
  },
  "cloud": {
    "playLabel": "Make a rainbow",
    "hello": "drifts closer and lets a few drops ripple.",
    "response": "floats beneath a small rainbow as its raindrops dance.",
    "snack": "rests for a moment beneath a warm glow.",
    "part": ".sprite-rain",
    "greetFrames": [
      "none",
      "translateY(1px)",
      "none"
    ],
    "playFrames": [
      "none",
      "translateY(3px)",
      "translateY(-1px)",
      "translateY(2px)",
      "none"
    ],
    "idleFrames": [
      "none",
      "translateY(1.3px)",
      "none"
    ],
    "bodyFrames": [
      "none",
      "translate(-3px,-4px)",
      "translate(3px,-6px)",
      "none"
    ],
    "toy": "rainbow",
    "duration": 2700,
    "origin": "32px 47px",
    "idleDuration": 6.71
  },
  "duck": {
    "playLabel": "Paddle the pond",
    "hello": "gives a small wing wave.",
    "response": "waddles into a pond ripple with its wings out.",
    "snack": "takes a nibble and gives a pleased wing tuck.",
    "part": ".sprite-wings",
    "greetFrames": [
      "none",
      "scaleX(1.07)",
      "none"
    ],
    "playFrames": [
      "none",
      "rotate(-5deg) scaleX(1.1)",
      "rotate(5deg) scaleX(.96)",
      "none"
    ],
    "idleFrames": [
      "none",
      "scaleX(1.025)",
      "none"
    ],
    "bodyFrames": [
      "none",
      "translateX(-4px) rotate(-4deg)",
      "translateX(4px) rotate(4deg)",
      "none"
    ],
    "toy": "pond",
    "duration": 1800,
    "origin": "32px 39px",
    "idleDuration": 6.84
  },
  "penguin": {
    "playLabel": "Slide to the snowflake",
    "hello": "opens its flippers in a friendly welcome.",
    "response": "shuffles, leans and slides toward a snowflake.",
    "snack": "takes a bite and settles its flippers.",
    "part": ".sprite-wings",
    "greetFrames": [
      "none",
      "scaleX(1.08)",
      "none"
    ],
    "playFrames": [
      "none",
      "scaleX(1.2)",
      "rotate(-6deg)",
      "rotate(6deg)",
      "none"
    ],
    "idleFrames": [
      "none",
      "rotate(-1.5deg)",
      "none"
    ],
    "bodyFrames": [
      "none",
      "rotate(-5deg)",
      "translateX(7px) rotate(5deg)",
      "none"
    ],
    "toy": "snowflake",
    "duration": 2200,
    "origin": "32px 38px",
    "idleDuration": 6.97
  },
  "turtle": {
    "playLabel": "Peek from the shell",
    "hello": "peeks up slowly to greet you.",
    "response": "tucks a little into its shell, then peeks back out.",
    "snack": "takes a slow nibble before peeking up again.",
    "part": ".sprite-head",
    "greetFrames": [
      "none",
      "translateY(-1px)",
      "rotate(3deg)",
      "none"
    ],
    "playFrames": [
      "none",
      "translateY(3px) scale(.91)",
      "translateY(-2px) scale(1.02)",
      "none"
    ],
    "idleFrames": [
      "none",
      "translateY(.7px)",
      "none"
    ],
    "bodyFrames": [
      "none",
      "translateY(2px)",
      "translateY(-1px)",
      "none"
    ],
    "toy": "leaf",
    "duration": 3000,
    "origin": "32px 30px",
    "idleDuration": 7.1
  },
  "dragon": {
    "playLabel": "Lift a spark",
    "hello": "stretches its wings in a warm greeting.",
    "response": "lifts its wings and watches a tiny spark rise.",
    "snack": "nibbles and lets its wings fold comfortably.",
    "part": ".sprite-wings",
    "greetFrames": [
      "none",
      "scaleX(1.08)",
      "none"
    ],
    "playFrames": [
      "none",
      "scaleX(1.24)",
      "scaleX(.93)",
      "scaleX(1.12)",
      "none"
    ],
    "idleFrames": [
      "none",
      "scaleX(1.028)",
      "none"
    ],
    "bodyFrames": [
      "none",
      "scaleX(1.04)",
      "translateY(-5px)",
      "none"
    ],
    "toy": "spark",
    "duration": 2300,
    "origin": "32px 35px",
    "idleDuration": 7.23
  },
  "hamster": {
    "playLabel": "Roll the seed",
    "hello": "lifts its paws and tidies its cheeks.",
    "response": "rolls a seed between its paws, then gives a tiny hop.",
    "snack": "holds its snack carefully in both paws.",
    "part": ".sprite-arms",
    "greetFrames": [
      "none",
      "translateY(-2px) scaleX(.94)",
      "none"
    ],
    "playFrames": [
      "none",
      "rotate(-7deg)",
      "rotate(7deg)",
      "translateY(-3px)",
      "none"
    ],
    "idleFrames": [
      "none",
      "translateY(-.6px)",
      "none"
    ],
    "bodyFrames": [
      "none",
      "scaleY(.96)",
      "translateY(-3px)",
      "none"
    ],
    "toy": "seed",
    "duration": 2000,
    "origin": "32px 42px",
    "idleDuration": 7.36
  },
  "raccoon": {
    "playLabel": "Solve the little puzzle",
    "hello": "raises a curious paw to say hello.",
    "response": "turns a little puzzle piece in its paws.",
    "snack": "holds its snack and takes a thoughtful nibble.",
    "part": ".sprite-arms",
    "greetFrames": [
      "none",
      "rotate(-5deg)",
      "translateY(-1px)",
      "none"
    ],
    "playFrames": [
      "none",
      "rotate(-9deg)",
      "scaleX(.9)",
      "rotate(9deg)",
      "none"
    ],
    "idleFrames": [
      "none",
      "rotate(1.8deg)",
      "none"
    ],
    "bodyFrames": [
      "none",
      "rotate(3deg)",
      "rotate(-3deg)",
      "none"
    ],
    "toy": "puzzle",
    "duration": 2400,
    "origin": "32px 42px",
    "idleDuration": 7.49
  },
  "bee": {
    "playLabel": "Visit the flower",
    "hello": "flutters its wings in a soft buzz.",
    "response": "loops around a flower and settles beside it.",
    "snack": "pauses for a tiny sip.",
    "part": ".sprite-wings",
    "greetFrames": [
      "none",
      "scaleX(.85)",
      "scaleX(1.1)",
      "none"
    ],
    "playFrames": [
      "none",
      "scaleX(.65)",
      "scaleX(1.18)",
      "scaleX(.7)",
      "none"
    ],
    "idleFrames": [
      "none",
      "scaleX(.96)",
      "scaleX(1.025)",
      "none"
    ],
    "bodyFrames": [
      "none",
      "translate(-4px,-5px)",
      "translate(4px,-7px)",
      "translate(-2px,-2px)",
      "none"
    ],
    "toy": "flower",
    "duration": 1900,
    "origin": "32px 29px",
    "idleDuration": 7.62
  },
  "octopus": {
    "playLabel": "Juggle a shell",
    "hello": "lifts its arms in a gentle wave.",
    "response": "ripples its arms to balance a tiny shell.",
    "snack": "takes a bite as its arms curl contentedly.",
    "part": ".sprite-tentacles",
    "greetFrames": [
      "none",
      "scaleX(1.07)",
      "scaleY(.97)",
      "none"
    ],
    "playFrames": [
      "none",
      "scaleX(1.14) scaleY(.9)",
      "scaleX(.93) scaleY(1.06)",
      "none"
    ],
    "idleFrames": [
      "none",
      "scaleX(1.03)",
      "scaleX(.985)",
      "none"
    ],
    "bodyFrames": [
      "none",
      "scaleX(1.07) scaleY(.95)",
      "translateY(-3px) scaleX(.97)",
      "none"
    ],
    "toy": "shell",
    "duration": 2500,
    "origin": "32px 47px",
    "idleDuration": 7.75
  },
  "dog": {
    "playLabel": "Fetch the ball",
    "hello": "wags its tail and lifts a friendly paw.",
    "response": "leans toward a rolling ball with an eager tail wag.",
    "snack": "takes a bite and gives a happy tail wag.",
    "part": ".sprite-tail",
    "greetFrames": [
      "none",
      "rotate(-16deg)",
      "rotate(15deg)",
      "rotate(-10deg)",
      "none"
    ],
    "playFrames": [
      "none",
      "rotate(-24deg)",
      "rotate(23deg)",
      "rotate(-17deg)",
      "none"
    ],
    "idleFrames": [
      "none",
      "rotate(-4deg)",
      "rotate(4deg)",
      "none"
    ],
    "bodyFrames": [
      "none",
      "translateX(3px) rotate(2deg)",
      "translateY(-3px)",
      "none"
    ],
    "toy": "ball",
    "duration": 1750,
    "origin": "45px 47px",
    "idleDuration": 7.88
  },
  "badger": {
    "playLabel": "Pat the soft earth",
    "hello": "sniffs gently and shifts its paws.",
    "response": "pats a soft patch of earth with steady paws.",
    "snack": "settles its paws and takes a calm nibble.",
    "part": ".sprite-arms",
    "greetFrames": [
      "none",
      "translateY(1px)",
      "translateY(-1px)",
      "none"
    ],
    "playFrames": [
      "none",
      "translateY(3px)",
      "translateY(-2px)",
      "translateY(2px)",
      "none"
    ],
    "idleFrames": [
      "none",
      "translateY(.5px)",
      "none"
    ],
    "bodyFrames": [
      "none",
      "translateX(-2px) scaleY(.98)",
      "translateX(2px)",
      "none"
    ],
    "toy": "earth",
    "duration": 2350,
    "origin": "32px 43px",
    "idleDuration": 8.01
  },
  "rat": {
    "playLabel": "Explore the ribbon",
    "hello": "tilts its head with a curious whisker twitch.",
    "response": "follows the end of a ribbon with two quick little looks.",
    "snack": "nibbles, then gives a curious look.",
    "part": ".sprite-head",
    "greetFrames": [
      "none",
      "rotate(-5deg)",
      "rotate(4deg)",
      "none"
    ],
    "playFrames": [
      "none",
      "translateX(-2px) rotate(-8deg)",
      "translateX(2px) rotate(7deg)",
      "none"
    ],
    "idleFrames": [
      "none",
      "rotate(-1.4deg)",
      "rotate(1.4deg)",
      "none"
    ],
    "bodyFrames": [
      "none",
      "translateX(-3px)",
      "translateX(3px) rotate(2deg)",
      "none"
    ],
    "toy": "ribbon",
    "duration": 1900,
    "origin": "32px 32px",
    "idleDuration": 8.14
  },
  "squirrel": {
    "playLabel": "Balance the acorn",
    "hello": "flicks its fluffy tail in greeting.",
    "response": "balances an acorn with a light hop and a tail flick.",
    "snack": "holds a nibble while its tail curls.",
    "part": ".sprite-tail",
    "greetFrames": [
      "none",
      "rotate(9deg)",
      "rotate(-6deg)",
      "none"
    ],
    "playFrames": [
      "none",
      "rotate(19deg)",
      "translateY(-2px) rotate(-13deg)",
      "none"
    ],
    "idleFrames": [
      "none",
      "rotate(3deg)",
      "none"
    ],
    "bodyFrames": [
      "none",
      "scaleY(.95)",
      "translateY(-6px)",
      "none"
    ],
    "toy": "acorn",
    "duration": 1850,
    "origin": "45px 46px",
    "idleDuration": 8.27
  },
  "bat": {
    "playLabel": "Catch a moonbeam",
    "hello": "opens its wings just a little to greet you.",
    "response": "stretches both wings and bobs through a moonbeam.",
    "snack": "settles its wings for a quiet bite.",
    "part": ".sprite-wings",
    "greetFrames": [
      "none",
      "scaleX(1.05)",
      "none"
    ],
    "playFrames": [
      "none",
      "scaleX(1.17)",
      "scaleX(.89)",
      "scaleX(1.08)",
      "none"
    ],
    "idleFrames": [
      "none",
      "scaleX(1.018)",
      "none"
    ],
    "bodyFrames": [
      "none",
      "translateY(-3px)",
      "translateY(-6px) rotate(-2deg)",
      "none"
    ],
    "toy": "moonbeam",
    "duration": 2600,
    "origin": "32px 33px",
    "idleDuration": 8.4
  },
  "goblin": {
    "playLabel": "Polish the toy coin",
    "hello": "waves a small hand and gives a polite bow.",
    "response": "polishes a toy coin and shows its shine.",
    "snack": "takes a little bite, then wipes its hands.",
    "part": ".sprite-arms",
    "greetFrames": [
      "none",
      "rotate(-8deg)",
      "rotate(4deg)",
      "none"
    ],
    "playFrames": [
      "none",
      "rotate(-12deg)",
      "scaleX(.88)",
      "rotate(10deg)",
      "none"
    ],
    "idleFrames": [
      "none",
      "rotate(1.1deg)",
      "none"
    ],
    "bodyFrames": [
      "none",
      "rotate(-3deg)",
      "translateY(2px) scaleY(.97)",
      "none"
    ],
    "toy": "coin",
    "duration": 2150,
    "origin": "32px 41px",
    "idleDuration": 8.53
  },
  "rock": {
    "playLabel": "Catch a glint",
    "hello": "gives a satisfied wobble and a little glint.",
    "response": "rocks gently from side to side as a glint crosses its facets.",
    "snack": "rests with a contented little wobble.",
    "part": ".sprite-facets",
    "greetFrames": [
      "none",
      "translateY(-.5px)",
      "none"
    ],
    "playFrames": [
      "none",
      "translateX(-1px)",
      "translateX(1px)",
      "none"
    ],
    "idleFrames": [
      "none",
      "translateY(.35px)",
      "none"
    ],
    "bodyFrames": [
      "none",
      "rotate(-7deg)",
      "rotate(6deg)",
      "rotate(-2deg)",
      "none"
    ],
    "toy": "glint",
    "duration": 2800,
    "origin": "32px 38px",
    "idleDuration": 8.66
  },
  "hedgehog": {
    "playLabel": "Uncurl for a leaf",
    "hello": "peeks up and lets its spines settle.",
    "response": "uncurls a little and reaches toward a leaf.",
    "snack": "takes a careful nibble with its paws close.",
    "part": ".sprite-spines",
    "greetFrames": [
      "none",
      "scale(.98)",
      "scale(1.01)",
      "none"
    ],
    "playFrames": [
      "none",
      "scale(.93)",
      "scale(1.06)",
      "none"
    ],
    "idleFrames": [
      "none",
      "scale(1.009)",
      "none"
    ],
    "bodyFrames": [
      "none",
      "scale(.96)",
      "translateY(-2px) scale(1.025)",
      "none"
    ],
    "toy": "autumnleaf",
    "duration": 2700,
    "origin": "32px 40px",
    "idleDuration": 8.79
  },
  "otter": {
    "playLabel": "Toss a pebble",
    "hello": "waves a paw and leans closer.",
    "response": "tosses a smooth pebble between its paws.",
    "snack": "holds a snack in its paws and settles down.",
    "part": ".sprite-arms",
    "greetFrames": [
      "none",
      "rotate(6deg)",
      "rotate(-3deg)",
      "none"
    ],
    "playFrames": [
      "none",
      "rotate(-10deg)",
      "translateY(-3px)",
      "rotate(9deg)",
      "none"
    ],
    "idleFrames": [
      "none",
      "translateY(.8px)",
      "none"
    ],
    "bodyFrames": [
      "none",
      "translateX(2px) rotate(3deg)",
      "translateX(-2px) rotate(-2deg)",
      "none"
    ],
    "toy": "pebble",
    "duration": 2100,
    "origin": "32px 42px",
    "idleDuration": 8.92
  },
  "moth": {
    "playLabel": "Drift to the lantern",
    "hello": "fans its patterned wings in greeting.",
    "response": "makes a slow, gentle turn beside a lantern glow.",
    "snack": "pauses its wings for a quiet sip.",
    "part": ".sprite-wings",
    "greetFrames": [
      "none",
      "scaleX(1.06)",
      "none"
    ],
    "playFrames": [
      "none",
      "scaleX(.82)",
      "scaleX(1.13)",
      "scaleX(.9)",
      "none"
    ],
    "idleFrames": [
      "none",
      "scaleX(1.022)",
      "scaleX(.99)",
      "none"
    ],
    "bodyFrames": [
      "none",
      "translate(-2px,-3px) rotate(-3deg)",
      "translate(2px,-5px) rotate(3deg)",
      "none"
    ],
    "toy": "lantern",
    "duration": 2900,
    "origin": "32px 32px",
    "idleDuration": 9.05
  },
  "snail": {
    "playLabel": "Follow the dewdrop",
    "hello": "raises its antennae in a slow hello.",
    "response": "extends its antennae and glides toward a dewdrop.",
    "snack": "samples a tiny leaf with a slow nod.",
    "part": ".sprite-ears",
    "greetFrames": [
      "none",
      "translateY(-1px) scaleY(1.06)",
      "none"
    ],
    "playFrames": [
      "none",
      "rotate(-5deg) scaleY(1.13)",
      "rotate(5deg) scaleY(1.04)",
      "none"
    ],
    "idleFrames": [
      "none",
      "rotate(-1.2deg)",
      "rotate(1.2deg)",
      "none"
    ],
    "bodyFrames": [
      "none",
      "translateX(3px) scaleX(1.035)",
      "translateX(7px) scaleX(.985)",
      "none"
    ],
    "toy": "dewdrop",
    "duration": 3200,
    "origin": "32px 26px",
    "idleDuration": 9.18
  },
  "mushroom": {
    "playLabel": "Send a little spore",
    "hello": "tips its cap in a friendly greeting.",
    "response": "bobs once and watches a tiny spore drift away.",
    "snack": "rests beneath its cap for a moment.",
    "part": ".sprite-cap",
    "greetFrames": [
      "none",
      "rotate(-4deg)",
      "rotate(2deg)",
      "none"
    ],
    "playFrames": [
      "none",
      "scaleY(.95)",
      "translateY(-3px) rotate(5deg)",
      "none"
    ],
    "idleFrames": [
      "none",
      "rotate(.8deg)",
      "rotate(-.8deg)",
      "none"
    ],
    "bodyFrames": [
      "none",
      "scaleY(.96)",
      "translateY(-4px)",
      "none"
    ],
    "toy": "spore",
    "duration": 2450,
    "origin": "32px 27px",
    "idleDuration": 9.31
  }
};
