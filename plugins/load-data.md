# load-data

* generates: weka.core.dataset.Instances

Loads the dataset and forwards it. Optionally, a custom loader definition can be supplied.

```
usage: load-data [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                 [-N LOGGER_NAME] [-i [INPUT ...]] [-I [INPUT_LIST ...]]
                 [--resume_from RESUME_FROM] [-u] [-L CMDLINE]
                 [-c CLASS_INDEX] [--incremental]

Loads the dataset and forwards it. Optionally, a custom loader definition can
be supplied.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -i [INPUT ...], --input [INPUT ...]
                        Path to the data file(s) to read; glob syntax is
                        supported; Supported placeholders: {HOME}, {CWD},
                        {TMP} (default: None)
  -I [INPUT_LIST ...], --input_list [INPUT_LIST ...]
                        Path to the text file(s) listing the data files to
                        use; Supported placeholders: {HOME}, {CWD}, {TMP}
                        (default: None)
  --resume_from RESUME_FROM
                        Glob expression matching the file to resume from,
                        e.g., '*/012345.arff' (default: None)
  -u, --use_custom_loader
                        Whether to use the supplied custom loader rather than
                        auto-detection. (default: False)
  -L CMDLINE, --custom_loader CMDLINE
                        The command-line of the custom loader to use
                        (classname + options). (default: None)
  -c CLASS_INDEX, --class_index CLASS_INDEX
                        The class index to use on the data, e.g., 1, first, 3,
                        last. (default: None)
  --incremental         Whether to load the data row by row rather than in one
                        go. (default: False)
```

Available placeholders:

* `{HOME}`: The home directory of the current user.
* `{CWD}`: The current working directory.
* `{TMP}`: The temp directory.
