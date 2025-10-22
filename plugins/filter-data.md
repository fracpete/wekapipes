# filter-data

* accepts: weka.core.dataset.Instances, weka.core.dataset.Instance
* generates: weka.core.dataset.Instances, weka.core.dataset.Instance

Filters the data coming through.

```
usage: filter-data [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                   [-N LOGGER_NAME] [--skip] [-f CMDLINE] [-a] [-L FILE]
                   [-S FILE]

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
  -a, --always_initialize
                        Whether to initialize the filter with each data item
                        passing through. (default: False)
  -L FILE, --load_from FILE
                        The file to load the serialized filter from. Available
                        placeholders: - {HOME}: The home directory of the
                        current user. - {CWD}: The current working directory.
                        - {TMP}: The temp directory. (default: None)
  -S FILE, --save_to FILE
                        The file to save the initialized filter to. Available
                        placeholders: - {HOME}: The home directory of the
                        current user. - {CWD}: The current working directory.
                        - {TMP}: The temp directory. (default: None)
```

Available placeholders:

* `{HOME}`: The home directory of the current user.
* `{CWD}`: The current working directory.
* `{TMP}`: The temp directory.
