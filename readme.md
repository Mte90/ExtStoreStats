# ExtStoreStats
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/e2e229674466432db73f94c543748918)](https://www.codacy.com/app/mte90net/ExtStoreStats?utm_source=github.com&utm_medium=referral&utm_content=Mte90/ExtStoreStats&utm_campaign=badger)
[![License](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)   

Do you want to know the number of downloads for each of your extensions on different marketplaces?

Actually, it is not impossible to track that.
The idea is to create a script with cron which saves that amount and generates a graph everyday.

# Output

Write to console the status and generate a json for every extension specified in the `config.ini` (copy `config-sample.ini` and change depending on your needs), you can see a [demo](https://mte90.github.io/ExtStoreStats/) here.

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
