#ExtStoreStats [WIP]
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/e2e229674466432db73f94c543748918)](https://www.codacy.com/app/mte90net/ExtStoreStats?utm_source=github.com&utm_medium=referral&utm_content=Mte90/ExtStoreStats&utm_campaign=badger)
[![License](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)   

Do you want know the number of download for your extensions on different marketplace?  
Actually is not impossible also have a track of that, the idea is to create a script with cron that everyday save that amount and generate a graph.

# Output

Write in console the status but also generate a json for every extension specified in the `config.ini`, you can see a [demo](https://mte90.github.io/ExtStoreStats/) here.

```
bash:~/ExtStoreStats  $  ./index.py 
Addons Mozilla Extension Gathering for: glotdict
Download: 68
Google Web Store Extension Gathering for: glotdict/jfdkihdmokdigeobcmnjmgigcgckljgl
Download: 236
Total Download: 304
```

# Install

`pip install -r requirements.txt`