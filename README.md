# tddtnews

This is a suite of tools used for the creation and sending of newsletters specifically for Texas Dragon/Lion Dance Team, located in Austin, TX

---

#### Version 1.0.1 Beta 

##### Changelog:

- Fixed `tddtgui.bat` and `tddtgui.sh`. Works on windows but needs to be tested in mac/linux
- Added major feature: images can be inserted into news section
- Visual changes to `liondancebeat.jinja`

##### Features:

- auto-updating preview that lets you see what the newsletter looks like before you publish
- automatically searches out for events in the next 2 months, so no need to manually type those events in
- an image hoster function is included, which automatically uploads public images to your google drive (adding images to the newsletter will be added in a later update)
- a news adder function lets you easily add your own written sections with images to the newsletter. Images uploaded by the image hoster will automatically be available to insert.

---
#### Installation
I haven't tested these steps on a different device, but in theory, this is how you would run the application

1. install poetry following instructions at https://python-poetry.org/docs/#installation 
2. download latest release from https://github.com/wuben2602/tddtnews
3. navigate to the folder created by step 2 and run `tddtgui.bat` in windows or `tddtgui.sh` in mac/linux
---
#### Contributing
1. new issues can be created if you have a github account at https://github.com/wuben2602/tddtnews
2. email issues to ben@tddt.org