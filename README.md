# wekapipes
Weka command-line pipelines that make use of [seppl](https://github.com/waikato-datamining/seppl),
[kasperl](https://github.com/waikato-datamining/kasperl) and
[python-weka-wrapper3](https://github.com/fracpete/python-weka-wrapper3).


## Installation

Via PyPI:

```bash
pip install wekapipes
```

The latest code straight from the repository:

```bash
pip install git+https://github.com/fracpete/wekapipes.git
```


## Tools

### Running pipelines

```
usage: wp-run [-h] [--help-all] [--help-plugin NAME] [-u INTERVAL]
              [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-b]
              [--placeholders FILE] [--load_pipeline FILE]
              [--dump_pipeline FILE] [-c PATH] [-s] [-p] [-M SIZE]

Tool for running Weka pipelines.

readers (8):
   from-storage, from-text-file, get-email, list-files, load-data, 
   poll-dir, start, watch-dir
filters (24):
   block, check-duplicate-filenames, copy-files, discard-by-name, 
   filter-data, list-to-sequence, max-records, metadata, 
   metadata-from-name, metadata-to-placeholder, move-files, passthrough, 
   randomize-records, record-window, rename, sample, set-metadata, 
   set-placeholder, set-storage, split-records, stop, sub-process, tee, 
   trigger
writers (6):
   console, delete-files, save-data, send-email, to-storage, 
   to-text-file

options:
  -h, --help           Show basic help message and exit.
  --help-all           Show basic help message plus help on all plugins and exit.
  --help-plugin NAME   Show help message for plugin NAME and exit.
  -u, --update_interval INTERVAL
                       Outputs the progress every INTERVAL records (default: 1000).
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                       The logging level to use (default: WARN).
  -b, --force_batch    Processes the data in batches.
  --placeholders FILE  The file with custom placeholders to load (format: key=value).
  --load_pipeline FILE The file to load the pipeline command from.
  --dump_pipeline FILE The file to dump the pipeline command in.
  -c, --classpath PATH The additional classpath elements to use for the JVM.
  -s, --system_classpath
                       Whether to use the system CLASSPATH as well.
  -p, --packages       Whether to load the installed Weka packages.
  -M, --max_heap SIZE  The maximum amount of heap space to allow, e.g., 256m or 2g.
```

### Executing pipeline multiple times

```
usage: wp-exec [-h] --exec_generator GENERATOR [--exec_dry_run]
               [--exec_prefix PREFIX] [--exec_placeholders FILE]
               [--exec_format {cmdline,file}]
               [--exec_logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
               [--exec_classpath [PATH ...]] [--exec_system_classpath]
               [--exec_packages] [--exec_max_heap SIZE]
               ...

Tool for executing a pipeline multiple times, each time with a different set
of variables expanded. A variable is surrounded by curly quotes (e.g.,
variable 'i' gets referenced with '{i}'). When supplying multiple generators,
then these get treated as nested executions. Available generators: csv-file,
dirs, list, null, prompt, range, text-file

positional arguments:
  pipeline              The pipeline template with variables to expand and
                        then execute; see '--exec_format' option.

options:
  -h, --help            show this help message and exit
  --exec_generator GENERATOR
                        The generator plugin(s) to use, incl. their options.
                        Flag needs to be specified for each generator.
                        (default: None)
  --exec_dry_run        Applies the generator to the pipeline template and
                        only outputs it on stdout. (default: False)
  --exec_prefix PREFIX  The string to prefix the pipeline with when in dry-run
                        mode. (default: None)
  --exec_placeholders FILE
                        The file with custom placeholders to load (format:
                        key=value). (default: None)
  --exec_format {cmdline,file}
                        The format that the pipeline is in. The format
                        'cmdline' interprets the remaining arguments as the
                        pipeline arguments to execute. The format 'file'
                        expects a file to load the pipeline arguments from.
                        This file format allows spreading the pipeline
                        arguments over multiple lines: it simply joins all
                        lines into a single command-line before splitting it
                        into individual arguments for execution. (default:
                        cmdline)
  --exec_logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  --exec_classpath [PATH ...]
                        The additional classpath elements to use for the JVM.
                        (default: None)
  --exec_system_classpath
                        Whether to use the system CLASSPATH as well. (default:
                        None)
  --exec_packages       Whether to load the installed Weka packages. (default:
                        None)
  --exec_max_heap SIZE  The maximum amount of heap space to allow, e.g., 256m
                        or 2g. (default: None)
```


### Locating files

Readers tend to support input via file lists. The `wp-find` tool can generate
these.

```
usage: wp-find [-h] -i DIR [DIR ...] [-r] -o FILE [-m [REGEXP ...]]
               [-n [REGEXP ...]] [--split_ratios [SPLIT_RATIOS ...]]
               [--split_names [SPLIT_NAMES ...]]
               [--split_name_separator SPLIT_NAME_SEPARATOR]
               [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

Tool for locating files in directories that match certain patterns and store
them in files.

options:
  -h, --help            show this help message and exit
  -i DIR [DIR ...], --input DIR [DIR ...]
                        The dir(s) to scan for files. (default: None)
  -r, --recursive       Whether to search the directories recursively
                        (default: False)
  -o FILE, --output FILE
                        The file to store the located file names in (default:
                        None)
  -m [REGEXP ...], --match [REGEXP ...]
                        The regular expression that the (full) file names must
                        match to be included (default: None)
  -n [REGEXP ...], --not-match [REGEXP ...]
                        The regular expression that the (full) file names must
                        match to be excluded (default: None)
  --split_ratios [SPLIT_RATIOS ...]
                        The split ratios to use for generating the splits
                        (int; must sum up to 100) (default: None)
  --split_names [SPLIT_NAMES ...]
                        The split names to use as filename suffixes for the
                        generated splits (before .ext) (default: None)
  --split_name_separator SPLIT_NAME_SEPARATOR
                        The separator to use between file name and split name
                        (default: -)
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
```


### Generating help screens for plugins

```
usage: wp-help [-h] [-c [PACKAGE ...]] [-e EXCLUDED_CLASS_LISTERS]
               [-T {pipeline,generator}] [-p NAME] [-f {text,markdown}]
               [-L INT] [-o PATH] [-i FILE] [-t TITLE]
               [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

Tool for outputting help for plugins in various formats.

options:
  -h, --help            show this help message and exit
  -c [PACKAGE ...], --custom_class_listers [PACKAGE ...]
                        The custom class listers to use, uses the default ones
                        if not provided. (default: None)
  -e EXCLUDED_CLASS_LISTERS, --excluded_class_listers EXCLUDED_CLASS_LISTERS
                        The comma-separated list of class listers to exclude.
                        (default: None)
  -T {pipeline,generator}, --plugin_type {pipeline,generator}
                        The types of plugins to generate the help for.
                        (default: pipeline)
  -p NAME, --plugin_name NAME
                        The name of the plugin to generate the help for,
                        generates it for all if not specified (default: None)
  -f {text,markdown}, --help_format {text,markdown}
                        The output format to generate (default: text)
  -L INT, --heading_level INT
                        The level to use for the heading (default: 1)
  -o PATH, --output PATH
                        The directory or file to store the help in; outputs it
                        to stdout if not supplied; if pointing to a directory,
                        automatically generates file name from plugin name and
                        help format (default: None)
  -i FILE, --index_file FILE
                        The file in the output directory to generate with an
                        overview of all plugins, grouped by type (in markdown
                        format, links them to the other generated files)
                        (default: None)
  -t TITLE, --index_title TITLE
                        The title to use in the index file (default: image-
                        dataset-converter plugins)
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
```


### Plugin registry

```
usage: wp-registry [-h] [-c CUSTOM_CLASS_LISTERS] [-e EXCLUDED_CLASS_LISTERS]
                   [-l {plugins,pipeline,custom-class-listers,env-class-listers,readers,filters,writers,generators}]

For inspecting/querying the registry.

options:
  -h, --help            show this help message and exit
  -c CUSTOM_CLASS_LISTERS, --custom_class_listers CUSTOM_CLASS_LISTERS
                        The comma-separated list of custom class listers to
                        use. (default: None)
  -e EXCLUDED_CLASS_LISTERS, --excluded_class_listers EXCLUDED_CLASS_LISTERS
                        The comma-separated list of class listers to exclude.
                        (default: None)
  -l {plugins,pipeline,custom-class-listers,env-class-listers,readers,filters,writers,generators}, --list {plugins,pipeline,custom-class-listers,env-class-listers,readers,filters,writers,generators}
                        For outputting various lists on stdout. (default:
                        None)
```

### Testing generators

```
usage: wp-test-generator [-h] -g GENERATOR
                         [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

Tool for testing generators by outputting the generated variables and their
associated values. Available generators: csv-file, dirs, list, null, prompt,
range, text-file

options:
  -h, --help            show this help message and exit
  -g GENERATOR, --exec_generator GENERATOR
                        The generator plugin(s) to use, incl. their options.
                        Flag needs to be specified for each generator.
                        (default: None)
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
```


## Plugins

You can find help screens for the plugins here:

* [Pipeline plugins](plugins/README.md) (readers/filters/writers)
* [Generator plugins](generators/README.md) (used by `wp-exec`)


## Command-line examples

Examples can be found on the [wekapipes-examples](https://fracpete.github.io/wekapipes-examples/)
website.


## Class listers

The *image-dataset-converter* uses the *class lister registry* provided 
by the [seppl](https://github.com/waikato-datamining/seppl) library.

Each module defines a function, typically called `list_classes` that returns
a dictionary of names of superclasses associated with a list of modules that
should be scanned for derived classes. Here is an example:

```python
from typing import List, Dict


def list_classes() -> Dict[str, List[str]]:
    return {
        "seppl.io.Reader": [
            "mod.ule1",
            "mod.ule2",
        ],
        "seppl.io.Filter": [
            "mod.ule3",
            "mod.ule4",
        ],
        "seppl.io.Writer": [
            "mod.ule5",
        ],
    }
```

Such a class lister gets referenced in the `entry_points` section of the `setup.py` file:

```python
    entry_points={
        "class_lister": [
            "unique_string=module_name:function_name",
        ],
    },
```

`:function_name` can be omitted if `:list_classes`.

The following environment variables can be used to influence the class listers:

* `WP_CLASS_LISTERS`
* `WP_CLASS_LISTERS_EXCL`
* `WP_CLASS_LISTERS_IGNORED` - for class listers that provide ignored classes

Each variable is a comma-separated list of `module_name:function_name`, defining the class listers.


## Caching plugins

In order to speed up plugin discovery, they discovered plugins can be cached
on disk after the initial discovery. Installing additional plugins after
the cache has been initialized will not make them visible, the cache will
require resetting first.

The cache can be managed through the following environment variable:

```
WP_CLASS_CACHE
```

It supports the following options:

* `off`: disables the cache
* `on`: enables the cache
* `reset`: resets the cached plugins first and enables the cache
