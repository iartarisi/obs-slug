OBS slug
========

Some (most) times OBS is slow. This is a script to install a package without waiting for all of the dependencies in a project to get published. Right after building, they should be available for `osc getbinaries`.

This script requires `osc` and `zypper`.

```bash
$ ./obs-slug.py package-name
```
