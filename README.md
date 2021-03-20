## Columbia Project Management course 3/20/21


### Example command

* ``-file <file>`` argument is the csv file with the data you want to process. put the file in your directory
* ``-name <name>`` argument is the name you want to use for output files
* ``-task_duration_col <task_duration_col>`` argument is the column you want to use for calculating critical path times


```python critical_path_analyzer.py -file bicycle_data.csv -name optimistic -task_duration_col Optimistic```
