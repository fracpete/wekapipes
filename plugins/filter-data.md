# filter-data

* accepts: weka.core.dataset.Instances, weka.core.dataset.Instance
* generates: weka.core.dataset.Instances, weka.core.dataset.Instance

Filters the data coming through.

```
usage: filter-data [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                   [-N LOGGER_NAME] [--skip] -f CMDLINE

Filters the data coming through.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  -f CMDLINE, --filter CMDLINE
                        The command-line of the filter to use (classname +
                        options). (default: None)
```
