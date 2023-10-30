File [mysterious_audio](src/mysterious_audio.wav) di modulate sama dikasih highpass filter di audacity. Buat ngebenerinnya bisa dibalikin pake Nyquist script (Ada di Tools > Nyquist Prompt)

```shell
;version 4
(setf cf 4000) ; the carrier frequency
(let ((demod (mult *track* (hzosc cf))))
  (lowpass8 demod cf))
```

Pas udah ditranscribe hasilnya bakal : b84c72d4bd56f2849db23f984f1d824f658d79b8

Itu password buat private key yang bakal dipake buat decrypt [flag.encrypted](src/flag.encrypted). Buat decryptnya bisa pake openssl

```shell
openssl rsautl -decrypt -inkey private.key -in flag.encrypted -out flag.txt
```

Flagnya ada di flag.txt
