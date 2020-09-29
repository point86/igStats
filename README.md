 # igStats
A command-line utility written in Python that connects to your Instagram account, and retrieve the list of profiles that you are following and the list of profiles that are following you.
It will then display a report that shows:
- list of profiles that you are following and they aren't following you back (Following - Followers).
- list of profiles that are following you and you aren't following them back (Followers - Following).

## Requirements
- Firefox web browser (version ≥60).
- Geckodriver (downloadable via https://github.com/mozilla/geckodriver/releases).
- Python 3.x
With additional packages (downloadable with pip):
-- Selenium
-- BeautifulSoup

## Usage

First you need to create a configuation file named `igStats.ini` and place it in the same directory as this script.
```ini
[settings]
Instagram Profile = <your Instagram profile name>
Firefox Profile = <path to your Firefox profile>
Dump Followers  = <Yes|No>
```
Firefox profile's path can be found by typing `about:profiles` in your Firefox's search bar. You can leave that variable blank, but then you will need to perform log-in every time you will use this program.
Then you have 2 options, you can run `igStats.py` or `igStatsBrowser.py`. The only difference between them is that the latter will present you two pretty printed HTML files, instead of a simple text output.

### igStats
This is the fastest program, it shows you a text based output on the command line.
```bash
$ python3 igStats.py
```
### igStatsBrowser
```bash
$ python3 igStatsBrowser.py
```
This is slower because it will also download all profiles images that are involved, and it will present a pretty printed HTML output.
It will generate two HTML files, `fwing-fwers.html` and `fwers-fwing.html` which respectively contains *"Following - Followers"* and *"Followers - Following"* lists.

### igDiff
```bash
$ python3 igDiff.py followers_xxx.pkl followers_yyy.pkl
```
It will show you the difference between two dumps of your Instagram followers list. (Dumps must be previously generated with igStats.py or igStatsBrowser.py .

## Disclaimer
Although this program doesn't let you modify your Instagram's followers/following lists, it can be seen as a bot and your Instagram profile can be disabled. Use it at your own risk!

## License

MIT License

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.