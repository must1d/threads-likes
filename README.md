# Threads Likes

This repository contains a web scraper that is able to collect the likes of threads of a user on [Threads](https://www.threads.net/).
The implementation is very poor and simulates a real user scrolling through the threads.

To install run:
```bash
pdm install
```
To collect the data on the likes:
```bash
pdm run src/collect_likes.py -u {USERNAME}
```
To analyze the likes:
```bash
pdm run src/analyze_likes.py
```
