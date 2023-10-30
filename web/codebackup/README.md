# CodeBackup

by Bonceng

---

## Flag

```
COMPFEST12{CR3aTing_Is_H4rde12_thaN_s0lv1nG_UpGraD3d_1badf416}
```

## Description
Wanna try my codeBackup? Sorry, my server's storage is small. Besides that, database processing is so slow on my server, but I can guarantee that your files is already uploaded.

Since it's beta version, I will clear all client's folder every hour.

P.S. We've upgraded this problem, a little bit different from the original.

## Attachment
- share/Dockerfile

## Difficulty
Medium-Hard

## Hints
- Have you tried to open my local files?
- Why I have to process my seed first?
- Template have pros and cons

## Tags
SSTI, LFI, PRNG, Scripting

## Deployments
> **Notes:** cronjobs to delete user uploads file isn't implemented in Dockerfile yet.

- Install pip requirements, docker engine>=19.03.12, and docker-compose>=1.26.2.
- Edit variable `VAR` in `init.py`.
- To generate configuration and Dockerfile, run:
    ```
    python3 init.py
    ```
- To run the container, run:
    ```
    docker-compose up --build --detach
    ```

## Notes
- [Middle-Square PRNG](https://en.wikipedia.org/wiki/Middle-square_method)
- [SSTI Filter bypass](https://0day.work/jinja2-template-injection-filter-bypasses/)
- Hati hati kena DDOS