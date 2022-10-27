# What is this?

This is an effort to create acceptable social media cards in a smarter, automated way. It's an outgrowth from the AutomatingVisuals team in a JournalismAI fellowship. The impetus for the effort, and some of the findings, are [discussed in this blog post](https://blogs.lse.ac.uk/polis/2022/10/11/lessons-from-prototyping-an-ai-visual-pipeline/). The program is tentatively called Euchre.

## Installation

 - Download or clone the repo.
 - Change into the directory.
 - Ensure you have a working copy of Python.
 - Run *pip install -r requirements.txt*

## Doing stuff

To launch Euchre, run *flask run* or *python app.py* -- either should be fine. It should show a message in the console that includes something like *Running on http://127.0.0.1:5000*

For the web interface, copy-paste that address into your web browser, or more simply, try typing *localhost:5000* into your browser's address bar.

This should bring you to the program's web interface.

## Automating cards

Once running, Euchre can be used with HTTP GET or POST requests and all relevant options to generate social media cards automatically. Generate the cards with a call to the base address plus */generate/* with all of the necessary options as part of your payload.

## Payload options

In the interim, you can figure out what the options are and how they're sent by checking the source code to the web interface.

## Can this ... ?

Probably not. Pull requests are welcome if you see something to improve, but the potential of this effort is limited. If you need something potentially more flexible, @thomaswilburn identified [Vercel's OG Image Generation](https://vercel.com/docs/concepts/functions/edge-functions/og-image-generation) as something potentially worth a look.

## Licensing ##

Details are available in the [LICENSE](LICENSE) file. Euchre's core is released under an MIT license, but is built atop things supplied with a GPL license and an Open Font License.

## Why "Euchre"?

Euchre is a card game that may be most known to people in America's midwest.

It's a trump game with some unusual rules. For example, if spades is chosen as the trump suit, the highest cards become the jack of spades, the jack of clubs, the ace of spaces, then the king of spades.

In other words, Euchre is a way to do weird things with cards.

## Credits

The Automating Visuals team is comprised of people who were working at McClatchy and Gannett organizations at the beginning of the fellowship:

 - [Theresa Poulson](https://github.com/theresapoulson), Senior Product Manager, McClatchy (US)
 - [Tyler Dukes](https://github.com/mtdukes), Investigative Reporter, McClatchy (US)
 - [Sean Smith](https://github.com/ssmithgannett), Product Manager, Gannett / USA TODAY Network (US)
 - [Mike Stucka](https://github.com/stucka), National Data Solutions Editor, Gannett / USA TODAY Network (US)

This was done under the auspices of the [JournalismAI Fellowship 2022](https://www.lse.ac.uk/media-and-communications/polis/JournalismAI), with particular support from [Mattia Peretti](https://github.com/xhgMattia) and Lakshmi Sivadas. Euchre lessons were provided decades ago particularly by Mark Perry and Joe Finnegan.
