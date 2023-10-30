# Compfest Pay

by Zafirr 

---

## Flag

```
FLAG=COMPFEST12{XSS_and_HPP_what_a_duo_deadliner_challenge_btw_f5aed4}
```

## Description
Compfest Pay! (Totally not a copy of Arkav Pay (Arkavidia 6.0) which was totally not a copy of ZKPay (Seccon Quals 2019))

## Attachment

* share/

Ini semua dizip. Upload ke google docs dan CTFd.

## Difficulty
Hard

## Hint


## Deployment
### Backend
- Untuk migrate dan initiate database
  ```
  python manage.py makemigrations users handle_transaction
  python manage.py migrate
  python manage.py loaddata seed
  ```
- Gunakan file .env untuk environment variables
- Untuk menjalankan service:
  ```
  python manage.py runserver 8000
  ```

### Frontend
Jalankan `python app.py`

## Note
* Buat Deployment: Jalanin biar backend bisa interact dengan frontend. Tapi yang lain gabisa interaksi dengan backend