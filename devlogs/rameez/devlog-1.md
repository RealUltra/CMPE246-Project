# Dev Log #1 — Web Server and UI

**Date: 2026-03-31**

## Goal(s)

- Set up the rp4 as a permanent AP.
- Host a web server on the rp4.
- Display the radar data with a nice UI on the local web server.
- Make the radar code run as soon as the rp4 boots.

## Implementation

- Create the UI in p5.js.
- Set up a web server in python with flask, and use websockets to communicate with the UI.
- Changed up radar main functionality to run constantly as opposed to doing sweeps on command.
- Fixed beeping functionality.

## Results

- Rp4 is a permanent AP from boot.
- Web server hosted on rp4 with a nice UI for the radar.
- Radar code runs on startup.

## Review [Optional]

While the results meet my expectations for the most part, I would've preferred to give more time to testing so that I could find bugs.

## Next Steps

- Testing the project. Fixing any last minute bugs.
