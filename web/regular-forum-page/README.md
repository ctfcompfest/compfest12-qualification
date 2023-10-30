# Regular Forum Page

## Flag
```
COMPFEST13{html_t4g_1s_n0t_C4s3_5ent1t1v3_5bc733a9f8}
```

## Description

Check out my sweet new forum page! Mods will check often in to prevent bad things from happening. 

## Difficulty

Medium

## Hint

- I have a dedicated moderator, you know...
- Tags are allowed, you see...

## Deployment

- Set environment variable `DOMAIN` with domain of the web, so the bot could access the web.
    ```
    environment:
      - DOMAIN=<serverip>:<portoutsidedocker>
    ```
    BUKAN LOCALHOST

- Build and run the web and bot.
    ```
    docker-compose build
    docker-compose up # use -d to run in background
    ```
