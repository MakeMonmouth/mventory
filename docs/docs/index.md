# Welcome to MVentory

Mventory is an API-driven inventory solution for Makers, Makerspaces, Hackspaces, and just about anyone else who needs to keep track of "stuff".

I've written it to scratch an itch because I couldn't find anything else out there that would give me a simple way to keep track of the various components and materials in my garage, and wanted something that could translate easily from my house to a Makerspace in future.

## How does it work?

### What does "API-Driven" mean?

Mventory is "API-driven".  This means that apart from the very basic admin pages there is no "pretty" interface built in, but the ability to communicate with the platform from almost any other platform is there from day one.

Happy with using the built-in admin pages? Great! Go for it!

Want to write an app for your phone that you can use whilst walking around the Makerspace? Yup, you can do that too!

Feel like building your own [ASRS](https://en.wikipedia.org/wiki/Automated_storage_and_retrieval_system) for your workbench? No worries, we've got you covered!

In short by having the built-in admin but allowing anyone to write their own front-end for the platform, all we need to worry about is storing and presenting the raw data to whatever you choose to use to query it.  This makes the code a lot easier to maintain for us, whilst keeping the options for future integration wide open!

### OK, so what can I do with it?

Mventory has the concept of Buildings, Rooms, Storage Units, Bins, and Components (in descending size order).

A component is the smallest unit of measurement and could be anything from a bolt of cloth or a spool of 3D printer filament through to SMD resistors, LED's, or linear actuators.

Components live in "Bins".  A "Bin" is a sub-division of a Storage Unit and could be a box, a drawer, or a specific location on a peg board.

Bins live inside "Storage Units" (chests of drawers, toolboxes, peg boards etc), and Storage Units live inside "Rooms".

Finally, Rooms live inside "Buildings".

This may feel like overkill for a small home setup, but if you're working in a Makerspace that has multiple units on a yard or similar then it could be incredibly useful!
