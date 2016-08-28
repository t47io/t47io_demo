# t47io Lab Demo

<img src="https://demo.t47.io/site_media/images/logo_t47.png" alt="T47 Logo" width="150px" align="right">

This is the _Source Code_ repository for **Lab Demo** Website. The demo server is freely accessible at https://demo.t47.io/. The production server is served for **DasLab** Website at https://daslab.stanford.edu/.

## Installation

**Lab Demo** requires the following *Python* packages as dependencies, most of which can be installed through [`pip`](https://pip.pypa.io/).

```json
boto >= 2.38.0
Django >= 1.9.1
django-adminplus >= 0.5
django-crontab >= 0.7.0
django-environ >= 0.4.0
django-filemanager == 0.0.2
django-suit >= 0.2.15
django-widget-tweaks >= 1.4.1
dropbox >= 4.0
gviz-api.py == 1.8.2
icalendar >= 3.9.1
MySQL-python >= 1.2.5
PyGithub >= 1.26.0
pytz >= 2015.7
requests >= 2.9.1
simplejson >= 3.8.1
slacker >= 0.9.0
```

The `gviz-api.py` is available at https://github.com/google/google-visualization-python/.

The `django-filemanager` is a modified version of https://github.com/IMGIITRoorkee/django-filemanager/. The source code is available internally. Install with `sudo python setup.py install`.

**Lab Demo** also requires proper setup of `mysql.server`, `apache2`, `mod_wsgi`, `pandoc` and `cron` jobs.

Lastly, assets preparation is required for the 1st time through running `util_prep_dir.sh`, `util_system_version.sh`, `util_minify.sh`, `util_chmod.sh` and manually replacing `config/*.conf`. For full configuration, please refer to **Documentation**.


## Usage

To run the test/dev server, use:

```bash
cd path/to/server_demo/repo
python manage.py runserver
```

## Documentation

Documentation is available at admin [manual](https://demo.t47.io/admin/man/) and [reference](https://demo.t47.io/admin/ref/).

## License

**Copyright &copy; 2015-2016: Siqi Tian _[[t47](https://t47.io/)]_, Stanford University. All Rights Reserved.**

The original **DasLab Server** _Source Code_ is proprietary and confidential. Unauthorized copying of this repository, via any medium, is strictly prohibited.


by [**t47**](https://t47.io/), *January 2016*.

